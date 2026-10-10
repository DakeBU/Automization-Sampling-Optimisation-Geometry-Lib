import os,sys,subprocess
from check import *

assert git('rev-parse','HEAD')==COMMIT and not git('diff','--name-only','HEAD')
ci_base='runs/20261007-companion-priority/pbps-gaussian-reflected-mean52/remote52/'
ci_paths=[ci_base+'checkpoint.2.'+n for n in ['snapshot.json','pr.raw.json','stderr.log']]
ci=load(ci_paths[0]); raw=path(ci_paths[1]).read_bytes()
assert ci['actual_raw_sha256']==sha(raw) and ci['pr']==load(ci_paths[1])
assert ci['pr']['headRefOid']=='241e01d0d1917a6400a0f43ea48697b72cee88df'
rollup=ci['pr']['statusCheckRollup']; assert len(rollup)==5
assert sum(x['status']=='COMPLETED' and x['conclusion']=='SUCCESS' for x in rollup)==4
assert next(x for x in rollup if x['name']=='deploy website')['conclusion']=='SKIPPED'
for p in ci_paths:
    blob=subprocess.check_output(['git','show',SCI+':'+p],cwd=R)
    assert blob.replace(b'\r\n',b'\n')==path(p).read_bytes().replace(b'\r\n',b'\n')
    (O/('remote52.'+path(p).name+'.raw.snapshot')).write_bytes(path(p).read_bytes())
dump('remote52-provenance.check.json',dict(status='PASS',actual_inputs=[pin(p) for p in ci_paths],snapshot_head=ci['pr']['headRefOid'],checks=rollup,science_Git_LF_equal=True,scope='Preserved historical52 actual remote snapshot only; no current53 CI, merge, deploy, main/live or PURIFIED inference.53 science/integration have not been pushed.'))
final_inputs=strict('inputs.final.json')
c=load(O/'checks.json'); m=load(O/'metadata-review.json'); g=load(O/'graph.current.json')
assert c['status']==m['status']=='PASS'
inputs={}
def add(e):
    assert equal(e),e['path']; inputs[e['path']]=pin(e['path'])
for x in final_inputs['checks']: add(x['current']); x.get('exact_reviewed_original_snapshot') and add(x['exact_reviewed_original_snapshot'])
for p in ['math-freeze.json','reviewer.source.inventory.json','source.0.review.json','reviewer.source.run.json','reviewer.source.lease.json','source.review.lease.json','anonymous-decoder/run.json','anonymous-decoder/result0.json','anonymous-decoder/binding-receipt.json','anonymous-decoder/lease.json','whole-proof-review53/receipt.json','whole-proof-review53/run.json','whole-proof-review53/lease.json','whole-proof-review53/compiler.lease.json','exact-verification53/receipt.json','exact-verification53/run.json','exact-verification53/lease.json','exact-verification53/compiler.lease.json','verified.json','root.integration.0.lease.json','root.desktop-capture53.lease.json','visual.inspection.json','integration.notes.json','integration-whitespace53/diagnosis.json','whitespace-diagnosis53/diagnosis.json','sync-before-aggregate53-fetch.json','sync-before-aggregate53-fetch.log']:
    add(pin(B/p))
for x in load(B/'reviewer.source.inventory.json')['rows']: add(x['snapshot'])
for row in load(O/'integration-Git-bindings.json')['bindings']: add(row['current'])
for e in c['visual_inputs']: add(e)
for gate in c['integration_gates']: add(gate['status']);add(gate['log'])
for e in m['inputs']:add(e)
for e in ci_paths:add(pin(e))
add(g['input']);add(pin('website/scripts/publication_reader.py'));add(pin('tools/astis_publication.py'));add(pin('lean-toolchain'));add(pin('lake-manifest.json'))
for x in c['whitespace']:add(x['gzip'])
for p in ['whole-proof-review53/run.json','exact-verification53/run.json']:
    for e in load(B/p)['actual_outputs']:add(e)
for p in ['reviewer.source.run.json','reviewer.source.lease.json','source.review.lease.json']:
    for e in load(B/p).get('outputs',[]):add(e)
