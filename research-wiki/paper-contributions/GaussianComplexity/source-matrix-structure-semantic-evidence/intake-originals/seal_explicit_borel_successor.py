"""Repair only the unformed typing convention, before any proof or new intake."""
from pathlib import Path
import hashlib,json,subprocess
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
sha=lambda b:hashlib.sha256(b).hexdigest()
dump=lambda o:(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
def create(n,b):
    with (W/n).open('xb') as f:f.write(b)
old=(W/'statement-seal-v1.json').read_bytes()
assert sha(old)=='21e234c0df5fc8438c13ee1e4bb27290f67357714db300cd2f0e59c9e27055d3'
s=json.loads(old)
typing='''  letI : MeasurableSpace
      (Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ) :=
    borel (Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ)
'''
for key,filename in [('producer','producer-signature.v2.unclaimed.txt'),('actual_private_consumer','consumer-signature.v2.unclaimed.txt')]:
    prior=s[key]['signature'];assert 'letI' not in prior
    signature=prior.replace('  let D :=',typing+'  let D :=',1)
    s[key]['signature']=signature;s[key]['signature_sha256']=sha(signature.encode())
    create(filename,signature.encode())
s['predecessor']={'file':str(W/'statement-seal-v1.json'),'sha256':sha(old),'status':'TYPE_FORMATION_FAILED, missing measurable structure for Matrix; never source/topology admitted or proved.'}
s['seal_id']='GC-actual-centered-structure-unclaimed-20261113-v2-explicit-borel'
s['HEAD']=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()
s['state']='EXACT_PROOF_FREE_UNCLAIMED_SIGNATURES;EXPLICIT_STANDARD_BOREL;FORMATION_PENDING;NO_SOURCE_OR_TOPOLOGY_ADMISSION'
s['definition_audit']['matrix_sigma_algebra']='Explicit literal borel of the finite real matrix topology selected by Matrix.Norms.L2Operator. This is a fixed standard typing convention, not a quantified measurable-space assumption or altered probability law. Coordinate/product-Borel compatibility must be independently audited before proof.'
s['binder_audit'].append({'binder':'local letI MeasurableSpace Matrix := borel Matrix','classification':'TYPING','meaning':'Fixes standard finite-dimensional real matrix Borel sigma algebra as a definition; no caller input or extra proposition. No alternate norm/measure certificate.'})
s['typing_successor_reason']='The first genuine proof-free formation failed to synthesize Matrix MeasurableSpace for Measurable/iIndepFun. The v2 interface explicitly fixes the standard Borel structure; all source quantities, hq, conclusions and mathematical constants are unchanged. No mathematical route was refuted.'
s['scope_boundary']='Unclaimed exact statement only; source graph/type audit/topology challenge and new SAU admission still required after existing R10 verification. No new proof, Bernstein tail, duplicate radius/variance theorem, main lower bound or integration credit.'
create('statement-seal-v2.json',dump(s))
formation='''import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowIndependence
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixMean
noncomputable section
open MeasureTheory ProbabilityTheory
open scoped BigOperators Matrix Kronecker Matrix.Norms.L2Operator
set_option autoImplicit false
namespace UnclaimedStructureFormationV2
def ProducerProp
'''+s['producer']['signature'].replace(' :\n',' : Prop :=\n',1)+'''\ndef ConsumerProp
'''+s['actual_private_consumer']['signature'].replace(' :\n',' : Prop :=\n',1)+'''\n#check ProducerProp
#check ConsumerProp
end UnclaimedStructureFormationV2
'''
create('StructureFormation.v2.lean',formation.encode())
diagnosis={'failure_class':'API_BLOCKED','failed_formation_receipt':'.astis/huanjian-resume-20261103/20261113T051728188098Z-unclaimed-source-matrix-structure-literal-prop-formation.receipt.json','mathematical_failure':False,'input_binder_added':False,'correction':'Explicit fixed standard finite matrix Borel structure in exact signature, independently reviewable.','old_seal_sha256':sha(old),'new_seal_sha256':sha(dump(s)),'target_proof_attempts':0,'ledger_intake_calls':0}
create('formation-v1-typing-diagnosis.json',dump(diagnosis))
print(json.dumps(diagnosis))
