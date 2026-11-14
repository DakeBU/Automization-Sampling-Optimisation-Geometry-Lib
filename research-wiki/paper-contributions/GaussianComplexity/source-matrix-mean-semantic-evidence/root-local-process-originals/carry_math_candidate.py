"""Carry only the compiled mean packet and its complete bounded originals."""
from pathlib import Path

old = Path('.astis/huanjian-gc-source-row-independence-20261112/carry_math_candidate.generated.py').read_text()
code = old.replace('source-row-independence', 'source-matrix-mean')
code = code.replace('GaussianComplexitySourceRowIndependence', 'GaussianComplexitySourceMatrixMean')
code = code.replace('6ef180f7495ef79e1f70bac7909036fc6f7f73bc', '90f3fe822621cba10350450798fae107b9c92335')
code = code.replace('88a55849ce9e13a9a04edff6aac13ce32d4370712b1b7a422fba0d570ff0b25e',
                    'b55a1acb837288d580a667903987e5f809610626eb4848c750ff8d3a6c01149b')
code = code.replace('.astis/semantic-neutral-20261112/ri_tc_24a6/conceptual-v1',
                    '.astis/semantic-neutral-20261112/mm_tc_7f32/conceptual-v1')
code = code.replace("assert sha(concept_manifest.read_bytes()) == '9dfef374661ee32ade97303841ff4da3a2e1bfa85acf03d578d78c8408327a03'",
                    "expected_concept = json.loads((workspace / 'expected-conceptual-original.json').read_bytes())\nassert sha(concept_manifest.read_bytes()) == expected_concept['freeze_sha256']")
code = code.replace("frozen['new_candidates'] == 0", "frozen['new_candidates'] == []")
code = code.replace("'owned_theorems': 2, 'handwritten_roots': 2, 'generated_reachable_internal': 0",
                    "'owned_theorems': 3, 'handwritten_roots': 2, 'generated_reachable_internal': 1")
code = code.replace('20261112T080727870702Z-source-matrix-mean-normal-intake.receipt.json',
                    '20261112T124409793898Z-source-matrix-mean-normal-intake.receipt.json')
code = code.replace("'actual_intake_readback_tool_chunk': 'f7be51'", "'actual_intake_readback_tool_chunk': '6d2689'")
code = code.replace('Both unchanged sealed mathematical targets compiled on first implementation attempt. Independent final source/native acceptance and normal PROVED_LOCAL pending.',
                    'Unchanged sealed producer compiled first attempt; actual sum consumer compiled after two diagnosed proof-local elaboration/API fixes. Original strict kernel probe passed first attempt. Independent final source/native acceptance and normal PROVED_LOCAL pending.')
start = code.index("create(evidence / 'local-attempt-diagnoses.json'")
stop = code.index("\nreview = json.loads", start)
code = code[:start] + '''create(evidence / 'local-attempt-diagnoses.json', dump({
    'sealed_statements_changed': False, 'formalizer_API_pristine': False,
    'preseal_formation_failures': 0,
    'preseal_definition_lookup_exposure': 'Overbroad definition-location lookup exposed adjacent standard theorem headers/proof fragments. Exact exposure and original tool chunk ids are retained from the first seal; no pristine API chronology asserted.',
    'reservation_description_failure': 'New unadmitted C description omitted literal Samplinglib/Mathlib labels required by the schema. Original C and exit1 retained; versioned v2 adds the actual library provenance labels only. Ledger unchanged before normal intake.',
    'post_admission_proof_API_lookup': 'ProofAPI exit1: Integrable.finset_sum and Matrix kronecker_sum/sum_kronecker names were unavailable. Actual integrable_finsetSum and linear-map sum rules were then inspected; rejected probe unchanged.',
    'producer_implementation_failures': 0,
    'consumer_implementation_failures': 2,
    'consumer_attempt1': 'Bare function annotation for proof-local t made field notation resolve to Function.transpose and omitted matrix multiplication. Version2 exposes definitionally equal Matrix annotation only, unchanged sealed statement.',
    'consumer_attempt2': 'Finset.smul_sum has implicit arguments; applying three positional placeholders failed. Version3 uses the same lemma by type inference, unchanged route and statements.',
    'consumer_first_failure_detailed_record': str(workspace / 'consumer-firstbuild-diagnosis.json'),
    'actual_strict_kernel_probe_failures': 0,
    'salvage': 'Actual first-moment producer and real two-sum consumer retained. Two handwritten roots and one emitted internal proof helper are all kernel-inspected, closed/reachable with standard axioms. No discarded mathematical fragment, extra source hypothesis, duplicate public radial/marginal lemma or assumption wrapper.',
}))
''' + code[stop:]
code = code.replace('Prove original Gaussian row independence and actual truncated-matrix independence',
                    'Prove actual Gaussian truncated matrix means and both finite-sum expectations')
generated = Path(__file__).resolve().parent / 'carry_math_candidate.generated.py'
with generated.open('x') as out:
    out.write(code)
exec(compile(code, str(generated), 'exec'))
