from pathlib import Path
import datetime,hashlib,json,subprocess
R=Path('E:/Samplinglib');O=Path(__file__).parent;B=O.parent
def pin(p):
 p=Path(p);b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def load(p):return json.loads(p.read_text('utf8'))
def put(n,v):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteHistoryExtension.lean'
L=R/'website/content/declaration_lessons/pbps-actual-finite-history-extension.json'
P=R/'website/content/publications/pbps-actual-finite-history-extension.json'
S=B/'root.statement-seal90.json';F=B/'publication-freeze90.after-exposition.json'
assert pin(M)['raw_sha256']=='6cdc14328be5ec3ece3f028e6e1dd0185ee4031a8e651956ee0f55d4beebf029'
assert pin(S)['raw_sha256']=='29f7e3600b6712794943f3dc6b472dd8b53cb03435a803fe54d450c0396a9028'
assert pin(L)['raw_sha256']=='f8e3db3c9cffc10938fc6350ec16a589eeb43dc2130c48f0f41544511a56b905'
assert pin(P)['raw_sha256']=='908c65e23b7608a2609a515da742a1db378f087c3143807cf1ed21a5f8728022'
assert L.read_bytes()==(O/'lesson90.proposed-total-append-formula.exactraw.json').read_bytes()
assert P.read_bytes()==(O/'publication90.proposed-total-append-formula.exactraw.json').read_bytes()
freeze=load(F);assert freeze['publication_binding_sha256']=='b3a9241d785c8132839c366f260d5fbc3dcaa40aba8566560ec814e6c5716472'
decision=B/'independent-exposition-repair90/decision90.native.json'
manifest=B/'independent-exposition-repair90/closed-raw-manifest90.json'
assert pin(decision)['raw_sha256']=='fec067eeb31ccddc42dca9c971f0c6ada7022e1f3633f77c436d620c40232bdf'
assert pin(manifest)['raw_sha256']=='d84d81f127d5f9e4d4db4b48c32b7c1d627d9033db444fc5f87f7434160b193c'
d=load(decision);assert d['decision']=='ACCEPT_EXACT_TWO_FIELD_EXPOSITION90_REPAIR' and d['required_repairs']==[]
assert d['reviewer_id']=='/root/exposition_repair89'
validated=[]
for z in load(manifest)['inputs']+load(manifest)['artifacts']:
 p=Path(z.get('closed_snapshot',z['path']));p=p if p.is_absolute() else R/p
 q=pin(p);assert q['raw_sha256']==z['sha256'] and q['bytes']==z['bytes']
 validated.append(q)
put('distinct-exposition-review90.RAW-validation.json',{'all_25_descriptors_match':len(validated)==25,'checked_descriptors':validated,'decision':pin(decision),'manifest':pin(manifest),'private_source_extracts_and_reviewer_script_contents_not_read':True,'scope':'Exact distinct repair review only; no final source or decoder verdict consulted.'})
old_audit=B/'audit.before-decoder90.json';pre_overlay=B/'audit.before-exposition90.json'
assert pin(old_audit)['raw_sha256']=='b130806b77fc1b3ec3c4799e36f77fc1cde2c7b275c1465a1db27ed0bd1f93c4'
assert pin(pre_overlay)['raw_sha256']=='c623aa7dde64d17fa772cec53e70d4aae769b46016100ffa7090df79b17a1427'
q=O/'.private.coordinator-audit90.original-draft.exactraw.json'
with q.open('xb') as out:out.write(old_audit.read_bytes())
assert pin(q)['raw_sha256']==pin(old_audit)['raw_sha256']
original_index=load(O/'original-exposition-snapshot-index90.json')
resolutions=[]
for z in original_index['snapshots']:
 e=dict(z['original']);e['closed_snapshot']=z['closed_snapshot']['path'];resolutions.append(e)