for e in load(B/'anonymous-decoder/binding-receipt.json')['output_artifacts']:add(e)
for e in c['native_logical_checks']:
    selfcheck(e['input']['path'],e['self_field'])
receipt=dict(schema_version=1,status='ACCEPT_SCOPED_REPOSITORY_PROOFSEAL53',verifier='whole_math52',checked_commit=COMMIT,science_commit=SCI,result_kind='integration-node',blockers=[],source_math_blockers=[],compiler_invocations=0,checked_utc=utc(),exact_statement=dict(LF_bytes=758,LF_sha256='43d2831fa373729dc44cfd575fa4e1b68b2462688db8445320f13e433ddbe23e',production_lines=99,Test_lines=103),prior_review_reuse='Complete independent whole mathematics53 and exact-commit53 are preserved raw/LF/logically and reused without replay/reproof. This seal examines repository integration, source/publication binding and actual reader captures.',mathematical_reasons=[
 'Genuine Gibbs partition positivity produces exp(-V) L1 and actual source mu probability internally. Tilted-tilted composition, the affine inverse half and normalized scale2/translation-y Jacobian cancellation produce the exact coefficient1/(8eta) and literal source-volume S_y equality to the reflected actual posterior at EVERY y.',
 'The entire signed compact C1 mean function is transferred through every-y equality to the previously independently reviewed Gaussian mean theorem. There is no AE derivative transfer, supplied normalization/law/domain/derivative certificate or wrapper credit. Genuine original-source consumers retain both Hessian bounds and beta*eta<=1, the SAME mu/J conditional R, sourceS probability and identity, and noncentered rank0 mean1/derivative0.',
 'Lower-only curvature, all positive eta, compact C1, finite Hilbert and rank0 are disclosed sufficient analytic background extensions. The three real parents and all body ingredients remain unchanged from the sealed scientific packet. Actual Tf closed-gradient membership and full rough B13 are not proved by C1.'],repository_reasons=[
 'All492 mathematical originals and506 source-opening originals are checked; the only admitted audit/cell mismatches are mapped to their exact reviewed BEFORE raw snapshots and current metadata is explicitly reviewed. All506 archived source-opening snapshots match their originals. No silent skip, restoration or invented hash.',
 'Production/Test/source audit/lesson/publication/source review preserve scientific Git and current LF; production/Test raw bytes match the original independent math snapshots. All119 actual integration-owned current Git LF bindings pass. Future54/55 are not integrated or inspected.',
 'All12 actual integration.0 gate statuses/logs bind exit0; root9156/Test9441 and mandatory ASTIS fake-closure gate passed. Registry has494 formalizedLocal entries and real native_decide494 consumer. ExampleCases public aggregator is declaration-free; Test53 is a real root import. No compatibility theorem gate bypass.',
 'Real reviewed publication check and source gate pass; accepted equivalent-after-elaboration source audit binds full publication digest f418bdbebf422f0ccb6feadbd83f4d8da8d6de35101705473bf57abbeaffc6ee. Nine actual consumed source bodies pass the ASTIS fake-closure scan. Only the independent whole_math52 verifier authored VERIFIED; original PhaseKernel remains the sole STABILIZING lane.',
 'Eight native whole/source/decoder/exact logical run recipes validate with their actual named self fields. Decoder plain STRING/source-text blindness and inherited source identity exposure are disclosed; strict source identity blindness is false. Complete packet, native closed leases, original failed-only sorryAx, T53-1 minimal representation repair and decoder schema negative remain preserved.',
 'Current official graph input digest is recomputed by the actual helper and exactcell one-hop report matches the native gate. Four incident relations are structural ownership and incomplete source/name/audit references, not four certified theorem implications. Actual affine/Gibbs parent consumers remain mathematical dependencies despite incomplete scan coverage.',
 'Science whitespace negative646 findings195 exact immutable paths and integration negative159 findings3 exact immutable paths reproduce byte-for-byte from mtime0 gzip. Authored exact-path checks pass; full-staged whitespace PASS is explicitly false.',
 'Four actual archived desktop PNGs and DOM records were inspected and pinned; two owned browsers/HTTP and Node flows succeeded and closed. Source statement, six formula steps, initially folded exact Lean and source/derivative boundary are visible. Historical remote241 four SUCCESS/deploy SKIPPED is bound separately and provides no new53 CI evidence.'],graph_publication_inputs_sha256=g['publication_inputs_sha256'],graph_incident_count=4,lean_source_gate=dict(actual_checks=12,root_jobs=9156,Tests_jobs=9441,focused_scientific_verifier_PID=41368,focused_scientific_exit=0,new_compiler_invocations=0,source_audit='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261008-PBPSLiteralReflectedMean.json',source_verdict=c['source_review_verdict'],fake_closure_scan=c['fake_closure_scan']),presentation_debt=['Combined formula horizontal overflow/scrollbar','Repeated statement lesson rendering','Dense graph long-name wrapping and compact ASCII','Historical pending-review/integration wording survives in immutable lesson/handoff despite actual later accepted scoped checks'],open_boundary=['Actual Tf closed-gradient membership','Full rough all-L2/H1 B13','Gamma/halfturn/hypocoercivity/invariance/nonexplosion/implementation/main/errors/cost','Actual-input PBPS/SPHMC composition and four-paper Goal','Full reader/mobile/copy/download/Exposition Seal','Main merge, new53 remote CI, deploy/live and postmerge PURIFIED'],no_new_canonical_mutation=True,no_new_VERIFIED_or_STABILIZING=True)
