"""Extend the same public P lesson with its exact, separately scoped private T consumer.

P's source proposition, code, original decoder and actual parents stay identical.
The added T proof is not a new public theorem or a P->R8 Lean implication.
"""
from pathlib import Path
import copy
import hashlib
import json
import sys
sys.dont_write_bytecode=True
sys.path.insert(0,'tools')
import astis_publication as publication
import astis_semantic_roundtrip as semantic
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
E=Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-semantic-evidence')
slug='huanjian-gaussian-source-matrix-variance'
lesson_path=Path('website/content/declaration_lessons')/(slug+'.json')
pub_path=Path('website/content/publications')/(slug+'.json')
audit_path=Path('research-wiki/semantic-roundtrip/audits')/(slug+'.json')
C=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-variance.json')
T=Path('Tests/GaussianComplexityFixedSpectrumSourceMatrixVariance.lean')
sha=lambda raw:hashlib.sha256(raw.encode() if isinstance(raw,str) else raw).hexdigest()
dump=lambda obj:(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
def create(p,raw):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(raw)
previous={}
for i,p in enumerate([lesson_path,pub_path,audit_path,C,E/'publication-draft-record.json']):
    raw=p.read_bytes(); dest=E/'before-full-consumer-reader-v3.originals'/(str(i)+'-'+p.name)
    create(dest,raw); previous[str(p)]={'path':str(dest),'sha256':sha(raw)}
lesson=json.loads(lesson_path.read_bytes()); unit=lesson['units'][0]
assert len(unit['steps'])==4
old_deps=copy.deepcopy(unit['astis_dependencies'])
t=T.read_text(); lines=t.splitlines(keepends=True)
assert len(lines)==206 and sha(t)=='c72d3573c6047b75983a958ad8b98de9c399e13277daa852a66c3e5a0820e73b'
extra=[
    {'title':'Form the actual centered matrices',
     'text':'The separately stated private consumer uses the same original experiment and exact cutoff. Write Mi for the actual expectation of Yi and Zi=Yi-Mi. The existing actual first-moment producer supplies Yi integrability; the uncentered producer supplies Yi-square integrability. Each actual Yi is a nonnegative paired rank-one matrix. Apply the same canonical PSD-integral theorem to obtain full PSD of Mi. Hence Zi is Hermitian and its ordinary square is PSD. All application premises are proved internally.',
     'formula':r'M_i=\mathbb E_\mu Y_i,\quad Z_i=Y_i-M_i,\quad Y_i\in L^1(\mu),\quad Y_i\succeq0,\ M_i\succeq0,\ Z_i^2\succeq0.',
     'lean':''.join(lines[:105])},
    {'title':'Center without assuming matrices commute',
     'text':'Expand the ordinary square with both cross terms Yi Mi and Mi Yi. Fixed right and left multiplication preserve actual integrability and commute separately with the Bochner integral. The probability integral of the constant Mi squared supplies the remaining term. Thus each centered square is integrable and its expectation is the uncentered second moment minus Mi squared. Integrate PSD centered squares and add the PSD sum of mean squares to the already proved uncentered comparison.',
     'formula':r'\mathbb E_\mu[Z_i^2]=\mathbb E_\mu[Y_i^2]-M_i^2,\qquad A_i:=\mathbb E_\mu[Z_i^2],\qquad0\preceq\sum_i A_i\preceq C I_{r^2},\quad C=\frac{2r(r+2)}d.',
     'lean':''.join(lines[105:148])},
    {'title':'Weight by the actual cosine and bound the real operator norms',
     'text':'For the exact deterministic wi=cos((2q+1)theta_i), the range of cosine gives0<=wi squared<=1. The ordinary weighted square is wi squared times Zi squared, so its actual integrability and expectation follow. The residual sum of (1-wi squared)Ai is PSD. Both expectation sums are therefore full PSD matrices bounded above by C times the identity. Real continuous functional calculus places their real spectra in[0,C] and bounds their actual Euclidean operator norms. This is the private centered/weighted consequence, separate from P public uncentered conclusion.',
     'formula':r'w_i=\cos((2q+1)\theta_i),\quad0\le w_i^2\le1,\quad\mathbb E_\mu[(w_i Z_i)^2]=w_i^2 A_i,\quad\left\|\sum_i A_i\right\|\le C,\quad\left\|\sum_i\mathbb E_\mu[(w_i Z_i)^2]\right\|\le C.',
     'lean':''.join(lines[148:])},
]
assert ''.join(x['lean'] for x in extra)==t
unit['steps']+=extra
unit['reader_note']='The main statement is the public uncentered producer. The final three proof steps give its complete actual centered and cosine-weighted private consumer, under the same source conditions.'
unit['dependency_notes']='Public P materially calls exactly the same four canonical ASTIS parents listed above. The separate private consumer calls P, FixedSpectrumSourceMatrixMean.actual_source_truncated_matrix_means and RealMatrixPositiveIntegral.integral_posSemidef. Its external providers include both integrable fixed-product integral rules, integral_add/sub, probReal_univ, Matrix.posSemidef_conjTranspose_mul_self, Matrix.nonneg_iff_posSemidef, le_algebraMap_iff_spectrum_le, StarOrderedRing.nonneg_iff_spectrum_nonneg, norm_cfc_le and cfc_id over the real L2Operator MatrixOrder instances. These private-consumer references are not additional direct P parents or public theorem credit; every common declaration stays one canonical node.'
unit['lean_proof']='Seven source-ordered formula steps with exact adjacent Lean: the first four reproduce the complete public uncentered module, and the last three reproduce the complete private centered/weighted consumer module.'
unit['boundary']='Public P proves actual original-experiment Y-square integrability and the uncentered PSD sum bound only. Its separately compiled private consumer proves integrability of actual centered and cosine-weighted centered squares and both true real operator-norm bounds2r(r+2)/d, including q=0. It is not a public Tests provider or a new public theorem node. Public aggregate API canonicalization, matrix concentration, full Lemma4.4, both main lower bounds, genuine exact-matvec/precision/TV/dimension-kappa/worst-query-cap/expected-cost adapters, serialized main/site/source-index/globalgraph delivery and purification remain unfinished.'
unit['sources'] += [
    {'url':'https://arxiv.org/html/2610.20492v1#A3.Ex118','label':'Centered variance comparison Ex118','scope':'Private actual consumer only, following the public uncentered producer.'},
    {'url':'https://arxiv.org/html/2610.20492v1#A3.Ex120','label':'Cosine-weighted centered comparison Ex120','scope':'Private actual consumer only; p15 concentration excluded.'},
    {'path':str(T),'line':22,'label':'Complete private actual centered and weighted consumer','scope':'Exact closed statement and proof of actual square integrability and both operator-norm bounds; no public provider or separate declaration credit.'},
]
unit['tests']=['lake build Tests.GaussianComplexityFixedSpectrumSourceMatrixVariance']
assert unit['astis_dependencies']==old_deps
lesson_path.write_bytes(dump(lesson))
pub=json.loads(pub_path.read_bytes()); item=pub['items'][0]; binding=item['bindings'][0]
assert item['statement']==unit['statement']
publication.inputs.cache_clear(); publication.load.cache_clear()
audit=json.loads(audit_path.read_bytes()); old_decoder=semantic.decoder_packet(audit)
assert audit['state']=='source-reviewed' and audit['source_review']['state']=='accepted'
old_binding=audit['publication_binding_sha256']
audit['publication_binding_sha256']=publication.binding_digest(item,binding)
audit['publication_context']=publication.review_context(item,binding)
assert audit['publication_binding_sha256']!=old_binding
audit['state']='blind-reconstructed'; audit['semantic_slots']={}; audit['deltas']=[]
audit['verdict']='pending'; audit['source_review']={'state':'pending'}; audit['repairs']=[]
audit_path.write_bytes(dump(audit))
assert semantic.decoder_packet(audit)==old_decoder
packet=semantic.semantic_reviewer_packet(audit)
packet_path=E/'anti-anchored-reviewer-packet.full-consumer-v3.json'
create(packet_path,dump(packet))
record={
    'kind':'Extended private-consumer reader under unchanged public P statement/code/source/decoder',
    'previous_originals':previous,'old_publication_binding_sha256':old_binding,
    'publication_binding_sha256':audit['publication_binding_sha256'],
    'current_public_P_statement_and_code_unchanged':True,'same_original_P_decoder_packet':True,
    'canonical_audit_state':'blind-reconstructed; fresh extended whole-consumer/source review pending',
    'anti_anchored_packet':str(packet_path),'anti_raw_sha256':sha(packet_path.read_bytes()),
    'anti_canonical_packet_sha256':packet['packet_sha256'],
    'P_exact_folds':4,'T_exact_folds':3,'T_file_sha256':sha(t),'T_lines':206,
    'source_private_consumer_supplement':str(W/'private-centered-consumer-supplement.audit-draft.json'),
    'new_public_declarations':0,'remaining':'Independent T code-only/anonymous supplement/fresh source and native/reader acceptance. No normalR9PL/V yet.'}
create(E/'full-consumer-reader-v3.record.json',dump(record))
cell=json.loads(C.read_bytes())
assert cell['status']=='claimed'
cell['evidence']['partial_public_producer_publication_binding_sha256']=audit['publication_binding_sha256']
cell['evidence']['remaining_private_consumer_unimplemented']=False
cell['evidence']['private_consumer_final_source']={'file':str(T),'sha256':sha(t),'lines':206,'review':'pending; no wholeSAU/source/native V credit'}
cell['reuse_plan']['actual_private_consumer_parents']=[
    unit['declaration'],
    'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixMean.actual_source_truncated_matrix_means',
    'AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveIntegral.integral_posSemidef']
cell['reader_contract']['status']='Four complete P folds plus three complete206-line private T folds authored, under unchanged exact statements. Fresh extended code/source/decoder/native/reader acceptance pending; public P only remains the canonical declaration.'
C.write_bytes(dump(cell))
publication.inputs.cache_clear(); publication.load.cache_clear()
publication.check_advance([unit['declaration']],reviewed=False)
print(json.dumps(record))
