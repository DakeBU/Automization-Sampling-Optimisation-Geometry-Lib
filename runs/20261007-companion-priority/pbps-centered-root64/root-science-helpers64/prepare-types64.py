from pathlib import Path
import hashlib, json

r = Path('runs/20261007-companion-priority/pbps-centered-root-preproof64')
assert json.loads((r / 'root.primary64.adoption.json').read_bytes())['parent63_native_verified_commit'] == '4d02622332d02d0bd6c977d3cee48fd535ebf203'
sha = lambda b: hashlib.sha256(b).hexdigest()
def write(p, text):
    assert not p.exists(), p
    p.write_text(text, encoding='utf-8', newline='\n')

h0 = '''theorem positive_square_order
    {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω)
    (A B : Lp ℝ 2 μ →L[ℝ] Lp ℝ 2 μ)
    (hA : A.IsPositive) (hB : B.IsPositive)
    (hSquareOrder : (B*B-A*A).IsPositive) :
    (B-A).IsPositive
'''
base = Path('AutoSamplingTheory/ExampleCases/ProximalBPS/MacroscopicDefectRoot.lean').read_text(encoding='utf-8')
h1 = base[base.index('theorem actual_unique_positive_macroscopic_defect_root'):base.index(':= by')]
h1 = h1.replace('actual_unique_positive_macroscopic_defect_root', 'actual_centered_root_order_inverse')
anchor = '''              (∀ f : HP, ‖B f‖ = ‖ΓP f‖ ∧
                ‖ΓP f‖^2 = ‖f‖^2-‖A f‖^2) ∧
              (∀ G : HP →L[ℝ] HP,
                G.IsPositive → G*G=(1 : HP →L[ℝ] HP)-A*A → G=ΓP)
'''
assert h1.count(anchor) == 1
tail = '''              ∃ q : Lp ℝ 2 ν,
                (q : E → ℝ) =ᵐ[ν] (fun _ => (1 : ℝ)) ∧ T q = q ∧
                (∀ u : Lp ℝ 2 ν, inner ℝ q u = ∫ y, u y ∂ν) ∧
                let qP : HP := e q
                let HP0 := (innerSL ℝ qP).ker
                let γ : ℝ := 2*Real.sqrt ((α : ℝ)*η)/(1+(α : ℝ)*η)
                (∀ f : HP, f ∈ HP0 ↔ (∫ y, (e.symm f) y ∂ν) = 0) ∧
                ΓP qP = 0 ∧ 0 < γ ∧
                ∃ ΓP0 : HP0 →L[ℝ] HP0,
                  (∀ f : HP0, (ΓP0 f : HP) = ΓP (f : HP)) ∧
                  ΓP0.IsPositive ∧ (ΓP0-γ • (1 : HP0 →L[ℝ] HP0)).IsPositive ∧
                  IsUnit ΓP0 ∧
                  ∃ Inv : HP0 →L[ℝ] HP0,
                    Inv*ΓP0=(1 : HP0 →L[ℝ] HP0) ∧
                    ΓP0*Inv=(1 : HP0 →L[ℝ] HP0) ∧ ‖Inv‖ ≤ 1/γ
'''
h1 = h1.replace(anchor, tail)
imports0 = '''import AutoSamplingTheory.TechnicalLemmas.Measure.L2RealComplexOperator
import Mathlib.Analysis.InnerProductSpace.StarOrder
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Instances
import Mathlib.Analysis.SpecialFunctions.ContinuousFunctionalCalculus.Rpow.Order
open MeasureTheory
open scoped ENNReal
set_option autoImplicit false
namespace AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareOrder
noncomputable section
'''
imports1 = '''import AutoSamplingTheory.ExampleCases.ProximalBPS.MacroscopicDefectRoot
import AutoSamplingTheory.ExampleCases.ProximalBPS.RoughMeanGradient
import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianMarginalPoincare
open MeasureTheory ProbabilityTheory
open scoped ContDiff NNReal ENNReal Topology
set_option autoImplicit false
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.CenteredRootOrderInverse
noncomputable section
'''
for i, (h, imports, ns) in enumerate([
    (h0, imports0, 'AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareOrder'),
    (h1, imports1, 'AutoSamplingTheory.ExampleCases.ProximalBPS.CenteredRootOrderInverse')]):
    write(r / ('header' + str(i) + '.lean'), h)
    write(r / ('type-only' + str(i) + '.lean'), imports + h +
          ':= by\n  exact noProof64_TYPE_ONLY_INTENTIONALLY_UNDEFINED\nend\nend ' + ns + '\n')
rows = []
for i in range(2):
    p = r / ('header' + str(i) + '.lean'); b = p.read_bytes()
    rows.append(dict(path=p.as_posix(), bytes=len(b), raw_sha256=sha(b), lf_sha256=sha(b)))
write(r / 'header-candidate64.json', json.dumps(dict(
    status='CANDIDATE64_TYPE_ONLY_NO_PROOF_NO_CLAIM_NO_STATEMENT_SEAL', headers=rows,
    exact_source='PBPS arXiv2609.06905v1 B15 centered positive-root operator order; B16 actual centered bounded inverse producer; D1/internal CFC background completion',
    sharp_C4_production_assembly_required=True,
    explicit_internal_adapters=['SAME literal conditional operator alignment',
        'Three canonical complex lifts/subtraction/order descent',
        'Full marginal constant projection and Gamma kills constant',
        'SAME macro GammaP centered restriction and internally proved bounded inverse'],
    no_extra_public_source_certificates=True, rank0_and_alphaeta1_retained=True,
    B16_polar_isometry_not_yet_asserted=True,
    inverse_only_centered=True, proof_search_started=False), ensure_ascii=False, indent=2) + '\n')
print('Prepared TWO exact named64 TYPE candidates; undefined proof body is intentional diagnostic only. No proof/search/claim/Statement Seal.')
