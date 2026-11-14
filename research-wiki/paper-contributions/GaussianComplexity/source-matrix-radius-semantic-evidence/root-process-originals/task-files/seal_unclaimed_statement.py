"""Seal the exact next statement and binder/definition audit; no intake or proof search."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import subprocess
W = Path(__file__).resolve().parent.relative_to(Path.cwd())
sha = lambda raw:hashlib.sha256(raw).hexdigest()
oldpath = Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-statement-seal.json')
old = json.loads(oldpath.read_bytes())
producer = (W/'producer-signature.unclaimed.txt').read_text()
consumer = (W/'consumer-signature.unclaimed.txt').read_text()
prefix = old['producer']['signature'].split('  let C : ℝ := ')[0]
assert producer.startswith(prefix) and consumer.startswith(prefix)
assert sha(producer.encode()) == '1892e3dadd3ca32820013ea11d534614dcdc1e48d2b8acedc0859c9e66be0214'
assert sha(consumer.encode()) == 'afa15c4d676a73be278b8bd0afd572b4f4d3fd2612d0b4d66d4f837fb1da762e'
rp = Path('.astis/huanjian-resume-20261103/20261112T180145746523Z-unclaimed-source-matrix-radius-literal-Prop-formation.receipt.json')
rraw = rp.read_bytes(); receipt = json.loads(rraw)
assert receipt['exit_code'] == 0
assert sha(Path(receipt['log']).read_bytes()) == receipt['log_sha256']
source = json.loads((W/'unclaimed-next-source-boundary.json').read_bytes())
protocols = ['AGENTS.md','.agents/skills/astis-substantive-advance/SKILL.md',
    '.agents/skills/astis-semantic-roundtrip/SKILL.md','docs/contributor-codex-contract.md',
    'docs/theorem-publication-protocol.md','docs/proof-digestion-protocol.md','docs/evidence-routed-memory-protocol.md']
seal = {
    'schema_version':1,'seal_id':'ASTIS-GC-SOURCE-MATRIX-RADIUS-STATEMENT-v1',
    'created_utc':datetime.now(timezone.utc).isoformat(),
    'state':'STATEMENT_SEALED_UNCLAIMED;INDEPENDENT_SOURCE_TYPE_GRAPH_AND_TOPOLOGY_PENDING',
    'HEAD':subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),
    'source':{'source_id':'arXiv:2610.20492v1','title':'On Complexity of Gaussian Sampling',
        'path':source['source'],'sha256':source['source_sha256'],'anchor':'A3.SS2.p13',
        'faithful_scope':'Actual pointwise truncated-summand operator norm and actual mean operator norm; private real centered/cosine-weighted radius consumer. Same literal original product experiment.',
        'attributed_readable':source['attributed_readable_source'],
        'formula_alttexts':source['exact_source_formula_alttexts']},
    'producer':{'name':'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixRadius.actual_source_truncated_matrix_norm_bounds',
        'planned_file':'AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumSourceMatrixRadius.lean',
        'signature':producer,'signature_sha256':sha(producer.encode())},
    'actual_private_consumer':{'name':'AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumSourceMatrixRadius.actual_source_centered_summand_radius',
        'planned_file':'Tests/GaussianComplexityFixedSpectrumSourceMatrixRadius.lean',
        'signature':consumer,'signature_sha256':sha(consumer.encode()),
        'consumer_edge':'Must actually apply both producer norm bounds to the literal Z=Y-integralY and prove the same bound after the literal cosine scalar. No supplied triangle/norm/mean certificate.'},
    'binder_audit':[
        {'binder':'d q : ℕ','classification':'TYPING','meaning':'Finite natural dimension and degree; r=q+1. q=0 retained.'},
        {'binder':'hq : 2*q+1<d','classification':'SOURCE','meaning':'Same source admissible frequency/dimension range as the exact original experiment. Independent source audit must validate this attribution and q0 scope; no additional condition assumed.'}],
    'EXCESS_public_binders':[],
    'definition_audit':{
        'kind':'literal','exact_experiment_prefix_sha256':sha(prefix.encode()),
        'experiment_prefix_byte_equal_to_previous_sealed_experiment':True,
        'previous_exact_definition_audit_seal':str(oldpath),'previous_seal_sha256':sha(oldpath.read_bytes()),
        'carriers':'Real finite Euclidean D and E; actual independent standard Gaussian columns under product probability; finite r²-by-r² real matrices with L2Operator norm.',
        'cutoff':'The literal row norm squared <=L closed cutoff, zero outside, exactly the source indicator. No fallback selection or characterized object.',
        'mean':'Actual Bochner integral of literal Y under the same mu, not an arbitrary population matrix. Actual integrability must be proved internally or consumed from an exact public provider.',
        'weights':'Exact cos((2q+1)*theta_i); no changed spectrum/phase/grid/normalization.',
        'radius':'Exact2r(L+1)/d, not the weaker4rL/d; bounds for Y and actual mean are outputs.',
        'matrix_norm':'Same real Euclidean induced operator norm as previous full type/instance audit. Neither Frobenius/entrywise nor a certificate alias.',
    },
    'proof_ingredients_not_binders':source['forbidden_extra_binders'],
    'scope_boundary':'Only source p13 and necessary literal definitions/prerequisites. p14 variance is a separate existing packet; p15 Bernstein, probability tails, full Lemma4.4, main lower bounds and oracle/TV/precision/cap/cost excluded. No public/private API placement or integration/purification credit.',
    'actual_statement_formation':{'receipt':str(rp),'receipt_sha256':sha(rraw),'exit_code':0,'log_sha256':receipt['log_sha256'],
        'evidence_scope':'Both complete literal Prop definitions type-check. No theorem inhabitant/proof was supplied. hq linter warning is retained because formation does not prove the bounds.'},
    'preseal_exposure':source['preseal_exposure'],'formalizer_API_pristine':False,
    'new_target_proof_search_or_implementation_attempts':0,'new_SAU_frontier_or_ledger_intake_calls':0,
    'process_memory':{'registry':'research-wiki/process-memory.json','sha256':sha(Path('research-wiki/process-memory.json').read_bytes()),
        'scope':'Previously read evidence-routed process-only rules remain in force; no negative mathematical route or new premise inferred from control-plane memory.'},
    'protocol_files':{p:sha(Path(p).read_bytes()) for p in protocols},
    'mutation_rule':'Proof changes may not alter these signatures/definitions for convenience. Any independently established genuine source/type defect requires a separately versioned successor and retained original. No proof search before independent source graph and distinct topology admission.',
}
with (W/'statement-seal-v1.json').open('x') as out:out.write(json.dumps(seal,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'seal_id':seal['seal_id'],'seal_sha256':sha((W/'statement-seal-v1.json').read_bytes()),'state':seal['state'],'new_proof_attempts':0,'new_intake_calls':0}))
