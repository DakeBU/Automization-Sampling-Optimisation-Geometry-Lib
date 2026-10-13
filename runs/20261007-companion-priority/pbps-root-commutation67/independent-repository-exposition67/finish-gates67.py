from pathlib import Path
import os,sys,subprocess,json,hashlib,datetime,re
ROOT=Path('E:/Samplinglib');O=Path(__file__).resolve().parent
assert not (O/'lease.final.json').exists()
SCI='3da29415011a971a65f749502a625e416213f487';BASE='eb3d5ffbb6853f2a0aa4a8c66aefce19d8050176'
def ld(p):return json.loads(Path(p).read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();return {'path':p.as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_sha256':sha(b.replace(b'\r\n',b'\n'))}
def wr(p,j):p.write_bytes((json.dumps(j,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode())
rows=[]
for n in ['publication-diff-private-inventory','site-full-validator']:
 d=O/'independent-gates'/n;j=ld(d/'receipt.json');assert j['actual_exit']==0
 for k in ['stdout','stderr']:assert pin(Path(j[k]['path']))['RAW_sha256']==j[k]['RAW_sha256']
 rows.append(j)
plain=O/'independent-gates/authored-canonical-whitespace';p=ld(plain/'receipt.json');assert p['actual_exit']==2
findings=[]
for m in re.finditer(r'^(.+):(\d+): trailing whitespace\.$',(plain/'stdout.RAW.log').read_text(encoding='utf-8'),re.M):
 path,line=m.group(1),int(m.group(2));raw=(ROOT/path).read_bytes().splitlines(keepends=True)[line-1];payload=raw.removesuffix(b'\r\n')
 assert raw.endswith(b'\r\n') and payload.rstrip(b' \t')==payload
 findings.append({'path':path,'line':line,'exact_line_RAW_sha256':sha(raw),'line_end':'CRLF','trailing_space_or_tab_before_terminator':False})
assert findings
owned=[z['path'] for z in ld(O.parent/'integration67/owned-before.json')['owned']];cmd=['git','-c','core.whitespace=cr-at-eol','diff','--check',SCI,'--',*owned];d=O/'independent-gates/authored-canonical-whitespace-CRLF-aware';d.mkdir(exist_ok=True);a=d/'stdout.RAW.log';b=d/'stderr.RAW.log';start=datetime.datetime.now(datetime.timezone.utc).isoformat()
if (d/'receipt.json').exists():
 j=ld(d/'receipt.json');pid=j['actual_foreground_PID'];rc=j['actual_exit'];assert j['command']==cmd
 for k in ['stdout','stderr']:assert pin(Path(j[k]['path']))['RAW_sha256']==j[k]['RAW_sha256']
else:
 with a.open('wb') as aa,b.open('wb') as bb:
  q=subprocess.Popen(cmd,cwd=ROOT,stdout=aa,stderr=bb);pid=q.pid;rc=q.wait()
 j={'schema':'repository67-actual-independent-readonly-gate-v1','actual_foreground_PID':pid,'actual_exit':rc,'command':cmd,'started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stdout':pin(a),'stderr':pin(b),'canonical_writes':False};wr(d/'receipt.json',j)
assert rc==0;rows.append(j)
registry=ROOT/'AutoSamplingTheory/TechnicalLemmas/Registry.lean';count=len(re.findall(r'localDecl\s*:=\s*"([^"]+)"',registry.read_text(encoding='utf-8')));assert count==514
for path,needle in [('AutoSamplingTheory/TechnicalLemmas.lean','import AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareCommute'),('AutoSamplingTheory/ExampleCases.lean','import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualRootCommutation'),('Tests.lean','import Tests.ProximalBPSActualRootCommutation')]:assert needle in (ROOT/path).read_text(encoding='utf-8')
wr(O/'whitespace-exact-byte-diagnosis67.json',{'schema':'repository67-exact-added-line-CRLF-diagnosis-v1','actual_PID':os.getpid(),'plain_git_diff_check_actual_PID':p['actual_foreground_PID'],'plain_exit':2,'complete_findings':findings,'all_findings_only_CRLF_line_terminator':True,'new_trailing_space_or_tab_before_CRLF':0,'explicit_CRLF_aware_actual_PID':pid,'explicit_CRLF_aware_exit':0,'config_scope':'single git command -c; no git config/canonical file mutation','authored_complement_PASS':True,'full_staged_whitespace_claim':False,'prior_INT66_closed_whitespace_findings_not_changed':True})
wr(O/'independent-gates67.result.json',{'schema':'repository67-independent-readonly-gates-result-v1','actual_PID':os.getpid(),'status':'PASS_SCOPED_CRLF_AWARE','gates':rows,'Registry_count':count,'mandatory_compiler_gate_reused_by_exact_root_receipt':True,'no_proof_search_or_Lean_recompile':True,'authored_whitespace_PASS':True,'plain_default_CRLF_only_negative_retained':True,'full_staged_whitespace_claim':False,'publication_diff_base':BASE,'canonical_Git_ledger_writes':False})
print(json.dumps({'actual_PID':os.getpid(),'status':'PASS_SCOPED_CRLF_AWARE','independent_gates':len(rows),'CRLF_only_plain_findings':len(findings),'CRLF_aware_git_PID':pid,'actual_exit':rc,'Registry':count}))
