from pathlib import Path
import json,hashlib,os
r=Path('runs/20261007-companion-priority/pbps-polar65');d=r/'exact-science-verification';load=lambda n:json.loads((d/n).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
lease,run,verdict=[load(n) for n in ['lease.final.json','run.json','verdict.json']]
assert lease['status']=='CLOSED_LAST' and lease['last_owned_write'] and lease['final_owned_file_count']==61
assert sha((d/'lease.final.json').read_bytes())=='37fff7e69a8da80afe88fd6d88997c2ca1a6f88cbc7baf458c64ab171f2df504'
assert sha(json.dumps({k:v for k,v in run.items() if k!='run_sha256'},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())==run['run_sha256']==lease['whole_logical_run_sha256']=='46cd394fd1736933f7b76fb6bf8edf433883d68d996f6c47bb32470a1f9aa276'
assert sha(Path(run['complete_named_RAW_verdict_payload']['path']).read_bytes())==lease['complete_named_RAW_verdict_sha256']=='d4cd38ea2a2ed16f15f1ab82c0e55752fb6429843d42f6adb01cf6dd9281b1e4'
listed={Path(x['path']).resolve() for x in lease['all_owned_except_this_final_lease']}|{(d/'lease.final.json').resolve()};assert listed=={p.resolve() for p in d.rglob('*') if p.is_file()}
for x in lease['all_owned_except_this_final_lease']:
 b=Path(x['path']).read_bytes();assert len(b)==x['raw_bytes'] and sha(b)==x['raw_sha256'] and sha(b.replace(b'\r\n',b'\n').replace(b'\r',b'\n'))==x['lf_sha256']
assert not lease['VERIFIED_append'] and not (r/'verified.json').exists()
out=r/'root.exact65-blocker.adoption.json';assert not out.exists()
out.write_text(json.dumps(dict(status='EXACT_SCI65_REQUIRED_FRONTIER_BLOCKER_ADOPTED',actual_root_pid=os.getpid(),checked_commit=lease['checked_commit'],native_owned_files=61,native_whole_logical_run_sha256=run['run_sha256'],native_complete_RAW_verdict_sha256=lease['complete_named_RAW_verdict_sha256'],blocker=verdict['blocker'],strict_reduction=verdict['strict_reduction'],VERIFIED=False,remaining='Correct exact process-only reuse_plan Samplinglib label and independently verify a new science commit; preserve all accepted math/source/native bytes.'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Adopted CLOSED61 exact SCI65 obstruction: mandatory frontier failure retained; no VERIFIED credit.')
