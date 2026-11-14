"""Repair the actual reader failure; renew changed context without replaying old review."""
from pathlib import Path
import json,hashlib,subprocess,sys
sys.path.insert(0,'tools')
import astis_publication as pub
import astis_semantic_roundtrip as rt
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
E=Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-radius-semantic-evidence')
R=E/'reader-source-label-repair'
ident='huanjian-gaussian-source-matrix-radius'
L=Path('website/content/declaration_lessons')/(ident+'.json')
A=Path('research-wiki/semantic-roundtrip/audits')/(ident+'.json')
C=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-radius.json')
sha=lambda b:hashlib.sha256(b).hexdigest()
dump=lambda o:(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
git=lambda *a:subprocess.check_output(['git',*a])
def create(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(b)
head=git('rev-parse','HEAD').decode().strip();assert head=='7c92a4dbb0f1747b8150574981b501c16af858c9'
assert not git('diff','HEAD','--name-only') and not git('diff','--cached','--name-only')
for tag,p in [('lesson',L),('audit',A),('cell',C)]:create(R/'originals'/('before-'+tag+'.json'),p.read_bytes())
v=json.loads(L.read_bytes());src=v['units'][0]['sources'][0];assert not src.get('label');src['label']=src['anchor']
L.write_bytes(dump(v))
data=pub.inputs();item=next(x for x in pub.load() if x['id']==ident);binding=item['bindings'][0]
ctx=pub.review_context(item,binding,data);bh=pub.binding_digest(item,binding,data)
a=json.loads(A.read_bytes());oldbinding=a['publication_binding_sha256']
for k in ['semantic_slots','deltas','verdict','source_review','independent_original_overlay']:a.pop(k,None)
a['state']='blind-reconstructed';a['publication_binding_sha256']=bh;a['publication_context']=ctx
a['reader_label_repair']={'prior_reader_commit':'4b58558a6003444af9964fba077e74bf5e63052d','prior_binding_sha256':oldbinding,'new_binding_sha256':bh,'scope':'Single source citation display label added. Full code, theorem statements, mathematical prose/formulae and blind packets unchanged. Fresh incremental source acceptance pending.'}
A.write_bytes(dump(a))
t=json.loads((E/'private-consumer-source-reviewed.bounded.json').read_bytes())
for k in ['semantic_slots','deltas','verdict','source_review','independent_original_overlay']:t.pop(k,None)
t['state']='blind-reconstructed';tctx=t['publication_context'];tctx['canonical_public_producer_context']=ctx
t['publication_binding_sha256']=sha(json.dumps(tctx,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
create(W/'private-consumer-audit.label-repair.reconstructed.v2.json',dump(t))
for a0,n in [(a,'fresh-P-review.label-repair.v2.json'),(t,'fresh-T-review.label-repair.v2.json')]:
    pkt=rt.semantic_reviewer_packet(a0);create(W/n,dump(pkt));create(R/n,dump(pkt))
cell=json.loads(C.read_bytes());cell['evidence']['source_label_reader_repair']={'status':'fresh incremental source/reader reacceptance pending','old_source_review_originals_retained':True,'changed':'One required label added to first lesson.sources citation','new_publication_binding_sha256':bh};cell['reader_contract']['status']='Actual immutable4b585 production generator failed on missing source label; single citation label repaired, new context source review and actual reader retry pending.';C.write_bytes(dump(cell))
native=Path('.astis/semantic-neutral-20261113/radius_native_5bf8');rp=native/'receipts/20261113T013532500465Z-reader-build.json'
create(R/'native-original-failure-receipt.json',rp.read_bytes())
create(R/'diagnosis.json',dump({'class':'IMPLEMENTATION_FAILED','actual_failure':'production declaration_lessons.render_unit → source_citation_anchor KeyError:label','old_reader_commit':'4b58558a6003444af9964fba077e74bf5e63052d','repair':'Only required first citation display label added, equal to its existing source anchor. No CSS or fixture normalization.','math_code_changed':False,'old_binding':oldbinding,'new_binding':bh,'fresh_review_required':True}))
paths=[L,A,C,*[p for p in R.rglob('*') if p.is_file()]]
spec=W/'source-label-repair-paths.private.nul';create(spec,b'\0'.join(str(p).encode() for p in paths)+b'\0')
subprocess.run(['git','add','-f','--pathspec-from-file='+str(spec),'--pathspec-file-nul'],check=True)
assert set(git('diff','--cached','--name-only').decode().splitlines())==set(map(str,paths))
subprocess.run(['git','commit','--quiet','-m','Repair Gaussian radius source citation label after real reader failure'],check=True)
commit=git('rev-parse','HEAD').decode().strip()
result={'successor_reader_commit':commit,'actual_failed_reader_commit':'4b58558a6003444af9964fba077e74bf5e63052d','single_source_label_change':True,'P_binding_sha256':bh,'private_T_binding_sha256':t['publication_binding_sha256'],'fresh_P_packet_sha256':json.loads((W/'fresh-P-review.label-repair.v2.json').read_bytes())['packet_sha256'],'fresh_T_packet_sha256':json.loads((W/'fresh-T-review.label-repair.v2.json').read_bytes())['packet_sha256'],'ledger_mutations':0}
create(W/'actual-source-label-repair-commit.json',dump(result));print(json.dumps(result))
