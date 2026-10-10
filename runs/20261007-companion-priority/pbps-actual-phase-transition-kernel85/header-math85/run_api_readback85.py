from pathlib import Path
import datetime,hashlib,json,os,subprocess
R=Path('E:/Samplinglib');O=Path(__file__).parent
def info(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),RAW_sha256=hashlib.sha256(b).hexdigest(),RAW_bytes=len(b))
def save(n,d):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
src=O/'header85.local-checks.lean';dst=O/'header85.local-checks.actual-api.lean';old=src.read_text(encoding='utf8')
new=old.replace('#check ProbabilityTheory.Kernel.id_prod_apply\n','#check ProbabilityTheory.Kernel.id_prod_apply\'\n#check ProbabilityTheory.Kernel.prod_apply\n#check ProbabilityTheory.Kernel.IsMarkovKernel.map\n#check MeasureTheory.Measure.map_const\n')
assert old!=new;dst.write_text(new,encoding='utf8',newline='\n')
save('reviewer-api-name-diagnosis85.json',dict(status='REVIEWER_PROBE_API_NAME_ONLY',failed_source=info(src),failed_receipt=info(O/'complete-header-local-checks.receipt.json'),cause='Reviewer #check used nonexistent Kernel.id_prod_apply. Pinned Prod.lean provides id_prod_apply\' and prod_apply. Exact original candidate separately compiled EXIT0 before probe; candidate needs no repair.',corrected_full_header_copy=info(dst),original_candidate_modified=False,proof_search=False))
cmd=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env','lean',str(dst)];env=os.environ.copy();env['PYTHONUTF8']='1';env.pop('ELAN_TOOLCHAIN',None)
start=datetime.datetime.now(datetime.timezone.utc).isoformat();q=subprocess.run(cmd,cwd=R,env=env,capture_output=True)
for s in ['stdout','stderr']:(O/('complete-header-actual-api.'+s+'.log')).write_bytes(getattr(q,s))
save('complete-header-actual-api.receipt.json',dict(command=cmd,cwd=str(R),started_utc=start,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),exit_code=q.returncode,terminal_closed=True,foreground=True,stdout=info(O/'complete-header-actual-api.stdout.log'),stderr=info(O/'complete-header-actual-api.stderr.log')))
print('complete-header-actual-api',q.returncode)
