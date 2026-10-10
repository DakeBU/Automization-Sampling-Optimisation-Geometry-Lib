from pathlib import Path
import copy,hashlib,json,os,sys
sys.path.insert(0,str(Path.cwd()/'tools'))
import astis_publication as pub
import astis_semantic_roundtrip as rt
import astis_advance as adv
r=Path('runs/20261007-companion-priority/pbps-actual-harmonic-flow73');o=r/'independent-source73'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def check(z,path=None):
 p=Path(path or z['path']);b=p.read_bytes();assert len(b)==z.get('RAW_bytes',z.get('bytes')) and sha(b)==z.get('RAW_sha256',z.get('raw_sha256')),p
 assert sha(b.replace(b'\r\n',b'\n'))==z.get('LF_sha256',z.get('lf_sha256')),p
 return b
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
def write(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
lp=o/'lease.final.json';assert sha(lp.read_bytes())=='eea3a804b990e96ee4a93124e507b83482b00a6e9aa0092a474e5de858611129'
l=load(lp);rows=l['all_files_except_self'];assert l['status']=='CLOSED_LAST' and l['exit_code']==0 and len(rows)==68 and l['owned_file_count_including_self']==69
assert not l['canonical_Git_ledger_or_old_CLOSED_written'] and not l['VERIFIED_or_full_paper_credit']
assert {p.resolve() for p in o.rglob('*') if p.is_file()}=={Path(z['path']).resolve() for z in rows}|{lp.resolve()}
for z in rows:
 check(z);assert Path(z['path']).stat().st_mtime_ns<=lp.stat().st_mtime_ns
m=load(l['whole_owned_manifest']['path']);check(l['whole_owned_manifest']);assert len(m['files'])==m['count']==67
for z in m['files']:check(z)
run=load(o/'source.0.run.json');h=sha(can({k:v for k,v in run.items() if k!='run_sha256'}))
assert h==run['run_sha256']==l['whole_logical_run_sha256']=='2c8aa1cf7b0f4cd81bc55009070889064c8c8bcec23839189fa46b4ee42e6acb'
assert run['reviewer']=='/root/independent_primary69' and not run['fresh_math_compile_or_other_verdict_used']
pp=o/'complete-named-review-decision-input-payload.json';assert sha(pp.read_bytes())=='1fc44526c9200ba3d546e225acb4766dbd8f46c2c08586a50b8a1ce7d7d36ebf'
payload=load(pp);assert payload['whole_logical_run_sha256']==h and payload['named_payload_count']==5 and len(payload['named_payloads'])==5
for z in payload['named_payloads']:assert check(z['pin'])==z['complete_RAW_UTF8'].encode()
check(run['input_manifest']);inputs=load(run['input_manifest']['path']);assert inputs['current_input_count']==8 and inputs['historical_input_count']==8 and inputs['source_contract_input_count']==17
for key in ['final_current_inputs','protocol_and_freeze_inputs','immutable_source_contract_inputs','repair_authority_inputs']:
 for z in inputs[key]:check(z)
check(inputs['primary_reference']);assert len(inputs['repair_authority_inputs'])==3
overlay=load(r/'root.reader-metadata-overlay73.adoption.json');approved={z['path']:z for z in overlay['exact_current']};versions=[]
for z in inputs['historical_versions']:
 old=check(z,o/z['RAW_snapshot']);lf=(o/z['LF_snapshot']).read_bytes();assert lf==old.replace(b'\r\n',b'\n')
 current=Path(z['path']).read_bytes()
 if sha(current)!=z['RAW_sha256']:
  assert z['path'] in approved;check(approved[z['path']]);versions.append(dict(path=z['path'],historical_RAW_sha256=z['RAW_sha256'],approved_current_RAW_sha256=sha(current)))
 else:check(z)
assert len(versions)==2
check(run['coverage']);cov=load(run['coverage']['path']);assert cov['unclassified']==0 and cov['all_source_classifications_unchanged'] and cov['local_source_math_exposition_accepted']
assert cov['counts']==dict(module_lines=178,source_regions=13,source_blocks=51,source_items=79,NODE=24,EXCLUDED=55,source_nodes=23,source_edges=37,internal_bridges_produced=7,source_callers=6,conclusions=9,lesson_steps=6)
plan=load(r/'publication-plan.json');claim=load(r/'claim.json');assert adv.current_advances()[claim['advance_id']]['state']=='EXPLORING'
assert load(r/'root.math73.adoption.json')['native_files']==39
assert load(r/'root.decoder73.adoption.json')['status']=='CLOSED_BLIND_DECODER73_ADOPTED_ONLY'
ap=Path('research-wiki/semantic-roundtrip/audits')/(plan['audit_ids'][0]+'.json');cp=Path('research-wiki/frontier-cells')/(plan['active_cells'][0]+'.json');pubp=Path('website/content/publications')/(plan['slugs'][0]+'.json')
audit,cell,publication=load(ap),load(cp),load(pubp);packet=load(r/'source-review.packet.json');d=load(o/'source.0.decision.json');admission=load(o/'source.0.admission-fields.json')
assert audit['state']=='blind-reconstructed' and rt.semantic_reviewer_packet(audit)==packet
assert d['verdict']=='equivalent-after-elaboration' and d['blocking_semantic_deltas']==0 and not d['repairs'] and d['review_run_sha256']==h
assert d['independent_from_formalizer'] and d['independent_from_decoder'] and len(d['deltas'])==10 and all(z['severity']=='informational' for z in d['deltas'])
assert set(d['semantic_slots'])==set(rt.SEMANTIC_SLOTS) and all(z['relation']!='not-audited' and z['evidence'] for z in d['semantic_slots'].values())
assert packet['packet_sha256']==d['reviewer_packet_sha256']==admission['official_packet_sha256']
assert sha((r/'source-review.packet.json').read_bytes())==admission['official_packet_RAW_sha256']
assert audit['publication_binding_sha256']==d['publication_binding_sha256']==admission['publication_binding_sha256']
accepted=copy.deepcopy(audit);accepted.update(admission['audit_fields']);assert rt.semantic_reviewer_packet(accepted)==packet
cell['source_proof_coverage']=admission['cell_source_proof_coverage'];publication['items'][0]['source_proof_coverage']=admission['publication_source_proof_coverage']
registry=rt.load_registry();registry['audits']=[accepted if x['id']==accepted['id'] else x for x in registry['audits']];errors=rt.validate_registry(registry);assert not errors,errors
for p,kind in [(ap,'audit'),(cp,'cell'),(pubp,'publication')]:
 q=r/(kind+'.before-source-admission73.exactraw.json');assert not q.exists();q.write_bytes(p.read_bytes())
write(ap,accepted);write(cp,cell);write(pubp,publication);pub.inputs.cache_clear();pub.load.cache_clear();pub.check_advance(plan['mathematical_declarations'],reviewed=True)
item=next(x for x in pub.load() if x['id']==plan['slugs'][0]);assert pub.binding_digest(item,item['bindings'][0],pub.inputs())==accepted['publication_binding_sha256'] and pub.review_context(item,item['bindings'][0],pub.inputs())==accepted['publication_context']
mirror=load(r/'conceptual-mirror-audit73.json');mirror={k:mirror[k] for k in ['status','discovery_ids','reason']}
boundary='Actual deterministic harmonic flow, nine clauses and six retained analytic callers focused-compiled, independently mathematically reviewed, blindly reconstructed and source-reviewed. Exact SCI73, serialized shared integration and reader acceptance remain pending. No bounce/rate/clock/random path, actual terminal Markov kernel, nonexplosion/invariance/reversal/main/errors/expected-query costs/actual-input composition or whole-paper/Exposition/PURIFIED/main/live/Goal credit.'
e=dict(result_kind='theorem-edge',theorem_delta=claim['theorem_delta'],lean_declarations=plan['mathematical_declarations'],publication_declarations=plan['mathematical_declarations'],lean_files=claim['proposed_files'],focused_checks=[dict(command=claim['focused_checks'][0],result='Root17888 EXIT0/2523jobs; independent fresh directLean39960 EXIT0/standard3. Prior39356/37068 distinct compiler diagnostics retained.')],truth_boundary=boundary,conceptual_mirror_audit=mirror,useful_discoveries=[],active_cells=plan['active_cells'],reader_lesson=['website/content/declaration_lessons/'+plan['slugs'][0]+'.json'],integration_notes='One actual deterministic theorem for Proposition3.1 harmonic construction; genuine continuous/Borel flow, exact ODE/group/weightedSUM energy/pi endpoint. Gradient continuity is internally reused. No actual stochastic endpoint or fake consumer.')
for key in ['statement_seal','source_proof_coverage','proof_digestion','purification']:e[key]=[dict(declaration=plan['mathematical_declarations'][0],declaration_level=cell['declaration_level'],report=cell[key])]
adv.transition_advance(claim['advance_id'],'PROVED_LOCAL',worker_id=claim['created_by'],evidence=e)
cell['status']='proved_locally';cell['conceptual_mirror_audit']=mirror;cell['evidence'].update(proof_review=(r/'independent-math73/decision.json').as_posix(),source_review=(o/'source.0.decision.json').as_posix(),execution_boundary=boundary);write(cp,cell)
for p in [r/'proved-local.json',r/'root.source73.adoption.json']:assert not p.exists()
write(r/'proved-local.json',e);write(r/'root.source73.adoption.json',dict(status='ACCEPTED_INDEPENDENT_SOURCE73_ACTUAL_DETERMINISTIC_FLOW_ONLY',actual_root_PID=os.getpid(),native_owned_files=69,native_whole_logical_run_sha256=h,native_complete_named_RAW=pin(pp),native_lease=pin(lp),finite_current_input_maps=versions,coverage=cov['counts'],no_mathematical_repair=True,official_reviewer_packet_unchanged=True,publication_binding_unchanged=True,VERIFIED=False,full_paper=False,Goal_complete=False))
print('PASS73 PROVED_LOCAL once: CLOSED39 math/4strictblind/69source; exactSCI/integration/reader pending.')
