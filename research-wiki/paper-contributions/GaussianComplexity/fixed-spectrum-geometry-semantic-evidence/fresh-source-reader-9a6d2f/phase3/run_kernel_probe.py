from pathlib import Path
import json,subprocess,os,hashlib
ROOT=Path('/Users/zhouhuanjian/ASTIS-GC');OUT=ROOT/'.astis/semantic-neutral-20261109/src_9a6d2f/phase3'
z=json.loads((OUT/'inputs/evidence__full-anti-anchored-reviewer-packet.json').read_text());public=z['lean']['statement']
test=(ROOT/'Tests/GaussianComplexityFixedSpectrumGeometry.lean').read_text();at=test.index('private theorem actual_first_order_oracle_measurable');chunk=test[at:].split(' := by',1)[0];body=chunk.split('(O : Matrix.orthogonalGroup (Fin d) ℝ) :\n',1)[1]
private='∀ {d : ℕ} (hd : 2 ≤ d) {κ : ℝ} (hκ : 2 ≤ κ) (O : Matrix.orthogonalGroup (Fin d) ℝ),\n'+body
probe='''import Tests.GaussianComplexityFixedSpectrumGeometry
import Lean
open Matrix InnerProductSpace Lean
open scoped ContDiff
set_option autoImplicit false
set_option pp.universes true

def ExpectedPublic : Prop :=
'''+public+'''
example : ExpectedPublic :=
  @AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGeometry.actual_potential_geometry

def ExpectedPrivate : Prop :=
'''+private+'''

run_cmd do
  let env := (← getEnv).setExporting false
  setEnv env
  let wanted := env.constants.toList.filter fun (n, _) =>
    n.toString == "AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGeometry.actual_potential_geometry" ||
    n.toString.endsWith ".actual_first_order_oracle_measurable"
  unless wanted.length == 2 do throwError "expected exactly two audited constants, found {wanted.length}"
  for (n, ci) in wanted do
    let some value := ci.value? true | throwError "missing kernel proof value for {n}"
    let used := value.getUsedConstants
    let astis := used.filter fun k => k.toString.startsWith "AutoSamplingTheory."
    logInfo m!"DIRECT_ASTIS {n}: {astis}"
    logInfo m!"DIRECT_ALL {n}: {used}"
    logInfo m!"ACTUAL_TYPE {n}: {ci.type}"
    let axs ← Lean.collectAxioms n
    logInfo m!"KERNEL_AXIOMS {n}: {axs}"
    if n.toString.endsWith ".actual_first_order_oracle_measurable" then
      Lean.Elab.Command.liftCoreM <| addDecl <| Declaration.thmDecl {
        name := Name.mkSimple "IndependentPrivateLiteralTypeCheck"
        levelParams := []
        type := mkConst (Name.mkSimple "ExpectedPrivate")
        value := mkConst n
      }
      logInfo "PRIVATE_LITERAL_KERNEL_TYPE_APPLICATION_PASS"

#print axioms IndependentPrivateLiteralTypeCheck
#print axioms AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGeometry.actual_potential_geometry
'''
p=OUT/'lean-evidence/KernelProbe.lean';p.write_text(probe)
env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1';env['LEAN_PATH']=json.loads((OUT/'lean-evidence/fresh-compilation.json').read_text())['LEAN_PATH']
bin='/Users/zhouhuanjian/.elan/toolchains/leanprover--lean4---v4.33.0/bin/lean';cmd=[bin,'-R',str(OUT/'lean-evidence'),'-o',str(OUT/'lean-evidence/KernelProbe.olean'),str(p)]
r=subprocess.run(cmd,cwd=ROOT,env=env,text=True,capture_output=True);(OUT/'lean-evidence/kernel-probe.log').write_text(r.stdout+r.stderr)
(OUT/'lean-evidence/kernel-probe-run.json').write_text(json.dumps({'command':cmd,'returncode':r.returncode,'probe_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'same_tree_LEAN_PATH':env['LEAN_PATH'],'sealed_public_statement_sha256':z['lean']['statement_sha256'],'private_literal_type_utf8_sha256':hashlib.sha256(private.encode()).hexdigest()},indent=2)+'\n')
print(r.stdout+r.stderr);raise SystemExit(r.returncode)
