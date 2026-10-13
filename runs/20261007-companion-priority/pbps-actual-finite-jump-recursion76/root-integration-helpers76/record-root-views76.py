from pathlib import Path
import hashlib,json,os
r=Path('runs/20261007-companion-priority/pbps-actual-finite-jump-recursion76')
rows=[]
for name in ['unit0-statement.png']+[f'unit0-proof-{n}.png' for n in range(1,11)]+['branch-actual-consumer.png']:
 p=Path('.astis/pbps-recursion76/visual76-cdp')/name
 rows.append(dict(path=p.resolve().as_posix(),RAW_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),actually_viewed_by_root=True))
p=Path('.astis/pbps-recursion76/visual76-copy/unit0-copy-and-download.png')
rows.append(dict(path=p.resolve().as_posix(),RAW_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),actually_viewed_by_root=True))
out=r/'root.viewed-captures76.json';assert not out.exists() and len(rows)==13
out.write_text(json.dumps(dict(viewed_by_root=True,actual_root_PID=os.getpid(),images=rows,
 observation='All thirteen actual PNG images were opened using view_image and inspected by root: attributed complete statement; ten displayed formula proofs with initially folded Lean; exact current declaration and flow/bounce/clock references in branch; copy/download page. Dense plain statement notation, horizontal equation scroll and graph labels are retained reader debt. Callback/download byte checks are separate machine evidence, not inferred from the screenshot.',
 full_Exposition_Seal=False,PURIFIED=False,live=False,Goal_complete=False),ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS76 root actual thirteen-image visual inspection recorded after views.')
