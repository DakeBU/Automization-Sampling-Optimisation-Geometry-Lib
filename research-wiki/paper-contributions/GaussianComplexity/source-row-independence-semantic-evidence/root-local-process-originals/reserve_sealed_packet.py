"""Prepare one new exact-type reservation without mutating any earlier cell or ledger."""
from pathlib import Path

old = Path('.astis/huanjian-gc-source-row-law-20261112/reserve_sealed_packet.py').read_text()
code = old.replace('source-row-law', 'source-row-independence')
code = code.replace('GaussianComplexitySourceRowLaw', 'GaussianComplexitySourceRowIndependence')
code = code.replace('huanjian_gc_20261112_source_row_law', 'huanjian_gc_20261112_source_row_independence')
code = code.replace('60a86f45ca29cd5cae96e59e8b14975674f59df9', '6ef180f7495ef79e1f70bac7909036fc6f7f73bc')
code = code.replace('f9476ec7454a0927d3a1068226ad635b464d9b5d631f4992421d4b3b39b70ec3', '88a55849ce9e13a9a04edff6aac13ce32d4370712b1b7a422fba0d570ff0b25e')
code = code.replace('2d07278f66962c1f106c5f498d8d970e3aedc7d9e5ca27715da0c5c3483d4112', '138bad640d592e268d0c770a91cf113237920c9d79e4115ce13593924565dda3')
code = code.replace('assert len(states) == 305', 'assert len(states) == 306')
code = code.replace("states['ASTIS-SA-20261112-GaussianComplexityWeightedCosineFrame']", "states['ASTIS-SA-20261112-GaussianComplexitySourceRowLaw']")
code = code.replace('assert len(older) == 465', 'assert len(older) == 466')
start, stop = code.index('searches = ['), code.index("\nslug = ", code.index('searches = ['))
code = code[:start] + '''searches = [
    'Samplinglib exact canonical FixedSpectrumSourceRowLaw.actual_source_row_marginal_law is compiled and known from the previous packet, including row measurability; its whole code/API exposure is disclosed. It does not prove joint independence.',
    'Mathlib literal iIndepFun and its kernel/finite-intersection meanings, product measurable structures, finite product Gaussian law and real-entry matrix definitions were audited with actual current prints/instances. New proof API retrieval waits for source/type/topology acceptance and normal intake.',
    'Bounded GaussianComplexity Row filename inventory found existing TruncatedRowMoment and SourceRowLaw; the proposed SourceRowIndependence production/test files do not exist. No new independence proof implementation has been attempted.',
]
''' + code[stop:]
code = code.replace('Original Gaussian column-experiment row laws and global good cutoff event',
                    'Original Gaussian row joint independence and actual truncated-matrix independence')
code = code.replace('arXiv2610.20492v1 C.2 p1 row construction and p10 Ex104/Ex105 with the printed probability0.999, under the standing integer query range',
                    'arXiv2610.20492v1 C.2 p1 joint independence and p12 first sentence/Ex107 actual independent truncated matrices; standing integer query range')
code = code.replace("seal['shared_floor_audit']['existing_canonical_consumer_parent']",
                    "seal['shared_floor_audit']['known_existing_node']")
code = code.replace('The source-specific coordinate row map has a fixed original column-product law. Prove its actual measurable Gaussian marginal transport and consume it in the same experiment global truncation event, reusing the canonical exponential moment.',
                    'The existing marginal-law node is canonical. Complement it with full independence of the literal physical-row family and consume that result in actual source Yi measurability/independence; no duplicate marginal theorem or independence certificate input.')
code = code.replace('C.2 p1 and p10 Ex104/Ex105', 'C.2 p1 and p12 first sentence/Ex107, with literal grid and cutoff definitions')
code = code.replace('Source row-law identification, canonical product realization, measurability, exponential-moment/tail transport, finite union and closed good-event complement need internal formal proofs.',
                    'Source omits the product-coordinate regrouping/full joint independence and measurable truncated-matrix composition details. These need actual internal proofs; marginals alone do not supply independence.')
code = code.replace('C.2 row experiment, actual Measure.pi and MeasurePreserving meanings',
                    'C.2 row experiment/Ex107 and actual iIndepFun/kernel/product/matrix-entry meanings')
code = code.replace('All rows use one concrete tuple of independent standard Gaussian columns. Derive marginal laws and tails internally, retain q=0, add no tau-smallness or law certificate.',
                    'All rows and Yi use one actual product experiment. Establish full row independence and derive measurability/independence of literal Yi internally, q=0 included; no law, Gram/norm, tau/kappa or independence certificate input.')
code = code.replace('Prospective original experiment statement, source formula steps and exact adjacent Lean after actual proof.',
                    'Prospective exact joint-independence statement and actual Yi consumer; formula explanation and adjacent Lean follow actual proof.')
code = code.replace('Independent raw source and exact types only. Actual compiled law/consumer edges require the new proof.',
                    'Preliminary raw reading and newly sealed exact types only; formal graph/type/topology review pending. Actual compiled independence/consumer edges require the new proof.')
generated = Path(__file__).resolve().parent / 'reserve_sealed_packet.generated.py'
with generated.open('x') as out:
    out.write(code)
exec(compile(code, str(generated), 'exec'))
