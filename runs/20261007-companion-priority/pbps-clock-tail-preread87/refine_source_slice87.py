from pathlib import Path
import json,hashlib
pre=Path(__file__).parent;p=pre/'source-slice87.json';d=json.loads(p.read_bytes())
d['predecessor_raw_sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
d['nodes'][-1]['claim']='Conditional next-wait survival for a past-measurable random integrated hazard threshold'
d['nodes'].append({'id':'S87-I5','claim':'Finite-wait density, final no-event survival, deterministic-depth iteration and fullA7 assembly','classification':'OPEN_NOT_CLOSED_BY_THIS_SAU','anchors':['A1.SS1.SSS0.Px1.p4/A1.E7']})
d['dependencies'].append({'from':'S87-I4','to':'S87-I5'})
d['reviewer_requested_identity_refinement']='Preserve independently frozen I4=conditional next-wait survival and I5=later distributional/iteration assembly; no mathematical or candidate header change.'
out=pre/'source-slice87.v2.json';assert not out.exists();out.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
print(hashlib.sha256(out.read_bytes()).hexdigest())
