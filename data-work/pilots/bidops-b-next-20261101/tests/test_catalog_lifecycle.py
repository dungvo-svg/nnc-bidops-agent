from datetime import date
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from src.four_bv_intake import import_four
from src.catalog_lifecycle import (initialize_lifecycle,active_worklist,resolve_line,transition_case,
                                   extend_deadline,plan_closure,create_fulfillment,finish_fulfillment,source_worklist)
from src.catalog_intake import IntakeConflict
from tests.test_four_bv_intake import row
import hashlib


class CatalogLifecycleBehavior(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix="common-lifecycle-",dir=Path(__file__).resolve().parent)
        self.root=Path(self.temp.name);self.db=self.root/'catalog.sqlite'
        rows=[row(),row('X-2','1',**{'SL Mahosot':''})]
        source=self.root/'source.json';source.write_text(json.dumps(rows,ensure_ascii=False),encoding='utf-8')
        data=source.read_bytes()
        manifest={'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'row_count':2,
                  'sources':[{'group':'vt','drive_file_id':'fictional-source','url':'https://example.invalid/',
                              'extracted_content_sha256':'a'*64,'raw_xlsx_sha256':None,'selected_rows':2}],
                  'case_deadlines_planning_only':{'Settha':'2026-11-26','Mahosot':'2026-11-25','SVNK':None,'Me and Dek':'2026-11-27'}}
        mp=self.root/'manifest.json';mp.write_text(json.dumps(manifest),encoding='utf-8')
        import_four(source,mp,self.db);initialize_lifecycle(self.db)
        self.identity={'mpsc':'SYNTHETIC-CODE','specification':'fictional30mm','uom':'EA',
                       'registration_id':None,'valid_from':None,'valid_until':None}

    def tearDown(self):self.temp.cleanup()

    def query(self,sql,params=()):
        db=sqlite3.connect(self.db)
        try:return db.execute(sql,params).fetchall()
        finally:db.close()

    def shared_lines(self):
        return self.query("SELECT l.line_id,l.case_id FROM case_line l JOIN common_source_record r ON r.parser_index=cast(l.source_row AS TEXT) WHERE r.master_code='X-1'")

    def resolve_shared(self):
        for line,case in self.shared_lines():
            resolve_line(self.db,'resolve-'+case,line,'reviewed-variant',self.identity,'synthetic://review/'+case,'fictional-independent-owner')

    def test_unresolved_same_name_is_separate_until_explicit_resolution(self):
        self.assertEqual(3,len(active_worklist(self.db,as_of=date(2026,10,31))))
        self.resolve_shared()
        work=active_worklist(self.db,as_of=date(2026,10,31))
        shared=next(x for x in work if x['resolved_variant_id'])
        self.assertEqual(2,len(work));self.assertEqual('30',shared['quantity_total'])
        self.assertEqual(2,len(shared['demands']))

    def test_close_only_removes_exclusive_prebid_and_shared_variant_survives(self):
        self.resolve_shared()
        before=self.query('SELECT (SELECT count(*) FROM case_line),(SELECT count(*) FROM common_source_record),(SELECT count(*) FROM normalized_variant)')
        transition_case(self.db,'close','SETTHA2027','close','synthetic://explicit-close')
        work=active_worklist(self.db,as_of=date(2026,10,31))
        self.assertEqual(1,len(work));self.assertEqual('20',work[0]['quantity_total'])
        self.assertEqual(before,self.query('SELECT (SELECT count(*) FROM case_line),(SELECT count(*) FROM common_source_record),(SELECT count(*) FROM normalized_variant)'))
        transition_case(self.db,'reopen','SETTHA2027','reopen','synthetic://reopen')
        self.assertEqual(2,len(active_worklist(self.db,as_of=date(2026,10,31))))

    def test_deadline_and_planned_close_do_not_auto_close_or_fake_an_hour(self):
        plan_closure(self.db,'plan','SETTHA2027','2026-11-26','synthetic://plan')
        work=active_worklist(self.db,as_of=date(2026,12,1))
        self.assertEqual(3,len(work))
        self.assertTrue(any('overdue_unknown_not_auto_closed' in d['flags'] for g in work for d in g['demands']))
        extend_deadline(self.db,'extend','SETTHA2027','2026-12-10','synthetic://extension')
        status,hour=self.query("SELECT status,official_closing_time FROM tender_case WHERE case_id='SETTHA2027'")[0]
        self.assertEqual('active',status);self.assertIsNone(hour)
        work=active_worklist(self.db,as_of=date(2026,12,1))
        self.assertTrue(all('overdue_unknown_not_auto_closed' not in d['flags'] for g in work for d in g['demands'] if d['case_id']=='SETTHA2027'))

    def test_won_fulfillment_is_independent_until_explicitly_finished(self):
        self.resolve_shared()
        line=next(line for line,case in self.shared_lines() if case=='SETTHA2027')
        transition_case(self.db,'won','SETTHA2027','win','synthetic://award')
        create_fulfillment(self.db,'purchase','remaining',line,None,'synthetic://remaining-not-yet-counted')
        work=active_worklist(self.db,as_of=date(2026,10,31))
        self.assertEqual({'prebid','fulfillment'},{x['need_family'] for x in work})
        fulfillment=next(x for x in work if x['need_family']=='fulfillment')
        self.assertIsNone(fulfillment['quantity_total'])
        finish_fulfillment(self.db,'delivered','remaining','fulfilled','synthetic://delivery')
        self.assertEqual(1,len(active_worklist(self.db,as_of=date(2026,10,31))))

    def test_closed_case_extension_and_late_import_do_not_reactivate_demand(self):
        transition_case(self.db,'close','SETTHA2027','close','synthetic://close')
        extend_deadline(self.db,'extend','SETTHA2027','2026-12-10','synthetic://extension')
        import_four(self.root/'source.json',self.root/'manifest.json',self.db)
        work=active_worklist(self.db,as_of=date(2026,10,31))
        self.assertEqual(1,len(work));self.assertEqual('MAHOSOT2027',work[0]['demands'][0]['case_id'])

    def test_duplicate_event_is_idempotent_and_changed_action_conflicts(self):
        first=transition_case(self.db,'same-event','SETTHA2027','close','synthetic://close')
        self.assertEqual(first,transition_case(self.db,'same-event','SETTHA2027','close','synthetic://close'))
        with self.assertRaises(IntakeConflict):
            transition_case(self.db,'same-event','SETTHA2027','reopen','synthetic://reopen')

    def test_active_view_is_read_only(self):
        before=hashlib.sha256(self.db.read_bytes()).hexdigest()
        active_worklist(self.db,as_of=date(2026,10,31))
        self.assertEqual(before,hashlib.sha256(self.db.read_bytes()).hexdigest())

    def test_common_source_inquiry_is_once_per_original_row_before_identity_resolution(self):
        source=source_worklist(self.db,as_of=date(2026,10,31))
        self.assertEqual(2,len(source))
        shared=next(x for x in source if x['master_code']=='X-1')
        self.assertEqual(2,shared['demand_count'])
        self.assertEqual(['MAHOSOT2027','SETTHA2027'],shared['case_refs'])
        self.assertFalse(shared['identity_verified']);self.assertFalse(shared['cross_record_merge'])
        self.assertEqual('same_original_master_row',shared['reuse_scope'])
        self.assertEqual(3,len(active_worklist(self.db,as_of=date(2026,10,31))))

    def test_common_source_group_survives_other_consumer_and_reopen_restores_exclusive(self):
        transition_case(self.db,'close','SETTHA2027','close','synthetic://close')
        source=source_worklist(self.db,as_of=date(2026,10,31))
        self.assertEqual(1,len(source));self.assertEqual('X-1',source[0]['master_code'])
        self.assertEqual(['MAHOSOT2027'],source[0]['case_refs'])
        transition_case(self.db,'reopen','SETTHA2027','reopen','synthetic://reopen')
        self.assertEqual(2,len(source_worklist(self.db,as_of=date(2026,10,31))))
