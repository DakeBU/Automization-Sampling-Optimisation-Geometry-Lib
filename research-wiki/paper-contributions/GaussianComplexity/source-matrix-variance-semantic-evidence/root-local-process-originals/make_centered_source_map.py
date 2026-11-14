"""Add source-ordered private-consumer correspondence; keep the accepted P map exact."""
from pathlib import Path
import hashlib
import json
helper=Path('.astis/huanjian-real-matrix-positive-integral-20261112/make_source_lean_map.generated.py').read_text()
exec(compile(helper[:helper.index('shared_maps = [')],'<frozen-source-span-helpers>','exec'))
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
E=Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-semantic-evidence')
T=Path('Tests/GaussianComplexityFixedSpectrumSourceMatrixVariance.lean')
assert sha(T.read_bytes())=='c72d3573c6047b75983a958ad8b98de9c399e13277daa852a66c3e5a0820e73b'
def upstream_source(path,first,last,name):
    s=code_span(Path('.lake/packages/mathlib/Mathlib')/path,first,last)
    return {'source_id':name,'file':s['path'],'file_sha256':s['file_sha256'],
        'origin':'EXTERNAL_BACKGROUND','raw_utf8_start':s['raw_UTF8_byte_span'][0],
        'raw_utf8_end':s['raw_UTF8_byte_span'][1],'char_start':s['decoded_char_span'][0],
        'char_end':s['decoded_char_span'][1],'lf_line_start':first,'lf_line_end':last,
        'span_sha256':s['span_sha256']}
bochner=lambda a,b,n:upstream_source('MeasureTheory/Integral/Bochner/ContinuousLinearMap.lean',a,b,n)
cfc=lambda a,b,n:upstream_source('Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Unital.lean',a,b,n)
maps=[
    mapping([primary('A3.SS2.p1'),primary('A3.Ex107.m1'),primary('A3.SS2.p13')],[(T,1,83)],
        'The same source range, original Gaussian-column product, actual rows, exact closed Yi, actual integral mean, centered Zi, deterministic frequency2q+1 and coefficient C are literal. Public P supplies squared integrability and the uncentered PSD bound; existing actual means supply Yi integrability. No public certificate binder.',
        'EXACT_SAME_EXPERIMENT_PRIVATE_CONSUMER_SETUP'),
    mapping([primary('A3.Ex107.m1'),primary('A3.SS2.p13'),primary('A3.Ex118.m1')],[(T,84,105)],
        'Actual Yi is a nonnegative paired rank-one matrix. The canonical shared PSD-integral node applies to its derived integrability and pointwise PSD, making actual Mi Hermitian. Zi is Hermitian and its ordinary square is full PSD.',
        'AUTHORED_INTERNAL_PSD_AND_MEAN_APPLICABILITY'),
    mapping([primary('A3.Ex118.m1'),bochner(233,247,'Mathlib.actual_integrable_fixed_left_and_right_products'),
             upstream_source('MeasureTheory/Measure/Typeclasses/Probability.lean',116,118,'Mathlib.probReal_univ')],[(T,106,132)],
        'Noncommutative expansion keeps both Yi Mi and Mi Yi. Both are actually integrable; the two distinct fixed-product integral identities and probability constant integral give E Zi²=E Yi²−Mi². No matrix commutativity or totalized nonintegrable shortcut.',
        'SOURCE_CENTERING_WITH_EXPLICIT_BOCHNER_CONTRACTS'),
    mapping([primary('A3.Ex117.m1'),primary('A3.Ex118.m1')],[(T,133,148)],
        'The shared node integrates actual PSD centered squares; full PSD mean squares add to the public uncentered comparison. Obtain actual PSD sum A and full PSD CI−sum A internally.',
        'SOURCE_UNWEIGHTED_VARIANCE_ORDER_COMPARISON'),
    mapping([primary('A3.Ex120.m1')],[(T,150,177)],
        'Actual deterministic cosine weights satisfy0<=wi²<=1. Each weighted ordinary square and its expectation equal wi² times the unweighted quantities; integrate only after actual integrability. Sum the PSD residual (1−wi²)Ai for the weighted upper comparison.',
        'SOURCE_WEIGHTED_VARIANCE_WITH_INTERNAL_INTEGRABILITY'),
    mapping([primary('A3.Ex118.m1'),primary('A3.Ex120.m1'),
             upstream_source('Analysis/Matrix/Order.lean',58,62,'Mathlib.full_PSD_matrix_order'),
             cfc(941,944,'Mathlib.real_nonnegative_spectrum'),
             cfc(1059,1062,'Mathlib.real_upper_spectrum_bound'),
             upstream_source('Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Isometric.lean',103,110,'Mathlib.norm_cfc_le'),
             cfc(383,386,'Mathlib.cfc_id')],[(T,179,206)],
        'For each real full-PSD expectation sum, CI−B PSD implies spectrum in[0,C]. Existing real CFC bounds the actual L2 operator norm by C. Apply twice to the actual unweighted/weighted sums; all four exact T conclusions follow. No complex CStarAlgebra shortcut or entrywise norm.',
        'SOURCE_NORM_ENDPOINT_WITH_EXISTING_REAL_CFC_BACKGROUND'),
]
prior=E/'source-lean-map.draft.json'
record={'kind':'Author full R9 producer/private-consumer source map; not an independent verdict',
    'primary_source_sha256':sha(raw),'prior_public_producer_map':{'path':str(prior),'sha256':sha(prior.read_bytes()),'unchanged':True},
    'private_consumer_file_sha256':sha(T.read_bytes()),'mappings':maps,
    'formal_ASTIS_boundaries':{'public_P':'Exactly4 existing canonical parents, unchanged from previous packet.',
        'private_T':['FixedSpectrumSourceMatrixVariance.actual_source_truncated_matrix_second_moments','FixedSpectrumSourceMatrixMean.actual_source_truncated_matrix_means','RealMatrixPositiveIntegral.integral_posSemidef']},
    'scope':'Private centered/weighted consumer Ex118/120, including q0, actual integrability and true real operator norms. No new public API or source credits beyond reviewed packet; p15 concentration, main result/oracle/cost/integration/purification remain open.',
    'selected_route':'Actual generic PSD integral + noncommutative centering + cosine residual + real CFC.',
    'alternative_route_boundary':'Existing full R9 source graph alternatives remain unchanged; no false AND or new mathematical source gap is introduced.'}
out=E/'source-lean-map.full-consumer-v3.draft.json'
with out.open('xb') as f:f.write((json.dumps(record,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps({'path':str(out),'sha256':sha(out.read_bytes()),'consumer_mappings':len(maps),'P_map_unchanged':True}))
