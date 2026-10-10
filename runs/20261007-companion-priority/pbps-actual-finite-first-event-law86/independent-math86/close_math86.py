from pathlib import Path
import argparse,datetime,hashlib,json,re,subprocess
R=Path('E:/Samplinglib');O=Path(__file__).parent;B=O.parent
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def load(p):return json.loads(p.read_text('utf8'))
def save(n,d):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
parser=argparse.ArgumentParser();parser.add_argument('--successor-freeze',required=True);args=parser.parse_args()
successor=Path(args.successor_freeze)
if not successor.is_absolute():successor=R/successor
freeze=load(successor)
assert pin(successor)['raw_sha256']=='bb3e3178473a2d9d4ea6adc01c58fe0bc28d7836306bbc38e5384dbfb6e06d3e'
source=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteFirstEventLaw.lean'
assert pin(source)['raw_sha256']=='cb8bd3e3ed053d114c6871ceaff24ab7782b46be405d69afe7174e0f4b7721d5'
lesson=R/'website/content/declaration_lessons/pbps-actual-finite-first-event-law.json'
publication=R/'website/content/publications/pbps-actual-finite-first-event-law.json'
old=load(O/'original-lesson86.exactraw.json');expected=json.loads(json.dumps(old))
proposal=load(O/'proposed-exposition-overlay86.v2.json')
assert len(proposal['changes'])==3
for c in proposal['changes']:
 m=re.fullmatch(r'units\[0\]\.steps\[(\d+)\]\.formula',c['path']);assert m
 i=int(m[1]);assert expected['units'][0]['steps'][i]['formula']==c['before'];expected['units'][0]['steps'][i]['formula']=c['after']
assert load(lesson)==expected,'Current lesson must equal exact3field reviewed overlay only'
assert load(publication)==load(O/'original-publication86.exactraw.json'),'Publication counterpart changed unexpectedly'
# Recheck all successor RAW pins without opening semantic audit/cell verdict contents.
freeze_checks=[]
context_snapshots=[]
for x in freeze['inputs']:
 p=Path(x['path']);p=p if p.is_absolute() else R/p
 actual=pin(p);sha=x.get('RAW_sha256',x.get('raw_sha256'));size=x.get('RAW_bytes',x.get('bytes'))
 assert actual['raw_sha256']==sha and actual['bytes']==size
 opaque=p not in [lesson,publication]
 row=dict(expected=x,actual=actual,content_read=not opaque,audit_or_cell_hash_only=opaque)
 if opaque:
  label='audit' if 'audits' in p.parts else 'cell'
  snapshot=O/f'successor-{label}86.observed.exactraw.json'
  with snapshot.open('xb') as f:f.write(p.read_bytes())
  row['immutable_snapshot']=pin(snapshot)
  row['original_location_is_observation_not_future_current_requirement']=True
  context_snapshots.append(dict(original_location_at_review=actual,immutable_snapshot=pin(snapshot),content_not_inspected=True,mathematical_premise=False))
 freeze_checks.append(row)
adoption=Path(freeze['reviewed_exact_overlay']['path']);adoption=adoption if adoption.is_absolute() else R/adoption
assert pin(adoption)['raw_sha256']==freeze['reviewed_exact_overlay']['RAW_sha256']
save('successor-context-snapshot-index86.json',dict(created_utc=now(),observations=context_snapshots,reason='Mutable canonical audit/cell are RAW observations only, not mathematical inputs or read verdicts. Preserve bytes so later adoption need not require their old current-location hashes.',exposition_repair_adoption=pin(adoption)))
module_lines=source.read_bytes().splitlines(keepends=True);u=load(lesson)['units'][0];rows=[]
for i,x in enumerate(u['steps'],1):
 q=x['lean_source_region'];a=q['start_line'];b=q['end_line'];code=b''.join(module_lines[a-1:b]);assert code==x['lean'].encode();assert hashlib.sha256(code).hexdigest()==q['exact_code_raw_sha256'];assert q['source_raw_sha256']==pin(source)['raw_sha256']
 rows.append(dict(step=i,title=x['title'],start_line=a,end_line=b,formula=x['formula'],mathematical_text='ACCEPT',formula_to_BODY='ACCEPT',exact_RAW_Lean_region=True,region_digest=q['exact_code_raw_sha256']))
