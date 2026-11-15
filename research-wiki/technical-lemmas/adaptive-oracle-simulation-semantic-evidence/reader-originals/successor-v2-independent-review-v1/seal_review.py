"""Seal already completed independent artifact review; no browser/server/API/Git."""
from pathlib import Path
import datetime as dt
import hashlib
import json

OWN=Path(__file__).resolve().parent
ACTOR=OWN.parent
RUN=ACTOR/'successor-v2-runtime'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
load=lambda p:json.loads(Path(p).read_text())
def dump(path,value):
    Path(path).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
measurement=load(OWN/'measurements.v1.json')
summary=load(OWN/'recompute-summary.v1.json')
actual=load(RUN/'actual-result.json')
assert summary['independent_checks']==220 and not summary['false']
assert len(measurement['screenshots'])==50 and all(x['independently_viewed_this_actual_run'] for x in measurement['screenshots'])
assert all(c['pass'] for c in measurement['checks'])
assert not measurement['remaining_reader_residuals']
report=f'''# Independent bounded reader acceptance: R18 CSS successor v2

Outcome: **ACCEPTED_BOUNDED_READER_DELIVERY**, with zero remaining required reader residuals for this exact isolated preview and the two exercised CSS viewports. This conclusion follows my actual inspection of all 50 PNGs, exact artifact/fixture checks and independent raw-measurement recomputation; it is not inherited from the 514 runtime check flags, the source verdict, a previous reader verdict or another actor's native result.

The actual run is bound to result SHA `da29a2e155e55e9c198bbf6f33013489283ab6668b8b5d82c1e9ec8157a4392e`, assignment `a291b00199047560b54dd2f1480d1d94cc30f748770c2d418a4be99d67d0e2f9`, runner `eb6c70e85d71b96cf4f659b7e18e255e36b13e161e8f635a20148273bc08e7d7`, preview manifest `4c45858dc2ff77e6cf3fb0c3198ded46d7ef4820d342170e2d9223e372bb9ebf` and mathematical snapshot `57016008083947405bc7d430838537014a40f987`. The true OS receipt records exit 0 over 126.140 seconds, fd1 stdout 165 bytes SHA `b41926bf509c5e09e3e41c9c1ec6e745f2c09fb0e6e5d1286f762a6edbc0a22f`, fd2 empty and no exception. All 485 original check names and code/predicates remain, alongside the 29 added regression records; the runtime contains 514 records with no false check. My independent artifact/raw recomputation has 220 checks and no false result, bound in `measurements.v1.json` SHA `{sha(OWN/'measurements.v1.json')}`.

I individually viewed all 23 desktop and 27 mobile screenshots from this actual run, including images whose bytes happen to match an earlier run. Each image is bound by exact SHA, dimensions and a specific observation in the measurement artifact. The statement/formula hierarchy is clear, assumptions/proof/Lean are folded initially, representative formula proofs have adjacent Lean controls, exact source starts and final codepoints are legible, source-index and parent context distinguish private T from public nodes, and all graph focus/detail views remain readable. Long mathematical/source content is intentionally locally scrollable; long graph core labels remain ellipsized with their full identity in the adjacent detail. These intended presentations are not missing content.

The original 14 px mobile failure is actually resolved within the owning formula. Both `mobile-proof-expanded` and the additional post-regression measurement have viewport/html/body widths 390/390/390. The mobile local formula has client width 311, content scroll width 354 and actual right scroll 43 of maximum 43 px. Its last visible CHTML transpose glyph moves from outside the local horizontal clip at the left scroll state into x=322.265625–331.84375 within the actual x=49.390625–360.390625 clip after scrolling. Its vertical range y=412.203125–420.421875 is inside y=409.03125–434.03125. All 31 visible glyph boxes retain strict vertical containment before and after, and their glyph-class sequence is unchanged. This is the visible formula endpoint, separately identified from assistive content. The desktop formula also reaches its local maximum 30 px scroll and retains the complete endpoint. Original font sizes remain 18.2952 px desktop and 17.424 px mobile, with the original 108.9% relationship to the parent; no font shrinking hides the overflow.

All 35 assumption native MathML roots per viewport remain nonempty in the MathML namespace, with exactly unchanged text across the scroll operation. Their retained ancestor data have no `display:none`, `visibility:hidden` or `aria-hidden=true` on the accessible MathML route. Target MathML is also unchanged before/after. The CSS successor adds only one scoped owning-inline rule plus vertical padding; every HTML, mathematical source, Lean, backend and other served asset byte remains unchanged. No content or assistive subtree was removed to reduce body width.

Independent byte checks confirm the five displayed adjacent Lean spans partition all P170/T118 lines, both focused readers retain the exact spans and all four source pages/downloads retain their complete context. All 20 actual saved module downloads match their frozen source bytes. All 18 natural source-anchor traces were recomputed from their samples with the retained ≥500 ms/four-sample/0.25 px stability and original strict header visibility predicate. All 16 source full-codepoint boxes and all eight graph clipped-label/font measurements were recomputed. The graph retains exactly seven nodes and nine directed structural/scanner-reference edges, with six solid structural and three dashed reference arrows, no private-T declaration node and readable exact identities in detail. The 1490 requests and 1490 responses use one loopback origin; HTTP, console, page and blocked-external errors are zero. The final 104 served files and 24 assignment-frozen inputs still match their exact hashes.

The original failed packet remains **FAIL**, unchanged at SHA `f7e3488bdca1e854664f1eb2e91f48169e554293964ed5019915a792ceb01578`. The causal diagnostic remains separately bound at `a209eae553a0da5cadc3e1c26c0c358139925c0fd711ec02e0134cf504524650`; its success did not grant reader acceptance. The new acceptance applies only to the distinct CSS successor. The referenced source-review binding `38ae6f3bf655bb00e7b6054b55d2936fc06d254393ff607d4336cdbfb85201f6` is an input gate, not a source-fidelity verdict produced or independently reissued by this reader.

Scope is headless Chrome 157.0.8103.51 with desktop 1440×1000 and mobile 390×844 CSS viewports, device scale factor 1. This is not physical-touch or screen-reader audio testing. MathML availability is established by retained DOM/namespace/text/ancestor evidence. Some clipboard/navigation/DOM equality operations retain exact-runner assertions rather than a saved clipboard/DOM transcript; those were reviewed against the exact runner, immutable fixture, saved artifacts and actual images. No new browser, server, normal API, Lean, Git, canonical or ledger write was performed during this independent review. This isolated-reader acceptance is not whole-production/public delivery, a root/Lean gate, main integration, purification or Goal completion.
'''
(OWN/'READER-OUTCOME.v1.md').write_text(report)
stamp=dt.datetime.now(dt.timezone.utc).isoformat()
run={'schema':'r18-independent-reader-review-run-v1','reviewer':'adaptive_oracle_reader_audit_r18','completed_utc':stamp,
 'role':'Independent reader/visual reviewer; not mathematical prover, lesson author, native/source/blind actor or CSS successor implementer',
 'outcome':'ACCEPTED_BOUNDED_READER_DELIVERY','remaining_required_reader_residuals':[],
 'report':{'path':str((OWN/'READER-OUTCOME.v1.md').relative_to(ACTOR)),'sha256':sha(OWN/'READER-OUTCOME.v1.md')},
 'measurements':{'path':str((OWN/'measurements.v1.json').relative_to(ACTOR)),'sha256':sha(OWN/'measurements.v1.json')},
 'actual_result':{'path':'successor-v2-runtime/actual-result.json','sha256':sha(RUN/'actual-result.json')},
 'actual_OS_receipt':{'path':'successor-v2-runtime/runtime-process/receipt.json','sha256':sha(RUN/'runtime-process/receipt.json')},
 'actual_assignment_sha256':sha(RUN/'execution-assignment.ROOT.actual-v2.json'),'preview_manifest_sha256':actual['preview_manifest_sha256'],
 'actual_screenshots_individually_viewed':50,'independent_recomputations':220,'original485_checks_retained':True,
 'headless_CSS_viewports':[[1440,1000],[390,844]],'physical_touch_test':False,
 'acceptance_boundary':'Exact isolated candidate104 preview only; no whole production/public/root/main/purification/Goal credit',
 'source_fidelity_verdict':'NOT PRODUCED; existing source gate is separate',
 'no_browser_server_API_Lean_Git_canonical_or_ledger_writes_during_review':True,
 'hash_DAG':'This run binds report/measurements/actual evidence; it does not reference the later capsule or explicit manifest.'}
