from pathlib import Path
import os,sys,subprocess,json,hashlib,datetime,re
ROOT=Path('E:/Samplinglib');O=Path(__file__).resolve().parent
assert not (O/'lease.final.json').exists()
SCI='3da29415011a971a65f749502a625e416213f487';BASE='eb3d5ffbb6853f2a0aa4a8c66aefce19d8050176'
def ld(p):return json.loads(Path(p).read_bytes())
def pin(p):
 b=p.read_bytes();return {'path':p.as_posix(),'RAW_bytes':len(b),'RAW_sha256':hashlib.sha256(b).hexdigest(),'LF_sha256':hashlib.sha256(b.replace(b'\r\n',b'\n')).hexdigest()}
rows=[]
commands=[('publication-diff-private-inventory',[sys.executable,'-X','utf8','tools/astis_publication.py','check','--base',BASE]),('site-full-validator',[sys.executable,'-X','utf8','website/scripts/check_site.py'])]
owned=[z['path'] for z in ld(O.parent/'integration67/owned-before.json')['owned']]
commands.append(('authored-canonical-whitespace',['git','diff','--check',SCI,'--',*owned]))
for label,cmd in commands:
 d=O/'independent-gates'/label;d.mkdir(parents=True,exist_ok=True);a=d/'stdout.RAW.log';b=d/'stderr.RAW.log';start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with a.open('wb') as aa,b.open('wb') as bb:
  p=subprocess.Popen(cmd,cwd=ROOT,stdout=aa,stderr=bb);pid=p.pid;rc=p.wait()
 j={'schema':'repository67-actual-independent-readonly-gate-v1','actual_foreground_PID':pid,'actual_exit':rc,'command':cmd,'started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stdout':pin(a),'stderr':pin(b),'canonical_writes':False}
 (d/'receipt.json').write_bytes((json.dumps(j,sort_keys=True,indent=2)+'\n').encode());rows.append(j);print(json.dumps({'label':label,'actual_PID':pid,'actual_exit':rc}),flush=True);assert rc==0,(label,b.read_text(encoding='utf-8'))
registry=ROOT/'AutoSamplingTheory/TechnicalLemmas/Registry.lean';text=registry.read_text(encoding='utf-8');count=len(re.findall(r'localDecl\s*:=',text));assert count==514,count
for path,needle in [('AutoSamplingTheory/TechnicalLemmas.lean','import AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareCommute'),('AutoSamplingTheory/ExampleCases.lean','import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualRootCommutation'),('Tests.lean','import Tests.ProximalBPSActualRootCommutation')]:assert needle in (ROOT/path).read_text(encoding='utf-8')
j={'schema':'repository67-independent-readonly-gates-result-v1','actual_PID':os.getpid(),'status':'PASS','gates':rows,'Registry_count':count,'mandatory_compiler_gate_reused_by_exact_root_receipt':True,'no_proof_search_or_Lean_recompile':True,'authored_whitespace_PASS':True,'full_staged_whitespace_claim':False,'publication_diff_base':BASE,'canonical_Git_ledger_writes':False}
(O/'independent-gates67.result.json').write_bytes((json.dumps(j,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode());print(json.dumps({'actual_PID':os.getpid(),'status':'PASS','independent_gates':len(rows),'Registry':count}))
