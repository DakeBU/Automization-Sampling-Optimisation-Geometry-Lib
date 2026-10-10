from pathlib import Path
import copy, hashlib, json, sys
root=Path.cwd();sys.path.insert(0,'tools')
import astis_publication as pub, astis_semantic_roundtrip as rt, astis_advance as adv
r=root/'runs/20261007-companion-priority/pbps-sharp-energy68'
load=lambda p:json.loads(p.read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
failure=r/'admit-independent68-exact7-inputs'
receipt=load(failure/'receipt.json')
assert receipt['actual_foreground_pid']==20028 and receipt['exit_code']==1
assert b'publication_declarations must cover exactly the proved Lean declarations' in (failure/'stderr.log').read_bytes()
partial=load(failure/'exact-precanonical-to-PROVED_LOCAL-boundary.json')
for row in partial['rows']:
 b=(root/row['path']).read_bytes()
 assert len(b)==row['RAW_bytes'] and sha(b)==row['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==row['LF_sha256']
assert not (r/'proved-local.json').exists()
plan,claim=load(r/'publication-plan.json'),load(r/'claim.json')
source=load(r/'root.source68.adoption.json')
for folder,count,lease_sha,field in [
 ('independent-source68',363,'e5962c11b38f64e3d782175c959e2c25c4b5e2bcad750eaf963cf4f547c89aeb','all_regular_owned_files_excluding_manifest_self_and_final_lease'),
 ('independent-source-delta-schema68',24,'3a6254f1334127de61473688605872877e9caef3c109975864c852f0d9f7f828','rows')]:
 d=r/folder;lease=load(d/'lease.final.json');manifest=load(d/'owned-manifest.json')
 assert sha((d/'lease.final.json').read_bytes())==lease_sha and lease['status']=='CLOSED_LAST'
 files={p.relative_to(d).as_posix():p for p in d.rglob('*') if p.is_file()}
 assert len(files)==count and set(files)=={row['path'] for row in manifest[field]}|{'owned-manifest.json','lease.final.json'}
 for row in manifest[field]:
  b=files[row['path']].read_bytes();assert len(b)==row['RAW_bytes'] and sha(b)==row['RAW_sha256']
  assert sha(b.replace(b'\r\n',b'\n'))==row['LF_sha256']
 run=load(d/'review-run.json');assert sha(can({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']==lease['whole_logical_run_sha256']
 assert (d/'lease.final.json').stat().st_mtime_ns>=max(p.stat().st_mtime_ns for p in files.values())
audit_paths=['research-wiki/semantic-roundtrip/audits/'+aid+'.json' for aid in plan['audit_ids']]
finite=[]
proposal=load(r/'source-delta-schema-adapter68/proposal.json')
for i,key in enumerate(['0','1','consumer']):
 before=r/f'audit.{key}.before-source-admission.exactraw.snapshot.json'
 old=load(before);decision=load(r/'independent-source68'/f'source.{key}.decision.json')
 adapter=load(r/f'source.{key}.review.root-adapter.json')
 assert adapter['deltas']==proposal['entries'][i]['canonical_deltas']
 assert {k:v for k,v in adapter.items() if k not in ['deltas','exact_delta_schema_map','native_complete_RAW_review_sha256','native_review_bytes_preserved','external_whole_run_binding']}=={k:v for k,v in decision.items() if k!='deltas'}
 expected=copy.deepcopy(old);expected.update(state='accepted',semantic_slots=decision['semantic_slots'],deltas=adapter['deltas'],verdict=decision['verdict'],repairs=[])
 expected['source_review']=dict(state='accepted',reviewer=decision['reviewer'],independent_from_formalizer=True,independent_from_decoder=True,evidence=decision['review_evidence'],review_run_sha256=decision['review_run_sha256'],reviewer_packet_sha256=decision['reviewer_packet_sha256'],run_artifact=(r/f'source.{key}.review.root-adapter.json').relative_to(root).as_posix())
 current=root/audit_paths[i] if i<2 else r/'consumer.semantic-audit68.accepted.json'
 assert load(current)==expected
 assert rt.semantic_reviewer_packet(old)==rt.semantic_reviewer_packet(expected)==load(r/f'source.{key}.reviewer-packet.json')
 if i<2:finite.append(dict(canonical_path=audit_paths[i],original_exact_RAW_snapshot=before.relative_to(root).as_posix(),current_accepted_RAW_sha256=sha(current.read_bytes()),original_RAW_sha256=sha(before.read_bytes()),only_review_admission_fields_changed=True))
payload=load(r/'independent-source68/complete-RAW-input-payload.json')
for row in payload['entries']:
 p=root/row['source_path'];b=p.read_bytes()
 if row['source_path'] in audit_paths:
  i=audit_paths.index(row['source_path']);b=(r/f'audit.{i}.before-source-admission.exactraw.snapshot.json').read_bytes()
 assert len(b)==row['RAW_bytes'] and sha(b)==row['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==row['LF_sha256']
 assert (r/'independent-source68'/row['raw_snapshot']).read_bytes()==b
assert not rt.validate_registry(rt.load_registry())
pub.inputs.cache_clear();pub.load.cache_clear();pub.check_advance(plan['mathematical_declarations'],reviewed=True)
mirror=load(r/'conceptual-mirror-audit68.json');mirror={k:mirror[k] for k in ['status','discovery_ids','reason']}
boundary=claim['truth_boundary']+' Independent math275, source363, decoder31+25 and separately reviewed V2/schema24 admitted. Complete Test is a compiled separately source-reviewed consumer. Exact SCI68 and serialized aggregate remain pending. Generic S,T prose aliases need a later independent overlay; full Exposition/PURIFIED unearned.'
cells=[(root/'research-wiki/frontier-cells'/f'{cid}.json',cid) for cid in plan['active_cells']]
e=dict(result_kind='integration-node',theorem_delta=claim['theorem_delta'],lean_declarations=plan['mathematical_declarations'],publication_declarations=plan['mathematical_declarations'],genuine_compiled_source_consumers=[claim['target_declarations'][2]],lean_files=claim['proposed_files'],focused_checks=[dict(command='lake build Tests.ProximalBPSSharpCorrectorEnergy',result='Root38372 EXIT0/3950; clean actual21404 EXIT0. Independent leaf41164/main18400/Test42008 EXIT0; all3 standard axioms only.'),dict(command='Independent mathematics, blind decoding and primary-first whole-module source review',result='CLOSED math275/source363/blind31+25/schema24;344 source nodes/11 literal BODY spans/3 packets/21 slots. Exact V2 independently reviewed; no source mathematical repair.')],truth_boundary=boundary,conceptual_mirror_audit=mirror,useful_discoveries=[],active_cells=plan['active_cells'],reader_lesson=['website/content/declaration_lessons/'+s+'.json' for s in plan['slugs']],integration_notes='Two production declarations plus genuine full original-input Test consumer. Exact coefficient1/(2gamma) and every0<omegaWeight<=gamma; rank0/alphaeta1 retained. Next source69 intertwining header only, not proof/dependency. Sole stabilization lane; no whole main/cost/composition/Exposition/PURIFIED/Goal claim.')
for key in ['statement_seal','source_proof_coverage','proof_digestion','purification']:
 e[key]=[dict(declaration=decl,declaration_level=load(p)['declaration_level'],report=load(p)[key]) for (p,cid),decl in zip(cells,plan['mathematical_declarations'])]
adv.transition_advance(claim['advance_id'],'PROVED_LOCAL',worker_id=claim['created_by'],evidence=e)
for i,(p,cid) in enumerate(cells):
 cell=load(p);assert cell['status']=='claimed'
 (r/f'cell.{i}.before-proved.exactraw.snapshot.json').write_bytes(p.read_bytes())
 cell['status']='proved_locally';cell['conceptual_mirror_audit']=mirror
 cell['evidence'].update(proof_review=(r/'independent-math68/named-mathematical-review.payload.json').relative_to(root).as_posix(),source_review=(r/f'source.{i}.review.root-adapter.json').relative_to(root).as_posix(),execution_boundary=boundary)
 p.write_text(json.dumps(cell,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
(r/'proved-local.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
(r/'source-admission-finite-current-maps68.json').write_text(json.dumps(dict(status='EXACT2_SOURCE_REVIEW_ADMISSION_MAPS',rows=finite,all_other144_source_input_rows_current_RAW_identical=True,failed_owner_transition_retained=True,production_publications=2,full_compiled_and_source_reviewed_Test_consumers=1),indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS68 PROVED_LOCAL:2 production theorem/publication declarations plus1 genuine fully reviewed Test consumer; exact source maps preserved. SCI68 verification pending.')
