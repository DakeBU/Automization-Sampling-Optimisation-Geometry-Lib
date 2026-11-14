"""Reserve one exact actual-variance packet, without normal intake or proof search."""
from pathlib import Path

code = Path('.astis/huanjian-gc-source-matrix-mean-20261112/reserve_sealed_packet.generated.py').read_text()
code = code.replace('source-matrix-mean', 'source-matrix-variance')
code = code.replace('GaussianComplexitySourceMatrixMean', 'GaussianComplexitySourceMatrixVariance')
code = code.replace('huanjian_gc_20261112_source_matrix_mean', 'huanjian_gc_20261112_source_matrix_variance')
code = code.replace('b55a1acb837288d580a667903987e5f809610626eb4848c750ff8d3a6c01149b', '5f905cafe6035238cebdedd4f841e87b703e741b4c8aa204471d89e4c07e8a14')
code = code.replace('assert len(states) == 307', 'assert len(states) == 308')
code = code.replace("states['ASTIS-SA-20261112-GaussianComplexitySourceRowIndependence']", "states['ASTIS-SA-20261112-GaussianComplexitySourceMatrixMean']")
code = code.replace('assert len(older) == 467', 'assert len(older) == 468')
first = code.index('searches = [')
last = code.index('\nslug = ', first)
code = code[:first] + '''searches = [
    'Samplinglib/ASTIS prior canonical Gaussian row law, radial fourth moment matrix and weighted cosine coefficient bound are compiled and known from the prior accepted packets. Actual matrix means are independently VERIFIED. Their exact identities are reused; prior proof/API exposure is disclosed.',
    'Samplinglib/ASTIS old private canonical-row uncentered aggregate remains immutable history. The new packet concerns literal physical rows on the actual original product law, then genuine centered/cosine-weighted operator-norm variance conclusions. No duplicate canonical public radial/frame lemma credit.',
    'Mathlib exact standard definition and actual-instance prints cover ordinary finite matrix multiplication, full PosSemidef, integrability/Bochner meaning and L2Operator norm/completeness. New-target generic matrix variance/PSD-to-norm API retrieval is pending exact source graph/topology admission; no new target implementation yet.',
]
''' + code[last:]
insertion = '''
cell['title'] = 'Actual Gaussian matrix squared moments and centered variance operator bounds'
cell['source_anchor'] = 'arXiv2610.20492v1 C.2 p13 Z definition; p14 Ex113/114 and centered/cosine-weighted variance comparisons; original p1/p10/Ex107 experiment and exact Fact C5 features. Bernstein p15 excluded.'
cell['reuse_plan']['decision_reason'] = 'Use existing canonical row-law, radial-fourth and weighted-frame results to obtain actual uncentered squared moments; consume them in actual centered and cosine-weighted centered integrability and operator-norm bounds. Any missing multi-route generic lemma must receive one shared canonical cell before its proof; never add a variance/PSD/norm certificate as a binder.'
cell['source_detail_audit'].update({
    'primary_anchor': 'C.2 p1,p10,Ex107,p13,p14,Ex113/114 and Fact C5; all p15 excluded',
    'gap': 'Actual-law transport, squared integrability, Hermitian/PSD facts, centered Bochner variance identity, weighted comparison and PSD domination to actual L2 operator norm all require internal proofs. A source omission is not an extra theorem hypothesis.',
    'consulted': [{'source': 'Pinned original source and literal canonical definitions', 'anchor': 'Actual closed-cutoff Yi, actual mean/Z and p14 centered/cos² comparisons', 'hypothesis_adapter': 'Same original independent-column product experiment and exact midpoint features; sole range2q+1<d including q0. Every integrability, positivity, moment/Gram/norm estimate is derived internally.'}],
})
cell['reader_contract']['status'] = 'Exact uncentered PSD and two genuine centered operator-norm targets sealed; readable formula proof and adjacent initially folded exact Lean await real proof.'
cell['graph_contribution']['visual_review'] = 'Own raw source freezes and exact sealed types; independent type/graph/topology admission pending. No compiled variance edge or runtime reader evidence yet.'
'''
code = code.replace('create(cell_path, dump(cell))', insertion + '\ncreate(cell_path, dump(cell))')
generated = Path(__file__).resolve().parent / 'reserve_sealed_packet.generated.py'
with generated.open('x') as out:
    out.write(code)
exec(compile(code, str(generated), 'exec'))
