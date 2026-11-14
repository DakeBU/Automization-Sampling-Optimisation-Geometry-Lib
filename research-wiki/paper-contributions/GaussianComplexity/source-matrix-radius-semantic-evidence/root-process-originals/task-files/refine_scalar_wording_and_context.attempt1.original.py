from pathlib import Path
import json,sys,hashlib
sys.path.insert(0,'tools')
import astis_publication as pub
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
E=Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-radius-semantic-evidence')
ident='huanjian-gaussian-source-matrix-radius'
L=Path('website/content/declaration_lessons')/(ident+'.json')
S=Path('website/content/publications')/(ident+'.json')
A=Path('research-wiki/semantic-roundtrip/audits')/(ident+'.json')
dump=lambda o:(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
sha=lambda b:hashlib.sha256(b).hexdigest()
def create(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(b)
for p in [L,S,A]:create(W/'authored-v1-originals'/p.name,p.read_bytes())
for p,key in [(L,'units'),(S,'items')]:
    v=json.loads(p.read_bytes());row=v[key][0]
    assert 'Positivity of \\(d,r,L\\)' in row['assumptions'][0]
    row['assumptions'][0]=row['assumptions'][0].replace('Positivity of \\(d,r,L\\) is derived internally.','Positivity of \\(d,r\\) and nonnegativity of \\(L\\) are derived internally.')
    p.write_bytes(dump(v))
data=pub.inputs();item=next(x for x in pub.load() if x['id']==ident);b=item['bindings'][0]
ctx=pub.review_context(item,b,data);bh=pub.binding_digest(item,b,data)
a=json.loads(A.read_bytes());a['publication_binding_sha256']=bh;a['publication_context']=ctx;A.write_bytes(dump(a))
create(W/'candidate-publication-context.v2.json',dump({'publication_binding_sha256':bh,'publication_context':ctx}))
t=json.loads((W/'private-consumer-audit.bound.v1.json').read_bytes());tctx=t['publication_context'];tctx['canonical_public_producer_context']=ctx
t['publication_binding_sha256']=sha(json.dumps(tctx,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
create(W/'private-consumer-audit.bound.v2.json',dump(t));create(W/'private-consumer-registry.bound.v2.json',dump({'schema_version':1,'audits':[t]}))
print(json.dumps({'P_binding_sha256':bh,'private_T_binding_sha256':t['publication_binding_sha256'],'change':'Only scalar wording d/r positive and L nonnegative, matching actual internal estimate. Code, formulae, statements and anonymous decoder inputs unchanged.'}))
