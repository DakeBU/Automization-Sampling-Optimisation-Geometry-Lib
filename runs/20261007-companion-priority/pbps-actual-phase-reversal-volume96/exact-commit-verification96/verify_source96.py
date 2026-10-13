"""Independent mechanical audit of native source acceptance and metadata transfer."""
from pathlib import Path
import hashlib,json,gzip,sys,subprocess,copy
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;B=O.parent;S=B/'independent-final-source96'
C=sys.argv[1];sha=lambda b:hashlib.sha256(b).hexdigest();load=lambda p:json.loads(p.read_bytes())
canon=lambda v:json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def rel(p):return p.relative_to(R).as_posix()
def info(p):return dict(path=rel(p),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()==C
freeze=load(O/'input-freeze96.json');assert freeze['status']=='PASS' and freeze['verified_commit']==C
v=load(S/'semantic-verdict96.native.json');run=load(S/'source-review-run96.native.json');manifest=load(S/'closed-raw-manifest96.native.json')
assert info(S/'semantic-verdict96.native.json')['raw_sha256']=='0870916f0eaed150aad843fd59acb679501e7750590e4dc6c8f4c38e3b84e5d0'
assert info(S/'closed-raw-manifest96.native.json')['raw_sha256']=='12932cde8b249950207d6be783a38a1d61b43f555acbcd59f04bff9990bdf46f'
assert info(S/'source-review-run96.native.json')['raw_sha256']==v['review_run_sha256']=='2153aa3921fb80979b5f00d99a0769e312e764a5b8a5a5804966d612d62ce595'
a=load(R/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualPhaseReversalVolume.json')
assert a['state']==v['source_review']['state']=='accepted'
for key in ['semantic_slots','deltas','verdict','repairs']:assert a[key]==v[key],key
assert len(v['semantic_slots'])==7 and not any(x['blocking'] for x in v['deltas']) and not v['repairs']
assert v['verdict']=='equivalent-after-elaboration' and v['independent_from_formalizer'] and v['independent_from_decoder']
sr=copy.deepcopy(v['source_review']);sr['evidence']=sr['run_artifact'];assert sr==a['source_review']
assert run['reviewer']==v['reviewer']=='source_final96'
assert not run['prior_reviewer_decisions_seen'] and not run['prior_audit_verdicts_seen']
assert run['independent_from_formalizer'] and run['independent_from_decoder'] and run['blocking_semantic_deltas']==0
packet=load(B/'reviewer-packet96-v2.json');ph=packet.pop('packet_sha256')
assert sha(canon(packet))==ph==v['reviewer_packet_sha256']==a['source_review']['reviewer_packet_sha256']
assert info(B/'reviewer-packet96-v2.json')['raw_sha256']==run['reviewer_packet_raw_sha256']==v['reviewer_packet_raw_sha256']
for flag in ['all_six_source_binders','all_eight_literal_lets','all_thirteen_conjuncts','zero_normal','rank_zero','all_real_times','actual_sqrt_eta_scaling','actual_product_volume','real_integrable_A6']:assert run[flag],flag
assert not run['fake_closure_scan_matches']
cov=load(S/'compiled-source-coverage96.native.json');primary=(R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html').read_bytes()
assert len(cov['regions'])==19
for x in cov['regions']:
 b=primary[x['byte_start']:x['byte_end_exclusive']];assert len(b)==x['bytes'] and sha(b)==x['raw_sha256'] and x['raw_slice_verified'],x['html_id']
pubpath=R/'website/content/publications/pbps-actual-phase-reversal-volume.json';current=load(pubpath)
oldraw=gzip.decompress((B/'publication-before-final-coverage96.raw.gz').read_bytes());old=json.loads(oldraw)
record=next(x for x in manifest['inputs'] if x['path']==rel(pubpath));assert sha(oldraw)==record['raw_sha256'] and len(oldraw)==record['bytes']
transfer=load(B/'source-admission-transfer96.json');assert old['items'][0]['source_proof_coverage']==transfer['coverage_before']
old['items'][0]['source_proof_coverage']=transfer['coverage_after'];assert old==current
sys.path[:0]=[str(R),str(R/'tools')]
from tools import astis_publication as pub
item=current['items'][0];b=item['bindings'][0];binding=pub.binding_digest(item,b)
assert binding==a['publication_binding_sha256']==v['publication_binding_sha256']==transfer['publication_binding_unchanged']=='3e5f721b28cd99ba9a7a9ea8d0087f5b1024abf1b82788b6f4ffa650747d82ae'
before=json.loads(oldraw);assert pub.binding_digest(before['items'][0],before['items'][0]['bindings'][0])==binding
assert item['source_proof_coverage']['coverage_report']==rel(S/'compiled-source-coverage96.native.json')
assert v['exposition_review']['verdict']=='accepted' and v['exposition_review']['seven_exact_proof_regions']
out=dict(status='PASS',verified_commit=C,native_verdict=info(S/'semantic-verdict96.native.json'),native_run=info(S/'source-review-run96.native.json'),closed_native_manifest=info(S/'closed-raw-manifest96.native.json'),review_run_hash_recipe='SHA256 of exact native run bytes, not canonical JSON',reviewer_packet_sha256=ph,publication_binding_sha256=binding,canonical_fields_copied_exactly=True,source_review_evidence_path_only_normalization=True,publication_metadata_only_coverage_update=True,reviewed_original_publication_raw_sha256=sha(oldraw),source_regions_verified=19,six_source_hypotheses=True,seven_exposition_regions=True,scope=run['boundary'])
p=O/'source-acceptance96.native.json';assert not p.exists();p.write_bytes((json.dumps(out,ensure_ascii=False,indent=2)+'\n').encode());print('PASS native source acceptance and exact coverage-only publication transfer')
