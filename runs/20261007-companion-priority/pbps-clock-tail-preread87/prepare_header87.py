from pathlib import Path
import hashlib,json,datetime,subprocess,os,sys
R=Path('E:/Samplinglib'); pre=Path(__file__).parent
r=pre.parent/'pbps-actual-finite-history-tail-law87';r.mkdir(exist_ok=True)
def pin(p):
 b=p.read_bytes();return {'path':str(p.relative_to(R)).replace('\\','/'),'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def new(p,x):
 assert not p.exists(),p
 p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
freeze=pre/'independent-source-first87/source-first.freeze.native.json'
manifest=pre/'independent-source-first87/primary-source.raw-manifest.native.json'
assert pin(freeze)['raw_sha256']=='d8e37422b5597b0a5761282bcf88b94453a7b21a5176ef0cb71c2363f5ab87d7'
assert pin(manifest)['raw_sha256']=='965e42dbbf61bcdc6eee394513c718d20136fa341db4ca547f783da827307071'
m=json.loads(manifest.read_bytes());source=Path(m['source']['local_path'])
assert pin(source)['raw_sha256']==m['source']['raw_sha256']
for a in m['anchors']:
 assert hashlib.sha256(source.read_bytes()[a['byte_start_zero_based']:a['byte_end_exclusive']]).hexdigest()==a['raw_span_sha256']
old=(R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteJumpRecursion.lean').read_text(encoding='utf-8')
decl=old.split('private def ',1)[1].split('    let eventTime',1)[0]
decl=decl.replace('actual_fixed_reference_finite_jump_recursion_statement','actual_finite_history_tail_law_statement',1)
before,after=decl.split('    let H :',1)
decl=before+'    let Λ :'+after.split('    let Λ :',1)[1]
header='''import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteJumpRecursion
import AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct

/-! Prospective header87. Source-implicit deterministic-depth probability bridge.
The actual stopped recursion is retained literally. History at depth n uses clocks
0,...,n-1; the unused raw real tail starts at n. No random-depth restart,
physical-time residual clock, conditional event density or full path law claim. -/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryTailLaw
open InnerProductSpace MeasureTheory ProbabilityTheory
open scoped ContDiff NNReal ENNReal Topology Interval
noncomputable section
set_option autoImplicit false

private def '''+decl+'''    let P : Measure (ℕ → ℝ) := Measure.infinitePi (fun _ : ℕ => expMeasure (1 : ℝ))
    let ε : (ℕ → ℝ) → ℕ → ℝ≥0 := fun ω k => Real.toNNReal (ω k)
    let history : E → E → (E × E) → (n : ℕ) → (ℕ → ℝ) →
        (Fin (n + 1) → ((ℝ≥0 × (E × E)) ⊕ Unit)) :=
      fun y xRef z₀ n ω j => record y xRef z₀ (ε ω) j.val
    let tail : ℕ → (ℕ → ℝ) → (ℕ → ℝ) := fun n ω k => ω (n + k)
    let past : ℕ → MeasurableSpace (ℕ → ℝ) := fun n =>
      ⨆ k ∈ Set.Iio n, MeasurableSpace.comap (fun ω : ℕ → ℝ => ω k) inferInstance
    ∀ y xRef : E, ∀ z₀ : E × E, ∀ n : ℕ,
      Measurable (history y xRef z₀ n) ∧ Measurable (tail n) ∧
      (∀ ω ω' : ℕ → ℝ, (∀ k < n, ω k = ω' k) →
        history y xRef z₀ n ω = history y xRef z₀ n ω') ∧
      Measurable[past n] (history y xRef z₀ n) ∧
      Measure.map (tail n) P = P ∧
      IndepFun (history y xRef z₀ n) (tail n) P ∧
      Measure.map (fun ω => (history y xRef z₀ n ω, tail n ω)) P =
        (Measure.map (history y xRef z₀ n) P).prod P ∧
      (∀ A : Set (Fin (n + 1) → ((ℝ≥0 × (E × E)) ⊕ Unit)), MeasurableSet A →
        Measure.map (tail n) (P.restrict (history y xRef z₀ n ⁻¹' A)) =
          (P (history y xRef z₀ n ⁻¹' A)) • P)

#check @actual_finite_history_tail_law_statement
end
end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryTailLaw
'''
p=r/'header87.proposed.lean';assert not p.exists();p.write_text(header,encoding='utf-8',newline='\n')
new(r/'header87.preparation.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'header':pin(p),'primary_first_freeze':pin(freeze),'primary_raw_manifest':pin(manifest),'all_primary_span_raw_hashes_reverified':True,'proof_BODY_exists':False,'production_Lean_changed':False,'scope':'Fixed deterministic event depth only. G86-11 independence substrate, not the conditional event-law iteration part. No Markovness/A7/invariance/complete-paper credit.'})
env=os.environ.copy();env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH'];env.pop('ELAN_TOOLCHAIN',None)
q=subprocess.run([str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env','lean',str(p)],cwd=R,env=env,capture_output=True)
(r/'header87.typecheck.stdout.log').write_bytes(q.stdout);(r/'header87.typecheck.stderr.log').write_bytes(q.stderr)
new(r/'header87.typecheck.receipt.json',{'exit_code':q.returncode,'terminal_closed':True,'header':pin(p)})
print(q.stdout.decode(errors='replace'));print(q.stderr.decode(errors='replace'));sys.exit(q.returncode)
