"""Unclaimed next-boundary statement formation only, never a theorem/proof or intake."""
from pathlib import Path
import hashlib
import json
import subprocess
from bs4 import BeautifulSoup
W = Path(__file__).resolve().parent.relative_to(Path.cwd())
source = Path('.astis/huanjian-resume-20261103/2610.20492v1.html')
sha = lambda raw:hashlib.sha256(raw).hexdigest()
assert sha(source.read_bytes()) == '6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915'
raw = source.read_bytes()
soup = BeautifulSoup(raw,'html.parser')
paragraph = soup.find(id='A3.SS2.p13')
assert paragraph is not None
signature = '''    {d q : ℕ} (hq : 2 * q + 1 < d) :
  let D := EuclideanSpace ℝ (Fin d)
  let E := EuclideanSpace ℝ (Fin (q + 1))
  let Ω := Fin (q + 1) → D
  let μ : Measure Ω := Measure.pi (fun _ : Fin (q + 1) => stdGaussian D)
  let r : ℝ := ((q + 1 : ℕ) : ℝ)
  let L : ℝ := 2 * r + 3 * Real.log (1000 * (d : ℝ))
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 - 1 / 2) * Real.pi / (d : ℝ)
  let t : Fin d → Fin (q + 1) → ℝ := fun i k =>
    if k.val = 0 then 1 else Real.sqrt 2 * Real.cos ((k.val : ℝ) * θ i)
  let row : Fin d → Ω → E := fun i ω =>
    WithLp.toLp 2 (fun b : Fin (q + 1) => ω b i)
  let Y : Fin d → Ω →
      Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ := fun i ω =>
    if ‖row i ω‖ ^ 2 ≤ L then
      (d : ℝ)⁻¹ • Matrix.kronecker
        (Matrix.vecMulVec (WithLp.ofLp (row i ω)) (WithLp.ofLp (row i ω)))
        (Matrix.vecMulVec (t i) (t i))
    else 0
'''
producer = signature+'''  (∀ i : Fin d, ∀ ω : Ω, ‖Y i ω‖ ≤ 2 * r * L / (d : ℝ)) ∧
    (∀ i : Fin d, ‖∫ ω, Y i ω ∂μ‖ ≤ 2 * r / (d : ℝ))
'''
consumer = signature+'''  let mean : Fin d → Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ :=
    fun i => ∫ ω, Y i ω ∂μ
  let Z : Fin d → Ω → Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ :=
    fun i ω => Y i ω - mean i
  let w : Fin d → ℝ := fun i => Real.cos (((2 * q + 1 : ℕ) : ℝ) * θ i)
  let Rstar : ℝ := 2 * r * (L + 1) / (d : ℝ)
  (∀ i : Fin d, ∀ ω : Ω, ‖Z i ω‖ ≤ Rstar) ∧
    (∀ i : Fin d, ∀ ω : Ω, ‖w i • Z i ω‖ ≤ Rstar)
'''
code = '''import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixVariance
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixMean
noncomputable section
open MeasureTheory ProbabilityTheory
open scoped BigOperators Matrix Kronecker Matrix.Norms.L2Operator
namespace UnclaimedStatementFormation
def producerStatement '''+producer.replace(' :\n',' : Prop :=\n',1)+'''
def consumerStatement '''+consumer.replace(' :\n',' : Prop :=\n',1)+'''
#check producerStatement
#check consumerStatement
end UnclaimedStatementFormation
'''
def create(p,text):
    with p.open('x') as out:out.write(text)
create(W/'producer-signature.unclaimed.txt',producer)
create(W/'consumer-signature.unclaimed.txt',consumer)
create(W/'StatementFormation.lean',code)
record = {'state':'UNCLAIMED_STATEMENT_FORMATION_ONLY_NOT_A_SEAL',
    'current_HEAD':subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),
    'source':str(source),'source_sha256':sha(raw),'source_anchor':'A3.SS2.p13',
    'attributed_readable_source':paragraph.get_text(' ',strip=True),
    'exact_source_formula_alttexts':[m.get('alttext') for m in paragraph.select('math')],
    'producer_signature_sha256':sha(producer.encode()),'consumer_signature_sha256':sha(consumer.encode()),
    'status_boundary':'No SAU/frontier/ledger intake, claim or mathematical proof attempted. Do not begin proof search before exact statement seal and independent source graph/type/topology admission. R9 current variance unit verification has priority.',
    'source_conditions':'d,q natural; only2q+1<d. Original product law, closed cutoff, actual mean, real L2 matrix operator norm. q0 retained.',
    'forbidden_extra_binders':['row law certificate','feature norm bound','mean/norm certificate','integrability certificate','PSD certificate','concentration theorem as assumption'],
    'preseal_exposure':'ROOT already knows actual R9 literal experiment, actual matrix-mean API, real CFC route and canonical PSD integral from preceding work; not API-pristine. Previous EmpiricalCovariance background was read only as an existing general preconcentration scope, with no new target proof/API retrieval.',
    'definition_audit_draft':'All experiment definitions literal and unchanged from preceding sealed actual experiment; all norm bounds are outputs. p14 variance and p15 matrix Bernstein excluded from this proposed radius packet.'}
create(W/'unclaimed-next-source-boundary.json',json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:record[k] for k in ['state','source_anchor','producer_signature_sha256','consumer_signature_sha256','status_boundary']}))
