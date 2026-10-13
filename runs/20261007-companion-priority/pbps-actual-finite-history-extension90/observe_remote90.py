from pathlib import Path
import subprocess,json,datetime,hashlib
r=Path(__file__).parent;out=r/'remote-ci90-science-observed';out.mkdir(exist_ok=False)
queries=[('prior89-final',['gh','run','view','38096679670','--json','status,conclusion,headSha,jobs']),('science90',['gh','run','list','--branch','codex/sphmc-standardized-rgo','--limit','12','--json','databaseId,headSha,status,conclusion,name,url'])]
records=[]
for label,argv in queries:
 q=subprocess.run(argv,capture_output=True)
 for suffix,b in [('native.json',q.stdout),('stderr.log',q.stderr)]:(out/(label+'.'+suffix)).write_bytes(b)
 assert q.returncode==0,q.stderr.decode(errors='replace')
 value=json.loads(q.stdout)
 if label=='prior89-final':
  assert value['headSha']=='d3bdf486a84f8edaac6930336879b87949fd113c' and value['conclusion']=='success'
  records.append(dict(label=label,status=value['status'],conclusion=value['conclusion'],head=value['headSha']))
 else:records.append(dict(label=label,current=[v for v in value if v['headSha']=='8f70c088b7c06f4a3048ff5966f4dda7903f0aa0']))
(out/'receipt.json').write_text(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),observations=records,prior89_not_transferred_to90=True,Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
print(json.dumps(records))
