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
              CREATE TABLE IF NOT EXISTS draft_packet(packet_id TEXT PRIMARY KEY,draft_id TEXT NOT NULL,payload_sha256 TEXT NOT NULL,
                packet_sha256 TEXT NOT NULL,path TEXT NOT NULL,export_event TEXT NOT NULL);
              CREATE TABLE IF NOT EXISTS draft_return(return_id TEXT PRIMARY KEY,packet_id TEXT NOT NULL,status TEXT NOT NULL,
                claimed_owner TEXT,claimed_agent TEXT,content_sha256 TEXT NOT NULL,import_event TEXT NOT NULL,content TEXT NOT NULL);
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

    def export_packet(self,event_id,draft_id,expected_hash,out_path,as_of=None):
        """Write a NEW local JSON packet for a REVIEWED current draft. Nothing is sent or assigned."""
        out=Path(out_path).resolve()
        request={"draft_id":draft_id,"expected_hash":expected_hash,"out_path":str(out)}
        def change():
            row=self._current(draft_id,expected_hash)
            if row[3]!='REVIEWED':raise DraftConflict('only a current REVIEWED draft may be exported')
            # Same source-scope check as review: catalog drift after review needs a new draft.
            snapshot=_snapshot(self.catalog_path,as_of)
            fresh=snapshot['payloads'].get(row[0])
            if fresh is None or digest(fresh)!=expected_hash:raise DraftConflict('source scope/version drift; sync a new draft before export')
            if out in {self.queue_path,self.catalog_path} or (out.exists() and any(os.path.samefile(out,p) for p in (self.queue_path,self.catalog_path))):
                raise DraftConflict('packet export must not overwrite a database')
            packet_id='packet:'+digest([draft_id,expected_hash])
            if self.db.execute('SELECT 1 FROM draft_packet WHERE packet_id=?',(packet_id,)).fetchone():
                raise DraftConflict('packet already exported for this draft version')
            generation=self.db.execute('SELECT generation FROM draft_workpack WHERE draft_id=?',(draft_id,)).fetchone()[0]
            body={"schema":"bidops-workpack-packet/1","packet_id":packet_id,"draft_id":draft_id,"generation":generation,
                  "payload_sha256":expected_hash,"payload":json.loads(row[1]),
                  "source_semantic_sha256_at_export":snapshot['semantic_sha256'],"owner_id":None,"agent_id":None,
                  "dispatch_allowed":False,"delivery":"LOCAL_FILE_EXPORT_NOT_SENT"}
            packet=dict(body,packet_sha256=digest(body))
            self.db.execute('INSERT INTO draft_packet VALUES(?,?,?,?,?,?)',
                            (packet_id,draft_id,expected_hash,packet['packet_sha256'],str(out),event_id))
            out.parent.mkdir(parents=True,exist_ok=True)
            # Exclusive create; FileExistsError rolls back the row above, so nothing is recorded.
            with out.open('x',encoding='utf-8',newline='\n') as handle:
                handle.write(json.dumps(packet,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
            return {"packet_id":packet_id,"draft_id":draft_id,"payload_sha256":expected_hash,
                    "packet_sha256":packet['packet_sha256'],"path":str(out),"owner_id":None,"agent_id":None,
                    "dispatch_allowed":False,"delivery":"LOCAL_FILE_EXPORT_NOT_SENT"}
        return self._event(event_id,'packet_export',request,change)

    _RETURN_KEYS={"packet_id","packet_sha256","draft_id","result","evidence_refs","note","claimed_owner","claimed_agent"}

    @classmethod
    def _read_return(cls,return_path):
        try:
            data=json.loads(Path(return_path).read_bytes().decode('utf-8'))
        except (json.JSONDecodeError,UnicodeDecodeError) as exc:
            raise ValueError('return file is not valid UTF-8 JSON') from exc
        if not isinstance(data,dict):raise ValueError('return must be a JSON object')
        if set(data)!=cls._RETURN_KEYS:
            raise ValueError('return fields must be exactly: '+', '.join(sorted(cls._RETURN_KEYS)))
        for key in ('packet_id','packet_sha256','draft_id'):
            if not isinstance(data[key],str) or not data[key].strip():raise ValueError(key+' must be a non-empty string')
        if data['result'] not in ('evidence','blocker','hold'):raise ValueError('result must be evidence, blocker or hold')
        refs=data['evidence_refs']
        if not isinstance(refs,list) or any(not isinstance(r,str) or not r.strip() for r in refs):
            raise ValueError('evidence_refs must be a list of non-empty strings')
        if data['result']=='evidence' and not refs:raise ValueError('evidence result requires evidence_refs')
        if not isinstance(data['note'],str):raise ValueError('note must be a string')
        for key in ('claimed_owner','claimed_agent'):
            if data[key] is not None and not isinstance(data[key],str):raise ValueError(key+' must be a string or null')
        return data

    def import_return(self,event_id,return_path):
        """Record a return as an UNVERIFIED claim. Never changes drafts, slots or owners."""
        data=self._read_return(return_path)
        content_sha=digest(data);return_id='return:'+content_sha
        def change():
            packet=self.db.execute('SELECT draft_id,packet_sha256 FROM draft_packet WHERE packet_id=?',(data['packet_id'],)).fetchone()
            if not packet:raise DraftConflict('unknown packet')
            if packet[1]!=data['packet_sha256']:raise DraftConflict('packet hash mismatch')
            if packet[0]!=data['draft_id']:raise DraftConflict('draft_id does not match packet')
            if self.db.execute('SELECT 1 FROM draft_return WHERE return_id=?',(return_id,)).fetchone():
                raise DraftConflict('return already imported')
            draft=self.db.execute('SELECT slot_key,state FROM draft_workpack WHERE draft_id=?',(packet[0],)).fetchone()
            slot=self.db.execute('SELECT current_id,active FROM draft_slot WHERE slot_key=?',(draft[0],)).fetchone()
            live=bool(slot and slot[0]==packet[0] and slot[1] and draft[1]!='CANCELLED')
            status='RETURN_UNVERIFIED' if live else 'RETURN_HISTORY_ONLY'
            self.db.execute('INSERT INTO draft_return VALUES(?,?,?,?,?,?,?,?)',
                            (return_id,data['packet_id'],status,data['claimed_owner'],data['claimed_agent'],
                             content_sha,event_id,canonical(data)))
            return {"return_id":return_id,"packet_id":data['packet_id'],"draft_id":packet[0],"status":status,
                    "return_result":data['result'],"evidence_ref_count":len(data['evidence_refs']),
                    "claimed_owner":data['claimed_owner'],"claimed_agent":data['claimed_agent'],
                    "claims_note":"claimed_owner/claimed_agent are unverified claims from the returned file",
                    "verified_identity":False,"business_accepted":False,"owner_id":None,
                    "draft_state_changed":False}
        return self._event(event_id,'return_import',{"content_sha256":content_sha},change)

    def list_returns(self):
        rows=self.db.execute('SELECT return_id,packet_id,status,claimed_owner,claimed_agent,content_sha256,import_event,content FROM draft_return ORDER BY rowid').fetchall()
        keys=('return_id','packet_id','status','claimed_owner','claimed_agent','content_sha256','import_event')
        return [dict(zip(keys,r[:7]),content=json.loads(r[7])) for r in rows]

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
