from pathlib import Path
import hashlib,json,os,subprocess,sys
o=Path('runs/20261007-companion-priority/pbps-recursive-path-preread76');r=o.parent/'pbps-actual-hazard-clock75';out=Path(os.environ['ASTIS_FOREGROUND_OBSERVER_DIR'])
sha=lambda b:hashlib.sha256(b).hexdigest();load=lambda p:json.loads(Path(p).read_bytes());can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
lp=o/'lease.final.json';assert sha(lp.read_bytes())=='14288a2c7d55cb70322f91f75ad8b43310e352bba162714afd684396a8b84de5';l=load(lp);assert l['state']=='CLOSED_LAST' and l['owner']=='/root/independent_primary69' and not l['postclose_owned_writes_allowed'] and l['last_owned_write']=='lease.final.json'
rows=l['all_owned_except_only_self'];assert len(rows)==l['member_count']==42 and l['total_owned_including_self']==43
assert {p.resolve() for p in o.rglob('*') if p.is_file()}=={Path(z['path']).resolve() for z in rows}|{lp.resolve()}
for z in rows:
 p=Path(z['path']);b=p.read_bytes();assert len(b)==z['RAW_bytes'] and sha(b)==z['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==z['LF_sha256'];assert p.stat().st_mtime_ns<=lp.stat().st_mtime_ns
run=load(o/'run.json');h=sha(can({k:v for k,v in run.items() if k!='run_sha256'}));assert h==run['run_sha256']==l['run_whole_logical_sha256']=='4a716e203b393a49b2484cc53af772a0d315b8c010aa994abc942e47c786d51c'
payload=load(l['named_complete_payload']['path']);assert sha(Path(l['named_complete_payload']['path']).read_bytes())=='d47af992f9f30305ea864391a7ac8fe51dae7dbce4f86af592d43986f184b7da' and len(payload['names'])==10
for z in payload['names']:assert z['RAW_utf8'].encode()==Path(z['path']).read_bytes()
with (out/'native-readonly.stdout.log').open('wb') as s,(out/'native-readonly.stderr.log').open('wb') as e:
 p=subprocess.Popen([sys.executable,'-B','-X','utf8',str(o/'postclose_readonly76.py')],stdout=s,stderr=e);code=p.wait()
assert code==0
d=load(o/'decision.json');assert d['verdict']=='SELECT_ACTUAL_FINITE_STOPPED_POSTJUMP_RECURSION_ONLY' and d['new_analytic_callers']==0 and d['no_compile_credit'] and d['no_source_header_acceptance']
q=r/'root.preread76.adoption.json';assert not q.exists();q.write_text(json.dumps(dict(status='ACCEPTED_SOURCE_ONLY_FUTURE_FINITE_STOPPED_RECURSION_PLAN',actual_root_PID=os.getpid(),native_run_sha256=h,native_lease=dict(path=lp.as_posix(),RAW_sha256=sha(lp.read_bytes())),native_files=43,finite_inputs=32,named_complete_entries=10,native_readonly_PID=p.pid,native_readonly_EXIT=code,selected_contract=(o/'selected.contract.json').as_posix(),source_counts=run['source_counts'],source_graph_counts=run['source_graph_counts'],obligations=12,future_route_steps=7,historical75_status='At source preread:75 sealed but unproved. Root currently has only an internally compiled primitive; full75 proof/reviews pending.',new_SAU=False,source_header_accepted=False,theorem_compiled=False,Goal_complete=False),ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS76 CLOSED43 future source plan adopted only; no SAU/header/proof credit.')