dump('receipt.json',receipt)
outputs=[pin(p) for p in sorted(O.iterdir()) if p.is_file() and p.name not in {'run.json','lease.json','outputs.json'}]
dump('outputs.json',dict(actual_outputs=outputs,raw_recipe='SHA256 exact bytes',LF_recipe='SHA256 replacing CRLF byte pairs with LF only; no JSON reserialization'))
run=dict(schema_version=1,status='PASS',reviewer='whole_math52',checked_commit=COMMIT,science_commit=SCI,actual_closing_python_pid=os.getpid(),compiler_invocations=0,actual_inputs=list(inputs.values()),strict_inputs=pin(O/'inputs.final.json'),actual_outputs=outputs+[pin(O/'outputs.json')],native_logical_checks=c['native_logical_checks'],logical_recipe='SHA256 sorted compact UTF8 ensure_ascii=False allow_nan=False entire object minus run_sha256; no newline',actual_git_bindings=pin(O/'integration-Git-bindings.json'),scope='Scoped repository ProofSeal53, complete prior math reused and integration checked; open boundaries preserved',exit_code=0)
run['run_sha256']=logical(run);dump('run.json',run)
assert selfcheck(O/'run.json','run_sha256')['logical_sha256']==run['run_sha256']
for e in run['actual_inputs']+run['actual_outputs']:assert equal(e),e['path']
assert git('rev-parse','HEAD')==COMMIT and not git('diff','--name-only','HEAD')
lease=load(O/'lease.json');lease.update(status='CLOSED',read='CLOSED',write='CLOSED',Python='CLOSED',compiler='NOT_STARTED_CLOSED',closed_utc=utc(),actual_closing_python_pid=os.getpid(),actual_python_processes=[dict(pid=46448,exit_code=1,scope='Preserved readonly assertion failure on historical cell pin; diagnosed and corrected without mutation/compiler'),dict(pid=50212,exit_code=0,scope='Core checks PASS'),dict(pid=22720,exit_code=0,scope='119 actual Git LF bindings and scoped metadata PASS'),dict(pid=os.getpid(),exit_code=0,scope='Final strict checks and artifact closure')],exit_code=0,receipt=pin(O/'receipt.json'),run=pin(O/'run.json'),run_logical_sha256=run['run_sha256'],closure_recipe='Actual final owned file write is this CLOSED lease; no compiler started. Only readonly post-closure validation follows.')
dump('lease.json',lease)
print(json.dumps(dict(status=receipt['status'],checked_commit=COMMIT,science_commit=SCI,receipt=pin(O/'receipt.json'),run=pin(O/'run.json'),run_logical_sha256=run['run_sha256'],closed_lease=pin(O/'lease.json'),actual_inputs=len(inputs),actual_outputs=len(run['actual_outputs']),actual_closing_python_pid=os.getpid(),compiler_invocations=0),ensure_ascii=False))