dump(OWN/'review-run.v1.json',run)
capsule={'schema':'r18-bounded-reader-acceptance-capsule-v1','outcome':run['outcome'],'remaining_required_reader_residuals':[],
 'review_run':{'path':str((OWN/'review-run.v1.json').relative_to(ACTOR)),'sha256':sha(OWN/'review-run.v1.json')},
 'report':run['report'],'measurements':run['measurements'],'actual_result':run['actual_result'],
 'mathematical_snapshot':'57016008083947405bc7d430838537014a40f987','source_binding_reference':'38ae6f3bf655bb00e7b6054b55d2936fc06d254393ff607d4336cdbfb85201f6',
 'accepted_scope':run['acceptance_boundary'],'actual_PNGs_viewed':50,'actual_process_exit':0,'raw_checks':514,'independent_recomputations':220,
 'preserved_original_failure_sha256':'f7e3488bdca1e854664f1eb2e91f48169e554293964ed5019915a792ceb01578',
 'hash_DAG':'Capsule binds earlier artifacts. The later explicit manifest binds this capsule; no circular/self hash.'}
dump(OWN/'capsule.v1.json',capsule)

# Exact allowlist. No walk of chrome temp/profile/cache, foreign guards, ledgers or indexes.
selected=[OWN/x for x in ['build_review.py','seal_review.py','measurements.v1.json','recompute-summary.v1.json','READER-OUTCOME.v1.md','review-run.v1.json','capsule.v1.json']]
selected += [RUN/x for x in ['actual-result.json','runtime-process/receipt.json','runtime-process/stdout.raw','runtime-process/stderr.raw',
 'browser_check.py','browser_geometry.py','browser_anchor_wait.py','browser_inline_regression.py','browser_check.py.exact.diff',
 'execution-assignment.ROOT.actual-v2.json','ACTUAL-V2-PREFLIGHT.v1.json','CHECKER-PREFLIGHT.DRAFT.v1.json','CHECKER-REVIEW.DRAFT.v1.md']]
