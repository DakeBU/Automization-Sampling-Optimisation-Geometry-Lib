from common import *
assert load(O/'lease.json')['status']=='OPEN'
assert git('rev-parse','HEAD')==HEAD and git('rev-parse',HEAD+'^')==SCI and not git('diff','--name-only','HEAD')
assert path('lean-toolchain').read_text(encoding='utf-8').strip()=='leanprover/lean4:v4.33.0'
assert next(x for x in load('lake-manifest.json')['packages'] if x['name']=='mathlib')['rev']=='db584cd6d46c92f209a44c0f1c829460d327499d'
originals=strict(); dump('original-inputs.final.json',dict(status='PASS',math=552,source=566,total=1118,checks=originals))
n=load(O/'native.checks.json'); i=load(O/'integration.checks.json'); g=load(O/'graph.checks.json'); h=load(O/'history.checks.json'); gb=load(O/'git-bindings.json')
assert n['status']=='PASS' and i['status']==g['status']=='PASS_SCOPED' and h['status']=='PASS'
assert all(x['exit_code']==0 for x in load(O/'execution.json')['commands'])
assert len(originals)==1118 and not guard_denied
inputs={}
def add(e):
 assert equal(e),e['path']; p=e['path'].replace('\\','/'); actual=pin(p)
 if p in inputs: assert inputs[p]==actual
 else: inputs[p]=actual
for x in originals:
 add(x['current'])
 if x['explicit_original_BEFORE_snapshot']: add(x['explicit_original_BEFORE_snapshot'])
for runfolder in ['whole-proof-review54','exact-verification54']:
 run=load(B/runfolder/'run.json'); selfcheck(B/runfolder/'run.json')
 assert logical(run['run_binding_payload'])==run['review_run_binding_sha256']
 for e in run['actual_inputs']:
  if equal(e): add(e)
  else:
   assert runfolder=='exact-verification54' and e['path'].replace('\\','/')==CELL
   snap=load(B/'verified-inputs.before-shared-integration.json')['mappings'][0]['snapshot']; assert equal(e,snap['path']); add(snap); add(pin(e['path']))
 for e in run['actual_outputs']: add(e)
 for f in ['run.json','lease.json','compiler.lease.json']: add(pin(B/runfolder/f))
for f in ['math-freeze.json','reviewer.source.input-bindings.json','reviewer.source.run.json','reviewer.source.lease.json','source.review.lease.json','source.0.review.json','source.0.reviewer-packet.json','verified.json','verified-inputs.before-shared-integration.json','integration.notes.json','root.integration.0.lease.json','root.desktop-capture54.lease.json','visual.inspection.json','visual-observation-clarification54.json']:
 add(pin(B/f))
for e in load(B/'reviewer.source.run.json')['output_artifacts_before_run_and_leases']: add(e)
for e in load(B/'anonymous-decoder/binding-receipt.json')['output_artifacts']: add(e)
add(pin(B/'anonymous-decoder/binding-receipt.json'))
for d in [load(B/'anonymous-decoder/run.json'),load(B/'anonymous-decoder/lease.json')]:
 for e in d['input_artifacts']: add(e)
for row in h['preproof_complete_native_runs']: add(row['actual_current']['input'])
for row in h['preproof_actual_CLOSED_leases']: add(row['input'])
for row in h['original_7_production_Test_attempts']:
 for key in ['status','source','log','lease']: add(row[key])
for row in gb['current_HEAD_bindings']: add(row['current'])
for e in g['actual_normative_canonical_input_pins']: add(e)
add(g['generated_graph']); add(g['helper_whole'])
for e in g['whole_helpers']: add(e)
for row in i['actual_captures']:
 for key in ['capture','node_status','log']: add(row[key])
