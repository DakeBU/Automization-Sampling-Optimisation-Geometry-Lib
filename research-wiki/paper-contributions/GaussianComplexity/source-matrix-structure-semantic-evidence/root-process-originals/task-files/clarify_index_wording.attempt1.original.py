from pathlib import Path
import hashlib,json,sys
sys.path.insert(0,'tools')
import astis_publication as pub
import astis_semantic_roundtrip as rt
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
E=Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-structure-semantic-evidence')
ident='huanjian-gaussian-source-matrix-structure'
A=Path('research-wiki/semantic-roundtrip/audits')/(ident+'.json')
L=Path('website/content/declaration_lessons')/(ident+'.json')
P=Path('website/content/publications')/(ident+'.json')
T=Path('Tests/GaussianComplexityFixedSpectrumSourceMatrixStructure.lean')
sha=lambda b:hashlib.sha256(b).hexdigest()
dump=lambda o:(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
def create(p,b):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(b)
for p in [L,P,A,W/'private-consumer-audit.reconstructed.v2.json']:
 create(E/'author-originals/index-wording-v1-originals'/p.name,p.read_bytes())
old=r'Source index \(i\) corresponds to Lean index \(i.val+1\).'
new=r'For a Lean index \(j:\mathrm{Fin}\,d\), the corresponding source index is \(j.val+1\).'
for p in [L,P]:
 o=json.loads(p.read_bytes());rows=o['units'][0]['assumptions'] if p==L else o['items'][0]['assumptions']
 assert sum(old in s for s in rows)==1
 for i,s in enumerate(rows):rows[i]=s.replace(old,new)
 p.write_bytes(dump(o))
item=next(i for i in pub.load() if i['id']==ident);data=pub.inputs();binding=item['bindings'][0]
ctx=pub.review_context(item,binding,data);bh=pub.binding_digest(item,binding,data)
a=json.loads(A.read_bytes());before=rt.decoder_packet(a);a['publication_binding_sha256']=bh;a['publication_context']=ctx
assert rt.decoder_packet(a)==before;A.write_bytes(dump(a))
create(W/'candidate-publication-context.v2.json',dump({'publication_binding_sha256':bh,'publication_context':ctx}))
ta=json.loads((W/'private-consumer-audit.reconstructed.v2.json').read_bytes());tctx=dict(ta['publication_context']);tctx['canonical_public_producer_context']=ctx
ta['publication_context']=tctx;ta['publication_binding_sha256']=sha(json.dumps(tctx,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
create(W/'private-consumer-audit.reconstructed.v3.json',dump(ta));create(W/'private-consumer-registry.reconstructed.v3.json',dump({'schema_version':1,'audits':[ta]}))
out={'reason':'Independent source reviewer identified reversed index-correspondence wording; clarify that source_i=Lean_j.val+1. Mathematical statements, code, source restatement and both blind decodes unchanged.','P_binding_sha256':bh,'T_binding_sha256':ta['publication_binding_sha256'],'previous_source_context_preserved':True,'current_source_review':'requires independent current v2 packet review'}
create(E/'index-wording-clarification.json',dump(out));print(json.dumps(out))
