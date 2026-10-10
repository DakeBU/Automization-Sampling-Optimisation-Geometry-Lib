from pathlib import Path
import subprocess,json,datetime,hashlib
r=Path(__file__).parent/'prior-ci-observation87';assert not r.exists();r.mkdir()
commit='ea5422f595d24b528cb84ad6fe24ea5097222a2c';argv=['gh','run','list','--commit',commit,'--limit','8','--json','databaseId,name,status,conclusion,headSha,url']
q=subprocess.run(argv,capture_output=True);(r/'stdout.log').write_bytes(q.stdout);(r/'stderr.log').write_bytes(q.stderr);assert q.returncode==0
rows=json.loads(q.stdout);assert all(x['headSha']==commit for x in rows)
(r/'receipt.json').write_text(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),argv=argv,exit_code=q.returncode,observations=rows,raw_stdout_sha256=hashlib.sha256(q.stdout).hexdigest(),scope='Prior86 CI repair exact pushed commit only; no credit for uncommitted87, main/merge/purification/wholepaper.'),indent=2)+'\n',encoding='utf8',newline='\n')
print(json.dumps(rows))
