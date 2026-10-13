from pathlib import Path
import copy,hashlib,json,sys
sys.path.insert(0,str(Path.cwd()/'tools'));import astis_publication as pub,astis_semantic_roundtrip as rt
r=Path(__file__).parent;d=r/'exposition-repair-review86';sha=lambda b:hashlib.sha256(b).hexdigest();load=lambda p:json.loads(Path(p).read_bytes())
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b))
def save(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def new(p,x):assert not Path(p).exists(),p;save(p,x)
mp=d/'exposition-repair.run-manifest86.json';dp=d/'exposition-repair.decision86.json';ep=d/'exposition-repair.run-evidence86.json'
assert pin(mp)['RAW_sha256']=='91d458ee737cfb0d5b3de224b139f6e92e11634bab74c9d3e2443bb8dc7a7984'
assert pin(dp)['RAW_sha256']=='1c92845f3ddda9c04839db2386cd0f9f9e7c2046b79ea008aea781c336485f60'
assert pin(ep)['RAW_sha256']=='db2052bf5d648f779da99978054790cf3fc0accf0094bea8715d3767b064b8c6'
m=load(mp);v=load(dp);assert m['status']=='closed' and v['verdict']=='ACCEPT_EXACT_THREE_FORMULA_EXPOSITION_OVERLAY_ONLY'
for group in ['raw_inputs','raw_outputs']:
 for x in m[group]:assert pin(x['path'])['RAW_sha256']==x['raw_sha256'],x
op=r/'independent-math86/proposed-exposition-overlay86.v2.json';assert pin(op)['RAW_sha256']==v['proposal_raw_sha256']=='89944d1cf3edd59938dea6acd1f1ca761e14d83f2f33487f59f24f640784f3b4'
overlay=load(op);assert len(overlay['changes'])==v['operations_reviewed']==3
lp=Path('website/content/declaration_lessons/pbps-actual-finite-first-event-law.json');pp=Path('website/content/publications/pbps-actual-finite-first-event-law.json')
original=load(lp);updated=copy.deepcopy(original)
for x,y in zip(overlay['changes'],v['per_operation']):
 assert x['path']==y['path'] and x['before']==y['exact_before'] and x['after']==y['exact_after'] and x['before']!=x['after']
 index=int(x['path'].split('steps[')[1].split(']')[0]);assert index in [5,7,8]
 assert updated['units'][0]['steps'][index]['formula']==x['before'];updated['units'][0]['steps'][index]['formula']=x['after']
assert updated['units'][0]['formula']==original['units'][0]['formula']
assert updated['units'][0]['formula'].startswith(chr(92)+'int') and not updated['units'][0]['formula'].startswith(chr(92)*2)
snap=r/'independent-math86/original-lesson86.exactraw.json';assert snap.read_bytes()==lp.read_bytes()
before_module=pin('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteFirstEventLaw.lean');before_pp=pin(pp)
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualFiniteFirstEventLaw.json');a=load(ap);assert a['state']=='draft'
(r/'audit.before-exposition-repair86.json').write_bytes(ap.read_bytes());old_packet=load(r/'anonymous.decoder86.json')
save(lp,updated);pub.inputs.cache_clear();pub.load.cache_clear();item=load(pp)['items'][0]
a['publication_binding_sha256']=pub.binding_digest(item,item['bindings'][0],pub.inputs());a['publication_context']=pub.review_context(item,item['bindings'][0],pub.inputs());save(ap,a)
assert rt.decoder_packet(a)==old_packet
assert before_module==pin(before_module['path']) and before_pp==pin(pp)
pub.check_advance([a['lean']['declaration']],reviewed=False)
adoption=dict(status='DISTINCT_EXACT_THREE_FORMULA_REPAIR_ADOPTED_ONLY',proposal=pin(op),native_decision=pin(dp),native_run_manifest=pin(mp),native_run_evidence=pin(ep),all_native_inputs_and_outputs_rehashed_before_mutation=True,original_lesson_snapshot=pin(snap),current_lesson=pin(lp),publication_unchanged=pin(pp),module_unchanged=before_module,changed_fields=[x['path'] for x in overlay['changes']],unit_formula_escape_unchanged=True,anonymous_decoder_packet_unchanged=True,new_publication_binding_sha256=a['publication_binding_sha256'],source_verdict=False,VERIFIED=False)
new(r/'root.exposition-repair86.adoption.json',adoption)
new(r/'publication-freeze86.successor.json',dict(status='SUCCESSOR_AFTER_DISTINCT_EXACT_THREE_FORMULA_REVIEW',supersedes_original_freeze=pin(r/'publication-freeze86.json'),original_lesson_snapshot=pin(snap),inputs=[pin(p) for p in [lp,pp,ap,'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-finite-first-event-law.json']],module=before_module,publication_binding_sha256=a['publication_binding_sha256'],reviewed_exact_overlay=pin(r/'root.exposition-repair86.adoption.json'),steps=11,VERIFIED=False,PROVED_LOCAL=False))
print('Applied only3 independently accepted sequence formulas; source/header/BODY and anonymous packet unchanged')
print('Successor freeze',pin(r/'publication-freeze86.successor.json'))
