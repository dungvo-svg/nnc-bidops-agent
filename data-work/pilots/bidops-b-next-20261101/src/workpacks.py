"""Read-only catalog -> local DRAFT preparation inbox, with no dispatch or owner.

The existing ledger handles scoped synthetic missions with known quotes. This
bridge prepares earlier work from catalog needs without pretending it was assigned,
received, executed or commercially approved by a real employee/Agent.
"""
from datetime import date, datetime, timezone
import csv
import hashlib
import json
import os
from pathlib import Path
import sqlite3

from .catalog_lifecycle import source_worklist
from .ledger import canonical, digest


class DraftConflict(ValueError):
    pass


def _file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _catalog_signature(path):
    # A committed WAL transaction need not modify the main database file.
    # This is a fail-closed change detector, not a shared SQLite read transaction.
    wal=Path(str(path)+'-wal')
    try:
        return {"main_sha256":_file_hash(path),
                "wal_sha256":_file_hash(wal) if wal.exists() else None}
    except FileNotFoundError as exc:
        raise DraftConflict('catalog storage changed during signature read') from exc


def _snapshot(catalog_path, as_of=None):
    path=Path(catalog_path).resolve()
    if not path.is_file():
        raise FileNotFoundError(path)
    today=as_of or date.today()
    before=_catalog_signature(path)
    groups=source_worklist(path,as_of=today)
    if _catalog_signature(path)!=before:
        raise DraftConflict("catalog changed during read; no derived update made")
    payloads={}
    for group in groups:
        slot=canonical([group['record_id'],group['need_family']])
        payload={"schema":"bidops-draft-workpack/1","record_id":group['record_id'],
                 "need_family":group['need_family'],"label":group['name_raw'],
                 "source_anchor":group['source_anchor'],"reuse_scope":"same_original_master_row",
                 "identity_verified":group['identity_verified'],"case_refs":group['case_refs'],
                 "need_types":group['need_types'],"case_qualifications":group['case_demands'],
                 "owner_id":None,"agent_id":None,"dispatch_allowed":False,
                 "commercial_authorization":False,
                 "expected_output":"source-anchored preparation/evidence/blockers; qualify each case separately"}
        if slot in payloads:
            raise DraftConflict("duplicate source-work slot")
        payloads[slot]=payload
    return {"catalog_path":str(path),"catalog_file_sha256":before['main_sha256'],"as_of":today.isoformat(),
            "catalog_storage_signature":before,
            "semantic_sha256":digest(payloads),"payloads":payloads}


