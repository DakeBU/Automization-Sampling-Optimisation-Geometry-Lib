from pathlib import Path
import hashlib,json,sys
R=Path(__file__).resolve().parents[3];r=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'tools'))
import astis_semantic_roundtrip as rt, astis_publication as pub, astis_advance as adv
load=lambda p:json.loads(p.read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,x):p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
def pin(p):return dict(path=p.relative_to(R).as_posix(),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
def fresh(p,x):assert not p.exists();save(p,x)
def verify(rows):
    for x in rows:
        p=Path(x['path']);p=p if p.is_absolute() else R/p
        assert sha(p.read_bytes())==x['raw_sha256'],x['path']
        if 'bytes' in x:assert p.stat().st_size==x['bytes']
m=r/'independent-whole-math93/scoped-classical93';mm=m/'closed-RAW-scoped-classical93.native.json'
assert sha(mm.read_bytes())=='c978d756ee6c48577cbd51bd4e3c74342e9409428ed320b548061d6f39eb01ed'
verify(load(mm)['artifacts']);mn=load(m/'scoped-classical-transfer93.native.json')
assert sha((m/'scoped-classical-transfer93.native.json').read_bytes())=='3f8ec290bf6f82bab8621d29803d29ba63fa4b563483dc8c8d1ea0866a7b6a91'
assert mn['decision']=='ACCEPT_SCOPED_CLASSICAL_WHOLE_MATHEMATICS_TRANSFER' and not mn['necessary_fixes']
assert all(x['exit_code']==0 for x in mn['kernel_checks']);verify([mn['new_module']])
fresh(r/'root.math93.scoped-adoption.json',dict(status='ACCEPTED_INDEPENDENT_MATH_KERNEL_TRANSFER_ONLY',decision=pin(m/'scoped-classical-transfer93.native.json'),manifest=pin(mm),VERIFIED=False))
d=r/'primary-source93/scoped-transfer93';sm=d/'closed-RAW-transfer93.native.json';n=load(d/'source-review-decision93.native.json')
assert sha(sm.read_bytes())=='0fde87095c92ff54b2fbc704b83efdc049ff31b1e2c0f1079ae5cfbb5b31c788'
s=load(sm);verify(s['inputs']+s['outputs'])
assert sha((d/'source-review-decision93.native.json').read_bytes())=='4428adaadb0e9fb1b47e3b35f872669a8a1313125d30937dc4108ce7784f4b29'
rr=load(d/'review-run93.native.json')
assert rt.sha256_json({k:v for k,v in rr.items() if k!='review_run_sha256'})==n['review_run_sha256']==rr['review_run_sha256']
assert n['source_review_status']=='accepted' and not n['blocking_findings'] and not n['repairs']
ap=R/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualFiniteCountPath.json';a=load(ap)
assert a['state']=='blind-reconstructed'
p=rt.semantic_reviewer_packet(a);assert p==load(r/'anti-anchored.review93.v3.json') and p['packet_sha256']==n['reviewer_packet_sha256']
assert a['publication_binding_sha256']==n['publication_binding_sha256']
fresh(r/'audit.before-scoped-source93.json',a)
a.update(state='accepted',semantic_slots=n['semantic_slots'],deltas=n['deltas'],verdict=n['verdict'],source_review=dict(state='accepted',reviewer=n['reviewer'],independent_from_formalizer=True,independent_from_decoder=True,evidence=n['review_evidence'],review_run_sha256=n['review_run_sha256'],reviewer_packet_sha256=n['reviewer_packet_sha256'],run_artifact=n['review_run_artifact'],native_manifest=pin(sm)))
save(ap,a);pub.inputs.cache_clear();pub.load.cache_clear();pub.check_advance([a['lean']['declaration']],reviewed=True)
fresh(r/'root.source93.scoped-adoption.json',dict(status='ACCEPTED_INDEPENDENT_SOURCE_FIDELITY_ONLY',decision=pin(d/'source-review-decision93.native.json'),manifest=pin(sm),canonical_packet_sha256=p['packet_sha256'],publication_binding_sha256=n['publication_binding_sha256'],VERIFIED=False))
claim=load(r/'claim.json');cp=R/'research-wiki/frontier-cells'/f"{claim['frontier_cell']}.json";c=load(cp)
c['evidence']['proof_review']=(m/'scoped-classical-transfer93.native.json').relative_to(R).as_posix()
c['evidence']['source_review']=(d/'source-review-decision93.native.json').relative_to(R).as_posix()
c['evidence']['focused_checks'][0]['evidence']=(r/'checks93/scoped-classical-leaf/receipt.json').relative_to(R).as_posix()
c['source_proof_coverage']['compiled_source_review']=c['evidence']['source_review']
save(cp,c)
e=load(r/'proved-local93.json');e.update(independent_math=pin(r/'root.math93.scoped-adoption.json'),source_review=pin(r/'root.source93.scoped-adoption.json'),focused_checks=[pin(r/'checks93/scoped-classical-leaf/receipt.json')],source_proof_coverage=c['source_proof_coverage'])
fresh(r/'proved-local93.scoped.json',e)
print('Independent scoped-Classical math/source transfers adopted; no self-VERIFIED.')
