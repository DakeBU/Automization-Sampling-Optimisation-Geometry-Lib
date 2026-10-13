from pathlib import Path
import base64,copy,hashlib,json,os,sys
root=Path.cwd();sys.path.insert(0,str(root/'tools'))
import astis_publication as pub,astis_semantic_roundtrip as rt,astis_advance as adv
r=Path('runs/20261007-companion-priority/pbps-actual-projected-rotation70');o=r/'independent-source70';c=r/'independent-reader-helper-code70';s=r/'independent-source70-portable-admission'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest();can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def check(b,z):
 assert len(b)==z['RAW_bytes'] and sha(b)==z['RAW_sha256']
 assert sha(b.replace(b'\r\n',b'\n'))==z['LF_sha256']
 if 'LF_bytes' in z:assert len(b.replace(b'\r\n',b'\n'))==z['LF_bytes']
def lowcheck(z):
 b=Path(z['path']).read_bytes();lf=b.replace(b'\r\n',b'\n')
 assert (len(b),sha(b),len(lf),sha(lf))==(z['raw_bytes'],z['raw_sha256'],z['lf_bytes'],z['lf_sha256'])
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
def write(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def new(p,x):assert not Path(p).exists(),p;write(p,x)
# Independent two-script code review; original two V1 inputs have explicit finite maps.
cl=load(c/'lease.final.json');assert sha((c/'lease.final.json').read_bytes())=='7c06bef599446f7f9ce2b005a8a7e3551431c15cdc8d315758e1c96feb326d08'
assert cl['status']=='CLOSED_LAST' and cl['last_owned_write'] and not cl['postclose_writes_allowed']
assert cl['owned_file_count']==169 and sha(can(cl['manifest']))==cl['manifest_logical_sha256']
cf={p.resolve() for p in c.rglob('*') if p.is_file()};assert cf=={Path(z['path']).resolve() for z in cl['manifest']}|{(c/'lease.final.json').resolve()}
for z in cl['manifest']:
 lowcheck(z);assert Path(z['path']).stat().st_mtime_ns<=(c/'lease.final.json').stat().st_mtime_ns
cr=load(c/'run.json');ch=sha(can({k:v for k,v in cr.items() if k!='run_sha256'}))
assert ch==cr['run_sha256']==cl['whole_logical_run_sha256']=='ad54dbbdfbd5b2cda92f96bb028af610c24887aa8e9f99fd76f854888b39b4e7'
assert cr['complete_named_review']==load(c/'named-review.payload.json')
lowcheck(cr['named_complete_RAW_payload']);assert cr['named_complete_RAW_payload']['raw_sha256']=='0bd6ddddeb8e402b367aab76d6d5d8147f7f6da66f1606a7da9114ae60e98fb2'
cd=load(c/'decision.json');assert cd['accepted'] and not cd['full_browser_integration'] and not cd['SAU_VERIFIED']
for z in cd['checked_scripts']:lowcheck(z)
ci=load(c/'inputs.manifest.json');assert ci['input_count']==len(ci['inputs'])==29
for i,z in enumerate(ci['inputs']):
 for k in ['RAW_snapshot','LF_snapshot']:lowcheck(z[k])
 b=Path(z['RAW_snapshot']['path']).read_bytes();assert Path(z['LF_snapshot']['path']).read_bytes()==b.replace(b'\r\n',b'\n')
 assert len(b)==z['original']['raw_bytes'] and sha(b)==z['original']['raw_sha256']
 if i<2:
  assert z['review_phase']=='V1_historical'
  q=r/'reader-helper-contract70'/('inline_lean.py.V1.before-Prop-guard.exactraw.snapshot' if i==0 else 'check_cross_domain_browser.py.V1.before-open-panel-repair.exactraw.snapshot')
  assert b==q.read_bytes() and Path(z['original']['path']).resolve()==Path(cd['checked_scripts'][i]['path']).resolve()
 else:lowcheck(z['original'])
# Complete native source closure: every owned layer, complete named payload, all74 exact inputs.
lease=load(o/'lease.final.json');assert sha((o/'lease.final.json').read_bytes())=='d3974254b5a27965de598361a64dc52439441357a5f95a2a30863d7ac4b09779'
assert lease['status']=='CLOSED_LAST' and lease['last_owned_write']=='lease.final.json' and lease['no_further_owned_writes']
assert lease['owned_count']==319 and lease['bound_layer_count']==318
m=load(o/'owned-manifest.json');assert sha((o/'owned-manifest.json').read_bytes())==lease['native_manifest_RAW_sha256']
assert sha(can(m['files']))==m['entries_canonical_sha256']==lease['entries_canonical_sha256']
files={p.relative_to(o).as_posix():p for p in o.rglob('*') if p.is_file()}
assert len(files)==319 and set(files)=={z['path'] for z in lease['bindings']}|{'lease.final.json'}
assert set(files)=={z['path'] for z in m['files']}|{'owned-manifest.json','lease.final.json'}
for z in lease['bindings']:
 check(files[z['path']].read_bytes(),z);assert files[z['path']].stat().st_mtime_ns<=files['lease.final.json'].stat().st_mtime_ns
run=load(o/'source.0.review-run.json');h=sha(can({k:v for k,v in run.items() if k!='run_sha256'}))
assert h==run['run_sha256']==lease['whole_logical_run_sha256']=='828e2f967924bdd4f35941c540623bb202051850621276bda8f6e19e550f672b'
assert run['primary']['items']==419 and run['primary']['NODE']==175 and run['primary']['EXCLUDED']==244 and run['primary']['RAW_regions']==7
assert run['coverage']==dict(module_lines=544,module_NODE=521,module_EXCLUDED=23,source_obligations=24,semantic_slots=7,BODY_steps=8,BODY_lines=396,BODY_start=144,BODY_end=539,all_unclassified=0)
payload=load(o/'complete-named-review-decision-input-payload.json');assert sha((o/'complete-named-review-decision-input-payload.json').read_bytes())=='fd5143f227fdfc0cfd583a6eb72457b76981a293fc4ecb0018e052b61d0238d3'
assert payload['whole_logical_run_sha256']==h and payload['named_layer_count']==len(payload['named_layers'])==20
for z in payload['named_layers']:
 b=base64.b64decode(z['RAW_base64'],validate=True);check(b,z);assert (o/z['path']).read_bytes()==b
inputs=load(o/'complete-exact-RAW-LF-input-payload.json');assert inputs['input_count']==len(inputs['inputs'])==74
maps=[]
for i,z in enumerate(inputs['inputs']):
 b=base64.b64decode(z['RAW_base64'],validate=True);lf=base64.b64decode(z['LF_base64'],validate=True);check(b,z)
 assert (o/z['snapshot']).read_bytes()==b and (o/z['LF_snapshot']).read_bytes()==lf==b.replace(b'\r\n',b'\n')
 current=Path(z['original_path']).read_bytes()
 if current!=b:
  assert i in [21,26,28,31,32] and not z['assert_original_still_current_at_finalization']
  if i==21:assert current.count(b)==1
  elif i in [26,28]:
   q=r/'representation-metadata-repair70'/('1.before.exactraw.json' if i==26 else '0.before.exactraw.json');assert b==q.read_bytes()
   q=r/'representation-metadata-repair70'/('1.proposed.json' if i==26 else '0.proposed.json');assert current==q.read_bytes()
  else:
   j=i-31;assert b==Path(ci['inputs'][j]['RAW_snapshot']['path']).read_bytes();lowcheck(cd['checked_scripts'][j])
  maps.append(dict(index=i,original_path=z['original_path'],frozen_RAW_sha256=sha(b),current_RAW_sha256=sha(current),kind='exact-finite-source-fragment' if i==21 else 'independently-reviewed-two-field-metadata-overlay' if i in [26,28] else 'independently-reviewed-reader-code-version-map'))
assert [z['index'] for z in maps]==[21,26,28,31,32]
decision=load(o/'source.0.decision.json');assert sha((o/'source.0.decision.json').read_bytes())==lease['decision_RAW_sha256']=='35bbf2d2fdb493bc47719a24e03a103ba83c6a83406c62c812dca274ce1315b3'
assert decision['verdict']=='equivalent-after-elaboration' and decision['repairs']==[] and decision['independent_from_formalizer'] and decision['independent_from_decoder'] and decision['review_run_sha256']==h
assert len(decision['deltas'])==13 and all(z['severity']=='informational' for z in decision['deltas'])
assert set(decision['semantic_slots'])==set(rt.SEMANTIC_SLOTS) and all(z['relation']!='not-audited' and z['evidence'] for z in decision['semantic_slots'].values())
# Separately sealed5-locator portability supplement; mathematical admission fields unchanged.
sl=load(s/'lease.final.json');assert sha((s/'lease.final.json').read_bytes())=='f47ea29eb6048d8bd33ff2d9ec83285c96faec75ac9694be026364a84f30c811'
assert sl['status']=='CLOSED_LAST' and sl['owned_count']==14 and sl['no_further_owned_writes']
sm=load(s/'owned-manifest.json');assert sha((s/'owned-manifest.json').read_bytes())==sl['native_manifest_RAW_sha256'] and sha(can(sm['files']))==sl['entries_canonical_sha256']
sf={p.relative_to(s).as_posix():p for p in s.rglob('*') if p.is_file()};assert len(sf)==14 and set(sf)=={z['path'] for z in sl['bindings']}|{'lease.final.json'}
for z in sl['bindings']:check(sf[z['path']].read_bytes(),z);assert sf[z['path']].stat().st_mtime_ns<=sf['lease.final.json'].stat().st_mtime_ns
portable=load(s/'portable-admission-fields.proposed.json');assert sha((s/'portable-admission-fields.proposed.json').read_bytes())=='a403f152737024cb096381bfd30379c803d197f5cf7adc3e06823d58cc7eaaad'
approval=load(s/'portability-only.decision.json');assert approval['decision']=='APPROVE_EXACT_FIVE_LOCATOR_FIELDS_ONLY'
expected=load(o/'source.0.admission-fields.json');prefix=o.as_posix()+'/'
expected['audit_fields']['source_review']['evidence']=prefix+'source.0.review.complete-RAW.txt';expected['audit_fields']['source_review']['run_artifact']=prefix+'source.0.decision.json'
for key,name in [('source_graph','stageA.source-proof-graph70.frozen.json'),('source_inventory','stageB.primary419-current-exhaustive-decisions.json'),('coverage_report','stageB.all24-obligation-decisions.json')]:expected['publication_source_proof_coverage'][key]=prefix+name
assert portable==expected
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-PBPSActualProjectedRotation.json');audit=load(ap);assert audit['state']=='blind-reconstructed'
packet=load(r/'source-review.packet.1.json');assert rt.semantic_reviewer_packet(audit)==packet and packet['packet_sha256']==decision['reviewer_packet_sha256']==portable['official_packet_sha256']
accepted=copy.deepcopy(audit);accepted.update(portable['audit_fields']);assert rt.semantic_reviewer_packet(accepted)==packet
registry=rt.load_registry();registry['audits']=[accepted if x['id']==audit['id'] else x for x in registry['audits']];errors=rt.validate_registry(registry);assert not errors,errors
assert load(r/'root.math70.adoption.json')['native_files']==121 and load(r/'root.decoder70.adoption.json')['native_owned_files']==12
new(r/'root.reader-helper-code70.adoption.json',dict(status='ACCEPTED_BOUNDED_INDEPENDENT_READER_CODE_ONLY',native_files=169,input_rows=29,finite_V1_script_maps=[0,1],native_whole_logical_run_sha256=ch,native_lease=pin(c/'lease.final.json'),checked_scripts=cd['checked_scripts'],full_browser_integration=False,VERIFIED=False))
new(r/'root.source70.adoption.json',dict(status='ACCEPTED_INDEPENDENT_SOURCE70_ACTUAL_PROJECTED_ROTATION_ONLY',actual_root_PID=os.getpid(),native_owned_files=319,native_inputs=74,native_whole_logical_run_sha256=h,native_complete_named_RAW_sha256=lease['complete_named_payload']['RAW_sha256'],native_lease=pin(o/'lease.final.json'),portable_supplement_files=14,portable_supplement_lease=pin(s/'lease.final.json'),finite_current_input_maps=maps,source_items=419,source_NODE=175,source_EXCLUDED=244,whole_module_lines=544,BODY_steps=8,semantic_slots=7,informational_deltas=13,blocking_deltas=0,mathematical_repairs=[],VERIFIED=False,Goal_complete=False))
(r/'audit.before-source-admission.exactraw.json').write_bytes(ap.read_bytes());write(ap,accepted)
cp=Path('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-projected-rotation.json');pp=Path('website/content/publications/pbps-actual-projected-rotation.json')
(r/'cell.before-final-source-coverage.exactraw.json').write_bytes(cp.read_bytes());(r/'publication.before-final-source-coverage.exactraw.json').write_bytes(pp.read_bytes())
cell=load(cp);cell['source_proof_coverage']=portable['publication_source_proof_coverage'];write(cp,cell)
publication=load(pp);publication['items'][0]['source_proof_coverage']=portable['publication_source_proof_coverage'];write(pp,publication)
pub.inputs.cache_clear();pub.load.cache_clear();plan=load(r/'publication-plan.json');claim=load(r/'claim.json');pub.check_advance(plan['mathematical_declarations'],reviewed=True)
item=next(x for x in pub.load() if x['id']==plan['slugs'][0]);assert pub.binding_digest(item,item['bindings'][0],pub.inputs())==accepted['publication_binding_sha256'] and pub.review_context(item,item['bindings'][0],pub.inputs())==accepted['publication_context']
mirror=load(r/'conceptual-mirror-audit70.json');mirror={k:mirror[k] for k in ['status','discovery_ids','reason']}
boundary=claim['truth_boundary']+' Independent math121/blind12/source319 plus portable14 accepted:419 source items,544 lines,eight literal BODY steps,seven slots,13 informational deltas,zero mathematical repairs. Exact SCI70 and serialized aggregate/reader remain pending.'
e=dict(result_kind='theorem-edge',theorem_delta=claim['theorem_delta'],lean_declarations=plan['mathematical_declarations'],publication_declarations=plan['mathematical_declarations'],lean_files=claim['proposed_files'],focused_checks=[dict(command=claim['focused_checks'][0],result='Root9524 EXIT0/3949; independent fresh Lean42936 EXIT0; exactly propext,Classical.choice,Quot.sound. Retired inline-header/compiler API negatives retained.'),dict(command='Independent math,blind decoder,primary-first source/publication review',result='CLOSED121/12/319+portable14;419 source items,544lines,8literal BODY spans,7slots;13 informational nonblocking deltas;0 mathematical repairs.')],truth_boundary=boundary,conceptual_mirror_audit=mirror,useful_discoveries=[],active_cells=plan['active_cells'],reader_lesson=['website/content/declaration_lessons/'+s+'.json' for s in plan['slugs']],integration_notes='Same actual g,internally mean(g)=0,actual conditional gP and polar gV,correct-sign rotation and exact pair energy. Next B21 corrector/B4; no sharp-energy68 proof dependency. Sole stabilization lane. No main/cost/composition/fullExposition/PURIFIED/Goal claim.')
for key in ['statement_seal','source_proof_coverage','proof_digestion','purification']:e[key]=[dict(declaration=plan['mathematical_declarations'][0],declaration_level=cell['declaration_level'],report=cell[key])]
adv.transition_advance(claim['advance_id'],'PROVED_LOCAL',worker_id=claim['created_by'],evidence=e)
(r/'cell.before-proved.exactraw.json').write_bytes(cp.read_bytes());cell['status']='proved_locally';cell['conceptual_mirror_audit']=mirror;cell['evidence'].update(proof_review=(r/'independent-math70/named-review.payload.json').as_posix(),source_review=(o/'source.0.decision.json').as_posix(),execution_boundary=boundary);write(cp,cell)
new(r/'proved-local.json',e)
new(r/'source-admission-finite-current-maps70.json',dict(source_input_maps=maps,audit_before=pin(r/'audit.before-source-admission.exactraw.json'),audit_after=pin(ap),exact_review_admission_and_portable_coverage_fields_only=True,official_reviewer_packet_unchanged=True))
print('PASS70 PROVED_LOCAL: CLOSED121 math/12blind/319source+14portable;169 bounded reader-code review separate; actual original inputs/output rotation/energy only. Exact SCI70/aggregate/reader pending.')