selected += [RUN/x['path'] for x in actual['screenshots']]
for label in ['desktop','mobile']:
    selected += [RUN/'runtime-output'/f'{label}-step{i}-whole-module.lean' for i in range(1,6)]
    selected += [RUN/'runtime-output'/f'{label}-source-{tag}-whole-module.lean' for tag in ['P','T','RUN','FO']]
    selected += [RUN/'runtime-output'/f'{label}-private-T-module-context-download.lean']
selected += [ACTOR/x for x in ['actual-result.json','runtime-process/receipt.json','runtime-process/stdout.raw','runtime-process/stderr.raw',
 'diagnosis-v1/DIAGNOSIS.successor.v2.md','diagnosis-v1/diagnostic-result.actual-v1.json','diagnosis-v1/diagnostic-process-v1/receipt.json',
 'diagnosis-v1/diagnostic-process-v1/stdout.raw','diagnosis-v1/diagnostic-process-v1/stderr.raw']]
diagnostic=load(ACTOR/'diagnosis-v1/diagnostic-result.actual-v1.json')
selected += [ACTOR/'diagnosis-v1'/x['path'] for x in diagnostic['scans']+diagnostic['screenshots']]
assert len(selected)==len(set(selected))
for p in selected:
    assert p.is_file() and p.is_relative_to(ACTOR)
    assert not any(part in ['chrome-tmp','Cache','Code Cache','GPUCache','Default','Profiles','.git'] for part in p.relative_to(ACTOR).parts)
rows=[{'path':str(p.relative_to(ACTOR)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(selected)]
manifest={'schema':'r18-own-public-safe-explicit-selected-leaves-v1','root':str(ACTOR),'files':rows,'leaf_count':len(rows),
 'public_safe_scope':'Exact own selected artifact leaves only. No recursive inclusion and no Chrome temporary/profile/cache, foreign guard, ledger, ATLAS/source index or unrelated artifact.',
 'includes_original_failed_result_and_actual_causal_diagnostic':True,
 'does_not_include_self':True,'hash_DAG':'Manifest binds earlier run/capsule/evidence. Its hash is reported externally; no artifact here references it.'}
dump(OWN/'explicit-manifest.v1.json',manifest)
out={'outcome':run['outcome'],'required_residuals':0,'review_run_sha256':sha(OWN/'review-run.v1.json'),'capsule_sha256':sha(OWN/'capsule.v1.json'),
 'explicit_manifest_sha256':sha(OWN/'explicit-manifest.v1.json'),'selected_own_leaves':len(rows),'report_sha256':sha(OWN/'READER-OUTCOME.v1.md'),'measurements_sha256':sha(OWN/'measurements.v1.json')}
dump(OWN/'seal-summary.v1.json',out)
print(json.dumps(out,indent=2))
