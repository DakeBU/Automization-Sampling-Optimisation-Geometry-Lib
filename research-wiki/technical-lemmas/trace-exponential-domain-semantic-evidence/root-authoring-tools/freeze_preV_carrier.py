from pathlib import Path
import json,hashlib,subprocess,os,gzip,io,sys
r=Path.cwd();w=r/'.astis/huanjian-gc-trace-mgf-domain-20261115'
e=r/'research-wiki/technical-lemmas/trace-exponential-domain-semantic-evidence'
sha=lambda b:hashlib.sha256(b).hexdigest()
def git(*xs):return subprocess.check_output(['git',*xs],cwd=r,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'})
assert git('rev-parse','HEAD').decode().strip()=='ef5cfe9feb38b716aa17595aedcaea81b18fb032'
assert not git('diff','--cached','--name-only').strip()
assert sha((e/'PROVED_LOCAL-evidence.full.json').read_bytes())=='a17ff70fa56a86070673d630943b43148f32f874f6f3f1243ddf6b73c2d889bf'
sys.path.insert(0,str(r));from tools import astis_advance as api
state=api.current_advances()['ASTIS-SA-20261115-TraceExponentialDomain']
assert state['state']=='PROVED_LOCAL' and state['latest_evidence']==json.loads((e/'PROVED_LOCAL-evidence.full.json').read_text())
baseline=json.loads((w/'preservation-baseline.private.json').read_text())
for name,h in baseline['all_existing_frontier_sha256'].items():assert sha((r/name).read_bytes())==h,name
for name in ['freeze_source_reviewed_metadata.py','record_proved_local_once.py','select_exact_reader_served_delta.py',
 'package_independent_reader77.py','package_reader_served40_and_finish_preV.py']:
    p=e/'root-authoring-tools'/name;assert not p.exists();p.write_bytes((w/name).read_bytes())
out=e/'root-preV-integration-actual-runs';out.mkdir()
rows=[]
runroot=r/'.astis/huanjian-resume-20261103'
for p in sorted(runroot.glob('20261115T1*-gc-trace-exp-*.receipt.json')):
    v=json.loads(p.read_text());log=Path(v['log']);assert sha(log.read_bytes())==v['log_sha256']
    (out/p.name).write_bytes(p.read_bytes());buf=io.BytesIO()
    with gzip.GzipFile(fileobj=buf,mode='wb',filename='',mtime=0) as gz:gz.write(log.read_bytes())
    q=out/(log.name+'.gz');q.write_bytes(buf.getvalue());assert sha(gzip.decompress(q.read_bytes()))==v['log_sha256']
    rows.append({'original_receipt':str(p.relative_to(r)),'public_receipt':str((out/p.name).relative_to(r)),
        'lossless_log':str(q.relative_to(r)),'decoded_log_sha256':v['log_sha256'],'actual_exit_code':v['exit_code'],
        'actual_HEAD_before':v['head_before'],'actual_HEAD_after':v['head_after']})
(out/'ROOT-later-receipt-log-custody.v1.json').write_text(json.dumps({'records':rows,
 'qualification':'Original actual process receipts/logs preserved exactly; no future source/public identity retroactively claimed tested or Lean-built.'},ensure_ascii=False,indent=2)+'\n')
allowed=['research-wiki/frontier-cells/ASTIS-SHARED-REAL-TRACE-EXPONENTIAL-DOMAIN.json',
 'research-wiki/technical-lemmas/trace-exponential-domain-semantic-evidence/','runs/substantive_advances.jsonl']
assert all(any(p==a or a.endswith('/') and p.startswith(a) for a in allowed) for p in git('diff','--name-only').decode().splitlines())
git('add','--',*allowed);staged=git('diff','--cached','--name-only').decode().splitlines()
assert all(any(p==a or a.endswith('/') and p.startswith(a) for a in allowed) for p in staged)
git('diff','--cached','--check')
git('commit','-m','Retain Gaussian trace-domain local admission and accepted isolated reader')
c=git('rev-parse','HEAD').decode().strip()
v={'commit':c,'parent':'ef5cfe9feb38b716aa17595aedcaea81b18fb032',
 'actual_normal_state':'PROVED_LOCAL','normal_PL_calls':1,'normal_V_calls':0,
 'original_PL24_sha256':'a17ff70fa56a86070673d630943b43148f32f874f6f3f1243ddf6b73c2d889bf',
 'source_binding':'e44190bca918ce5a1e8f4ff5fc942c56ea400deb7a10af9929a698ef22a9d45c',
 'reader':'Independent PASS_BOUNDED_ISOLATED_READER; required residual0;77+40 exact archives and207 served-byte resolver',
 'mathematics_actually_rebuilt_at':'30172847ec40c24426f0b39afc4887719810eca0',
 'qualification':'New focused metadata gates will actually run on this carrier next. OriginalPL24 retains actualef5c gates and historical reader pending state. No new Lean build or proofV claim.',
 'exact_owned_paths':staged}
p=w/'preV-carrier.v1.json';assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:x for k,x in v.items() if k!='exact_owned_paths'}))