class WorkpackInbox:
    def __init__(self,queue_db,catalog_path):
        self.queue_path=Path(queue_db).resolve()
        self.catalog_path=Path(catalog_path).resolve()
        if self.queue_path==self.catalog_path or (self.queue_path.exists() and self.catalog_path.exists()
                                                  and os.path.samefile(self.queue_path,self.catalog_path)):
            raise DraftConflict("derived inbox must not be the source catalog")
        self.queue_path.parent.mkdir(parents=True,exist_ok=True)
        self.db=sqlite3.connect(self.queue_path,isolation_level=None)
        try:
            names={r[0] for r in self.db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            if names and 'draft_inbox_meta' not in names:
                raise DraftConflict("existing DB is not a draft inbox")
            self.db.executescript("""
              CREATE TABLE IF NOT EXISTS draft_inbox_meta(catalog_path TEXT PRIMARY KEY);
              CREATE TABLE IF NOT EXISTS draft_slot(slot_key TEXT PRIMARY KEY,current_id TEXT NOT NULL,generation INTEGER NOT NULL,active INTEGER NOT NULL);
              CREATE TABLE IF NOT EXISTS draft_workpack(draft_id TEXT PRIMARY KEY,slot_key TEXT NOT NULL,generation INTEGER NOT NULL,
                payload TEXT NOT NULL,payload_sha256 TEXT NOT NULL,source_snapshot TEXT NOT NULL,state TEXT NOT NULL,
                review_event TEXT,cancel_event TEXT);
              CREATE TABLE IF NOT EXISTS draft_event(event_id TEXT PRIMARY KEY,payload_sha256 TEXT NOT NULL,kind TEXT NOT NULL,receipt TEXT NOT NULL);
            """)
            prior=self.db.execute("SELECT catalog_path FROM draft_inbox_meta").fetchall()
            if prior and prior!=[(str(self.catalog_path),)]:
                raise DraftConflict("inbox is bound to another catalog path")
            self.db.execute("INSERT OR IGNORE INTO draft_inbox_meta VALUES(?)",(str(self.catalog_path),))
        except BaseException:
            self.db.close()
            raise

    def close(self):self.db.close()

    def _event(self,event_id,kind,payload,change,legacy_checksums=()):
        if not isinstance(event_id,str) or not event_id.strip():raise ValueError('event_id required')
        checksum=digest({"kind":kind,"payload":payload})
        self.db.execute('BEGIN IMMEDIATE')
        try:
            old=self.db.execute('SELECT payload_sha256,receipt FROM draft_event WHERE event_id=?',(event_id,)).fetchone()
            if old:
                if old[0]!=checksum and old[0] not in legacy_checksums:
                    raise DraftConflict('event_id reused with different payload or unverifiable legacy intent')
                self.db.execute('COMMIT');return json.loads(old[1])
            result=change()
            receipt={"event_id":event_id,"kind":kind,"payload_sha256":checksum,
                     "occurred_at":datetime.now(timezone.utc).isoformat(),"result":result,
                     "meaning":"local draft receipt only; no assignment, employee ACK or commercial approval"}
            self.db.execute('INSERT INTO draft_event VALUES(?,?,?,?)',(event_id,checksum,kind,canonical(receipt)))
            self.db.execute('COMMIT');return receipt
        except BaseException:
            if self.db.in_transaction:self.db.execute('ROLLBACK')
            raise

    def sync(self,event_id,as_of=None):
        snapshot=_snapshot(self.catalog_path,as_of)
        request={k:snapshot[k] for k in ('catalog_path','as_of','semantic_sha256')}
        def change():
            prior={r[0]:r[1:] for r in self.db.execute('SELECT slot_key,current_id,generation,active FROM draft_slot')}
            self.db.execute('UPDATE draft_slot SET active=0')
            created=unchanged=0
            for slot,payload in snapshot['payloads'].items():
                ph=digest(payload);old=prior.get(slot)
                state='DRAFT'
                if old:
                    old_draft=self.db.execute('SELECT payload_sha256,state FROM draft_workpack WHERE draft_id=?',(old[0],)).fetchone()
                    if old[2] and old_draft[0]==ph:
                        self.db.execute('UPDATE draft_slot SET active=1 WHERE slot_key=?',(slot,));unchanged+=1;continue
                    # A source refresh/reopen must not silently reverse an explicit cancellation.
                    if old_draft[1]=='CANCELLED':state='CANCELLED'
                generation=old[1]+1 if old else 1
                draft_id='draft:'+digest([slot,generation,ph])
                self.db.execute('INSERT INTO draft_workpack VALUES(?,?,?,?,?,?,?,NULL,NULL)',
                                (draft_id,slot,generation,canonical(payload),ph,snapshot['semantic_sha256'],state))
                self.db.execute('INSERT INTO draft_slot VALUES(?,?,?,1) ON CONFLICT(slot_key) DO UPDATE SET current_id=excluded.current_id,generation=excluded.generation,active=1',
                                (slot,draft_id,generation));created+=1
            inactive=self.db.execute('SELECT count(*) FROM draft_slot WHERE active=0').fetchone()[0]
            return {"created_versions":created,"unchanged_active":unchanged,"inactive_slots":inactive,
                    "source_groups":len(snapshot['payloads']),"catalog_file_sha256_at_read":snapshot['catalog_file_sha256'],
                    "owner_assigned":0,"dispatches":0}
        return self._event(event_id,'draft_sync',request,change)

    def _current(self,draft_id,expected_hash):
        row=self.db.execute('SELECT slot_key,payload,payload_sha256,state FROM draft_workpack WHERE draft_id=?',(draft_id,)).fetchone()
        if not row:raise ValueError('unknown draft')
        slot=self.db.execute('SELECT current_id,active FROM draft_slot WHERE slot_key=?',(row[0],)).fetchone()
        if slot[0]!=draft_id or not slot[1]:raise DraftConflict('draft is no longer active/current')
        if expected_hash!=row[2]:raise DraftConflict('draft payload hash mismatch')
        return row

    def review(self,event_id,draft_id,expected_hash,reviewer_label,evidence_ref,as_of=None):
        if not reviewer_label.strip() or not evidence_ref.strip():raise ValueError('local reviewer label and evidence required')
        # Retry identity is caller intent; unrelated source changes are not new intent.
        # A NEW event still validates this exact draft's source scope below.
        request={"draft_id":draft_id,"expected_hash":expected_hash,"reviewer_label":reviewer_label,"evidence_ref":evidence_ref}
        # Pre-fix receipts retained only a checksum, not the full review intent.
        # Authenticate a legacy retry against known immutable snapshot pins, without
        # rewriting its receipt or accepting an unverifiable/changed caller intent.
        legacy_checksums=tuple(digest({"kind":"draft_review","payload":{
            **request,"current_source_semantic_sha256":r[0]}})
            for r in self.db.execute('SELECT DISTINCT source_snapshot FROM draft_workpack'))
        def change():
            snapshot=_snapshot(self.catalog_path,as_of)
            row=self._current(draft_id,expected_hash)
            fresh=snapshot['payloads'].get(row[0])
            if fresh is None or digest(fresh)!=expected_hash:raise DraftConflict('source scope/version drift; sync a new draft before review')
            if row[3]!='DRAFT':raise DraftConflict('only an unreviewed DRAFT may be reviewed')
            self.db.execute("UPDATE draft_workpack SET state='REVIEWED',review_event=? WHERE draft_id=?",(event_id,draft_id))
            return {"draft_id":draft_id,"state":"REVIEWED","owner_id":None,"dispatch_allowed":False,"business_accepted":False,
                    "source_semantic_sha256_at_review":snapshot['semantic_sha256']}
        return self._event(event_id,'draft_review',request,change,legacy_checksums)

    def cancel(self,event_id,draft_id,expected_hash,reason):
        if not reason.strip():raise ValueError('cancellation reason required')
        def change():
            row=self._current(draft_id,expected_hash)
            if row[3]=='CANCELLED':raise DraftConflict('already cancelled; retry original event_id')
            self.db.execute("UPDATE draft_workpack SET state='CANCELLED',cancel_event=? WHERE draft_id=?",(event_id,draft_id))
            return {"draft_id":draft_id,"state":"CANCELLED","history_preserved":True}
        return self._event(event_id,'draft_cancel',{"draft_id":draft_id,"expected_hash":expected_hash,"reason":reason},change)

    def list_active(self,include_cancelled=False):
        rows=self.db.execute('SELECT w.draft_id,w.payload,w.payload_sha256,w.state,w.generation FROM draft_slot s JOIN draft_workpack w ON w.draft_id=s.current_id WHERE s.active=1 ORDER BY w.slot_key').fetchall()
        return [{"draft_id":r[0],"payload":json.loads(r[1]),"payload_sha256":r[2],"state":r[3],"generation":r[4]}
                for r in rows if include_cancelled or r[3]!='CANCELLED']

    def export_csv(self,path):
        out=Path(path).resolve()
        if out in {self.queue_path,self.catalog_path} or (out.exists() and any(os.path.samefile(out,p) for p in (self.queue_path,self.catalog_path))):
            raise DraftConflict('export must not overwrite a database')
        if out.exists():
            raise FileExistsError('choose a separate export path; existing files are not overwritten')
        out.parent.mkdir(parents=True,exist_ok=True)
        fields=['draft_id','state','generation','label','need_family','need_types','case_refs','owner_id','agent_id','source_anchor','payload_sha256','notice']
        with out.open('x',encoding='utf-8-sig',newline='') as handle:
            writer=csv.DictWriter(handle,fieldnames=fields);writer.writeheader()
            for draft in self.list_active(include_cancelled=True):
                p=draft['payload']
                values={k:draft[k] for k in ('draft_id','state','generation','payload_sha256')}
                values.update({k:p[k] for k in ('label','need_family','owner_id','agent_id','source_anchor')})
                values.update({'need_types':' | '.join(p['need_types']),'case_refs':' | '.join(p['case_refs']),
                               'notice':'DRAFT/local review only; owner unknown; no send/acceptance; case qualifications remain separate'})
                writer.writerow({k:("'"+v if isinstance(v,str) and v.lstrip('\ufeff \t\r\n\v\f')[:1] in {'=','+','-','@'} else v) for k,v in values.items()})
        return out


def main(argv=None):
    import argparse
    parser=argparse.ArgumentParser(description='Prepare local DRAFT workpacks from a read-only catalog; no owner assignment or dispatch.')
    parser.add_argument('--catalog',type=Path,required=True,help='existing read-only common catalog SQLite')
    parser.add_argument('--inbox',type=Path,required=True,help='separate derived inbox SQLite')
    parser.add_argument('--event-id',required=True,help='idempotent local sync operation ID')
    parser.add_argument('--as-of',type=date.fromisoformat,help='ISO observation date, otherwise today')
    parser.add_argument('--export-csv',type=Path,help='optional NEW CSV projection; existing files are preserved')
    args=parser.parse_args(argv)
    if not args.catalog.is_file():parser.error('catalog must already exist')
    if args.export_csv and (args.export_csv.exists() or args.export_csv.resolve() in {args.catalog.resolve(),args.inbox.resolve()}):
        parser.error('export must be a separate new file')
    inbox=WorkpackInbox(args.inbox,args.catalog)
    try:
        receipt=inbox.sync(args.event_id,args.as_of)
        if args.export_csv:inbox.export_csv(args.export_csv)
        print(json.dumps(receipt,ensure_ascii=True))
    finally:
        inbox.close()
    return 0


if __name__=='__main__':
    raise SystemExit(main())
