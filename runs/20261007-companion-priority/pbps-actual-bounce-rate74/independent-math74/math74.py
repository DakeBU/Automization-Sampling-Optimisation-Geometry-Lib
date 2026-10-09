from pathlib import Path
import ctypes, datetime, hashlib, json, os, re, subprocess, sys

ROOT=Path('E:/Samplinglib')
R=ROOT/'runs/20261007-companion-priority/pbps-actual-bounce-rate74'
PRE=ROOT/'runs/20261007-companion-priority/pbps-bounce-rate-preproof74'
OWN=R/'independent-math74'
PARENT='e91f9b3acfeea172c33053b28d88b7fea6e61e9d'
MODULE=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBounceRate.lean'
MODSHA='fcec688033797683b44f279a4d22971598926e6af3e9682ad76493d37580937c'
DECL='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBounceRate.actual_bounce_rate_energy_laws'
ACTOR='/root/header_math72'
PY=Path('C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe')
ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1')
sys.dont_write_bytecode=True
sha=lambda b:hashlib.sha256(b).hexdigest()
can=lambda j:json.dumps(j,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf8')
load=lambda p:json.loads(Path(p).read_bytes())

def pin(p):
 p=Path(p);b=p.read_bytes();lf=b.replace(b'\r\n',b'\n')
 return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_bytes=len(lf),LF_sha256=sha(lf))
