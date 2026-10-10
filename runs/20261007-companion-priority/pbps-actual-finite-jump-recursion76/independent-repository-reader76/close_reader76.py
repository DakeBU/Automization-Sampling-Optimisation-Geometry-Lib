import datetime, os, subprocess
import review76 as r

assert not (r.O/'lease.final.json').exists()
im=r.load(r.O/'inputs.manifest.json'); checks=r.load(r.O/'checks.json'); result=checks['result']
views=r.load(r.O/'independent-PNG-observations.json')
assert result['status']=='PASS_SCOPED_CURRENT_READER76_FINITE_CHECKS'
assert result['actor']==views['actor']==r.ACTOR
assert result['copy_callbacks']==result['RAW_downloads']==3 and len(result['formula_BODY_spans'])==10
assert views['independently_viewed_PNGs']==13 and len(result['current_gate_receipts'])==18
assert r.sha(r.DIS.read_bytes())=='54b29a35f4d68136e744724e6fafd567f33a54a56b33d13faf6f4ba6d7b9403d'
for item in im['inputs']:r.check(item)
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=r.ROOT,text=True).strip()==r.SCI
assert not any(path.is_file() for path in r.CACHE.rglob('*'))
debts=[
    'The complete statement is compact plain notation and dense. Some prose retains plain mathematical notation; long display rows require horizontal scrolling. Full Chapter1.3 Exposition Seal remains open.',
    'The selected compiled declaration card and six typed immediate relations are usable. Full graph context labels remain dense; three scanner references are not an exhaustive proof-dependency certificate or theorem implication.',
    'The three copy tests use isolated page clipboard callbacks. Physical OS clipboard, other viewport/device behaviour, deployment and live site were not tested.',
    'The source-review communication qualification is mandatory: mathematics acceptance status and a coordinate-metadata cue were received. The old broad false flag is immutable but cannot support an unconditional no-review-status-exposure claim. The independent capsule covers the bounded disclosed notice, not absence of additional undisclosed messages or private session-store evidence.',
    'The current source opening Prospective header76 only comment is stale process documentation. It neither negates the actual compiled theorem nor grants whole-result completion.',
    'Earlier complete Python/browser regressions are reused with current executable paths and mtime continuity only. Historical executable RAW hashes were not recorded; historical byte identity is not asserted.',
    'The result is the fixed-reference finite indexed stopped recursion, with deterministic zero thresholds. iid realization, SLLN/nonaccumulation, a unique all-time physical phase/path, Markov/invariance/reversal, terminal sampler, main/error/expected-cost bounds and actual-input composition remain open.',
    'No new source-fidelity judgment, mathematical certification, VERIFIED transition, whole-paper/Goal completion, PURIFIED, main, live or full Exposition Seal is conferred by this reader review.'
]
decision=dict(schema='independent-scoped-repository-reader76-decision/v1',status='ACCEPTED_SCOPED_AGGREGATE_CURRENT_READER76_WITH_READER_DEBT',accepted_scoped_aggregate=True,actor=r.ACTOR,checked_science_commit=r.SCI,dispatch_RAW_sha256=r.sha(r.DIS.read_bytes()),finite_dispatch_inputs=149,independent_of_formalizer_stabilizer=True,old_source_reviewer_actor_disclosed=r.ACTOR,self_validation_of_old_source_verdict=False,source_communication_qualification_checked_as_binding_and_disclosure_only=True,communication_qualification=result['communication_qualification'],new_VERIFIED_transition=False,new_independent_mathematics_certification=False,new_source_fidelity_certification=False,blockers=[],reader_debts=debts,Registry=525,publication_units=246,complete_module_lines=412,formula_BODY_steps=10,initially_closed_details=16,exact_Lean_code_panels=13,independently_viewed_PNGs=13,independently_viewed_PNG_records=views['records'],copy_callbacks=3,RAW_downloads=3,current_gate_receipts=18,Goal_complete=False,PURIFIED=False,full_Exposition_Seal=False,main=False,live=False,whole_paper=False)
r.save('decision.json',decision)
text='''Independent scoped repository/current-reader review76

ACCEPTED for the exact frozen scoped aggregate and current local reader at SCI e1f1d85d34426954829a97a46b563ea8e1dab8f1. There are no blocking items in the checked finite packet. All149 final dispatch RAW/LF pins are current; LF means CRLF byte pairs to LF only. The complete 412-line/22655-byte module is byte-identical to Git at SCI. This is reader/aggregate acceptance only; it neither re-proves mathematics nor self-validates the earlier source verdict.

The attributed complete ten-group statement, six original analytic callers, fixed reference, guarded finite/stopped representation, arbitrary nonnegative deterministic thresholds, original energy/cap and open physical-time/global-process boundary are present. Ten prose/formula steps match exact continuous BODY lines193-409. The current publication context and binding are independently recomputed. All16 Lean/details start folded; the13 code panels include exact statement/helper/proof content. Three distinct copy callbacks reproduce continuous current module fragments, and three HTTP200 RAW downloads reproduce all22655 source UTF8 bytes. Callback evidence is isolated-page evidence, not a physical OS clipboard test. All13 frozen PNGs were personally viewed at original detail, independently of root's viewing; recorded observations preserve the dense statement, horizontal formula scroll and dense graph context debts.

Eighteen actual terminal-closed successful current gate receipts bind SCI, including mandatory ASTIS root9187/Tests9487, Registry525, publication246, contributor/frontier/semantic/site/graph and fresh scoped browser evidence. The current graph digest is independently recomputed. The selected compiled module/declaration has six correctly typed direct declaration relations: module ownership, three producer scanner references, semantic-audit target and source correspondence. Literal direct local import is ActualHazardClock; actual import paths connect HarmonicFlow and BounceRate transitively. These labels are not an exhaustive proof-dependency certificate. Five affected generated outputs are exact and disjoint from preexisting collaborator paths. Prior full regressions are reused only under their explicit runtime-continuity qualification.

Native math82, source121, exactSCI97 and decoder4 closed file memberships and hashes are reused unchanged as finite evidence. The already unique nonowner VERIFIED append is checked read-only, not created here. Independent communication/protocol capsule18 by /root/exact_science63 is also checked unchanged. Canonical audit.source_review.communication_provenance_qualification binds its exact proposal, decision, lease and logical run. Packet/publication binding are unchanged. The qualified disclosure accurately preserves that the source reviewer received mathematics-acceptance status and a root coordinate-metadata cue; the immutable old false flag must not be interpreted as universal absence of review-status communication. That independent protocol decision reports the bounded notice does not invalidate the source admission, subject to its explicit additional-semantic-payload reaudit trigger. This reader checks that binding/disclosure, not that source judgment. No private session store, undisclosed-message absence or precise notice timestamp is claimed.

Three own checker negatives are preserved with exact executed-script snapshots and real child EXIT1: an editorial phrase was checked in statement rather than assumptions; three transitive producer imports were incorrectly expected to be direct; native compiler receipts use exit_code rather than terminal_EXIT. The final corrected finite checker34088/0 passed. These are checker errors, not changed source/publication/graph inputs. Current inputs, earlier CLOSED directories and canonical/Git/ledger files were never mutated by this reviewer.

Reader debts and retained truth boundaries:
'''+'\n'.join('- '+item for item in debts)+'\n'
named=r.O/'named-review76.txt';assert not named.exists();named.write_text(text,encoding='utf-8',newline='\n')
terminals=[]
for path in sorted((r.O/'terminals').glob('*.receipt.json')):
    receipt=r.load(path)
    assert receipt['terminal_closed'] and receipt['Popen_wait_used']
    out=r.check(receipt['stdout']);err=r.check(receipt['stderr'])
    terminals.append(dict(receipt_pin=r.pin(path),receipt=receipt,stdout_exact_UTF8=out.decode('utf-8'),stderr_exact_UTF8=err.decode('utf-8')))
