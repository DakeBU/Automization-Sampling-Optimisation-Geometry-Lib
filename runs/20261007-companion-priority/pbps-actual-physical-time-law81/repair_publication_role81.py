from pathlib import Path
import json,sys,hashlib
sys.path.insert(0,str(Path.cwd()/'tools'));import astis_publication as pub
r=Path('runs/20261007-companion-priority/pbps-actual-physical-time-law81');old=r/'publication-admin-v1';old.mkdir(exist_ok=False)
load=lambda p:json.loads(p.read_bytes())
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
pp=Path('website/content/publications/pbps-ideal-half-turn-kernel.json');ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSIdealHalfTurnKernel.json');fp=r/'publication-freeze81.json'
for p in [pp,ap,fp]:(old/p.name).write_bytes(p.read_bytes())
publication=load(pp);item=publication['items'][0];assert item['bindings'][0]['role']=='integration-node';item['bindings'][0]['role']='proof-edge';save(pp,publication)
pub.inputs.cache_clear();pub.load.cache_clear();audit=load(ap);audit['publication_binding_sha256']=pub.binding_digest(item,item['bindings'][0],pub.inputs());audit['publication_context']=pub.review_context(item,item['bindings'][0],pub.inputs());save(ap,audit)
freeze=load(fp);freeze['publication_binding_sha256']=audit['publication_binding_sha256']
for x in freeze['inputs']:
 p=Path(x['path']);b=p.read_bytes();x.update(RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
save(fp,freeze)
save(r/'publication-role-diagnosis81.json',dict(classification='IMPLEMENTATION_FAILED',scope='Publication metadata only before any decoder/final source review',negative_gate='role must distinguish proof-edge from prerequisite',fix='Publication binding role proof-edge; substantive advance result_kind remains integration-node.',mathematics_changed=False,previous_native_files=old.as_posix()))
pub.check_advance([item['bindings'][0]['declaration']],reviewed=False)
packet=r/'anonymous.decoder81.json';target=Path('.astis/decoder-81/input/packet.json');target.parent.mkdir(parents=True,exist_ok=True);assert not target.exists();target.write_bytes(packet.read_bytes())
print('Draft publication check PASS; anonymous packet copied byte-for-byte for decoder')