for row in i['visual_artifacts']: add(row['observed_raw_LF'])
for row in i['all12_native_gates']: add(row['status']); add(row['actual_log'])
inputrows=[inputs[k] for k in sorted(inputs)]; digest=logical(inputrows)
dump('inputs.actual.json',dict(status='PASS',count=len(inputrows),complete_actual_input_pins=inputrows,sorted_input_pins_logical_sha256=digest,recipe='Sorted by repository path; actual exact raw/LF/bytes descriptors; complete sorted compact UTF8 JSON array hashed. Original and explicit BEFORE snapshot cohorts remain separately recorded, never skipped.'))
debts=[
 'Cell serialized_shared_gate.scope has aggregate53 template typo; actual54 paths/counts/SCI pass. No extra scope credited.',
 'Cell independent_verification_details.full_shared_integration_pending is historical exact-stage true; later actual sharedPASS record supplies current aggregate state. Old native bytes retained.',
 'Graph scanner has lexical LogConcaveOn.prod name reference and omits WeightedC1GradientDomain adapter. Seven incident edges are incomplete references/correspondence/ownership, not certified theorem implication.',
 'Repeated long heading/statement, dense inline ASCII/source anchors and graph qualified-name wrapping. Four actual desktop formulas are legible; no observed54 overflow claimed. Root correction separately pinned.'
]
remaining=[
 'Full rough all-L2/H1 B.13 and actual operator/averaging bridge with approximation on differences',
 'Equivalence with separately defined source weak H1 domain',
 'Gamma, halfturn, dynamics, invariance/nonexplosion/implementation, main results, errors and unbounded expected costs',
 'Actual-input PBPS/SPHMC composition and remaining four-paper Goal',
 'Separate independent ExpositionSeal and full-reader/copy/download/mobile delivery',
 'New54 remote CI/push, main merge/deploy/live and postmerge PURIFIED'
]
reasons=[
 'The scientific exact1448 theorem/body and actual5900-byte Test are unchanged raw/LF from the complete closed independent mathematics and exact SCI reviews. All810 science Git bindings match their recorded SCI blobs, and all910 current union paths match integration HEAD LF. Only the scientific cell and ledger gained recorded serialized evidence; no production/Test/audit/lesson/publication delta.',
 'The unchanged four-parent proof constructs genuine Gibbs/augmentation/outer-law probability and both source mean/gradient L2 witnesses, chooses one dense closable genuine smoothcompact-gradient core BEFORE observers, identifies the literal source S at EVERY y, obtains C1 of the entire mean function, and invokes the existing C1 cutoff/mollifier domain adapter for the canonical SAME-nu toLp pair. No Tf compactness, AE derivative transfer, normalization/closure/Lp/domain certificate or private copied parent is introduced.',
 'The actual Test joins the real conditional P and reflection U on L2(J), A=PUP, to the genuine source mean and canonical graph pair, and retains noncentered rank0 mean1/gradient0 with MemLp.toLp_congr. Six successful focused standard3 closures and actual current whole root/Test gates preserve this reachability; failed-only compiler sorryAx remains confined to exit1 elaborations.',
 'Complete native math/exact/source/decoder full-run-minus-self hashes, separate binding payloads, original input cohorts, actual outputs and closed lease projections are recomputed. Source accepted informational domains/scopes/conclusion elaborations and source reviewer late indirect exposure AFTER its own semantic assessment remain explicit; decoder is source-TEXT-blind with plain strings, not strict identity blind.',
 'Real reviewed publication admission has unchanged full d3a360...b8d3 binding, accepted audit, and empty actual forbidden-closure scan across9 consumed source files. Public declaration-free ExampleCases aggregator and actual root Tests import/Registry495 consumer integrate the bounded result. The12 actual gates pass with root9157/Test9443; original PhaseKernel remains the sole STABILIZING owner and the sole54 VERIFIED transition belongs to whole_math52.',
 'Current full normative graph helper digest matches the generated graph under an installed future55 directory guard; bounded exact node/7 incident edges retain ownership versus incomplete reference semantics. Four genuine PNGs and four DOM records plus two successful isolated browser/HTTP/Node closures were independently inspected. Lossless gzip whitespace negatives737/254 and167/3 are reproduced; only exact authored-path checks pass, never whole staged whitespace.'
]
receipt=dict(schema_version=1,verdict='ACCEPT_SCOPED_REPOSITORY_PROOFSEAL54',status='PASS_SCOPED_WITH_EXPLICIT_DEBTS',reviewer='whole_math52',stage='independent-readonly-repository-seal54',result_kind='integration-node',checked_scientific_commit=SCI,checked_integration_commit=HEAD,advance_id=ADV,exact_declaration=TARGET,exact_signature_LF_bytes=1448,exact_signature_LF_sha256=n['exact_signature_LF_sha256'],production=n['production'],Tests=n['Tests'],native_provenance=dict(wholemath_inputs=566,wholemath_outputs=21,exact_inputs=613,exact_outputs=41,original_math_pins=552,original_source_pins=566,original_pin_checks=1118,science_Git_bindings=810,integration_Git_bindings=102,current_union_Git_bindings=910,complete_primary_native_runs=n['complete_full_runs'],preproof_native_runs=5,preproof_CLOSED_leases=5,actual_input_unique_count=len(inputrows),actual_input_pins_logical_sha256=digest),Lean_gate=dict(no_new_compiler=True,prior_whole_PID=37192,prior_exact_PID=7412,prior_focused_jobs=3898,current_root_jobs=9157,current_Tests_jobs=9443,Registry=495,actual12_serial_gates='PASS',standard3_closures=6,toolchain=pin('lean-toolchain'),manifest=pin('lake-manifest.json')),source_gate=dict(real_reviewed_publication_check=True,full_publication_binding_sha256=PUBSHA,source_audit=pin(AUDIT),source_native_review=pin(B/'source.0.review.json'),verdict='equivalent-after-elaboration',informational_elaborations=3,no_mathematical_repair=True,fake_closure_scan=pin(O/'native.checks.json'),actual_consumed_source_scans=9,fake_closure_hits=0,source_late_indirect_exposure_preserved=True,decoder_source_TEXT_blind=True,decoder_strict_identity_blind=False),graph=dict(actual_full_native_input_digest=g['native_graph_input_digest'],actual_canonical_input_pins=1840,exact_incident_edges=7,bounded_slice=pin(O/'graph.exact54.slice.json'),helper_guard=pin(O/'graph.checks.json')),visual=dict(actual_PNG=4,actual_DOM=4,actual_browser_captures=2,all_four_independently_viewed=True,root_actual_CLOSED_desktop_lease=i['desktop_actual_CLOSED_lease'],correction=i['observational_clarification'],scope='Bounded repository desktop inspection, not independent ExpositionSeal'),whitespace=dict(science_findings=737,science_exact_immutable_paths=254,integration_findings=167,integration_exact_immutable_paths=3,lossless_negative_reproductions=True,gzip_mtime=0,authored_exact_path_checks='PASS',whole_staged_PASS=False),mathematical_reasons=reasons,mathematical_blockers=[],source_blockers=[],observability_debts=debts,remaining_boundary=remaining,sole_STABILIZING='ASTIS-SA-20261005-SPHMCImplementedPhaseKernel',no_state_transition_or_canonical_edit=True,raw_native_stages_unchanged=True,new54_remote_CI_claimed=False,historical53_CI_applied_to54=False,evidence=dict(native=pin(O/'native.checks.json'),integration=pin(O/'integration.checks.json'),history=pin(O/'history.checks.json'),git=pin(O/'git-bindings.json'),cell_exact_delta=pin(O/'cell-integration-delta.json'),execution=pin(O/'execution.json'),originals_final=pin(O/'original-inputs.final.json'),all_actual_inputs=pin(O/'inputs.actual.json')))
dump('receipt.json',receipt)
outputs=[pin(p) for p in sorted(O.iterdir()) if p.is_file() and p.name not in {'lease.json','run.json','outputs.json','readback.json'}]
payload=dict(schema_version=1,stage='scoped-repository-ProofSeal54',reviewer='whole_math52',checked_science=SCI,checked_integration=HEAD,verdict=receipt['verdict'],receipt=pin(O/'receipt.json'),original_pin_checks=1118,actual_input_count=len(inputrows),actual_input_pins_logical_sha256=digest,prior_full_math_run=n['complete_full_runs'][0]['logical_sha256'],prior_exact_run=n['complete_full_runs'][1]['logical_sha256'],prior_source_run=n['complete_full_runs'][2]['logical_sha256'],prior_decoder_run=n['complete_full_runs'][3]['logical_sha256'],publication_binding_sha256=PUBSHA,graph_input_digest=g['native_graph_input_digest'],new_compiler_invocations=0,remaining_boundary=remaining)
run=dict(schema_version=1,status='PASS_SCOPED',stage='independent-readonly-repository-seal54',reviewer='whole_math52',checked_scientific_commit=SCI,checked_integration_commit=HEAD,actual_closing_python_PID=os.getpid(),new_compiler_invocations=0,actual_inputs=inputrows,actual_outputs_before_run_and_readback=outputs,run_binding_payload=payload,review_run_binding_sha256=logical(payload),payload_recipe='SHA256 exact run_binding_payload; sorted compact UTF8 ensure_ascii=False allow_nan=False; no newline',full_run_recipe='SHA256 COMPLETE run object minus ONLY run_sha256; sorted compact UTF8 ensure_ascii=False allow_nan=False; no newline',output_pin_placement='Pre-run outputs here; complete current output pins including actual run/readback in outputs.json, whose actual pin is in the final CLOSED lease. No self/cyclic lease hash.',exit_code=0,remaining_boundary=remaining)
run['run_sha256']=logical(run); dump('run.json',run)
assert selfcheck(O/'run.json')['logical_sha256']==run['run_sha256']
assert logical(load(O/'run.json')['run_binding_payload'])==run['review_run_binding_sha256']
for e in inputrows+outputs: assert equal(e)
assert load(O/'receipt.json')==receipt and git('rev-parse','HEAD')==HEAD and not git('diff','--name-only','HEAD')
dump('readback.json',dict(status='PASS',actual_python_PID=os.getpid(),all_actual_input_raw_LF_pins=len(inputrows),all_pre_run_output_raw_LF_pins=len(outputs),receipt=pin(O/'receipt.json'),run=pin(O/'run.json'),complete_run_sha256=run['run_sha256'],separate_payload_sha256=run['review_run_binding_sha256'],complete_logical_recipes_readback=True,actual_tracked_tree_clean=True,future55_guard_denied=guard_denied,compiler_started=False,performed_before_final_lease_closure=True))
manifest=[pin(p) for p in sorted(O.iterdir()) if p.is_file() and p.name not in {'lease.json','outputs.json'}]
dump('outputs.json',dict(status='PASS',count=len(manifest),actual_output_pins=manifest,output_list_logical_sha256=logical(manifest),recipe='All current owned files except this manifest and final lease; full run/readback included. Exact actual bytes/LF pins read back BEFORE closure. Final lease pins this manifest and run.'))
for e in manifest: assert equal(e)
assert load(O/'outputs.json')['actual_output_pins']==manifest
for e in inputrows: assert equal(e)
lease=load(O/'lease.json'); lease.update(status='CLOSED',read='CLOSED',write='CLOSED',Python='CLOSED',compiler='NOT_STARTED_CLOSED',closed_utc=utc(),actual_closing_python_PID=os.getpid(),exit_code=0,receipt=pin(O/'receipt.json'),run=pin(O/'run.json'),run_logical_sha256=run['run_sha256'],review_payload_sha256=run['review_run_binding_sha256'],actual_outputs_manifest=pin(O/'outputs.json'),actual_output_count=len(manifest),actual_input_count=len(inputrows),readback=pin(O/'readback.json'),closure_recipe='Actual last owned filesystem write. All current inputs, outputs, complete run self hash, separate payload, receipt and readback validated BEFORE this CLOSED lease. No filesystem read/write follows. No new compiler/canonical mutation/state transition.')
leasebytes=(json.dumps(lease,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
leasepin=dict(path=(O/'lease.json').relative_to(R).as_posix(),bytes=len(leasebytes),raw_sha256=sha(leasebytes),lf_sha256=sha(leasebytes.replace(b'\r\n',b'\n')))
result=dict(verdict=receipt['verdict'],checked_science=SCI,checked_integration=HEAD,original_pins=1118,actual_unique_inputs=len(inputrows),actual_outputs=len(manifest),new_compiler_invocations=0,all_leases='CLOSED',receipt=lease['receipt'],run=lease['run'],complete_logical_run_sha256=run['run_sha256'],separate_payload_sha256=run['review_run_binding_sha256'],actual_CLOSED_lease=leasepin,actual_closing_python_PID=os.getpid())
resulttext=json.dumps(result,ensure_ascii=False)
assert (O/'lease.json').write_bytes(leasebytes)==len(leasebytes)
print(resulttext)
