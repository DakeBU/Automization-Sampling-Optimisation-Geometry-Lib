from pathlib import Path
import json,hashlib,copy,sys
sys.path.insert(0,str(Path('tools').resolve()))
import astis_publication as pub,astis_semantic_roundtrip as rt,astis_advance as adv
r=Path('runs/20261007-companion-priority/pbps-real-root-unique62');n=r/'source-review62';load=lambda p:json.loads(Path(p).read_text(encoding='utf-8'));sha=lambda a:hashlib.sha256(a).hexdigest();can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def w(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
s=load(n/'run.json');l=load(n/'lease.json');assert l['status']=='CLOSED' and l['closed_last'] and l['actual_foreground_readback_exit_codes']==[0,0]
assert sha(can({k:v for k,v in s.items() if k!='run_sha256'}))==s['run_sha256']==l['run_sha256']=='212849f5c4513ce50c33232f1636f23627dda7cd274e88215b284e27383c38e9';assert sha((n/'named-source-review.payload.json').read_bytes())==s['named_source_payload_sha256']==l['named_source_payload_sha256']=='de3b4779c886e4e5f75e11fc6547ffc6b9b5333620c4ea8af286988a89abb61b'
seen=set()
def walk(x):
 if isinstance(x,dict):
  if 'path' in x and 'raw_sha256' in x:
   key=(x['path'],x['raw_sha256'],x.get('lf_sha256'))
   if key not in seen:
    p=Path(x['path']);a=p.read_bytes();z=a.replace(b'\r\n',b'\n');assert sha(a)==x['raw_sha256'],str(p)
    if 'lf_sha256' in x:assert sha(z)==x['lf_sha256'],str(p)
    for k,v in [('bytes',len(a)),('raw_bytes',len(a)),('lf_bytes',len(z))]:
     if k in x:assert x[k]==v,str(p)
    seen.add(key)
  for v in x.values():walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
for p in n.rglob('*.json'):walk(load(p))
assert load(r/'root.math62.adoption.json')['status']=='INDEPENDENT_PRECOMMIT_SCOPED_MATHEMATICS62_ACCEPTED';assert load(r/'root.decoder62.adoption.json')['status']=='ACTUAL_CLOSED_ANONYMOUS_DECODER_ADOPTED'
plan=load(r/'publication-plan.json');claim=load(r/'claim.json');accepted=[];adapters=[]
for i,(aid,slug) in enumerate(zip(plan['audit_ids'],plan['slugs'])):
 p=Path('research-wiki/semantic-roundtrip/audits')/(aid+'.json');a=load(p);q=load(n/f'source.{i}.review.json');assert a['state']=='blind-reconstructed';assert q['verdict']=='equivalent-after-elaboration' and len(q['semantic_slots'])==7 and not q['repairs'];assert all(not d['blocking'] for d in q['deltas']);assert q['independent_from_formalizer'] and q['independent_from_decoder'] and q['review_run_sha256']==s['run_sha256'];assert rt.semantic_reviewer_packet(a)['packet_sha256']==q['reviewer_packet_sha256'];assert q['publication_exposition_verdict']=='accepted-scoped-source-content; native rendered/copy/full-exposition seal separate'
 pub.inputs.cache_clear();pub.load.cache_clear();data=pub.inputs();item=next(x for x in pub.load() if x['id']==slug);assert pub.binding_digest(item,item['bindings'][0],data)==a['publication_binding_sha256']==q['publication_binding_sha256']
 ds=[dict(slot=d['slot'],severity='informational',description=d['description'],evidence='Independent native '+d['classification']+' nonblocking classification retained in '+(n/f'source.{i}.review.json').as_posix()) for d in q['deltas']]
 slots=copy.deepcopy(q['semantic_slots']); slot_adapters=[]
 for slot,fields in slots.items():
  for field,value in list(fields.items()):
   if isinstance(value,list):
    assert all(isinstance(v,str) and v for v in value);fields[field]='\n'.join(value);slot_adapters.append(dict(slot=slot,field=field,native=value,canonical=fields[field],recipe='Join every native string item with LF; retain order and full text; native verdict unchanged.'))
 b=copy.deepcopy(a);b.update(state='accepted',semantic_slots=slots,deltas=ds,verdict=q['verdict'],repairs=[]);b['source_review']=dict(state='accepted',reviewer=q['reviewer'],independent_from_formalizer=True,independent_from_decoder=True,evidence=q['review_evidence'],review_run_sha256=q['review_run_sha256'],reviewer_packet_sha256=q['reviewer_packet_sha256'],run_artifact=(n/f'source.{i}.review.json').as_posix());accepted.append((p,b));adapters.append(dict(native=(n/f'source.{i}.review.json').as_posix(),native_deltas=q['deltas'],canonical_deltas=ds,canonical_slot_format_adapters=slot_adapters))
registry=rt.load_registry();updates={a['id']:a for p,a in accepted};registry['audits']=[updates.get(a['id'],a) for a in registry['audits']];errors=rt.validate_registry(registry);assert not errors,errors
assert not (r/'proved-local.json').exists()
w(r/'root.source62.adoption.json',dict(status='BOTH_INDEPENDENT_SCOPED_SOURCE_AND_CURRENT_FORMULA_PROOFS_ACCEPTED',run_sha256=s['run_sha256'],named_source_review_payload_sha256=s['named_source_payload_sha256'],named_payload_hash_recipe='Raw complete named-source-review.payload.json hash, independently declared; not canonical JSON hash or whole native run.',qualified_unique_pin_readbacks=len(seen),canonical_delta_adapters=adapters,native_mutable_input_snapshots=(n/'input.manifest.json').as_posix(),earlier_negative_artifacts_unchanged=True,remaining_boundary=plan['remaining_boundary'],VERIFIED=False))
for i,(p,a) in enumerate(accepted):(r/f'audit.{i}.before-source-admission.raw.snapshot.json').write_bytes(p.read_bytes());w(p,a)
pub.inputs.cache_clear();pub.load.cache_clear();pub.check_advance(plan['mathematical_declarations'],reviewed=True)
mirror=load(r/'conceptual-mirror-audit.json');mirror={k:mirror[k] for k in ['status','discovery_ids','reason']};boundary=plan['remaining_boundary']+' Complete independent precommit mathematics, anonymous source/identity-blind decoder, anti-anchored primary-first source and current formula proofs accepted; exact-science verification and serialized integration pending.'
e=dict(result_kind='reusable-interface',theorem_delta=claim['theorem_delta'],lean_declarations=plan['mathematical_declarations'],publication_declarations=plan['mathematical_declarations'],lean_files=claim['proposed_files'],focused_checks=[dict(command='lake build Tests.ProximalBPSRealDefectRootUnique',result='Root actual520 EXIT0 PASS3918 and independent3700 EXIT0 PASS3918; two unchanged sealed headers, zero private providers, both standard3; genuine original-input ALL positive alternative-root Test passed.'),dict(command='Independent primary-first anti-anchored source/current exposition review',result='Two current seven-slot source decisions; blocking/repair counts checked directly; primary source plus exact cap, seven authored mathematical steps, source proof graph separate from Lean route.')],truth_boundary=boundary,conceptual_mirror_audit=mirror,useful_discoveries=[],active_cells=plan['active_cells'],reader_lesson=['website/content/declaration_lessons/'+x+'.json' for x in plan['slugs']],integration_notes='Generic canonical complex lifts transport equal squares; internal complex positive-square uniqueness plus real embedding injectivity gives positive real uniqueness on arbitrary-measure L2. Actual61 original-input SAME S/T/D/root receives uniqueness against ALL positive same-square alternatives, outside the observable quantifier and without alternative energy. Zero private providers. Printed joint GammaP/ontoM/typed B*B, centered order/inverse/polar/H1/dynamics/main/error/cost/composition remain separate. Existing sole PhaseKernel stabilization lane; no new lane.')
cells=[load(Path('research-wiki/frontier-cells')/(cid+'.json')) for cid in plan['active_cells']]
for k in ['statement_seal','source_proof_coverage','proof_digestion','purification']:e[k]=[dict(declaration=plan['mathematical_declarations'][i],declaration_level=x['declaration_level'],report=x[k]) for i,x in enumerate(cells)]
adv.transition_advance(claim['advance_id'],'PROVED_LOCAL',worker_id=claim['created_by'],evidence=e)
for i,(cid,x) in enumerate(zip(plan['active_cells'],cells)):
 p=Path('research-wiki/frontier-cells')/(cid+'.json');assert x['status']=='claimed';(r/f'cell.{i}.before-proved.raw.snapshot.json').write_bytes(p.read_bytes());x['status']='proved_locally';x['conceptual_mirror_audit']=mirror;x['evidence'].update(proof_review=(r/'independent-math62/native.receipt.json').as_posix(),source_review=[v['native'] for v in adapters],execution_boundary=boundary);w(p,x)
w(r/'proved-local.json',e)
print('62 PROVED_LOCAL after reviewed publication admission; two independent source/math/decoder-reviewed positive REAL root uniqueness declarations. Exact-science VERIFIED/integration pending.')
