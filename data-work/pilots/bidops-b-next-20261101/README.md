# NNC BidOps — isolated local B pilot

CEO BidOps supports multiple business branches; hospital tender work is the first slice. Each employee retains their own Agent and machine. This pilot demonstrates scoped internal work and evidence receipts, not remote control or live procurement authority.

## Run

Python 3.11+; standard library only. From this project root:

```powershell
python -m unittest discover -s tests -v
python demo.py --out demo-output
```

The demo uses fictional principals, sources, quotes and packages. Its SQLite database and JSON outputs are local to the chosen output directory. It does not read the source project, connect to a service, refresh a workbook, or send a mission to staff. Supply an empty/separate output directory for a clean run; follow the demo's existing-output behavior rather than deleting another run.

## What to review

- `AGENTS.md` and `CLAUDE.md`: coding entry points and ownership.
- `context/BRIEF.md`: current mission, decisions, business boundaries and known source conflicts.
- `context/source-manifest.json`: read-only originals/indexes and audit versions; indexed does not mean reread or operationally accepted.
- `docs/CODING-CONTRACT.md` and `docs/DATA-CONTRACT.md`: invariants, demand lifecycle and diagnostic consumption.
- `src/ledger.py`: deterministic SQLite state/event boundary.
- `tests/`: behavioral acceptance; see the execution receipt outside this repo for actual run counts.

Source intake is common; requirement/package rows remain distinct. Matching requires explicit variants and source versions, not MPSC/name alone. Goods, documents and money have separate evidence. Mission issue/receive/return and reviewed/applied/used are separate persisted steps. A useful mismatch may be consumed as a HOLD diagnostic without approving an incompatible offer.

Active sourcing is a view of active demand, not a destructive catalog deletion. Closing one package removes its prebid need only; shared demand and post-win fulfillment remain. Deadlines alone do not confirm closure. History, quote versions and provenance are retained.

## Repository and operational status

Local branch `pilot/bidops-b`; remote is absent. The explicitly requested private `nnc-lao/nnc-bidops` creation was attempted once, but GitHub account `VOSYDUNG` lacks `CreateRepository`. No personal/public fallback, grants or credentials were created. No code/business data was pushed.

This is a local synthetic kernel. It does not authenticate real principals, provide a cross-owner listener/transport, guarantee queue leases/backpressure/recovery across machines, or prove staff onboarding. Pilot capability strings are fixture policy, not security or company ACLs. Master writes, quotes/commitments, contact, submission, VM deployment and merge/deploy remain outside scope.

Actual Kom requirements are extracted separately as read-only, source-anchored intake for comparison with existing four-hospital rows. They are not bundled as fake synthetic data or silently matched to variants. Source documents, business bundles and extraction outputs stay outside Git; Excel/CSV is a human-facing export, never a second master.

## Read-only catalog intake

`src/catalog_intake.py` is a separate explicit-input adapter for the normalized Kom CSV. It preserves source-anchored case lines and unresolved identities, generates pending matching work, and records idempotent intake receipts. It does not infer missing MPSC/spec/UOM/quantity/validity, make historical prices current, or accept a suggested match. Run its `--help` for supported arguments; choose an ignored/outside-Git DB path and keep the exact CSV hash alongside the result. The actual local intake and receipt are outside this code repository under `../catalog/`.

`src/assessments.py` contains pure synthetic checks for certificate/product identity, separate expiry axes, shared capacity and cost deduplication. It neither queries a registry nor establishes legal eligibility, accounting treatment, availability or business approval.

## Four hospitals plus Kom

`src/four_bv_intake.py` and `src/catalog_lifecycle.py` extend the ignored local catalog from the pinned read-only four-hospital snapshot. The actual DB is `../catalog/common-catalog.sqlite`: 3,523 source records, 4,577 case obligations, no accepted variant merges or current quotes. `source_worklist()` shares inquiry work for the same original master row; case qualification remains separate. Closing one consumer does not erase another consumer or history; award/fulfillment and extension are distinct states. A clock passing a planning date does not confirm closure.

The accompanying `../catalog/BIDOPS-COMMON-REVIEW.xlsx` is a human projection with Summary, SourceWorklist, CaseDemand, ReviewQueue and Provenance. Data files remain outside Git. Parser indices are labeled as such; physical Excel-row addresses and raw-XLSX hashes are unknown for the four-hospital extraction. See the contracts for the unreproduced 3,143 fanout count and the verified 3,122 count.

## Draft workpack inbox

`src/workpacks.py` prepares one local DRAFT inquiry/evidence packet for the same original source row, retaining separate case qualifications. It reads the catalog and writes only a separate derived inbox; owner and Agent remain unknown. Run from this project:

```powershell
python -m src.workpacks --help
python -m src.workpacks --catalog ..\catalog\common-catalog.sqlite --inbox ..\workpacks\manual\inbox.sqlite --event-id draft-sync-001 --export-csv ..\workpacks\manual\DRAFT.csv
```

Sync runs only when requested; there is no continuous listener or staff dispatch. Exact retries retain their receipt. Changed source scope creates a new draft version; closed consumers disappear from the active projection, and reopening does not inherit an old review. Explicit cancellation stays cancelled across refresh. Choose a new export path to preserve existing files.

The API supports local review and cancellation receipts. `REVIEWED` means a local preparation review, not commercial acceptance, owner assignment, employee acknowledgement or permission to send. Neither this inbox nor an edited CSV promotes a quote/master or contacts a person. The initial sensitive-context continuation was blocked. After explicit approval, the exact existing Claude BidOps session received the frozen context and then reviewed the current code. Its review found exact-retry and export-race issues plus conditional WAL drift; host-side synthetic reproductions confirmed them before local fixes. Claude did not directly edit files or run tests. The resulting implementation is host-applied and independently checked; no real principal, dispatch or commercial approval was added.


The post-review suite passed100/100. Review event identity now follows caller intent rather than unrelated catalog changes; new review still checks actual draft-scope drift. Legacy checksum-only receipts are replayed only when immutable persisted snapshot evidence verifies the original intent; unverifiable legacy intent fails closed without rewriting history. CSV uses exclusive creation. The before/after source-change guard includes main DB and WAL; it detects tested concurrent WAL changes but is not an atomic single-transaction snapshot or a proof against every ABA race. The actual catalog remains in delete journal mode and all source/data hashes stayed unchanged.
