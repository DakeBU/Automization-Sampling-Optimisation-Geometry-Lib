from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
out=Path(sys.argv[1]);cmd=sys.argv[2:]
assert out.resolve().is_relative_to(Path('runs/20261007-companion-priority').resolve())
out.mkdir(parents=True,exist_ok=False)
sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.resolve().as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
(out/'foreground-helper.exactraw.py').write_bytes(Path(__file__).read_bytes())
inputs=[pin(p) for p in ['lean-toolchain','lake-manifest.json','runs/20261007-companion-priority/pbps-iid-product-preproof77/header77.proposed.lean','runs/20261007-companion-priority/pbps-iid-product-preproof77/header77.v2.proposed.lean','AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean'] if Path(p).is_file()]
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();started=datetime.datetime.now(datetime.timezone.utc).isoformat()
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf8',PYTHONUNBUFFERED='1',ASTIS_FOREGROUND_OBSERVER_DIR=out.resolve().as_posix());env.pop('ELAN_TOOLCHAIN',None)
with (out/'stdout.log').open('wb') as s,(out/'stderr.log').open('wb') as e:
 p=subprocess.Popen(cmd,env=env,stdout=s,stderr=e);print(json.dumps(dict(label=out.as_posix(),actual_foreground_PID=p.pid,status='RUNNING')),flush=True);code=p.wait()
q=dict(command=cmd,checked_parent=head,started_utc=started,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),actual_foreground_PID=p.pid,exit_code=code,terminal_closed=True,inputs=inputs,stdout=pin(out/'stdout.log'),stderr=pin(out/'stderr.log'),Goal_complete=False)
(out/'receipt.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print(json.dumps(dict(label=out.as_posix(),PID=p.pid,EXIT=code)),flush=True)
lines=(out/'stdout.log').read_text(encoding='utf8',errors='replace').splitlines()+(out/'stderr.log').read_text(encoding='utf8',errors='replace').splitlines()
print('\n'.join(lines[-55:] if code else [s for s in lines if any(t in s for t in ['PASS','Build completed','axioms:'])][-15:]))
sys.exit(code)
