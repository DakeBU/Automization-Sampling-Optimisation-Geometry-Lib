"""Independent readback of prior exact-input evidence, not a replay of reasoning."""
import hashlib, json, sys
from pathlib import Path
ROOT=Path('E:/Samplinglib')
sys.path.insert(0,str(ROOT))
from tools import astis_semantic_roundtrip_core as rt
P=ROOT/'runs/20261007-companion-priority/pbps-unit-exponential-product77'
OUT=P/'exact-commit-verification77'
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def raw(p):return sha(Path(p).read_bytes())
checks=[]
def artifact(obj):
    p=Path(obj['path'])
    if not p.is_absolute():p=ROOT/p
    assert raw(p)==obj['RAW_sha256'],str(p)
    checks.append({'path':str(p),'RAW_sha256':raw(p),'match':True})
math=load(P/'root.math77.adoption.json')
for k in ['native_lease','native_complete_named']:artifact(math[k])
for k in ['actual_module','probe','receipt']:artifact(math['fresh_compiler'][k])
decision=load(P/'independent-math77/decision.json')
for k in ['compiler','fake_closure_scan','mathematical_proof','seal_and_parent']:artifact(decision[k])
assert decision['accepted_whole_mathematics'] and decision['logical_premises']==0
audit=load(ROOT/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-UnitExponentialProduct.json')
assert audit['state']=='accepted' and audit['source_review']['reviewer']=='/root/source_review77'
packet=load(P/'source-review.packet.json')
expected=rt.semantic_reviewer_packet(audit)
assert packet==expected
assert packet['packet_sha256']==audit['source_review']['reviewer_packet_sha256']
assert audit['publication_binding_sha256']=='465fcece1be5adf9e62da6bad2639b3d4c65943b35b733b75e6f44227b6e09bf'
assert raw(P/'resume-source-review77/review-run-manifest.json')==audit['source_review']['review_run_sha256']
assert sha(audit['reconstruction']['text'].encode('utf-8'))==audit['reconstruction']['text_sha256']
assert sha(audit['lean']['statement'].encode('utf-8'))==audit['lean']['statement_sha256']
dec=load(P/'root.decoder77.adoption.json')
for k in ['native_lease','native_response','native_complete_run']:artifact(dec[k])
closure=load(P/'anonymous-decoder77/closure.json')
assert closure['source_text_visible'] is False and closure['source_or_proof_input_read'] is False
assert closure['sibling_or_repository_input_read'] is False
for p,h in closure['artifacts_sha256'].items():assert raw(Path(p))==h
blind=load(P/'anonymous-decoder77/parent-packet.json')
assert raw(P/'anonymous-decoder77/parent-packet.json')==closure['packet_raw_sha256']
assert blind==rt.decoder_packet(audit)
assert blind['packet_sha256']==audit['reconstruction']['decoder_packet_sha256']
assert raw(P/'anonymous-decoder77/run-manifest.json')==audit['reconstruction']['decoder_run_sha256']
assert raw(P/'anonymous-decoder77/response.json')==dec['native_response']['RAW_sha256']
assert closure['reconstructed_text_sha256']==audit['reconstruction']['text_sha256']
assert audit['lean']['formalizer']!=audit['source_review']['reviewer']
assert audit['reconstruction']['decoder']!=audit['source_review']['reviewer']
result={'status':'PASS_EXACT_PRIOR_EVIDENCE','verifier_id':'/root/exact_verify77',
    'checked_commit':'24cacd367f9936a68fc709a02b3b051802033aa6',
    'checked_artifacts':checks,'canonical_source_review_packet_equal':True,
    'source_review_run_hash':audit['source_review']['review_run_sha256'],
    'canonical_blind_decoder_packet_equal':True,'decoder_run_hash':audit['reconstruction']['decoder_run_sha256'],
    'publication_binding_sha256':audit['publication_binding_sha256'],
    'prior_independent_math_exact_module':math['fresh_compiler']['actual_module'],
    'separation':{'formalizer':audit['lean']['formalizer'],'decoder':audit['reconstruction']['decoder'],
       'source_reviewer':audit['source_review']['reviewer'],'exact_commit_verifier':'/root/exact_verify77'},
    'limitation':'Artifact hashes and declared source-blind protocol checked. No private hidden reasoning trajectory is fabricated or certified.'}
(OUT/'prior-evidence-readback.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('EXACT PRIOR EVIDENCE PASS')
