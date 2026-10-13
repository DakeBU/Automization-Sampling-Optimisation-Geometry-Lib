from pathlib import Path
import copy,hashlib,json,os
r=Path('runs/20261007-companion-priority/pbps-actual-projected-rotation70/representation-metadata-repair70');r.mkdir(exist_ok=False)
sha=lambda b:hashlib.sha256(b).hexdigest()
old='One actual production theorem planned; no private Prop/provider or wrapper Test.'
new='One public production theorem with an exact private literal statement definition; no proof provider or wrapper Test.'
rows=[]
for i,path in enumerate(['research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-projected-rotation.json','website/content/publications/pbps-actual-projected-rotation.json']):
 p=Path(path);before=p.read_bytes();a=json.loads(before);pointer='/purification/dead_code_audit' if i==0 else '/items/0/purification/dead_code_audit'
 z=a['purification'] if i==0 else a['items'][0]['purification'];assert z['dead_code_audit']==old;z['dead_code_audit']=new
 after=(json.dumps(a,ensure_ascii=False,indent=2)+'\n').encode()
 bp=r/f'{i}.before.exactraw.json';ap=r/f'{i}.proposed.json';bp.write_bytes(before);ap.write_bytes(after)
 rows.append(dict(path=path,JSON_pointer=pointer,before=bp.as_posix(),before_RAW_sha256=sha(before),proposed=ap.as_posix(),proposed_RAW_sha256=sha(after),old=old,new=new))
(r/'proposal.json').write_text(json.dumps(dict(kind='PROCESS_READER_METADATA_LITERAL_REPRESENTATION_CORRECTION',status='PROPOSED_NOT_APPLIED',actual_root_PID=os.getpid(),changes=rows,
 trigger='Independent whole-source reviewer identified stale no-private-Prop planning text after separately admitted literal representation.',
 mathematical_statement_or_BODY_changed=False,extra_public_hypothesis=False,source_fidelity_verdict=False,
 independent_repair_review_pending=True,source_packet_refresh_required_after_application=True),indent=2)+'\n',encoding='utf-8',newline='\n')
print('Two exact single-field metadata overlays prepared; canonical files and original official source packet unchanged.')