audit_path='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualFiniteHistoryExtension.json'
for snap in [q,O/'.private.coordinator-audit90.observed.exactraw.json']:
 e=pin(snap);e.update({'path':audit_path,'closed_snapshot':pin(snap)['path'],'read_scope':'Hash-only metadata snapshot; no JSON assessment content used.'});resolutions.append(e)
cell=O/'.private.coordinator-cell90.observed.exactraw.json'
e=pin(cell);e.update({'path':'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-finite-history-extension.json','closed_snapshot':pin(cell)['path'],'read_scope':'Hash-only original claimed-cell snapshot; no state acceptance evidence.'});resolutions.append(e)
for e in resolutions:
 p=R/e['closed_snapshot'];assert pin(p)['raw_sha256']==e['raw_sha256']
put('historical-input-resolution90.json',{
 'status':'AUTHORITATIVE_IMMUTABLE_ORIGINAL_AND_STAGE_SNAPSHOT_RESOLUTION','resolutions':resolutions,
 'root_original_audit_snapshot':pin(old_audit),'root_pre_exposition_audit_snapshot':pin(pre_overlay),
 'prior_negative_retained':pin(O/'coordinator-historical-hash90.negative.json'),
 'evolution':'Original draft audit b130 evolved to c623 before own original snapshot attempt; no silent rehash. Root retained before-decoder b130 snapshot now copied byteexact hash-only. Before-exposition c623 matches own observed snapshot. Root publication freezes remain native immutable historical records; their mutable canonical references resolve through these snapshots.',
 'no_audit_or_cell_JSON_semantic_content_read':True})
u=load(L)['units'][0];pub=load(P)['items'][0];assert u['statement']==pub['statement'] and u['assumptions']==pub['assumptions']
old_u=load(O/'lesson90.original.exactraw.json')['units'][0]
old_p=load(O/'publication90.original.exactraw.json')['items'][0]
def diff(a,b,path=''):
 if type(a)!=type(b):return [path]
 if isinstance(a,dict):return [t for k in sorted(set(a)|set(b)) for t in (diff(a[k],b[k],path+'/'+str(k)) if k in a and k in b else [path+'/'+str(k)])]
 if isinstance(a,list):
  assert len(a)==len(b);return [t for i,(x,y) in enumerate(zip(a,b)) for t in diff(x,y,path+'/'+str(i))]
 return [] if a==b else [path]
assert diff(old_u,u)==['/steps/0/formula'] and diff(old_p,pub)==['/formulae/0/tex']
lines=M.read_bytes().splitlines(keepends=True);regions=[]
for i,step in enumerate(u['steps']):
 sr=step['lean_source_region'];a=sr['start_line'];b=sr['end_line'];code=b''.join(lines[a-1:b])
 assert code.decode('utf8')==step['lean'] and hashlib.sha256(code).hexdigest()==sr['exact_code_raw_sha256'] and sr['source_raw_sha256']==pin(M)['raw_sha256']
 regions.append({'step':i+1,'lines':[a,b],'exact_code_raw_sha256':sr['exact_code_raw_sha256'],'title':step['title'],'formula':step['formula'],'independent_original_mathematics_check':'All formula/prose/code sequences checked in original-exposition90.audit; only first formula amended by distinctly reviewed exact proposal.'})
