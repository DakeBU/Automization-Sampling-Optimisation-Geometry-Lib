"""Export only an anonymous private-consumer supplement, with no public binding credit."""
from pathlib import Path
import hashlib
import json
import sys
sys.dont_write_bytecode=True
sys.path.insert(0,'tools')
import astis_semantic_roundtrip as semantic
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
N=Path('.astis/semantic-neutral-20261113/t_decode_vr_91ad')
sha=lambda raw:hashlib.sha256(raw.encode() if isinstance(raw,str) else raw).hexdigest()
dump=lambda obj:(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
def create(p,raw):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(raw)
sig=(W/'consumer-signature.original.txt').read_text()
assert sha(sig)=='95e81a02e5302de9a42e3b60038ffad6195315ac2eca99a4e6abb39978609f7e'
binders,result=sig.split(' :\n',1)
literal='∀ '+binders+',\n'+result
old=json.loads(Path('research-wiki/semantic-roundtrip/audits/huanjian-gaussian-source-matrix-variance.json').read_bytes())
log=Path('.astis/huanjian-resume-20261103/20261112T164441583114Z-source-matrix-variance-final-P-T-exact-proof-value-kernel-first.log').read_text()
roots=[line.split('PASS ',1)[1] for line in log.splitlines() if line.startswith('ACTUAL_FINAL_R9_ROOT_PROOF_VALUE_SEALED_KERNEL_APPLICATION_PASS ')]
assert len(roots)==2
name=next(n for n in roots if n.endswith('.actual_source_centered_variance_bounds'))
source=('For the original r=q+1 independent standard d-dimensional Gaussian columns and only2q+1<d, let Yi be the same literal closed-cutoff physical-row tensor matrices. '
    'Let Mi be each actual expectation under that original product probability measure and Zi=Yi-Mi. Let wi=cos((2q+1)theta_i), on the exact source midpoint grid. '
    'Every ordinary Zi squared and every ordinary (wi times Zi) squared is Bochner integrable. Both sums over physical rows of those actual matrix expectations have Euclidean operator norm at most2r(r+2)/d. '
    'This private implementation consumer covers only the centered and cosine-weighted variance comparisons; no concentration or main lower bound is included.')
audit={'id':'ASTIS-RT-SUPPLEMENT-20261112-GaussianSourceCenteredConsumer',
    'state':'draft','source':{**old['source'],'source_id':'private-actual-centered-variance-consumer-supplement','anchor':'arXiv2610.20492v1 C.2 p14 Ex118/120','original_text':source,'text_sha256':sha(source)},
    'lean':{'declaration':name,'file':'Tests/GaussianComplexityFixedSpectrumSourceMatrixVariance.lean',
        'statement':literal,'statement_sha256':sha(literal),'formalizer':'huanjian_gc_20261112_source_matrix_variance',
        'compiled':True,'decoder_context':old['lean']['decoder_context']},
    'reconstruction':{},'semantic_slots':{},'deltas':[],'verdict':'pending','source_review':{'state':'pending'},'repairs':[],
    'supplement_only':'Private implementation statement, no new public binding or canonical status. Review joins the full R9 public-owner source/whole-consumer audit.'}
packet=semantic.decoder_packet(audit)
create(W/'private-centered-consumer-supplement.audit-draft.json',dump(audit))
create(N/'input.json',dump(packet))
record={'neutral_input':str(N/'input.json'),'raw_sha256':sha((N/'input.json').read_bytes()),
    'canonical_packet_sha256':packet['packet_sha256'],'anonymous_statement_sha256':sha(literal),
    'exact_actual_private_const':name,'exact_final_file_sha256':sha(Path(audit['lean']['file']).read_bytes()),
    'source_or_implementation_not_sent_to_decoder':True,'public_binding_or_source_status_credit':False}
create(W/'centered-decoder-supplement-record.json',dump(record))
print(json.dumps(record))
