from datetime import date
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from src.workpacks import WorkpackInbox,DraftConflict
from src.ledger import digest
from src.four_bv_intake import import_four
from src.catalog_lifecycle import initialize_lifecycle,transition_case
from tests.test_four_bv_intake import row

AS_OF=date(2026,10,31)


class PacketExportImportBehavior(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='draft-packets-',dir=Path(__file__).resolve().parent)
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
        self.inbox.sync('sync1',AS_OF)

    def tearDown(self):
        self.inbox.close();self.temp.cleanup()

    def shared(self):return next(d for d in self.inbox.list_active(include_cancelled=True) if len(d['payload']['case_refs'])==2)

    def reviewed_shared(self,review_event='review1'):
        draft=self.shared()
        self.inbox.review(review_event,draft['draft_id'],draft['payload_sha256'],'fictional-local-reviewer','synthetic://review',AS_OF)
        return draft

    def export(self,event='export1',name='packet.json',draft=None):
        draft=draft or self.reviewed_shared()
        out=self.root/name
        receipt=self.inbox.export_packet(event,draft['draft_id'],draft['payload_sha256'],out,AS_OF)
        return draft,out,receipt

    def count(self,table):return self.inbox.db.execute('SELECT count(*) FROM '+table).fetchone()[0]

    def write_return(self,packet,name='return.json',**override):
        data={"packet_id":packet['packet_id'],"packet_sha256":packet['packet_sha256'],"draft_id":packet['draft_id'],
              "result":"evidence","evidence_refs":["synthetic://evidence/1"],"note":"synthetic note",
              "claimed_owner":"fictional-person","claimed_agent":None}
        data.update(override)
        path=self.root/name;path.write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8')
        return path

    # ---------------- export ----------------

    def test_export_blocks_catalog_drift_after_review(self):
        draft=self.reviewed_shared();out=self.root/'drift.json'
        transition_case(self.catalog,'close','SETTHA2027','close','synthetic://close')
        with self.assertRaises(DraftConflict):
            self.inbox.export_packet('e-drift',draft['draft_id'],draft['payload_sha256'],out,AS_OF)
        self.assertFalse(out.exists());self.assertEqual(0,self.count('draft_packet'))

    def test_export_requires_current_active_reviewed_draft_and_exact_hash(self):
        draft=self.shared();out=self.root/'p.json'
        with self.assertRaises(DraftConflict):  # still DRAFT
            self.inbox.export_packet('e-draft',draft['draft_id'],draft['payload_sha256'],out,AS_OF)
        self.inbox.review('review1',draft['draft_id'],draft['payload_sha256'],'local','synthetic://review',AS_OF)
        with self.assertRaises(DraftConflict):  # wrong hash
            self.inbox.export_packet('e-hash',draft['draft_id'],'0'*64,out,AS_OF)
        self.inbox.cancel('cancel1',draft['draft_id'],draft['payload_sha256'],'local planning cancelled')
        with self.assertRaises(DraftConflict):  # CANCELLED
            self.inbox.export_packet('e-cancel',draft['draft_id'],draft['payload_sha256'],out,AS_OF)
        self.assertFalse(out.exists());self.assertEqual(0,self.count('draft_packet'))
        self.assertEqual(0,self.count("draft_event WHERE kind='packet_export'"))

    def test_export_of_unreviewed_draft_without_cancel_leaves_nothing_behind(self):
        draft=self.shared();out=self.root/'p.json'
        with self.assertRaises(DraftConflict):
            self.inbox.export_packet('e1',draft['draft_id'],draft['payload_sha256'],out,AS_OF)
        self.assertFalse(out.exists());self.assertEqual(0,self.count('draft_packet'))

    def test_stale_reviewed_draft_cannot_be_exported(self):
        draft=self.reviewed_shared()
        transition_case(self.catalog,'close','SETTHA2027','close','synthetic://close')
        self.inbox.sync('sync2',AS_OF)
        out=self.root/'p.json'
        with self.assertRaises(DraftConflict):
            self.inbox.export_packet('e1',draft['draft_id'],draft['payload_sha256'],out,AS_OF)
        self.assertFalse(out.exists())

    def test_export_shared_draft_keeps_case_qualifications_separate_and_no_owner_or_dispatch(self):
        draft,out,receipt=self.export()
        packet=json.loads(out.read_text(encoding='utf-8'))
        self.assertEqual('bidops-workpack-packet/1',packet['schema'])
        self.assertEqual('packet:'+digest([draft['draft_id'],draft['payload_sha256']]),packet['packet_id'])
        self.assertEqual(draft['draft_id'],packet['draft_id']);self.assertEqual(draft['generation'],packet['generation'])
        self.assertEqual(draft['payload_sha256'],packet['payload_sha256']);self.assertEqual(draft['payload'],packet['payload'])
        self.assertEqual(2,len(packet['payload']['case_qualifications']))
        self.assertTrue(packet['payload']['source_anchor'])
        self.assertIsNone(packet['owner_id']);self.assertIsNone(packet['agent_id'])
        self.assertIs(False,packet['dispatch_allowed'])
        self.assertEqual('LOCAL_FILE_EXPORT_NOT_SENT',packet['delivery'])
        body={k:v for k,v in packet.items() if k!='packet_sha256'}
        self.assertEqual(digest(body),packet['packet_sha256'])
        self.assertEqual(packet['packet_sha256'],receipt['result']['packet_sha256'])
        stored=self.inbox.db.execute('SELECT packet_id,draft_id,payload_sha256,packet_sha256,path,export_event FROM draft_packet').fetchall()
        self.assertEqual([(packet['packet_id'],draft['draft_id'],draft['payload_sha256'],packet['packet_sha256'],str(out.resolve()),'export1')],stored)
        self.assertEqual('REVIEWED',self.shared()['state'])  # export does not change draft state

    def test_export_refuses_existing_file_and_database_paths(self):
        draft=self.reviewed_shared()
        for target in (self.queue,self.catalog):
            with self.assertRaises(DraftConflict):
                self.inbox.export_packet('e-db',draft['draft_id'],draft['payload_sha256'],target,AS_OF)
        existing=self.root/'existing.json';existing.write_text('SENTINEL',encoding='utf-8')
        with self.assertRaises(FileExistsError):
            self.inbox.export_packet('e-exist',draft['draft_id'],draft['payload_sha256'],existing,AS_OF)
        self.assertEqual('SENTINEL',existing.read_text(encoding='utf-8'))
        self.assertEqual(0,self.count('draft_packet'));self.assertEqual(0,self.count("draft_event WHERE kind='packet_export'"))
        # the failed attempts leave the event free for a clean export to a new path
        self.inbox.export_packet('e-exist',draft['draft_id'],draft['payload_sha256'],self.root/'ok.json',AS_OF)
        self.assertEqual(1,self.count('draft_packet'))

    def test_exact_export_retry_returns_same_receipt_and_leaves_file_unchanged(self):
        draft,out,first=self.export()
        before=out.read_bytes()
        again=self.inbox.export_packet('export1',draft['draft_id'],draft['payload_sha256'],out,AS_OF)
        self.assertEqual(first,again);self.assertEqual(before,out.read_bytes())
        self.assertEqual(1,self.count('draft_packet'));self.assertEqual(1,self.count("draft_event WHERE kind='packet_export'"))
        with self.assertRaises(DraftConflict):  # same event_id, different target
            self.inbox.export_packet('export1',draft['draft_id'],draft['payload_sha256'],self.root/'other.json',AS_OF)
        with self.assertRaises(DraftConflict):  # new event cannot mint a second packet for the same draft version
            self.inbox.export_packet('export2',draft['draft_id'],draft['payload_sha256'],self.root/'other.json',AS_OF)
        self.assertFalse((self.root/'other.json').exists());self.assertEqual(before,out.read_bytes())

    # ---------------- import ----------------

    def test_import_return_is_unverified_claim_and_changes_nothing_else(self):
        draft,out,_=self.export();packet=json.loads(out.read_text(encoding='utf-8'))
        events_before=self.count('draft_event')
        ret=self.write_return(packet,claimed_owner='CEO',claimed_agent='agent-007')
        receipt=self.inbox.import_return('import1',ret)
        res=receipt['result']
        self.assertEqual('RETURN_UNVERIFIED',res['status'])
        self.assertEqual('CEO',res['claimed_owner']);self.assertEqual('agent-007',res['claimed_agent'])
        self.assertIs(False,res['verified_identity']);self.assertIs(False,res['business_accepted'])
        self.assertEqual(events_before+1,self.count('draft_event'))
        after=self.shared()
        self.assertIsNone(after['payload']['owner_id']);self.assertIsNone(after['payload']['agent_id'])
        self.assertEqual(draft['payload_sha256'],after['payload_sha256']);self.assertEqual('REVIEWED',after['state'])
        self.assertEqual(draft['draft_id'],after['draft_id'])
        rows=self.inbox.list_returns();self.assertEqual(1,len(rows))
        self.assertEqual(packet['packet_id'],rows[0]['packet_id']);self.assertEqual('RETURN_UNVERIFIED',rows[0]['status'])
        self.assertEqual('CEO',rows[0]['claimed_owner']);self.assertEqual('import1',rows[0]['import_event'])
        self.assertEqual(rows[0]['return_id'],res['return_id']);self.assertTrue(rows[0]['return_id'].startswith('return:'))
        # the exported packet file itself is untouched and still has no owner
        self.assertIsNone(json.loads(out.read_text(encoding='utf-8'))['owner_id'])

    def test_import_rejections_record_nothing(self):
        _,out,_=self.export();packet=json.loads(out.read_text(encoding='utf-8'))
        bad=[('tampered-hash',{'packet_sha256':'f'*64}),
             ('unknown-packet',{'packet_id':'packet:'+'0'*64}),
             ('wrong-draft',{'draft_id':'draft:'+'1'*64})]
        for name,override in bad:
            with self.subTest(name):
                with self.assertRaises(DraftConflict):
                    self.inbox.import_return('i-'+name,self.write_return(packet,name+'.json',**override))
        self.assertEqual(0,self.count('draft_return'));self.assertEqual(0,self.count("draft_event WHERE kind='return_import'"))

    def test_malformed_returns_raise_value_error_and_record_nothing(self):
        _,out,_=self.export();packet=json.loads(out.read_text(encoding='utf-8'))
        cases={'bad-result':{'result':'approved'},'evidence-empty':{'evidence_refs':[]},
               'refs-not-list':{'evidence_refs':'x'},'refs-not-str':{'evidence_refs':[1]},
               'note-not-str':{'note':None},'owner-not-str':{'claimed_owner':5},'agent-not-str':{'claimed_agent':['a']},
               'unknown-key':{'verified':True}}
        for name,override in cases.items():
            with self.subTest(name):
                with self.assertRaises(ValueError):
                    self.inbox.import_return('i-'+name,self.write_return(packet,name+'.json',**override))
        data={"packet_id":packet['packet_id']}  # missing required fields
        missing=self.root/'missing.json';missing.write_text(json.dumps(data),encoding='utf-8')
        notjson=self.root/'notjson.json';notjson.write_text('{oops',encoding='utf-8')
        notobj=self.root/'notobj.json';notobj.write_text('[]',encoding='utf-8')
        for path in (missing,notjson,notobj):
            with self.subTest(path.name):
                with self.assertRaises(ValueError):self.inbox.import_return('i-'+path.name,path)
        self.assertEqual(0,self.count('draft_return'));self.assertEqual(0,self.count("draft_event WHERE kind='return_import'"))
        # non-evidence results may legitimately carry no references
        ok=self.write_return(packet,'hold.json',result='hold',evidence_refs=[],claimed_owner=None)
        self.assertEqual('RETURN_UNVERIFIED',self.inbox.import_return('i-hold',ok)['result']['status'])

    def test_exact_import_retry_same_receipt_but_changed_content_or_new_event_rejected(self):
        _,out,_=self.export();packet=json.loads(out.read_text(encoding='utf-8'))
        ret=self.write_return(packet)
        first=self.inbox.import_return('import1',ret)
        self.assertEqual(first,self.inbox.import_return('import1',ret))
        self.assertEqual(1,self.count('draft_return'));self.assertEqual(1,self.count("draft_event WHERE kind='return_import'"))
        changed=self.write_return(packet,'changed.json',note='different note')
        with self.assertRaises(DraftConflict):self.inbox.import_return('import1',changed)
        with self.assertRaisesRegex(DraftConflict,'return already imported'):self.inbox.import_return('import2',ret)
        self.assertEqual(1,self.count('draft_return'));self.assertEqual(1,self.count("draft_event WHERE kind='return_import'"))

    def test_return_after_source_change_is_history_only_and_current_draft_unaffected(self):
        draft,out,_=self.export();packet=json.loads(out.read_text(encoding='utf-8'))
        transition_case(self.catalog,'close','SETTHA2027','close','synthetic://close')
        self.inbox.sync('sync2',AS_OF)
        current=self.inbox.list_active();self.assertEqual(1,len(current))
        self.assertNotEqual(draft['draft_id'],current[0]['draft_id'])
        snapshot=[(d['draft_id'],d['state'],d['payload_sha256'],d['payload']['owner_id']) for d in current]
        slots_before=self.inbox.db.execute('SELECT * FROM draft_slot ORDER BY slot_key').fetchall()
        receipt=self.inbox.import_return('import1',self.write_return(packet,claimed_owner='CEO'))
        self.assertEqual('RETURN_HISTORY_ONLY',receipt['result']['status'])
        self.assertEqual(snapshot,[(d['draft_id'],d['state'],d['payload_sha256'],d['payload']['owner_id']) for d in self.inbox.list_active()])
        self.assertEqual(slots_before,self.inbox.db.execute('SELECT * FROM draft_slot ORDER BY slot_key').fetchall())

    def test_return_after_cancel_is_history_only_and_does_not_reactivate(self):
        draft,out,_=self.export();packet=json.loads(out.read_text(encoding='utf-8'))
        self.inbox.cancel('cancel1',draft['draft_id'],draft['payload_sha256'],'local planning cancelled')
        receipt=self.inbox.import_return('import1',self.write_return(packet))
        self.assertEqual('RETURN_HISTORY_ONLY',receipt['result']['status'])
        self.assertEqual('CANCELLED',self.shared()['state'])
        self.assertTrue(all(d['draft_id']!=draft['draft_id'] for d in self.inbox.list_active()))

    def test_claimed_owner_ceo_grants_nothing(self):
        draft,out,_=self.export();packet=json.loads(out.read_text(encoding='utf-8'))
        slot_before=self.inbox.db.execute('SELECT * FROM draft_slot ORDER BY slot_key').fetchall()
        wp_before=self.inbox.db.execute('SELECT * FROM draft_workpack ORDER BY draft_id').fetchall()
        res=self.inbox.import_return('import1',self.write_return(packet,claimed_owner='CEO'))['result']
        self.assertEqual('CEO',res['claimed_owner']);self.assertIs(False,res['verified_identity']);self.assertIs(False,res['business_accepted'])
        self.assertEqual(slot_before,self.inbox.db.execute('SELECT * FROM draft_slot ORDER BY slot_key').fetchall())
        self.assertEqual(wp_before,self.inbox.db.execute('SELECT * FROM draft_workpack ORDER BY draft_id').fetchall())
        self.assertTrue(all(d['payload']['owner_id'] is None and d['payload']['agent_id'] is None for d in self.inbox.list_active()))


if __name__=='__main__':
    unittest.main()