assert len(regions)==6 and regions[0]['lines'][0]==120 and regions[-1]['lines'][1]==340
assert all(x['lines'][1]+1==y['lines'][0] for x,y in zip(regions,regions[1:]))
put('final-exposition90.audit.json',{
 'status':'ACCEPT_CURRENT_COMPLETE_EXPOSITION_WITH_DISTINCT_EXACT_REPAIR','reviewer_id':'/root/exact_verify77',
 'module':pin(M),'lesson':pin(L),'publication':pin(P),'publication_freeze':pin(F),'publication_binding_sha256':freeze['publication_binding_sha256'],
 'complete_six_contiguous_BODY_regions':regions,'full_body_lines':[120,340],
 'complete_attributed_statement_and_conditions':True,'same_statement_and_assumptions_in_lesson_publication':True,
 'all_original_proof_steps_and_formulas_checked':pin(O/'original-exposition90.audit.json'),
 'distinct_repair_decision':pin(decision),'distinct_repair_manifest':pin(manifest),
 'proposer_does_not_self_approve_repair':True,'canonical_exact_accepted_candidates_verified':True,
 'only_changed_fields':['/units/0/steps/0/formula','/items/0/formulae/0/tex'],
 'repair_scope':'Display total live append using T+max{s,0} for every real s, raw Phi_s unchanged; stopped unchanged. Existing statement/Lean definition unchanged. All other reader bytes and embedded regions unchanged.',
 'required_exposition_repairs':[],'no_final_source_or_decoder_verdict_read':True,
 'source_scope':'Attributed ASTIS completion of one printed A.2/A.7 iteration ingredient with source A2 Borel construction. No fullA7/path/restart/Markov/global/main/wholeGoal credit.'})
input_freeze=load(O/'input-freeze90.json');kernel=load(O/'kernel-dependency90.json')
inputs=list(input_freeze['actual_inputs'])
for z in inputs:assert pin(R/z['path'])==z
for z in kernel['ASTIS_source_files']:assert pin(R/z['path'])==z
extras=[L,P,F,decision,manifest,old_audit,pre_overlay,
 R/'runs/20261007-companion-priority/pbps-actual-finite-history-tail-law87/independent-math87/prepare_and_compile87.py',
 R/'runs/20261007-companion-priority/pbps-actual-conditional-next-wait-density89/independent-math89/analyze_kernel89.attempt2.py']
for p in extras:inputs.append(pin(p))
for z in kernel['ASTIS_source_files']:
 if z not in inputs:inputs.append(z)
inputs+=resolutions
baseline=load(R/'runs/20261007-companion-priority/pbps-conditional-next-wait-density-preread89/pre-fetch89.workspace-RAW.json')['tracked_modified']
assert len(baseline)==21
for p,h in baseline.items():assert pin(R/p)['raw_sha256']==h
put('collaborator-preservation90.final.json',{'all_21_match':True,'files':[pin(R/p) for p in baseline]})
for name in ['fresh-focused-build','fresh-whole-source-kernel']:
 rc=load(O/(name+'.receipt.json'));assert rc['exit_code']==0 and rc['terminal_closed'] and rc['source']['raw_sha256']==pin(M)['raw_sha256']
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()
put('decision90.json',{
 'status':'ACCEPTED_INDEPENDENT_MATHEMATICS_AND_CURRENT_EXPOSITION_ONLY','reviewer_id':'/root/exact_verify77',
 'context_commit':head,'reviewed_worktree_module_not_yet_science_commit':pin(M),'seal':pin(S),
 'whole_private_Prop_and_six_source_binders_and28_lets_exact':True,
 'whole_BODY_mathematical_findings':pin(O/'whole-mathematics90.pre-exposition.json'),
 'current_complete_exposition':pin(O/'final-exposition90.audit.json'),
 'kernel':pin(O/'kernel-dependency90.json'),'fake_closure':pin(O/'fake-closure90.json'),
 'fresh_focused_and_complete_source_kernel_exit0':True,'standard_axioms_only':True,'axioms':kernel['axioms'],
 'actual_immediate_public_parents':kernel['immediate_public_producers'],
 'kernel_counts':{'owned_generated_and_public':kernel['owned_constant_count'],'immediate_public':kernel['immediate_public_count'],'immediate_private':kernel['immediate_private_generated_count'],'transitive_ASTIS_constants':kernel['transitive_ASTIS_constant_count'],'transitive_ASTIS_edges':kernel['transitive_ASTIS_edge_count'],'ASTIS_source_files':kernel['ASTIS_source_file_count'],'generic_direct_constants':kernel['generic_direct_count']},
 'actual88_absent':True,'source_ingredient_readback':pin(O/'source-ingredient-readback90.json'),
 'required_repairs':[],'historical_exposition_gap_resolved_by_distinct_reviewer':pin(decision),
 'all_21_collaborator_RAW_preserved':True,'no_final_source_or_decoder_verdict_read':True,
 'no_production_shared_ledger_cell_or_VERIFIED_writes':True,
 'remaining_OPEN':['Independent blind/source final acceptance and exact science-commit admission','shared integration/aggregate/site/reader/main/purification','ordered absolute-time density iteration and final survival/path/count assembly/fullA7/G86-11','random stopping/physical-time restart/Markov','global invariance/all-L2/cost/composition/main/wholepaper/Goal']})
