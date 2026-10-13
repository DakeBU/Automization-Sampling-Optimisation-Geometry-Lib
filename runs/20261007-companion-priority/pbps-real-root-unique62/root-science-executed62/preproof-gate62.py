from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
root=Path.cwd();label,command=sys.argv[1],sys.argv[2:];out=root/'runs/20261007-companion-priority/pbps-real-root-unique-preproof62'/label;out.mkdir(parents=True,exist_ok=False)
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.resolve().as_posix(),bytes=len(b),raw_sha256=hashlib.sha256(b).hexdigest(),lf_sha256=hashlib.sha256(b.replace(b'\r\n',b'\n')).hexdigest())
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();started=datetime.datetime.now(datetime.timezone.utc).isoformat();env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8',ASTIS_FOREGROUND_OBSERVER_DIR=out.resolve().as_posix());env.pop('ELAN_TOOLCHAIN',None)
math=['AutoSamplingTheory/TechnicalLemmas/Measure/L2RealComplexOperator.lean', 'AutoSamplingTheory/TechnicalLemmas/Measure/L2RealSquareRoot.lean', 'AutoSamplingTheory/ExampleCases/ProximalBPS/RealDefectRoot.lean', 'lean-toolchain', 'lake-manifest.json', 'runs\\20261007-companion-priority\\pbps-real-root-unique-preproof62\\header0.lean', 'runs\\20261007-companion-priority\\pbps-real-root-unique-preproof62\\header1.lean', 'runs\\20261007-companion-priority\\pbps-real-root-unique-preproof62\\elab0.lean', 'runs\\20261007-companion-priority\\pbps-real-root-unique-preproof62\\elab1.lean', 'runs\\20261007-companion-priority\\pbps-real-root-unique-preproof62\\statement-candidate.json'];inputs=[pin(root/p) for p in math if (root/p).is_file()]
snaps=out/'inputs';snaps.mkdir();input_snapshots=[]
for i,q in enumerate(inputs):
 b=Path(q['path']).read_bytes();rp=snaps/(str(i)+'.exactraw.snapshot');lp=snaps/(str(i)+'.LF.snapshot');rp.write_bytes(b);lp.write_bytes(b.replace(b'\r\n',b'\n'));input_snapshots.append(dict(original=q,exact_raw_snapshot=pin(rp),LF_snapshot=pin(lp)))

with (out/'stdout.log').open('wb') as o,(out/'stderr.log').open('wb') as e:
 child=subprocess.Popen(command,cwd=root,env=env,stdout=o,stderr=e);print(json.dumps(dict(label=label,actual_foreground_pid=child.pid,status="RUNNING_INPUTS_PINNED")),flush=True);code=child.wait()
x=dict(command=command,cwd=root.as_posix(),checked_science_parent=head,started_utc=started,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),actual_foreground_pid=child.pid,exit_code=code,terminal_closed=True,inputs=inputs,input_snapshots=input_snapshots,stdout=pin(out/'stdout.log'),stderr=pin(out/'stderr.log'),observer_dir_exclusion='Commit commands receive ASTIS_FOREGROUND_OBSERVER_DIR; the active directory must never be staged.',full_paper_completion=False)
(out/'receipt.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');print(json.dumps(dict(label=label,pid=child.pid,exit_code=code)))
lines=(out/'stdout.log').read_text(encoding='utf-8',errors='replace').splitlines()+(out/'stderr.log').read_text(encoding='utf-8',errors='replace').splitlines()
selected=[s for s in lines if any(t in s for t in ['error:','Build completed','PASS','FAIL','wrote:','checked'])];print('\n'.join(selected[-20:]))
if code:print('\n'.join(lines[-45:]))
sys.exit(code)
