"""Prepare a reservation only after the preceding original VERIFIED cycle is carried."""
from pathlib import Path

old = Path('.astis/huanjian-gc-source-row-independence-20261112/reserve_sealed_packet.generated.py').read_text()
code = old.replace('source-row-independence', 'source-matrix-mean')
code = code.replace('GaussianComplexitySourceRowIndependence', 'GaussianComplexitySourceMatrixMean')
code = code.replace('huanjian_gc_20261112_source_row_independence', 'huanjian_gc_20261112_source_matrix_mean')
code = code.replace("assert head == '6ef180f7495ef79e1f70bac7909036fc6f7f73bc'",
                    "expected = json.loads((workspace / 'expected-reservation-baseline.json').read_bytes())\nassert head == expected['head']")
code = code.replace('88a55849ce9e13a9a04edff6aac13ce32d4370712b1b7a422fba0d570ff0b25e',
                    'b55a1acb837288d580a667903987e5f809610626eb4848c750ff8d3a6c01149b')
code = code.replace("assert sha(ledger_raw) == '138bad640d592e268d0c770a91cf113237920c9d79e4115ce13593924565dda3'",
                    "assert sha(ledger_raw) == expected['ledger_sha256']")
code = code.replace('assert len(states) == 306', 'assert len(states) == 307')
code = code.replace("states['ASTIS-SA-20261112-GaussianComplexitySourceRowLaw']",
                    "states['ASTIS-SA-20261112-GaussianComplexitySourceRowIndependence']")
code = code.replace('assert len(older) == 466', 'assert len(older) == 467')
first = code.index('searches = [')
last = code.index('\nslug = ', first)
code = code[:first] + '''searches = [
    'Existing canonical actual-row Gaussian marginal law, truncated row second moment, and cosine Gram identities are compiled and known. Their exact compiled identities are reused; all prior code/API exposure is disclosed.',
    'The old private canonical-row matrix mean is an application of the same truncated-row node, not a new public canonical provider. The new statement concerns actual original-column maps and their actual sum integrals, not a duplicate canonical-row moment theorem.',
    'Literal Bochner integrability and integral definition, closed indicator, Gaussian product, Kronecker coordinate order and actual Matrix L2Operator/completeness instances are audited. No new target proof implementation/API search before seal/source-type-topology admission.',
]
''' + code[last:]
code = code.replace('Original Gaussian row joint independence and actual truncated-matrix independence',
                    'Actual original-experiment truncated matrix means and two mean sums')
code = code.replace('arXiv2610.20492v1 C.2 p1 joint independence and p12 first sentence/Ex107 actual independent truncated matrices; standing integer query range',
                    'arXiv2610.20492v1 C.2 p12 actual Yi first moments and Ex110 two mean sums, using original p1 experiment and Fact C5; standing integer query range')
code = code.replace("'planned_existing_parents': [seal['shared_floor_audit']['known_existing_node']]",
                    "'planned_existing_parents': seal['shared_floor_audit']['known_canonical_nodes']")
code = code.replace('The existing marginal-law node is canonical. Complement it with full independence of the literal physical-row family and consume that result in actual source Yi measurability/independence; no duplicate marginal theorem or independence certificate input.',
                    'Use the same canonical row law and truncated radial moment to derive actual Yi integrability and means under the original product law; consume these exact means with the existing cosine frame in both actual finite-sum integrals. No duplicated public radial/marginal theorem or supplied mean certificate.')
code = code.replace('C.2 p1 and p12 first sentence/Ex107, with literal grid and cutoff definitions',
                    'C.2 p1,p10,p12 Ex107/108/110 and exact Fact C5 feature sums')
code = code.replace('Source omits the product-coordinate regrouping/full joint independence and measurable truncated-matrix composition details. These need actual internal proofs; marginals alone do not supply independence.',
                    'Source suppresses actual row-law applicability, Bochner integrability/transport, tensor/scalar image commutation, finite integral exchange and exact cosine-frame assembly. All remain internal proof obligations, not theorem binders.')
code = code.replace('C.2 row experiment/Ex107 and actual iIndepFun/kernel/product/matrix-entry meanings',
                    'C.2 actual matrix means/two expectation sums and literal Bochner/indicator/Kronecker/operator-norm meanings')
code = code.replace('All rows and Yi use one actual product experiment. Establish full row independence and derive measurability/independence of literal Yi internally, q=0 included; no law, Gram/norm, tau/kappa or independence certificate input.',
                    'All actual Yi use one product experiment and source closed cutoff. Derive their integrability/means and finite-sum exchange internally, q=0 retained; no row-law/moment/integrability/Gram/mean/tau/kappa certificate input. Joint independence is separate existing credit and unnecessary for means.')
code = code.replace('Prospective exact joint-independence statement and actual Yi consumer; formula explanation and adjacent Lean follow actual proof.',
                    'Sealed exact actual Yi means and both actual sum integrals; formula proof and exact adjacent folded Lean await real proof.')
code = code.replace('Preliminary raw reading and newly sealed exact types only; formal graph/type/topology review pending. Actual compiled independence/consumer edges require the new proof.',
                    'Independent raw reading and newly sealed exact types only; formal source graph/type/topology admission pending. Actual compiled mean/consumer edges require real new proofs.')
generated = Path(__file__).resolve().parent / 'reserve_sealed_packet.generated.py'
with generated.open('x') as out:
    out.write(code)
exec(compile(code, str(generated), 'exec'))
