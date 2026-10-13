from pathlib import Path
import json,hashlib,subprocess,os,sys,datetime
pre=Path(__file__).parent
old=Path('runs/20261007-companion-priority/pbps-normalized-endpoint-preread104/refresh_context104.py').read_text()
old=old.replace("prev=pre.parent/'pbps-actual-phase-normalization103'","prev=pre.parent/'pbps-actual-normalized-endpoint104'").replace('next-primary104','next-primary105').replace('integration103/postpush-binding103.json','integration104/postpush-binding104.json')
old=old.replace('context-before-fetch104','context-before-fetch105').replace('capsule104','capsule105').replace('fetch104','fetch105').replace('fetch-status104','fetch-status105')
exec(compile(old,str(__file__),'exec'))
s=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteCountPath.lean').read_text(encoding='utf8')
a=s.index('private def actual_finite_count_path_statement')
b=s.index('    ∃ Z :',a)
c=s.index('      (∀ n : ℕ, ∀ T : ℝ≥0,',b)
context=s[a:b].replace('private def actual_finite_count_path_statement','def candidate',1)
# Reuse exact actual recursion and literal prescribed path/density definitions.
text='''import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualNormalizedEndpointSector
import AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct

/- Prospective type-only statement. No proof, seal or claim yet. -/
namespace PBPSCountableEndpointCandidate105
open MeasureTheory InnerProductSpace ProbabilityTheory
open scoped ContDiff NNReal ENNReal Classical
noncomputable section
set_option autoImplicit false

'''+context+'''    let R : E × E → E × E := fun z => (z.1, -z.2)
    let Vy : E → E → ℝ := fun y x => V x + ‖x - y‖ ^ 2 / (2 * η)
    let nu : E → Measure (E × E) := fun y =>
      ((volume : Measure E).tilted (fun x => -Vy y x)).prod
        (ProbabilityTheory.stdGaussian E)
'''+s[b:c]+'''      (∀ y r : E, ∀ T : ℝ≥0,
        let B : (n : ℕ) → (E × E) × Prefix n T → (E × E) × (E × E) :=
          fun n q => (q.1, Γ y r q.1 n T q.2 ⟨T, le_rfl⟩)
        let sigma : (n : ℕ) → Measure ((E × E) × Prefix n T) := fun n =>
          ((nu y).prod (m n T)).withDensity (fun q => ρ y r q.1 n T q.2)
        let L : ℕ → Measure ((E × E) × (E × E)) := fun n => Measure.map (B n) (sigma n)
        let M : (E × E) × (ℕ → ℝ) → (E × E) × (E × E) :=
          fun q => (q.1, Z y r q.1 T q.2)
        let Q : Measure ((E × E) × (E × E)) := Measure.map M ((nu y).prod P)
        let J : (E × E) × (E × E) → (E × E) × (E × E) :=
          fun q => (R q.2, R q.1)
        Q = Measure.sum L ∧ IsProbabilityMeasure Q ∧ MeasurePreserving J Q Q)

#check candidate
end
end PBPSCountableEndpointCandidate105
'''
p=pre/'Header105.lean';assert not p.exists();p.write_text(text,encoding='utf8',newline='\n')
env=os.environ.copy();env['PATH']=str(Path('.astis/toolchain/lean-4.33.0-windows/bin').resolve())+os.pathsep+env['PATH'];env.pop('ELAN_TOOLCHAIN',None);env['LEAN_NUM_THREADS']='2';env['PYTHONUTF8']='1'
argv=[str(Path('.astis/toolchain/lean-4.33.0-windows/bin/lake.exe').resolve()),'env','lean',str(p)]
q=subprocess.run(argv,capture_output=True,env=env)
(pre/'header105.stdout.log').write_bytes(q.stdout);(pre/'header105.stderr.log').write_bytes(q.stderr)
(pre/'header105.receipt.json').write_text(json.dumps(dict(argv=argv,exit_code=q.returncode,terminal_closed=True,header_raw_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),scope='Type-only prospective header; no proof or seal'),indent=2)+'\n',encoding='utf8',newline='\n')
print('HEADER105_TYPECHECK',q.returncode,q.stdout.decode(errors='replace')[-3500:]);assert q.returncode==0