def check(z):
 b=Path(z['path']).read_bytes();assert len(b)==z['RAW_bytes'] and sha(b)==z['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==z['LF_sha256'],z['path']
 return b
def save(n,j):
 assert not (OWN/'lease.final.json').exists()
 p=OWN/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((json.dumps(j,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode('utf8'))
def command(label,args,env=None):
 assert not (OWN/'lease.final.json').exists()
 d=OWN/'terminals';d.mkdir(parents=True,exist_ok=True);rp=d/(label+'.receipt.json');assert not rp.exists()
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 p=subprocess.Popen([str(x) for x in args],cwd=ROOT,env=env or ENV,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 print(json.dumps(dict(START=label,actual_foreground_PID=p.pid,driver_PID=os.getpid())),flush=True)
 out,err=p.communicate();(d/(label+'.stdout.RAW')).write_bytes(out);(d/(label+'.stderr.RAW')).write_bytes(err)
 rec=dict(label=label,actual_foreground_PID=p.pid,driver_PID=os.getpid(),command=[str(x) for x in args],terminal_EXIT=p.returncode,terminal_closed=True,started_UTC=start,finished_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),stdout=pin(d/(label+'.stdout.RAW')),stderr=pin(d/(label+'.stderr.RAW')))
 save('terminals/'+label+'.receipt.json',rec)
 print(json.dumps(dict(END=label,actual_foreground_PID=p.pid,terminal_EXIT=p.returncode)),flush=True)
 assert p.returncode==0,label+' failed; exact negative evidence retained'
 return out,rec
def prepare():
 assert not (OWN/'inputs.manifest.json').exists()
 frozen=load(R/'mathematics-freeze74.json')
 for z in frozen['inputs']:check(z)
 paths=[ROOT/'lean-toolchain',ROOT/'lake-manifest.json',MODULE,ROOT/'AutoSamplingTheory/TechnicalLemmas/Analysis/QuadraticRegularization.lean',PRE/'root.statement-seal74.json',R/'expanded74.frozen.header.lean',PRE/'header74.proposed.lean',PRE/'independent-header-math74/decision.json',ROOT/'.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Projection/Reflection.lean',ROOT/'.lake/packages/mathlib/Mathlib/MeasureTheory/Constructions/BorelSpace/Basic.lean',ROOT/'.lake/packages/mathlib/Mathlib/MeasureTheory/Group/Arithmetic.lean',R/'mathematics-freeze74.json',ROOT/'AutoSamplingTheory/TechnicalLemmas/Analysis/HessianStrongConvexity.lean']
 rows=[];(OWN/'inputs').mkdir(parents=True,exist_ok=True)
 for i,p in enumerate(paths):
  dest=OWN/'inputs'/f'{i:02d}.exactRAW.snapshot';dest.write_bytes(p.read_bytes());rows.append(dict(original=pin(p),snapshot=pin(dest)))
 assert pin(MODULE)['RAW_sha256']==MODSHA and len(MODULE.read_bytes())==10565
 out,rec=command('checked-parent',['git','rev-parse','HEAD']);assert out.decode().strip()==PARENT
 assert (ROOT/'lean-toolchain').read_bytes().replace(b'\r\n',b'\n')==b'leanprover/lean4:v4.33.0\n'
 assert next(x for x in load(ROOT/'lake-manifest.json')['packages'] if x['name']=='mathlib')['rev']=='db584cd6d46c92f209a44c0f1c829460d327499d'
 save('inputs.manifest.json',dict(input_count=len(rows),inputs=rows,checked_parent=PARENT,RAW_LF_recipe='Replace CRLF byte pairs with LF ONLY; preserve every other byte.',no_mutable_publication_cell_ledger_inputs=True,no_primary_source_or_decoder_verdict_read=True,combined_header_adoption_only_opaque_frozen_pin_checked_not_interpreted=True,actual_prepare_PID=os.getpid()))
 print(json.dumps(dict(status='PASS_PREPARE',inputs=len(rows),PID=os.getpid())),flush=True)
def compile():
 for z in load(OWN/'inputs.manifest.json')['inputs']:check(z['original']);check(z['snapshot'])
 out,_=command('fixed-lake-selected-env',['lake','env',PY,'-B','-X','utf8','-c',"import os,json;print(json.dumps({k:os.environ.get(k,'') for k in ['LEAN_PATH','LEAN_SRC_PATH']}))"])
 prefix,_=command('fixed-lean-prefix',['lake','env','lean','--print-prefix'])
 exe=Path(prefix.decode().strip())/'bin/lean.exe';env=dict(ENV,**json.loads(out))
 version,_=command('fixed-lean-version',[exe,'--version'],env);assert '4.33.0' in version.decode()
 output=OWN/'output/ActualBounceRate.olean';output.parent.mkdir(parents=True,exist_ok=True)
 _,rec=command('fresh-exact-whole-module',[exe,'-o',output,MODULE],env)
 # A separate audit-only driver re-elaborates all exact module bytes and prints the resulting declaration axioms.
 driver=OWN/'inputs/ActualBounceRate.axiom-audit.lean';raw=MODULE.read_bytes();suffix=('\n#print axioms '+DECL+'\n').encode('utf8');driver.write_bytes(raw+suffix)
 out,axrec=command('fresh-exact-source-standard-axioms',[exe,driver],env)
 m=re.search(r'depends on axioms:\s*\[([^]]*)\]',out.decode('utf8'),re.S)
 assert m and {x.strip() for x in m.group(1).split(',')}=={'propext','Classical.choice','Quot.sound'}
 assert sha(MODULE.read_bytes())==MODSHA
 save('fresh-compiler.json',dict(status='PASS',declaration=DECL,fresh_source_elaboration=True,Lake_build_cache_replay=False,terminal_EXIT=0,actual_foreground_Lean_PID=rec['actual_foreground_PID'],standard_axioms=['propext','Classical.choice','Quot.sound'],compiler_receipt=pin(OWN/'terminals/fresh-exact-whole-module.receipt.json'),output_olean=pin(output),canonical_olean_written=False,original_fixed_Lake_search_roots=True,LEAN_PATH=env['LEAN_PATH'],LEAN_SRC_PATH=env['LEAN_SRC_PATH'],real_Lean_executable=pin(exe),version_output=pin(OWN/'terminals/fixed-lean-version.stdout.RAW'),axiom_audit_receipt=pin(OWN/'terminals/fresh-exact-source-standard-axioms.receipt.json'),axiom_audit_PID=axrec['actual_foreground_PID'],axiom_audit_driver=pin(driver),axiom_driver_exact_module_prefix=True,axiom_driver_only_suffix=suffix.decode('utf8')))
 print(json.dumps(dict(status='PASS_FRESH_DIRECT_SOURCE',actual_foreground_Lean_PID=rec['actual_foreground_PID'],axiom_PID=axrec['actual_foreground_PID'],terminal_EXIT=0)),flush=True)
def audit():
 sys.path.insert(0,str(ROOT/'tools'));import astis
 source=MODULE.read_text(encoding='utf8');assert len(source.splitlines())==211
 proof_start=source.index(' := by')+6
 assert source[:proof_start]+'\n'==(PRE/'header74.proposed.lean').read_text(encoding='utf8')
 private=source[source.index('private def actual_bounce_rate_energy_statement'):source.index('\ntheorem actual_bounce_rate_energy_laws')]
 public=source[source.index('theorem actual_bounce_rate_energy_laws'):proof_start]
 callers=re.findall(r'\((h(?:αβ|α|V|H|βη|η))\s*:',private)
 assert callers==re.findall(r'\((h(?:αβ|α|V|H|βη|η))\s*:',public)==['hα','hαβ','hV','hH','hη','hβη']
 expanded=(R/'expanded74.frozen.header.lean').read_text(encoding='utf8')
 assert expanded[expanded.index('    let c :'):].strip()==private.split(': Prop :=',1)[1].strip()
 cleaned=astis.strip_lean_comments_and_strings(source)
 hits=[dict(line=i,text=s) for i,s in enumerate(cleaned.splitlines(),1) if astis.FORBIDDEN_REGEX.search(s)]
 assert not hits and len(re.findall(r'^theorem ',cleaned,re.M))==1 and len(re.findall(r'^private def ',cleaned,re.M))==1
 assert 'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHarmonicFlow' not in source
 save('literal-and-fake-closure-audit.json',dict(status='PASS',actual_audit_PID=os.getpid(),module_lines=211,private_public_callers=callers,header_exact_preserved=True,expanded_private_literal_exact=True,public_theorems=1,private_literal_specs=1,fake_closure_hits=hits,source_review=False,no_actual73_formal_parent=True))
 print(json.dumps(dict(status='PASS_LITERAL_FAKE_CLOSURE',PID=os.getpid(),fake_closures=0)),flush=True)
def readonly():
 lease=load(OWN/'lease.final.json');assert lease['status']=='CLOSED_LAST' and lease['reviewer']==ACTOR and not lease['VERIFIED']
 check(lease['manifest']);m=load(OWN/'native.manifest.json');rows=m['entries']
 assert len(rows)==m['entry_count'] and len(rows)+2==lease['owned_files'] and sha(can(rows))==m['logical_entries_sha256']
 assert {p.resolve() for p in OWN.rglob('*') if p.is_file()}=={Path(z['path']).resolve() for z in rows}|{(OWN/'native.manifest.json').resolve(),(OWN/'lease.final.json').resolve()}
 for z in rows:check(z);assert Path(z['path']).stat().st_mtime_ns<=(OWN/'lease.final.json').stat().st_mtime_ns
 run=load(OWN/'run.json');assert sha(can({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']==lease['run_sha256']
 assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==run['checked_parent']==PARENT
 assert run['status']=='ACCEPTED_MATHEMATICS_ONLY' and not run['source_review'] and not run['VERIFIED']
 payload=load(run['complete_named']['path']);check(run['complete_named'])
 assert payload['decision']==run['decision'] and payload['full_exact_module_UTF8']==check(run['candidate_module']).decode() and payload['input_manifest']==run['input_manifest']
 for z in run['input_manifest']['inputs']:assert check(z['original'])==check(z['snapshot'])
 c=run['fresh_compiler'];assert c['fresh_source_elaboration'] and not c['Lake_build_cache_replay'] and c['terminal_EXIT']==0
 assert set(c['standard_axioms'])=={'propext','Classical.choice','Quot.sound'}
 check(c['compiler_receipt']);check(c['output_olean']);check(c['axiom_audit_receipt'])
 kernel=ctypes.WinDLL('kernel32',use_last_error=True);kernel.OpenProcess.restype=ctypes.c_void_p
 handle=kernel.OpenProcess(0x00100000,False,lease['writer_PID'])
 if handle:
  kernel.WaitForSingleObject.argtypes=[ctypes.c_void_p,ctypes.c_ulong];kernel.CloseHandle.argtypes=[ctypes.c_void_p]
  assert kernel.WaitForSingleObject(handle,0)==0;kernel.CloseHandle(handle)
 else:assert ctypes.get_last_error()==87
 print(json.dumps(dict(status='PASS',actual_external_readonly_PID=os.getpid(),writer_PID=lease['writer_PID'],writer_terminated=True,owned_files=lease['owned_files'],input_count=run['input_manifest']['input_count'],run_sha256=run['run_sha256'],no_owned_writes=True,source_review=False,VERIFIED=False,terminal_EXIT_contract=0),ensure_ascii=False))
if __name__=='__main__':
 assert len(sys.argv)==2
 {'prepare':prepare,'compile':compile,'audit':audit,'readonly':readonly}[sys.argv[1]]()
