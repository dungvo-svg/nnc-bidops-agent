import csv
from datetime import date
import hashlib
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

from src.workpacks import WorkpackInbox,DraftConflict
import src.workpacks as workpacks
from src.ledger import canonical,digest
from src.four_bv_intake import import_four
from src.catalog_lifecycle import initialize_lifecycle,transition_case,create_fulfillment,extend_deadline
from tests.test_four_bv_intake import row

AS_OF=date(2026,10,31)


class WorkpackBridgeBehavior(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='draft-workpacks-',dir=Path(__file__).resolve().parent)
        self.root=Path(self.temp.name);self.catalog=self.root/'catalog.sqlite';self.queue=self.root/'inbox.sqlite'
        rows=[row(**{'Tên tiếng Anh':'\t=2+3'}),row('X-2','1',**{'SL Mahosot':''})]
        source=self.root/'source.json';source.write_text(json.dumps(rows,ensure_ascii=False),encoding='utf-8');data=source.read_bytes()
        manifest={'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'row_count':2,
                  'sources':[{'group':'vt','drive_file_id':'fictional','url':'https://example.invalid/',
                              'extracted_content_sha256':'a'*64,'raw_xlsx_sha256':None,'selected_rows':2}],
                  'case_deadlines_planning_only':{'Settha':'2026-11-26','Mahosot':'2026-11-25','SVNK':None,'Me and Dek':'2026-11-27'}}
        mp=self.root/'manifest.json';mp.write_text(json.dumps(manifest),encoding='utf-8')
        import_four(source,mp,self.catalog);initialize_lifecycle(self.catalog)
        self.inbox=WorkpackInbox(self.queue,self.catalog)

    def tearDown(self):
        self.inbox.close();self.temp.cleanup()

    def shared(self):return next(d for d in self.inbox.list_active() if len(d['payload']['case_refs'])==2)

    def test_one_common_inquiry_retains_separate_case_qualifications_and_source_is_read_only(self):
        before=hashlib.sha256(self.catalog.read_bytes()).hexdigest()
        receipt=self.inbox.sync('sync1',AS_OF)
        self.assertEqual(2,receipt['result']['source_groups'])
        shared=self.shared()
        self.assertEqual(2,len(shared['payload']['case_qualifications']))
        self.assertIsNone(shared['payload']['owner_id']);self.assertIsNone(shared['payload']['agent_id'])
        self.assertFalse(shared['payload']['dispatch_allowed'])
        self.assertFalse(shared['payload']['identity_verified'])
        self.assertEqual('DRAFT',shared['state'])
        self.assertEqual(before,hashlib.sha256(self.catalog.read_bytes()).hexdigest())

    def test_exact_sync_retry_and_reopen_db_do_not_duplicate_drafts_or_events(self):
        receipt=self.inbox.sync('sync1',AS_OF)
        ids=[d['draft_id'] for d in self.inbox.list_active()]
        self.inbox.close();self.inbox=WorkpackInbox(self.queue,self.catalog)
        self.assertEqual(receipt,self.inbox.sync('sync1',AS_OF))
        self.assertEqual(ids,[d['draft_id'] for d in self.inbox.list_active()])
        self.assertEqual(1,self.inbox.db.execute('SELECT count(*) FROM draft_event').fetchone()[0])

    def test_review_is_local_only_and_source_scope_drift_requires_new_draft(self):
        self.inbox.sync('sync1',AS_OF);draft=self.shared()
        review=self.inbox.review('review1',draft['draft_id'],draft['payload_sha256'],'fictional-local-reviewer','synthetic://review',AS_OF)
        self.assertFalse(review['result']['business_accepted']);self.assertIsNone(review['result']['owner_id'])
        transition_case(self.catalog,'close','SETTHA2027','close','synthetic://close')
        with self.assertRaises(DraftConflict):
            self.inbox.review('stale-review',draft['draft_id'],draft['payload_sha256'],'local','synthetic://review',AS_OF)
        with self.assertRaises(DraftConflict):self.inbox.sync('sync1',AS_OF)
        self.inbox.sync('sync2',AS_OF)
        active=self.inbox.list_active();self.assertEqual(1,len(active));self.assertEqual('DRAFT',active[0]['state'])
        self.assertGreater(active[0]['generation'],draft['generation'])
        self.assertEqual('REVIEWED',self.inbox.db.execute('SELECT state FROM draft_workpack WHERE draft_id=?',(draft['draft_id'],)).fetchone()[0])
        transition_case(self.catalog,'reopen','SETTHA2027','reopen','synthetic://reopen')
        self.inbox.sync('sync3',AS_OF)
        self.assertEqual(2,len(self.inbox.list_active()))
        self.assertTrue(all(d['state']=='DRAFT' for d in self.inbox.list_active()))

    def test_cancel_is_durable_and_sync_does_not_silently_revive_it(self):
        self.inbox.sync('sync1',AS_OF);draft=self.shared()
        first=self.inbox.cancel('cancel',draft['draft_id'],draft['payload_sha256'],'local planning cancelled')
        self.assertEqual(first,self.inbox.cancel('cancel',draft['draft_id'],draft['payload_sha256'],'local planning cancelled'))
        self.inbox.sync('sync2',AS_OF)
        self.assertEqual(1,len(self.inbox.list_active()))
        transition_case(self.catalog,'close','SETTHA2027','close','synthetic://close')
        self.inbox.sync('sync3',AS_OF)
        self.assertEqual([],self.inbox.list_active())
        self.assertEqual('CANCELLED',self.inbox.list_active(include_cancelled=True)[0]['state'])

    def test_won_case_fulfillment_is_a_separate_preparation_family(self):
        self.inbox.sync('sync1',AS_OF);shared=self.shared()
        line=next(d['line_id'] for d in shared['payload']['case_qualifications'] if d['case_id']=='SETTHA2027')
        transition_case(self.catalog,'win','SETTHA2027','win','synthetic://award')
        create_fulfillment(self.catalog,'fulfillment','remaining',line,None,'synthetic://remaining')
        self.inbox.sync('sync2',AS_OF)
        self.assertEqual({'prebid','fulfillment'},{d['payload']['need_family'] for d in self.inbox.list_active()})
        self.assertTrue(all(d['payload']['owner_id'] is None for d in self.inbox.list_active()))

    def test_inbox_or_export_cannot_overwrite_source_and_csv_neutralizes_formula_prefix(self):
        with self.assertRaises(DraftConflict):WorkpackInbox(self.catalog,self.catalog)
        self.inbox.sync('sync1',AS_OF)
        with self.assertRaises(DraftConflict):self.inbox.export_csv(self.catalog)
        out=self.root/'DRAFT.csv';self.inbox.export_csv(out)
        with out.open(encoding='utf-8-sig',newline='') as handle:
            data=list(csv.DictReader(handle))
        self.assertTrue(next(r['label'] for r in data if '=2+3' in r['label']).startswith("'"))
        self.assertTrue(all(r['owner_id']=='' and r['state']=='DRAFT' for r in data))
        previous=out.read_bytes()
        with self.assertRaises(FileExistsError):self.inbox.export_csv(out)
        self.assertEqual(previous,out.read_bytes())

    def exclusive(self):
        return next(d for d in self.inbox.list_active() if d['payload']['case_refs']==['SETTHA2027'])

    def test_exact_review_retry_survives_unrelated_change_but_rejects_changed_intent(self):
        self.inbox.sync('sync1',AS_OF);draft=self.exclusive()
        args=('review1',draft['draft_id'],draft['payload_sha256'],'local','synthetic://review',AS_OF)
        first=self.inbox.review(*args)
        extend_deadline(self.catalog,'extend-unrelated','MAHOSOT2027','2026-12-31','synthetic://extension')
        self.assertEqual(first,self.inbox.review(*args))
        with self.assertRaises(DraftConflict):
            self.inbox.review('review1',draft['draft_id'],draft['payload_sha256'],'different','synthetic://review',AS_OF)
        self.assertEqual(1,self.inbox.db.execute("SELECT count(*) FROM draft_event WHERE kind='draft_review'").fetchone()[0])

    def test_new_review_event_still_rejects_affected_source_drift(self):
        self.inbox.sync('sync1',AS_OF);draft=self.exclusive()
        extend_deadline(self.catalog,'extend-related','SETTHA2027','2026-12-31','synthetic://extension')
        with self.assertRaisesRegex(DraftConflict,'source scope/version drift'):
            self.inbox.review('new-review',draft['draft_id'],draft['payload_sha256'],'local','synthetic://review',AS_OF)
        self.assertEqual('DRAFT',self.exclusive()['state'])
        self.assertEqual(0,self.inbox.db.execute("SELECT count(*) FROM draft_event WHERE kind='draft_review'").fetchone()[0])

    def test_legacy_review_retry_preserves_receipt_and_does_not_accept_changed_intent(self):
        self.inbox.sync('sync1',AS_OF);draft=self.exclusive()
        request={'draft_id':draft['draft_id'],'expected_hash':draft['payload_sha256'],
                 'reviewer_label':'local','evidence_ref':'synthetic://review',
                 'current_source_semantic_sha256':workpacks._snapshot(self.catalog,AS_OF)['semantic_sha256']}
        checksum=digest({'kind':'draft_review','payload':request})
        old={'event_id':'legacy','kind':'draft_review','payload_sha256':checksum,
             'occurred_at':'2026-10-31T00:00:00+00:00','result':{'draft_id':draft['draft_id'],'state':'REVIEWED'}}
        self.inbox.db.execute("UPDATE draft_workpack SET state='REVIEWED',review_event='legacy' WHERE draft_id=?",(draft['draft_id'],))
        self.inbox.db.execute('INSERT INTO draft_event VALUES(?,?,?,?)',('legacy',checksum,'draft_review',canonical(old)))
        extend_deadline(self.catalog,'extend-unrelated','MAHOSOT2027','2026-12-31','synthetic://extension')
        args=('legacy',draft['draft_id'],draft['payload_sha256'],'local','synthetic://review',AS_OF)
        self.assertEqual(old,self.inbox.review(*args))
        with self.assertRaises(DraftConflict):
            self.inbox.review('legacy',draft['draft_id'],draft['payload_sha256'],'local','synthetic://different',AS_OF)
        self.assertEqual(canonical(old),self.inbox.db.execute("SELECT receipt FROM draft_event WHERE event_id='legacy'").fetchone()[0])

    def test_unverifiable_legacy_review_does_not_guess_old_intent(self):
        self.inbox.sync('sync1',AS_OF);draft=self.exclusive()
        request={'draft_id':draft['draft_id'],'expected_hash':draft['payload_sha256'],
                 'reviewer_label':'local','evidence_ref':'synthetic://review',
                 'current_source_semantic_sha256':'unpersisted-legacy-snapshot'}
        checksum=digest({'kind':'draft_review','payload':request})
        self.inbox.db.execute('INSERT INTO draft_event VALUES(?,?,?,?)',('legacy',checksum,'draft_review',canonical({'legacy':True})))
        with self.assertRaisesRegex(DraftConflict,'unverifiable legacy intent'):
            self.inbox.review('legacy',draft['draft_id'],draft['payload_sha256'],'local','synthetic://review',AS_OF)

    def test_csv_race_preserves_file_created_between_check_and_open(self):
        self.inbox.sync('sync1',AS_OF)
        out=self.root/'race.csv';original=Path.open;injected=False
        def racing_open(path,mode='r',*args,**kwargs):
            nonlocal injected
            if path==out and mode in ('x','w') and not injected:
                injected=True
                with original(path,'w',encoding='utf-8') as handle:handle.write('OTHER PROCESS SENTINEL')
            return original(path,mode,*args,**kwargs)
        with patch.object(Path,'open',racing_open):
            with self.assertRaises(FileExistsError):self.inbox.export_csv(out)
        self.assertTrue(injected)
        self.assertEqual('OTHER PROCESS SENTINEL',out.read_text(encoding='utf-8'))

    def test_wal_commit_during_snapshot_fails_closed_without_inbox_event(self):
        writer=sqlite3.connect(self.catalog)
        try:
            self.assertEqual('wal',writer.execute('PRAGMA journal_mode=WAL').fetchone()[0])
            writer.execute('PRAGMA wal_autocheckpoint=0')
            main_before=hashlib.sha256(self.catalog.read_bytes()).hexdigest()
            original=workpacks.source_worklist
            def concurrent_commit(*args,**kwargs):
                groups=original(*args,**kwargs)
                writer.execute("UPDATE tender_case SET deadline_observed='2027-01-15' WHERE case_id='MAHOSOT2027'")
                writer.commit()
                return groups
            with patch.object(workpacks,'source_worklist',concurrent_commit):
                with self.assertRaisesRegex(DraftConflict,'catalog changed during read'):
                    self.inbox.sync('racing-sync',AS_OF)
            self.assertEqual(main_before,hashlib.sha256(self.catalog.read_bytes()).hexdigest())
            self.assertEqual(0,self.inbox.db.execute('SELECT count(*) FROM draft_event').fetchone()[0])
            self.assertEqual([],self.inbox.list_active())
        finally:writer.close()
