# Independent normal-verification v1 — gate failure, no VERIFIED call

**Decision: HOLD / NOT VERIFIED.** Held metadata HEAD
`7d6d61f298e882f54c4bc36b1fb67502d2801e77` did not meet the required four
successful gates. The actual native mathematical candidate remains
`9964c33c4599f85d27dc8687e8bd6fdb5c44ff49`. No normal transition API was
called: calls 0, API failures 0, historical S VERIFIED count 0.

I independently read the gate actor's sealed report/seal, actual publication
receipt and exact raw stdout/stderr. Publication was executed once at the held
HEAD and exited 1. Its stdout is empty; stderr states that P's Frontier Cell
canonical declaration does not match. The receipt pins the same held HEAD
before and after the command. Semantic, contributor and frontier gates are
explicitly **NOT RUN**, not successful checks. This alone prevents VERIFIED.

The gate actor's 165 original-manifest files were hash-checked. All 172 current
phase originals, including the post-seal generation envelope, were copied
without rewriting their scripts, receipts or results. Full copying/hashing is
not claimed as semantic reading of every environment receipt. The gate actor's
earlier incorrect assertion that the top audit state had to be `accepted` is
retained as its distinct verifier-local implementation failure. Its corrected
schema check does not erase that failure or the later real gate failure.

ROOT subsequently diagnosed its own active-consumer metadata field and
announced a separately versioned correction. I made no shared correction and
did not treat the announced future fix as a successful gate. A future held
HEAD requires a distinct v2 phase; this v1 failure remains sealed.

My initial read-only preflight observed the exact held HEAD and an empty
tracked-only status. I read the substantive-advance skill and the real
`transition_advance` evidence/independence/publication requirements. Because
the four-gate prerequisite failed early, the full 309-foreign-advance /
43-discovery / all-regular-foreign-cell / tracked-byte/index/control pre/post
guard was **not completed**. No such full guard or mutation safety proof is
claimed. A strict raw ledger read at hold independently confirms zero S V
events. The raw ledger is private local only; its commitment, not its foreign
contents, is transferable. The own S cell at hold is preserved.

The native mathematical report, seal and portable manifest were copied and
their exact supplied hashes verified. Native/kernel/browser evidence review
was not completed in this failed normal phase and is not represented as an
additional independent native acceptance. The report's bootstrap archive
qualification, original kernel/browser failures and local-only lossless dump
boundary are retained; no missing bootstrap raw output or dump export is
invented.

Two review-side process limitations remain visible. First, I guessed an
incorrect PL append filename; it was absent. ROOT supplied the correct
`actual-PROVED_LOCAL-append.exact.jsonl`, which was then copied and checked
against SHA33090842789407870af22abf997ef521d6cf29ac38ce5cb87aaec46d5e9f7204.
Second, two large manifest displays were tool-truncated. The complete raw
manifest bytes are copied, but unprinted listing content is not claimed read.
These are not normal-API failures and are not mathematical/source refutations.

All previous source-fidelity decisions and raw/type/whole-code/anti freezes
remain unchanged. There was no sentinel or normal-V attempt, no own-cell
transition, no ledger append, no foreign/R9/queue/control/root mutation or
commit by me. S stays PROVED_LOCAL pending a new held-head verification;
centered T, full R9, main results, stabilization, integration/publication,
purification and whole Goal remain outside this phase.
