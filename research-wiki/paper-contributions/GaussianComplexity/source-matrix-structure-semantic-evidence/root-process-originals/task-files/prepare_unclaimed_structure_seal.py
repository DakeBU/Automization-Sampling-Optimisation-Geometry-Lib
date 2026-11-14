"""Unclaimed proof-free structure statement; no theorem proof or SAU transition."""
from pathlib import Path
import hashlib,json,subprocess
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
prev=Path('.astis/huanjian-gc-source-matrix-radius-20261113/consumer-signature.unclaimed.txt').read_text()
p=prev[:prev.index('  let w :')]+'''  (∀ i : Fin d, Measurable (Z i)) ∧
    iIndepFun Z μ ∧
    (∀ i : Fin d, Integrable (Z i) μ) ∧
    (∀ i : Fin d, (∫ ω, Z i ω ∂μ) = 0) ∧
    (∀ i : Fin d, ∀ ω : Ω, (Z i ω).IsHermitian)
'''
t=prev[:prev.index('  let Rstar :')]+'''  let X : Fin d → Ω → Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ :=
    fun i ω => w i • Z i ω
  (∀ i : Fin d, Measurable (X i)) ∧
    iIndepFun X μ ∧
    (∀ i : Fin d, Integrable (X i) μ) ∧
    (∀ i : Fin d, (∫ ω, X i ω ∂μ) = 0) ∧
    (∀ i : Fin d, ∀ ω : Ω, (X i ω).IsHermitian)
'''
sha=lambda b:hashlib.sha256(b).hexdigest()
dump=lambda o:(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
def create(f,b):
    with (W/f).open('xb') as out:out.write(b)
head=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()
create('producer-signature.unclaimed.txt',p.encode());create('consumer-signature.unclaimed.txt',t.encode())
formation='''import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowIndependence
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixMean
noncomputable section
open MeasureTheory ProbabilityTheory
open scoped BigOperators Matrix Kronecker Matrix.Norms.L2Operator
set_option autoImplicit false
namespace UnclaimedStructureFormation
def ProducerProp\n'''+p.replace(' :\n',' : Prop :=\n',1)+'''\ndef ConsumerProp\n'''+t.replace(' :\n',' : Prop :=\n',1)+'''\n#check ProducerProp
#check ConsumerProp
end UnclaimedStructureFormation
'''
create('StructureFormation.lean',formation.encode())
seal={'schema_version':1,'seal_id':'GC-actual-centered-structure-unclaimed-20261113-v1','HEAD':head,'state':'EXACT_PROOF_FREE_UNCLAIMED_SIGNATURES;FORMATION_PENDING;NO_SOURCE_OR_TOPOLOGY_ADMISSION','source':{'file':'.astis/huanjian-resume-20261103/2610.20492v1.html','sha256':'6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915','anchor':'AppendixC.2 p15 first structure assertion; original p1/p10/Ex107 experiment,p12 true means,p13 actual Zi definition; S4 Lemma4.4 q range','faithful_scope':'Actual centered and actual deterministic cosine-weighted sequences are measurable, jointly independent, integrable, mean zero and pointwise real Hermitian. No matrix tail claim.'},'producer':{'name':'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixStructure.actual_source_centered_matrix_structure','planned_file':'AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumSourceMatrixStructure.lean','signature':p,'signature_sha256':sha(p.encode())},'actual_private_consumer':{'name':'AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumSourceMatrixStructure.actual_source_weighted_centered_matrix_structure','planned_file':'Tests/GaussianComplexityFixedSpectrumSourceMatrixStructure.lean','signature':t,'signature_sha256':sha(t.encode()),'placement':'private real weighted consumer, not public API or separate registry credit'},'binder_audit':[{'binder':'d q:ℕ','classification':'TYPING','meaning':'Natural finite dimensions and nonnegative q, q0 retained.'},{'binder':'hq:2*q+1<d','classification':'SOURCE','meaning':'Original source dimension/query-degree regime only; d,r positivity internally derived.'}],'EXCESS_public_binders':[],'definition_audit':{'Omega_mu_rows':'literal original independent standard Gaussian columns and actual physical rows','features_cutoff':'literal midpoint cosine features; original inclusive row cutoff with original L','mean':'literal actual Bochner integral, not supplied mean or certificate; true integrability is internal','Z':'literal Yi minus its own actual unconditional mean on same original law','X':'literal deterministic cos((2q+1)theta_i) times Zi','Hermitian':'usual real matrix transpose symmetry; no substituted PSD or entrywise claim'},'proof_ingredients_not_binders':['Actual row joint independence and the measurable row-to-truncated-tensor map, deterministic centering/weight transformations.','Actual Yi integrability, probability mass, Bochner subtraction/constant integral for true zero mean.','Actual pointwise Yi symmetry and actual mean symmetry; no caller symmetry or mean-zero certificates.'],'preseal_exposure':{'API_pristine':False,'reason':'ROOT has preceding actual row/mean/radius/variance code context; during prior R10 bounded reuse audit saw generic EmpiricalCovariance packages and iIndepFun.comp locations. This is disclosed exposure, not an API-pristine protocol claim. No new target proof searched or supplied before seal.'},'scope_boundary':'Proof-free unclaimed candidate only. No Bernstein tail, variance/radius duplicate theorem, full C6/Lemma4.4/main lower bound, oracle/precision/TV/cap/cost, public API canonicalization or publication/integration/purification credit. Existing R10 cycle remains sole active SAU.','new_target_proof_attempts':0,'new_SAU_frontier_or_ledger_calls':0}
create('statement-seal-v1.json',dump(seal));print(json.dumps({'seal_sha256':sha(dump(seal)),'P_signature_sha256':sha(p.encode()),'T_signature_sha256':sha(t.encode()),'actual_theorem_proofs':0,'new_ledger_calls':0}))
