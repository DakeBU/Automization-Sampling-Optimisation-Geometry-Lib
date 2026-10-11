from pathlib import Path
import hashlib, json, re, subprocess, os, datetime

ROOT = Path('E:/Samplinglib')
OUT = ROOT / 'runs/20261007-companion-priority/pbps-prescribed-path-density-preread94/independent-header-math94'
HEADER = 'runs/20261007-companion-priority/pbps-prescribed-path-density-preread94/Header94.lean'
PROD = 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteCountPath.lean'
GRAPH = 'runs/20261007-companion-priority/pbps-actual-finite-count-path93/next-source-graph94/'
def sha(b): return hashlib.sha256(b).hexdigest()
def dump(name, value):
    p = OUT/name
    assert not p.exists(), str(p)
    p.write_bytes((json.dumps(value, ensure_ascii=False, indent=2)+'\n').encode('utf8'))
def info(p):
    b=p.read_bytes()
    return dict(path=p.relative_to(ROOT).as_posix(), raw_sha256=sha(b), bytes=len(b))
paths=[HEADER, PROD, 'lean-toolchain', 'lake-manifest.json',
       'runs/20261007-companion-priority/pbps-prescribed-path-density-preread94/draft-scope.json']
paths += [GRAPH+n for n in ['candidate-source-proof-graph94.native.json', 'candidate-source-coverage94.native.json', 'source-first-provenance94.native.json', 'closed-RAW-manifest94.native.json', 'artifact-checks94.native.json']]
inputs=[info(ROOT/p) for p in paths]
assert inputs[0]['raw_sha256']=='283fef6c66240aec21c4f34c72442d85e25db3f95dde1104a96cb3fe7d04e832'
assert inputs[1]['raw_sha256']=='5467078f497e0d40e1916550b2e5e9a5be992a69b20fc143bda06dd988d86d9d'
snap=OUT/'Header94.exactraw.lean'
assert snap.read_bytes() == (ROOT/HEADER).read_bytes()
h=(ROOT/HEADER).read_text(encoding='utf8')
p=(ROOT/PROD).read_text(encoding='utf8').split('private def actual_finite_count_path_statement',1)[1].split('\n    ∃ Z :',1)[0]
def lets(s):
    return {m.group(1):m.group(0).rstrip() for m in re.finditer(r'^    let ([^\s:]+)[\s\S]*?(?=^    let |^    ∀ y xRef|\Z)',s,re.M)}
hl,pl=lets(h.split('\n    ∀ y xRef',1)[0]),lets(p)
assert len(hl)==20
rows=[]
for name, literal in hl.items():
    assert name in pl and literal==pl[name], name
    rows.append(dict(name=name, identical_after_universal_newline_read=True, utf8_normalized_text_sha256=sha(literal.encode('utf8'))))
bind=lambda s:s[s.index('    {E : Type*}'):s.index('  classical')]
assert bind(h)==bind(p)
dump('literal-compatibility94.native.json',dict(status='PASS', comparison_recipe='Exact character equality after Python universal newline decoding; no whitespace trimming within a let; trailing separator whitespace excluded. Original byte hashes separately pinned.', analytic_binders_identical=True, shared_let_count=len(rows), shared_lets=rows, all_inputs=inputs))
env=os.environ.copy();env.pop('ELAN_TOOLCHAIN',None)
lake=str(ROOT/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe')
cmd=[lake,'env','lean',str(snap)]
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
proc=subprocess.run(cmd,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
(OUT/'header-elaboration.stdout.exactraw.log').write_bytes(proc.stdout)
(OUT/'header-elaboration.stderr.exactraw.log').write_bytes(proc.stderr)
dump('header-elaboration94.native.json',dict(kind='PROP_DEFINITION_ELABORATION_ONLY_NOT_PROOF',command=cmd,ELAN_TOOLCHAIN_removed=True,started_utc=start,ended_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),exit_code=proc.returncode,header_raw_sha256=sha(snap.read_bytes()),stdout=info(OUT/'header-elaboration.stdout.exactraw.log'),stderr=info(OUT/'header-elaboration.stderr.exactraw.log'),head_observed=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),mathlib_commit=subprocess.check_output(['git','-C','.lake/packages/mathlib','rev-parse','HEAD'],cwd=ROOT).decode().strip(),proof_claim=False))
assert proc.returncode==0,proc.stdout.decode('utf8',errors='replace')
print(json.dumps(dict(status='PASS',shared_lets=len(rows),header_sha256=inputs[0]['raw_sha256'],production_sha256=inputs[1]['raw_sha256'],header_elaboration_exit=proc.returncode)))
