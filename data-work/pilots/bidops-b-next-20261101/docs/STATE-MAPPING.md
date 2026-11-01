# Receipt mapping and evidence levels

| Business semantic | Current pilot state/event | What it proves locally |
| --- | --- | --- |
| Issued / transport delivered | mission issued, then received | Scoped request persisted and owning node recorded receipt; not responsibility accepted |
| Accepted | `respond_mission(..., accepted, evidence_ref)` | Owner explicitly accepts scope; alternative needs_input/rejected remains separate; WIP=1 prevents accepting another job silently |
| Produced | `mission_return` / candidate `returned` | Immutable candidate with source/requirement versions, blockers and digest persisted |
| Used as diagnostic | `candidate_diagnostic_use` | A different downstream owner records a HOLD decision reference; candidate remains unapproved/unapplied |
| Reviewed / applied / commercial used | three separate events | Explicit synthetic policy actions with current source/requirement/quote/identity validity checks; never writes a real master or submits |
| Cancelled | mission cancellation receipt | Stops new progression, preserves previous output/application/use history; no automatic undo |

Actor binding in this API is a check against explicit fixture configuration. A real adapter must supply an authenticated principal independently of LLM payload; matching strings is not authentication. Capability/owner fields do not grant company access.

Evidence labels remain separate: **L1 synthetic fixture**, L2 two local processes, L3 two machines under one owner, L4 two real owners, L5 business acceptance. The current core/demo tests establish L1 only. Prior L3 lab LIVE PASS remains its own historical evidence, not L4/L5 for tender employees.

## Remaining runtime gaps

This iteration does not implement a cross-owner listener, real authentication, distributed leases/fencing, priority scheduling/fairness, network offline delivery/recovery, quota or production adapter. Local WIP rejection is a capacity guard, not network backpressure. Quote-discovery missions without a predeclared quote scope are outside the current core. These gaps must be closed in a separate authorized runtime slice before calling the agent network operational; they do not prevent the reviewed local intake/decision demo.

The real Kom catalog import is a read-only intake into a separate, ignored local catalog DB; it is not L4/L5 adoption or a quotation acceptance. Candidate matches remain unresolved and need owner review.