qualification_dir=r.R/'integration76/source-communication-qualification76'
payload=dict(schema='independent-scoped-reader76-complete-named-RAW/v1',actor=r.ACTOR,decision=decision,inputs=im,named_review_UTF8=text,full_exact_module_UTF8=(r.ROOT/r.MOD).read_bytes().decode('utf-8'),checks=checks,PNG_observations=views,full_own_foreground_terminal_RAW_payloads=terminals,communication_qualification_exact_proposal=r.load(qualification_dir/'qualification.addendum.proposed.json'),communication_qualification_exact_decision=r.load(qualification_dir/'decision.json'),communication_notice_exact_UTF8=(qualification_dir/'communication-notice.exactraw.txt').read_bytes().decode('utf-8'),checker_diagnoses=[r.load(r.O/('checker-diagnosis'+str(number)+'.json')) for number in [1,2,3]],no_canonical_Git_ledger_or_prior_closed_directory_writes=True,new_source_or_mathematics_certification=False,new_VERIFIED_transition=False)
r.save('complete.named.RAW-payload.json',payload)
run=r.build_run(r.O/'decision.json',r.O/'inputs.manifest.json',r.O/'checks.json',r.O/'independent-PNG-observations.json',named,r.O/'complete.named.RAW-payload.json')
run.pop('run_sha256')
run.update(actual_execution_checker=r.pin(r.O/'check_reader76.py'),actual_final_writer_script=r.pin(r.O/'close_reader76.py'),dispatch_RAW_sha256=r.sha(r.DIS.read_bytes()),finite_dispatch_inputs=149,old_source_reviewer_actor_disclosed=r.ACTOR,self_validation_of_old_source_verdict=False,communication_qualification_run_sha256=result['communication_qualification']['whole_logical_run_sha256'],earlier_closed_source121_unchanged=True,observed_actual_own_foreground_child_receipts=[r.pin(path) for path in sorted((r.O/'terminals').glob('*.receipt.json'))],own_checker_negative_count=3,owned_runtime_directory=r.CACHE.as_posix(),owned_runtime_directory_files=[],no_writes_after_final_lease_in_either_owned_directory=True)
run['run_sha256']=r.sha(r.can(run));r.save('run.json',run)
assert r.sha(r.can({key:value for key,value in run.items() if key!='run_sha256'}))==run['run_sha256']
for item in im['inputs']:r.check(item)
assert not any(path.is_file() for path in r.CACHE.rglob('*'))
rows=[r.pin(path) for path in sorted(r.O.rglob('*'),key=lambda path:path.as_posix()) if path.is_file()]
lease=dict(schema='independent-scoped-reader76-CLOSED-LAST/v1',status='CLOSED_LAST',actor=r.ACTOR,checked_science_commit=r.SCI,writer_PID=os.getpid(),closed_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),all_prior_child_sessions_terminal_closed=True,completed_check_receipts=checks['actual_terminal_receipts'],postclose_owned_writes_forbidden=True,final_owned_write=True,files=rows,file_count_including_lease=len(rows)+1,closure_logical_sha256=r.sha(r.can(rows)),run_sha256=run['run_sha256'],complete_named_RAW_payload=run['complete_named_RAW_payload'],owned_runtime_directory=r.CACHE.as_posix(),owned_runtime_files=[],actual_writer_EXIT_observation='No self-asserted exit: final writer actual PID/EXIT and full stdout/stderr are captured by external foreground Popen.wait without postclose owned writes.',new_VERIFIED_transition=False,new_source_or_mathematics_certification=False)
r.save('lease.final.json',lease)
# Final owned write has occurred. Only external native stdout follows.
print(r.json.dumps(dict(status='CLOSED_LAST',actor=r.ACTOR,actual_writer_PID=os.getpid(),decision_RAW_sha256=run['decision']['RAW_sha256'],run_sha256=run['run_sha256'],run_RAW_sha256=r.sha((r.O/'run.json').read_bytes()),lease_RAW_sha256=r.sha((r.O/'lease.final.json').read_bytes()),complete_named_RAW_sha256=run['complete_named_RAW_payload']['RAW_sha256'],closure_logical_sha256=lease['closure_logical_sha256'],owned_count=lease['file_count_including_lease'],blockers=[],new_VERIFIED_transition=False),ensure_ascii=False,indent=2))