put('run90.json',{
 'status':'CLOSED_INDEPENDENT_WHOLE_MATHEMATICS_KERNEL_AND_CURRENT_EXPOSITION_REVIEW','reviewer_id':'/root/exact_verify77',
 'closed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'context_commit':head,'module':pin(M),
 'chronology':'Pinned primary directly reread and timestamped before production BODY; complete source manually read, fresh foreground focused and exact-source observational kernel checks run; independent full BODY mathematics and six-region original exposition audit; exact2field total-definition formula repair distinctly reviewed then root applied; final reader bytes equal accepted candidates. No final source/neutral decoder verdict consulted.',
 'terminal_receipts':[pin(O/(n+'.receipt.json')) for n in ['fresh-focused-build','fresh-whole-source-kernel']],
 'native_kernel_reasoning_trajectory_fabricated':False,'decision':pin(O/'decision90.json'),
 'historical_input_resolution':pin(O/'historical-input-resolution90.json'),
 'preserved_negatives':['Historical probe filename lookup before compiler','Draft audit stage-evolution hash mismatch before original snapshot; original root snapshot later resolved'],
 'no_repeated_unchanged_proof_or_Lean_check_after_exposition_only_repair':True,
 'not_final_source_blind_or_VERIFIED_admission':True})
artifacts=[pin(p) for p in sorted(O.iterdir()) if p.is_file() and p.name!='closed-RAW-manifest90.json']
put('closed-RAW-manifest90.json',{
 'status':'CLOSED_NONCIRCULAR_INDEPENDENT_WHOLE_MATHEMATICS_AND_CURRENT_EXPOSITION','reviewer_id':'/root/exact_verify77',
 'algorithm':'SHA256 exact raw bytes','frozen_inputs':inputs,'owned_artifacts':artifacts,
 'decision':pin(O/'decision90.json'),'run':pin(O/'run90.json'),
 'historical_input_resolution':pin(O/'historical-input-resolution90.json'),
 'distinct_repair_manifest_recursively_rehashed':pin(O/'distinct-exposition-review90.RAW-validation.json'),
 'self_hash_intentionally_omitted':True,
 'closure':'Every directly consulted input and reviewer output is pinned; kernel-bound actual source files rechecked. Historical canonical audit/reader slots resolve through explicit closed_snapshot bytes; original freezes/proposals/diagnoses are immutable. Reviewer-script/private-source-extract content from distinct review is hash-only, not consulted.',
 'privacy':'Long primary extracts and hash-only coordinator snapshots .private.* are local-only, excluded from public packets/archives.',
 'no_science_commit_VERIFIED_or_canonical_mutation':True})
for z in inputs+artifacts:
 p=R/z.get('closed_snapshot',z['path']);q=pin(p);assert q['raw_sha256']==z['raw_sha256'] and q['bytes']==z['bytes']
print(json.dumps({'decision':pin(O/'decision90.json'),'manifest':pin(O/'closed-RAW-manifest90.json'),'run':pin(O/'run90.json'),'frozen_inputs':len(inputs),'owned_artifacts':len(artifacts)},indent=2))
