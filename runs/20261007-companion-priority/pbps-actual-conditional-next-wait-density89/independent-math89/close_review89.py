import hashlib,json,subprocess
from pathlib import Path
from datetime import datetime,timezone
R=Path('E:/Samplinglib');O=Path(__file__).parent;B=O.parent
def pin(p):
    p=Path(p);b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def load(p):return json.loads(Path(p).read_text('utf8'))
def put(n,v):
    p=O/n
    with p.open('x',encoding='utf8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
    return pin(p)
def resolve(s):
    p=Path(s)
    return p if p.is_absolute() else R/p
def validate(d,use_snapshot=False):
    p=resolve(d.get('closed_snapshot') if use_snapshot and d.get('closed_snapshot') else d['path'])
    q=pin(p);sha=d.get('raw_sha256',d.get('sha256'))
    assert q['raw_sha256']==sha,(p,sha,q)
    if 'bytes' in d:assert q['bytes']==d['bytes'],(p,d['bytes'],q)
    return q
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()
assert head=='7c108c3181cee58bb9305445f903c5f71efda9c5',head
freeze=load(O/'input-freeze89.json');kernel=load(O/'kernel-dependency89.json')
inputs=[validate(d) for d in freeze['actual_inputs']+kernel['ASTIS_source_files']]
collab=load(O/'collaborator-preservation89.json'); nowcollab=[validate(d) for d in collab['RAWs']]
assert len(nowcollab)==21
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualConditionalNextWaitDensity.lean'
L=R/'website/content/declaration_lessons/pbps-actual-conditional-next-wait-density.json'
P=R/'website/content/publications/pbps-actual-conditional-next-wait-density.json'
assert L.read_bytes()==(O/'lesson89.proposed-sequencing-only.exactraw.json').read_bytes()
assert P.read_bytes()==(O/'publication89.original.exactraw.json').read_bytes()
assert M.read_bytes()==(O/'module89.exactraw.lean').read_bytes()
original=load(O/'lesson89.original.exactraw.json');current=load(L)
overlay=load(O/'proposed-exposition-overlay89.json')
original['units'][0]['steps'][1]['formula']=overlay['changes'][0]['after']
assert current==original
u=current['units'][0];lines=M.read_text('utf8').splitlines();regions=[]
for i,s in enumerate(u['steps']):
    d=s['lean_source_region'];a,z=d['start_line'],d['end_line'];code='\n'.join(lines[a-1:z])+'\n'
    assert s['lean']==code and hashlib.sha256(code.encode()).hexdigest()==d['exact_code_raw_sha256']
    assert d['source_raw_sha256']==pin(M)['raw_sha256']
    regions.append({'step':i+1,'lines':[a,z],'exact_code_raw_sha256':d['exact_code_raw_sha256'],'formula':s['formula'],'exact_code_and_formula_review':'accepted'})
assert [r['lines'] for r in regions]==[[115,258],[259,306],[307,358],[359,366],[367,406],[407,436]]
S=B/'publication-freeze89.after-exposition.json'; successor=load(S)
assert successor['publication_binding_sha256']=='4da0587d22739a11e111fc835b19408cd722d156f6876a03b84ef1c2673e2ade'
assert successor['only_repaired_pointer']=='/units/0/steps/1/formula'
assert successor['decoder_packet_unchanged'] is True
successor_pins=[validate(d) for d in successor['inputs']+[successor['module']]]
ED=B/'independent-exposition-repair89/decision89.native.json';EM=B/'independent-exposition-repair89/closed-raw-manifest89.json'
assert pin(ED)['raw_sha256']=='4dc476de282b2754b3fd2ac222c8e0d977fb05556a8b0af886f31850239642e6'
assert pin(EM)['raw_sha256']=='318e61b2051b906e939e10fde1fb8d034f59577774fad6439a91f9e4a8af5044'
ed=load(ED);em=load(EM)
assert ed['decision']=='ACCEPT_EXACT_ONE_FIELD_EXPOSITION_REPAIR' and ed['reviewer_id']!='/root/exact_verify77'
external=[validate(d,use_snapshot=True) for d in em['inputs']]+[validate(d) for d in em['artifacts']]
assert kernel['standard_axioms_only'] and kernel['axioms']==['propext','Classical.choice','Quot.sound']
assert kernel['all_project_constants_have_value'] and kernel['actual88_absent']
receipts=[load(O/n) for n in ['fresh-focused-build.receipt.json','fresh-whole-source-kernel.receipt.json']]
for r in receipts:
    assert r['exit_code']==0 and r['terminal_closed'];validate(r['stdout']);validate(r['stderr'])
final_exposition=put('final-exposition89.audit.json',{
 'status':'ACCEPTED_CURRENT_EXPOSITION_AFTER_DISTINCT_EXACT_OVERLAY_REVIEW','reviewer_id':'/root/exact_verify77','current_lesson':pin(L),'current_publication':pin(P),'successor_freeze':pin(S),
 'exact_six_contiguous_BODY_regions':regions,'full_statement_assumptions_measures_definitions_source_attribution_boundaries_read':True,
 'only_original_residual':'Premature step2 mass clause removed; step4 retains the mass theorem adjacent to its proof.',
 'distinct_repair_decision':pin(ED),'distinct_repair_manifest':pin(EM),'current_equal_exact_accepted_candidate':True,'publication_module_Seal_unchanged':True,
 'historical_original_inputs':'Original lesson/publication/freeze are immutable reviewer snapshots indexed by original-exposition-snapshot-index89.json. The old root draft freeze is historical metadata; its prior audit pin is not asserted to equal the current coordinator audit, and no final source/decoder verdict has been read.',
 'layout_limit':'Content and exact adjacent Lean checked; no browser visual/live delivery credit.'})
negatives=[pin(O/n) for n in ['kernel-analysis-import89.negative.json','exposition-boundary-probe89.negative.json']]
decision=put('decision89.json',{
 'status':'ACCEPTED_INDEPENDENT_MATHEMATICS_ONLY','reviewer_id':'/root/exact_verify77','completed_utc':datetime.now(timezone.utc).isoformat(),'checked_workspace_commit':head,
 'module':pin(M),'statement_seal':pin(B/'root.statement-seal89.json'),'whole_private_Prop_matches_reviewed_seal':True,'six_original_analytic_binders':True,'fourteen_literal_model_definitions':True,'nine_literal_packaging_definitions':True,'no_extra_public_provider_premises':True,
 'whole_mathematics':pin(O/'whole-mathematics89.json'),'full_statement_and_all_six_BODY_regions_exposition':final_exposition,
 'kernel':pin(O/'kernel-dependency89.json'),'standard_axioms_only':True,'axioms':kernel['axioms'],'all_project_constants_have_value':True,'owned_constants_including_generated':kernel['owned_constant_count'],
 'immediate_public_ASTIS_parents':kernel['immediate_public_producers'],'immediate_public_count':6,'immediate_private_generated_count':18,'transitive_ASTIS_constants':77,'transitive_ASTIS_edges':126,'ASTIS_source_files':11,'actual88_not_a_dependency':True,
 'fake_closure_scan':pin(O/'fake-closure89.json'),'focused_gate':pin(O/'fresh-focused-build.receipt.json'),'whole_source_kernel_gate':pin(O/'fresh-whole-source-kernel.receipt.json'),
 'case_coverage':'n0, null/empty A, d0, arbitrary unbounded-across-history finite Borel d, stopped/dead, top wait, wait=cutoff, nonpositive raw threshold, zero norm/rank0/flat hazard, unrealizable history, arbitrary ENNReal F including infinity.',
 'mathematical_route':'Actual87 full history/unused-tail product; actual86 positive finite Ioc law explicitly restricted by Iio to strict Ioo; genuine measurable Kernel.withDensity; every-history mass<=1; full joint measure identity and nonnegative parameter integration. No no-atom/closed-open mass equality/rho<=1/normalizer/finite-wait/conditional-distribution premise.',
 'required_repairs':[],'resolved_exposition_repair':{'proposal':pin(O/'proposed-exposition-overlay89.json'),'distinct_reviewer':'/root/exposition_repair89','decision':pin(ED),'applied_canonical_lesson':pin(L)},
 'publication_binding_sha256':successor['publication_binding_sha256'],'collaborator_RAWs_preserved':21,'retained_negative_diagnoses':negatives,
 'source_topology_limit':'Independent primary-first reconstruction and distinct preproof topology reused exactly; this is mathematics review, not final source/blind review. Survival88 remains adjacent rather than AND. No source topology inferred from implementation.',
 'no_final_source_or_decoder_verdict_read':True,'no_canonical_mutation_by_reviewer':True,'VERIFIED_transition':False,
 'remaining_OPEN':['Complete I5 ordered-time iteration/final survival/path factor','Full G86-11/A7 and finite path/count/summability law','Physical-time residual restart/random stopping/Markov/CK','Invariance/all-L2/cost/main composition/full paper/Goal','Exact science-commit independent admission','Aggregate/site/reader/live/main/PURIFIED']})
run=put('run89.json',{
 'status':'TERMINAL_CLOSED_INDEPENDENT_MATHEMATICS_AND_EXPOSITION_ACCEPTED','reviewer_id':'/root/exact_verify77','observed_workspace_commit':head,'decision':decision,
 'native_foreground_receipts':[pin(O/'fresh-focused-build.receipt.json'),pin(O/'fresh-whole-source-kernel.receipt.json')],
 'native_logs':[pin(O/r) for r in ['fresh-focused-build.stdout.log','fresh-focused-build.stderr.log','fresh-whole-source-kernel.stdout.log','fresh-whole-source-kernel.stderr.log']],
 'pinned_runtime':'Lean4.33.0-windows; repository lake-manifest and Mathlib commit db584cd6d46c92f209a44c0f1c829460d327499d; Python -X utf8/PYTHONUTF8=1',
 'negative_policy':'Original failed postprocessing/import and guessed exposition boundary scripts retained with diagnoses and successful successor scripts; no negative was a mathematical target repair.',
 'last_tool_observations':pin(O/'pending-exposition89.checkpoint.json'),'fresh_compiler_rerun_after_exposition_only_repair':'unnecessary; exact source/statement/whole BODY remained byte-identical',
 'canonical_source_audit':'hash-only as a successor freeze descriptor; no final verdict content consumed','no_fabricated_native_reasoning_trajectory':True,'no_VERIFIED_or_global_credit':True})
preservation=put('final-collaborator-preservation89.json',{'count':21,'all_match':True,'baseline':collab['baseline'],'RAWs':nowcollab})
actual_inputs=inputs+[pin(L),pin(P),pin(S),pin(ED),pin(EM)]+successor_pins+external
dedup={ (d['path'],d['raw_sha256']):d for d in actual_inputs }
owned=[pin(p) for p in sorted(O.rglob('*')) if p.is_file() and p.name!='closed-RAW-manifest89.json']
manifest=put('closed-RAW-manifest89.json',{
 'schema_version':1,'status':'CLOSED_ACCEPTED_INDEPENDENT_MATHEMATICS_AND_CURRENT_EXPOSITION','reviewer_id':'/root/exact_verify77','checked_workspace_commit':head,
 'frozen_current_inputs':list(dedup.values()),'owned_artifacts':owned,'decision':decision,'run':run,'collaborator_preservation':preservation,
 'historical_original_resolution':'Original target lesson/publication/freeze bytes resolve through owned immutable exactraw snapshots and snapshot index. External distinct repair inputs resolve through their declared closed_snapshot where supplied. Old draft freeze historical audit/cell pins are metadata, not new consulted source/blind verdicts.',
 'noncircular':'This manifest excludes itself; all listed owned outputs and consulted inputs are exact RAW SHA256/byte counts. Final manifest hash is returned externally.',
 'read_boundary':'No final source reviewer verdict, blind reconstruction verdict or final canonical audit content read. Separate exact-science admission remains required.'})
print(json.dumps({'decision':decision,'run':run,'closed_manifest':manifest,'final_exposition':final_exposition,'actual_input_records':len(dedup),'owned_artifacts':len(owned)},indent=2))
