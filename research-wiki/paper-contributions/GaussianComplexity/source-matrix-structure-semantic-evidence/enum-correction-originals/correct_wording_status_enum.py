from pathlib import Path
import hashlib,json,sys
sys.path.insert(0,'tools')
import astis_publication as pub
import astis_semantic_roundtrip as rt
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
E=Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-structure-semantic-evidence')
ident='huanjian-gaussian-source-matrix-structure.json'
L=Path('website/content/declaration_lessons')/ident;P=Path('website/content/publications')/ident;A=Path('research-wiki/semantic-roundtrip/audits')/ident
sha=lambda b:hashlib.sha256(b).hexdigest();dump=lambda o:(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
def create(p,b):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(b)
for p in [L,P]:
 o=json.loads(p.read_bytes());s=o['units'][0]['sources'][0] if p==L else o['items'][0]['source']
 assert s['wording_status']=='faithful paraphrase with explicit analytic prerequisites'
 s['wording_status']='faithful paraphrase';p.write_bytes(dump(o))
item=next(i for i in pub.load() if i['id']=='huanjian-gaussian-source-matrix-structure');data=pub.inputs();ctx=pub.review_context(item,item['bindings'][0],data);bh=pub.binding_digest(item,item['bindings'][0],data)
a=json.loads(A.read_bytes());ta=json.loads((E/'private-consumer-source-reviewed.bounded.json').read_bytes())
before=[rt.decoder_packet(x) for x in [a,ta]]
for x in [a,ta]:
 for k in ['semantic_slots','deltas','verdict','source_review','repairs','independent_original_overlay','reader_commit']:x.pop(k,None)
 x['repairs']=[];x['state']='blind-reconstructed'
a['publication_binding_sha256']=bh;a['publication_context']=ctx
tctx=dict(ta['publication_context']);tctx['canonical_public_producer_context']=ctx
ta['publication_context']=tctx;ta['publication_binding_sha256']=sha(json.dumps(tctx,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
assert [rt.decoder_packet(x) for x in [a,ta]]==before
A.write_bytes(dump(a));create(W/'private-consumer-audit.reconstructed.v4.json',dump(ta));create(W/'private-consumer-registry.reconstructed.v4.json',dump({'schema_version':1,'audits':[ta]}));create(W/'candidate-publication-context.v3-enum.json',dump({'publication_binding_sha256':bh,'publication_context':ctx}))
out={'change':'Only source.wording_status enum label corrected in authored lesson and publication. Exact math, source restatement, assumptions, formulas, proof, source-map, code and both decoder packets unchanged.','old_v3_acceptance':'Preserved immutable f9f1880376312fc98f773bfdfee612b795f4434e and original source archive; currentbinding pending freshindependent review.','P_binding':bh,'T_binding':ta['publication_binding_sha256'],'decoder_packets_unchanged':True}
create(E/'wording-enum-correction.json',dump(out));print(json.dumps(out))
