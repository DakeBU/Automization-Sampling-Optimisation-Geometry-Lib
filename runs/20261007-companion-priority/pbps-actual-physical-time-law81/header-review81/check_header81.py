from pathlib import Path
import hashlib,json,datetime,subprocess,os,re,importlib.util
R=Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-actual-physical-time-law81';S=R/'runs/20261007-companion-priority/pbps-physical-time-law-preread81';O=B/'header-review81';O.mkdir(parents=True,exist_ok=True)
H=B/'header81.proposed.lean'
def raw(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def save(n,v):
 with (O/n).open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
def txt(p):return p.read_text(encoding='utf-8')
assert raw(H)['RAW_sha256']=='c3d1ad6107ad0aa812a99461d7dc48720ba83709104f699a908a77a89bec1e76'
parent=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhysicalTimeMeasurability.lean'
paths=[H,B/'prospective-statement81.json',parent,R/'AutoSamplingTheory/TechnicalLemmas/Probability/GaussianConditionalKernel.lean',R/'AutoSamplingTheory/ExampleCases/ProximalBPS/GibbsAugmentation.lean',R/'AutoSamplingTheory/TechnicalLemmas/Analysis/HessianStrongConvexity.lean',R/'AutoSamplingTheory/TechnicalLemmas/Analysis/StrongConvexGibbsIntegrability.lean',R/'lean-toolchain',R/'lake-manifest.json']
paths+=list(S.glob('*.json'))
paths += [R/'.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Tilted.lean',R/'.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Prod.lean',R/'.lake/packages/mathlib/Mathlib/Probability/Kernel/Composition/Prod.lean']
save('input-freeze81.json',dict(reviewer='/root/exact_verify77',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),inputs=[raw(p) for p in paths],method='Prospective header/math and source-topology audit, not an independent blind decoder or final source reviewer. Source-only candidate graph was read first; pinned primary clauses independently reread after candidate/header.'))
def binders(t):
 start=t.index('    {E : Type*}');return t[start:t.index(' : Prop :=',start)]
assert binders(txt(H))==binders(txt(parent))
def defs(t,end):
 start=t.index('    let ');end=t.index(end,start);parts=re.split(r'(?=^    let )',t[start:end],flags=re.M)
 return {re.match(r'    let (\S+) ',v)[1]:v.rstrip() for v in parts if v}
dh=defs(txt(H),'    ∃ Z');dp=defs(txt(parent),'    ∃ Z');assert len(dh)==15 and len(dp)==11
assert all(dh[n]==dp[n] for n in dp)
h=txt(H);p=txt(parent)
old_conclusions=p[p.index('    ∃ Z'):p.index('\n\n',p.index('        Z y xRef z₀ 0 sample = z₀)'))].rstrip()
new_prefix=h[h.index('    ∃ Z'):h.index('      ∃ R')].rstrip()
assert new_prefix.endswith(' ∧');assert new_prefix[:-2]==old_conclusions
save('definition-readback81.json',dict(status='PASS',header=raw(H),original_six_binders_exact80=True,all_eleven_actual_lets_exact80=True,all_actual80_Z_conclusions_preserved=True,new_lets={n:dh[n] for n in ['q','γ','M','tπ']},product_readback='M_y=(q_y product stdGaussian_E) product P on ((reference,momentum),sample); initial phase=(fixed x,momentum); y and x remain fixed inputs, reference fixed during each run.',new_public_provider_premises=[],new_conclusions='Exact reference Markov kernel, joint returned-position Markov kernel, derived phase0 law and product-AE initialization plus actual live terminal arc at pi.'))
# Native independent primary clause readback; use the already-frozen stdlib parser
# as a text extractor only, and inspect resulting clauses independently.
spec=importlib.util.spec_from_file_location('primary81_extract',S/'primary_only81.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
ids=['S1.E1','S2.SS2.p1.1','S2.E8','alg1','alg1.l2','alg1.l4','alg1.l8','A1.SS1.p2.1','A1.SS1.p2.2','A1.SS2.p3.1','A1.SS2.p4.1']
regions=[]
for ident in ids:
 matches=[n for n in module.tree.elements if n.attrs.get('id')==ident];assert len(matches)==1,ident
 t=re.sub(r'\s+',' ',matches[0].text()).strip();regions.append(dict(id=ident,text=t,UTF8_sha256=hashlib.sha256(t.encode()).hexdigest()))
save('primary-clause-readback81.json',dict(source=raw(module.SRC),regions=regions,reading_order='Own primary readback follows source-only candidate/graph and header inspection; do not label this anti-anchored final source review.'))
snap=O/'header81.exact-snapshot.lean'
with snap.open('xb') as f:f.write(H.read_bytes())
cmd=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env',str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe'),str(snap)]
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf8');env.pop('ELAN_TOOLCHAIN',None)
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (O/'typecheck81.stdout.log').open('xb') as out,(O/'typecheck81.stderr.log').open('xb') as err:
 child=subprocess.Popen(cmd,cwd=R,env=env,stdout=out,stderr=err);print('Complete private header foreground PID',child.pid,flush=True);code=child.wait()
save('typecheck81.receipt.json',dict(status='PASS' if code==0 else 'FAIL',command_argv=cmd,cwd=str(R),actual_foreground_PID=child.pid,exit_code=code,terminal_closed=True,start_utc=start,end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),header=raw(H),exact_snapshot=raw(snap),repair_overlay=None,stdout=raw(O/'typecheck81.stdout.log'),stderr=raw(O/'typecheck81.stderr.log'),proof_BODY=False))
print('COMPLETE HEADER EXIT',code,flush=True)
raise SystemExit(code)
