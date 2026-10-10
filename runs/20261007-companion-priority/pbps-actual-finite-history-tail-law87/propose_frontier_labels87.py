"""Freeze exact control-plane producer-label correction after admission."""
from pathlib import Path
import json,hashlib,copy,sys
sys.path.insert(0,str(Path.cwd()/'tools'));import astis_advance as adv
r=Path(__file__).parent;load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
claim=load(r/'claim.json');assert adv.current_advances()[claim['advance_id']]['state']=='VERIFIED'
p=Path('research-wiki/frontier-cells')/(claim['frontier_cell']+'.json');raw=p.read_bytes();before=json.loads(raw);assert before['status']=='independently_verified'
after=copy.deepcopy(before);pub=load('website/content/publications/pbps-actual-finite-history-tail-law.json')['items'][0]
paths=[('shared_floor_audit','reason'),('reuse_plan','decision_reason'),('purification','duplicate_semantics_audit'),('purification','canonicalization')];changes=[]
for first,second in paths:
 old=before[first][second];assert '78' in old
 new=old.replace('actual78 recursion','actual76 recursion').replace('already78','already76');assert old!=new
 assert new in [pub['purification']['duplicate_semantics_audit'],pub['purification']['canonicalization']]
 after[first][second]=new;changes.append(dict(pointer='/'+first+'/'+second,before=old,after=new))
d=r/'frontier-label-repair87';d.mkdir(exist_ok=False)
original=d/'frontier87.original.exactraw.json';original.write_bytes(raw)
successor=d/'frontier87.proposed-successor.json';successor.write_text(json.dumps(after,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def pin(p):b=p.read_bytes();return dict(path=p.as_posix(),raw_sha256=sha(b),bytes=len(b))
proposal=dict(status='PROPOSED_CONTROL_METADATA_ONLY',proposer='/root',target=p.as_posix(),original=pin(original),proposed=pin(successor),changes=changes,required_changes=4,evidence='Copy exactly the two already independently accepted producer labels from current publication metadata into four stale frontier prose fields. Real declaration identities/parents and all source/Lean/reviewed publication payloads remain unchanged.',publication=dict(path='website/content/publications/pbps-actual-finite-history-tail-law.json',raw_sha256=sha(Path('website/content/publications/pbps-actual-finite-history-tail-law.json').read_bytes())),canonical_mutations=False)
(d/'proposal87.json').write_text(json.dumps(proposal,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n');print('Frontier four-label exact proposal SHA',sha((d/'proposal87.json').read_bytes()))
