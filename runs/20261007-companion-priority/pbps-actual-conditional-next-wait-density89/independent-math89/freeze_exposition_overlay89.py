import copy, hashlib, json
from pathlib import Path
from datetime import datetime, timezone

R=Path('E:/Samplinglib')
O=R/'runs/20261007-companion-priority/pbps-actual-conditional-next-wait-density89/independent-math89'
def raw(p):
    b=p.read_bytes(); return {'path':p.relative_to(R).as_posix(),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def write(name,obj):
    p=O/name
    assert not p.exists(),p
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    return raw(p)
targets=[('website/content/declaration_lessons/pbps-actual-conditional-next-wait-density.json','lesson89.original.exactraw.json','562710b8e30deeefed6f776ecced00d3fffef15620e29e4b3792fdac460a87ab'),('website/content/publications/pbps-actual-conditional-next-wait-density.json','publication89.original.exactraw.json','7d96cf475f1300cf9e3d95eeacbc936741ec3316eb37ec61575cba3a92a9d66c'),('runs/20261007-companion-priority/pbps-actual-conditional-next-wait-density89/publication-freeze89.json','publication-freeze89.original.exactraw.json','b7671021869ac1de82a8a1cb5c91dfbda561361fbf33bfeed64d5424dffb9905')]
inputs=[]; snapshots=[]
for path,name,sha in targets:
    p=R/path; assert raw(p)['sha256']==sha,(p,raw(p))
    q=O/name; assert not q.exists(),q; q.write_bytes(p.read_bytes())
    inputs.append(raw(p)); snapshots.append(raw(q))
index=write('original-exposition-snapshot-index89.json',{'frozen_at':datetime.now(timezone.utc).isoformat(),'current_at_freeze':inputs,'immutable_original_snapshots':snapshots,'rule':'Original freezes refer to original bytes; after canonical successor changes, historical inputs resolve through these immutable snapshots.'})
lesson=json.loads((O/'lesson89.original.exactraw.json').read_text(encoding='utf-8'))
before=lesson['units'][0]['steps'][1]['formula']
expected=r'K_d(h,ds)=D_d(h,s)\,ds,\quad K_d(h,\mathbb R)\le1,\quad \nu_d(dh,ds)=\mu_n(dh)D_d(h,s)\,ds.'
after=r'K_d(h,ds)=D_d(h,s)\,ds,\quad \nu_d(dh,ds)=\mu_n(dh)D_d(h,s)\,ds.'
assert before==expected,repr(before)
original=(O/'lesson89.original.exactraw.json').read_bytes()
old=json.dumps(before,ensure_ascii=False).encode(); new=json.dumps(after,ensure_ascii=False).encode()
assert original.count(old)==1
proposed=original.replace(old,new,1)
p=O/'lesson89.proposed-sequencing-only.exactraw.json'; assert not p.exists();p.write_bytes(proposed)
check=json.loads(proposed); reference=copy.deepcopy(lesson);reference['units'][0]['steps'][1]['formula']=after
assert check==reference
overlay=write('proposed-exposition-overlay89.json',{'status':'PROPOSED_REQUIRES_DISTINCT_REVIEW_NOT_APPLIED','proposer_id':'/root/exact_verify77','target':inputs[0],'proposed_target':raw(p),'changes':[{'json_pointer':'/units/0/steps/1/formula','before':before,'after':after,'rationale':'The exact second BODY region (259-306) establishes density/kernel construction, while the uniform kernel mass bound is established only in the fourth BODY region (359-366). Remove the premature mass clause from this proof-step formula. The theorem-level publication conclusion retains the bound.'}],'unchanged':{'production_module_sha256':'36813b659cbdbb4b31c6300abd1300858d42afe683046b8c06ff9c22806e8e37','publication':inputs[1],'statement_seal_sha256':'d810e6949956099186936ccdcbaf270c0a3a6572913ce1430c682ef5ae5ab5a7','anonymous_statement_packet':'no modification authorized or performed'},'decoded_tex_check':'Both formulas contain actual single backslash characters. No escaping repair is proposed.'})
packet=write('exposition-repair-review-packet89.json',{'purpose':'Distinct independent exact one-field sequencing repair review only','inputs':[inputs[0],inputs[1],{'path':'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualConditionalNextWaitDensity.lean','sha256':'36813b659cbdbb4b31c6300abd1300858d42afe683046b8c06ff9c22806e8e37','bytes':24975},overlay,raw(p)],'original_snapshots':snapshots[:2],'scope':'Check decoded before/after field, exact-only delta, exact adjacent BODY regions and mathematical sequencing. Do not inherit or consult earlier acceptance/source verdicts. No canonical mutation, theorem repair or source verdict is included.','region_to_compare':{'step2':[259,306],'step4':[359,366]},'residual':'Proposed overlay has not been independently accepted by its proposer.'})
outputs=[*snapshots,index,raw(p),overlay,packet,raw(O/'freeze_exposition_overlay89.py')]
manifest=write('exposition-overlay89.closed-RAW-manifest.json',{'schema_version':1,'status':'CLOSED_PROPOSED_OVERLAY_NOT_APPLIED','frozen_inputs':inputs,'owned_artifacts':outputs,'noncircular':'Manifest excludes itself; no acceptance claim for own proposed repair.'})
print(json.dumps({'overlay':overlay,'review_packet':packet,'closed_manifest':manifest,'proposed_lesson':raw(p)},indent=2))
