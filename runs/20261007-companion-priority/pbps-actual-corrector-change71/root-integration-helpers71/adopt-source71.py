from pathlib import Path
import copy, hashlib, json, os, sys
root=Path.cwd();sys.path.insert(0,str(root/'tools'))
import astis_publication as pub, astis_semantic_roundtrip as rt, astis_advance as adv
r=Path('runs/20261007-companion-priority/pbps-actual-corrector-change71');o=r/'independent-source71'
load=lambda p:json.loads(Path(p).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def check(b,z):
 assert len(b)==z['RAW_bytes'] and sha(b)==z['RAW_sha256'],z['path']
 lf=b.replace(b'\r\n',b'\n');assert sha(lf)==z['LF_sha256'],z['path']
 if 'LF_bytes' in z:assert len(lf)==z['LF_bytes'],z['path']
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
def write(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def new(p,x):assert not Path(p).exists(),p;write(p,x)
lease=load(o/'lease.final.json')
assert sha((o/'lease.final.json').read_bytes())=='0a87027cc6ecc00329097327a66026d2b4ac4afc46005fd4e3351c17632fd187'
assert lease['status']=='CLOSED_LAST' and lease['last_owned_write'] and not lease['canonical_Git_ledger_Goal_or_old_CLOSED_writes']
assert lease['owned_count']==277 and lease['bound_layer_count']==276
m=load(o/'owned-manifest.json')
assert sha((o/'owned-manifest.json').read_bytes())==lease['native_manifest_RAW_sha256']=='32d0e487577fbfb33dc66d3b216569c27fa641613db0b09f5d4a6732549c2351'
assert sha(can(m['files']))==m['entries_canonical_sha256']==lease['entries_canonical_sha256']
files={p.relative_to(o).as_posix():p for p in o.rglob('*') if p.is_file()}
assert len(files)==277 and set(files)=={z['path'] for z in lease['bindings']}|{'lease.final.json'}
assert set(files)=={z['path'] for z in m['files']}|{'owned-manifest.json','lease.final.json'}
for z in lease['bindings']:
 check(files[z['path']].read_bytes(),z)
 assert files[z['path']].stat().st_mtime_ns<=files['lease.final.json'].stat().st_mtime_ns,z['path']
run=load(o/'source.0.run.json');h=sha(can({k:v for k,v in run.items() if k!='run_sha256'}))
assert h==run['run_sha256']==lease['whole_logical_run_sha256']=='c58386e42e0944ee590fe84ddcbf4d6462297532adf758fdf5671c7c008070fb'
assert run['actor']=='/root/independent_primary69' and run['status']=='SOURCE_FIDELITY_ACCEPTED_BOUNDED_ONLY'
assert run['actual_author_pid']==24064 and run['no_canonical_Git_ledger_Goal_or_old_CLOSED_writes'] and run['no_root_math_or_prior_science_verdict_read']
for z in run['records']:check(Path(z['path']).read_bytes(),z)
payload=load(o/'complete-named-review-decision-input-payload.json')
assert sha((o/'complete-named-review-decision-input-payload.json').read_bytes())=='92ada58587378e938bf02e1b9d91f575d36e062df90e9b248bb1aec8e541a524'
decision=load(o/'source.0.decision.json');admission=load(o/'source.0.admission-fields.json')
assert payload['native_run_complete']==run and payload['decision_complete']==decision and payload['canonical_admission_fields_complete']==admission
assert payload['full_RAW_review_utf8'].encode()==(o/'source.0.review.RAW.md').read_bytes()
for name,x in payload['named_finite_input_records'].items():assert x==load(o/name),name
union=load(o/'source.0.complete-finite-input-manifest.json')
assert sha((o/'source.0.complete-finite-input-manifest.json').read_bytes())=='709ec6aabecf9b4e260963ee064f50c3bf7083dbc8d07eb8437aac26df709270'
assert union==payload['complete_finite_versioned_input_manifest_complete']
assert len(union['entries'])==union['count']==77 and union['distinct_paths']==73 and union['unmapped_input_drift']==0
assert sha(can(union['entries']))==union['entries_canonical_sha256']
maps=[];overlay=r/'reader-status-overlay71'
historical={
 'website/content/publications/pbps-actual-corrector-change.json':('0.before.exactraw.json','0.proposed.json'),
 'website/content/declaration_lessons/pbps-actual-corrector-change.json':('1.before.exactraw.json','1.proposed.json'),
 'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-corrector-change.json':('2.before.exactraw.json','2.proposed.json'),
 'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualCorrectorChange.json':('audit.before.exactraw.json','audit.1.proposed.json')}
for z in union['entries']:
 current=Path(z['path']).read_bytes();assert sha(current)==z['current_RAW_sha256_at_close'],z['path']
 for name in z['owned_RAW_snapshot_refs']:check((o/name).read_bytes(),z)
 for name in z['owned_LF_snapshot_refs']:
  lf=(o/name).read_bytes();assert sha(lf)==z['LF_sha256'] and b'\r\n' not in lf,z['path']
 if z['version_is_historical_approved_reader_overlay']:
  assert z['path'] in historical,z['path']
  before,after=historical[z['path']];check((overlay/before).read_bytes(),z)
  assert current==(overlay/after).read_bytes(),z['path']
  maps.append(dict(path=z['path'],historical_RAW_sha256=z['RAW_sha256'],current_RAW_sha256=sha(current),approved_overlay_before=pin(overlay/before),approved_overlay_after=pin(overlay/after)))
 else:check(current,z)
assert {z['path'] for z in maps}==set(historical) and len(maps)==4
assert load(r/'root.reader-status-overlay71.adoption.json')['status']
assert decision['verdict']=='equivalent-after-elaboration' and not decision['repairs']
assert decision['independent_from_formalizer'] and decision['independent_from_decoder'] and decision['review_run_sha256']==h
assert len(decision['deltas'])==16 and all(z['severity']=='informational' for z in decision['deltas'])
assert set(decision['semantic_slots'])==set(rt.SEMANTIC_SLOTS)
assert all(z['relation']!='not-audited' and z['evidence'] for z in decision['semantic_slots'].values())
assert run['counts']==dict(source_regions=4,source_math=255,source_NODE=144,source_EXCLUDED=111,graph_nodes=22,graph_edges=49,target_formulas=18,frozen_obligations=24,module_lines=528,module_NODE=506,module_EXCLUDED=22,BODY_steps=8,BODY_lines=377,decoder_rows=51,canonical_semantic_slots=7,informational_deltas=16,blocking_deltas=0,repairs=0)
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualCorrectorChange.json');audit=load(ap)
packet=load(r/'source-review.packet.1.json')
assert audit['state']=='blind-reconstructed' and rt.semantic_reviewer_packet(audit)==packet
assert packet['packet_sha256']==admission['official_packet_sha256']==decision['reviewer_packet_sha256']=='2c513c4f2660ad96817f683e072f1e7d56ddd0aa400da9bc82c51488ee0e59a8'
assert sha((r/'source-review.packet.1.json').read_bytes())==admission['official_packet_RAW_sha256']
assert admission['publication_binding_sha256']==audit['publication_binding_sha256']=='c1b90bd0a303ab6da562aac5f51e8c2d56b6a1f2cf89165b87cd79024dfada24'
accepted=copy.deepcopy(audit);accepted.update(admission['audit_fields'])
assert rt.semantic_reviewer_packet(accepted)==packet
registry=rt.load_registry();registry['audits']=[accepted if x['id']==audit['id'] else x for x in registry['audits']]
errors=rt.validate_registry(registry);assert not errors,errors
assert load(r/'root.math71.adoption.json')['native_files']==95 and load(r/'root.decoder71.adoption.json')['native_owned_files']==10
claim=load(r/'claim.json');plan=load(r/'publication-plan.json')
assert adv.current_advances()[claim['advance_id']]['state']=='EXPLORING'
cp=Path('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-corrector-change.json');pp=Path('website/content/publications/pbps-actual-corrector-change.json')
for p,n in [(ap,'audit.before-source-admission71.exactraw.json'),(cp,'cell.before-source-admission71.exactraw.json'),(pp,'publication.before-source-admission71.exactraw.json')]:assert not (r/n).exists();(r/n).write_bytes(p.read_bytes())
write(ap,accepted);cell=load(cp);publication=load(pp)
cell['source_proof_coverage']=admission['cell_source_proof_coverage'];publication['items'][0]['source_proof_coverage']=admission['publication_source_proof_coverage']
boundary='Actual same-C B21 theorem compiled and independently checked mathematically, blindly reconstructed and source-reviewed. Exact SCI71, serialized integration and reader validation remain pending. Actual B4/B27/B28 dynamics, H1/nonexplosion, full paper/main/errors/query costs/composition, full Exposition/PURIFIED/main/live/Goal remain separate.'
cell['source_detail_audit'].update(gap='Actual B21 is locally compiled and independently source-reviewed. Next exact B4 perturbation algebra and actual residual-dynamics producer remain open.',fidelity_boundary=boundary)
cell['evidence']['truth_boundary']=boundary
write(cp,cell);write(pp,publication)
pub.inputs.cache_clear();pub.load.cache_clear();pub.check_advance(plan['mathematical_declarations'],reviewed=True)
item=next(x for x in pub.load() if x['id']==plan['slugs'][0])
assert pub.binding_digest(item,item['bindings'][0],pub.inputs())==accepted['publication_binding_sha256']
assert pub.review_context(item,item['bindings'][0],pub.inputs())==accepted['publication_context']
mirror=load(r/'conceptual-mirror-audit71.json');mirror={k:mirror[k] for k in ['status','discovery_ids','reason']}
e=dict(result_kind='theorem-edge',theorem_delta=claim['theorem_delta'],lean_declarations=plan['mathematical_declarations'],publication_declarations=plan['mathematical_declarations'],lean_files=claim['proposed_files'],focused_checks=[dict(command=claim['focused_checks'][0],result='Root49980 EXIT0/3950; independent fresh Lean3064 EXIT0; standard3 only. Initial29980 deterministic heartbeat failure retained.'),dict(command='Independent math/blind/source review',result='CLOSED95/10/277;255source items,528module lines,8BODY377lines,51decoder rows,7slots,16informational deltas,0blocking,0mathrepairs.')],truth_boundary=boundary,conceptual_mirror_audit=mirror,useful_discoveries=[],active_cells=plan['active_cells'],reader_lesson=['website/content/declaration_lessons/'+s+'.json' for s in plan['slugs']],integration_notes='Same original six callers and twelve witnesses, actual g and same B20 C, exact B21 signed change. B4 exact perturbation next; no sharp-energy68 dependency. Sole stabilization lane; no full B4/main/cost/composition credit.')
for key in ['statement_seal','source_proof_coverage','proof_digestion','purification']:e[key]=[dict(declaration=plan['mathematical_declarations'][0],declaration_level=cell['declaration_level'],report=cell[key])]
adv.transition_advance(claim['advance_id'],'PROVED_LOCAL',worker_id=claim['created_by'],evidence=e)
cell['status']='proved_locally';cell['conceptual_mirror_audit']=mirror
cell['evidence'].update(proof_review=(r/'independent-math71/mathematical-verdict.json').as_posix(),source_review=(o/'source.0.decision.json').as_posix(),execution_boundary=boundary)
write(cp,cell);new(r/'proved-local.json',e)
new(r/'root.source71.adoption.json',dict(status='ACCEPTED_INDEPENDENT_SOURCE71_ACTUAL_CORRECTOR_CHANGE_ONLY',actual_root_PID=os.getpid(),native_owned_files=277,versioned_inputs=77,distinct_input_paths=73,native_whole_logical_run_sha256=h,native_complete_named_RAW=pin(o/'complete-named-review-decision-input-payload.json'),native_lease=pin(o/'lease.final.json'),finite_current_input_maps=maps,coverage=run['counts'],no_mathematical_repair=True,official_reviewer_packet_unchanged=True,publication_binding_unchanged=True,VERIFIED=False,full_paper=False,Goal_complete=False))
print('PASS71 PROVED_LOCAL: CLOSED95 math/10blind/277source; exact actual same-C B21 only. Exact SCI/aggregate/reader pending.')