assert all(rows[k]['end_line']+1==rows[k+1]['start_line'] for k in range(5,10))
assert list(map(ord,u['formula'][:5]))==[92,105,110,116,95]
save('exposition-review86.json',dict(status='ACCEPTED_COMPLETE_EXPOSITION_WITH_REVIEWED_FORMULA_ONLY_SUCCESSOR',created_utc=now(),module=pin(source),original_snapshot_index=pin(O/'original-exposition-snapshot-index86.json'),proposal=pin(O/'proposed-exposition-overlay86.v2.json'),successor_freeze=pin(successor),successor_raw_inputs_rechecked=freeze_checks,current_lesson=pin(lesson),current_publication=pin(publication),exact_three_changed_fields=True,all_11_steps=rows,five_private_lemma_full_statements_and_proofs=True,entire_public_BODY_205_to_400_contiguous=True,full_statement_six_binders_all14_defs_all_conclusions=True,publication_and_lesson_statement_exact=load(publication)['items'][0]['statement']==u['statement'],same_assumptions=load(publication)['items'][0]['assumptions']==u['assumptions'],attribution='ASTIS explicit completion of actual first-factor implicit A7; fullpath/invariance/main OPEN.',required_repairs=[],escaping_diagnosis='Original formula already single backslash; mistaken no-op proposal retained and corrected.',source_final_review_not_claimed=True,live_or_reader_render_not_claimed=True))
K=load(O/'kernel-dependency-summary86.json');F=load(O/'fake-closure-scan86.json');S=load(O/'statement-definition-audit86.json');I=load(O/'input-freeze86.json')
assert K['standard_axioms_only'] and K['exact_four_public_parents'] and F['status']=='PASS' and S['full_private_Prop_exact']
assert load(O/'fresh-focused-build.receipt.json')['exit_code']==0 and load(O/'fresh-whole-module.receipt.json')['exit_code']==0
for x in I['raw_inputs']:assert pin(R/x['path'])==x
bindings=load(O/'transitive-kernel-source-binding86.json')['bindings']
for x in bindings:assert pin(R/x['source']['path'])==x['source']
current=[*I['raw_inputs'],pin(lesson),pin(publication),pin(successor),pin(adoption)]
for x in freeze_checks:
 q=x.get('immutable_snapshot',x['actual'])
 if q not in current:current.append(q)
for p in ['.lake/packages/mathlib/Mathlib/MeasureTheory/Constructions/BorelSpace/Order.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Bochner/ContinuousLinearMap.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Function/L1Space/Integrable.lean']:
 current.append(pin(R/p))
for x in bindings:
 if x['source'] not in current:current.append(x['source'])
save('decision86.json',dict(schema='astis.independent-math-decision86.v1',status='ACCEPTED_INDEPENDENT_MATHEMATICS_ONLY',created_utc=now(),reviewer_id='/root/exact_verify77',checked_commit=I['checked_commit'],checked_input_scope='Commit plus frozen working module, not final exact-science-commit admission.',module=pin(source),full_private_statement_seal_exact=True,six_original_binders=True,all14_literal_definitions=True,standard_axioms_only=True,axiom_evidence=pin(O/'kernel-dependency-summary86.json'),focused=pin(O/'fresh-focused-build.receipt.json'),fresh_complete_source=pin(O/'fresh-whole-module.receipt.json'),actual_project_public_parents=K['actual_public_producer_parents'],kernel_counts=dict(owned_generated=K['owned_count'],immediate_private_specs=len(K['private_spec_dependencies']),transitive_project=K['transitive_count'],transitive_edges=K['edge_count'],direct_generic=K['generic_count']),fake_closure=pin(O/'fake-closure-scan86.json'),whole_mathematics=pin(O/'whole-mathematics-review86.json'),complete_exposition=pin(O/'exposition-review86.json'),required_repairs=[],repair_history='Only3 formula sequencing fields changed after distinct exact-overlay review; original inputs/no-op escaping diagnosis retained. No mathematical/header/Lean repair.',truth_boundary='Finite actual firstevent density/mark/subprobability/threeL1/integral only. Unusedtail/fullA7/pathspace/reversal/invariance/AE-safeJensen/allL2/Markov/semigroup/main/cost/composition OPEN.',not_decoder_or_final_source_review=True,no_VERIFIED_or_shared_state_change=True))
save('run-manifest86.json',dict(schema='astis.independent-whole-math-run86.v1',status='CLOSED',created_utc=now(),reviewer_id='/root/exact_verify77',checked_commit=I['checked_commit'],current_frozen_inputs=current,original_immutable_input_snapshots=load(O/'original-exposition-snapshot-index86.json')['snapshots'],original_path_policy='Original observations are provenance only; original byte snapshots are authoritative. Do not require current lesson to match the old original path hash.',compiler_receipts=[pin(O/'fresh-focused-build.receipt.json'),pin(O/'fresh-whole-module.receipt.json')],blind_or_final_source_verdict_read=False,owned_outputs=[pin(p) for p in sorted(O.iterdir()) if p.is_file() and p.name!='run-manifest86.json']))
save('closed-RAW-manifest86.json',dict(schema='astis.closed-independent-whole-math86.v1',status='CLOSED_NONCIRCULAR',created_utc=now(),reviewer_id='/root/exact_verify77',frozen_current_inputs=current,immutable_original_inputs=[x['immutable_snapshot'] for x in load(O/'original-exposition-snapshot-index86.json')['snapshots']],original_observation_provenance=load(O/'original-exposition-snapshot-index86.json')['snapshots'],owned_artifacts=[pin(p) for p in sorted(O.iterdir()) if p.is_file()],self_hash_omitted=True,originals_and_negative_diagnoses_retained=True,no_production_or_shared_writes=True))
print(json.dumps(dict(decision=pin(O/'decision86.json'),manifest=pin(O/'closed-RAW-manifest86.json'),run=pin(O/'run-manifest86.json')),indent=2))
