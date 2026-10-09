from pathlib import Path
import hashlib,json,sys
root=Path.cwd();sys.path.insert(0,str(root/'tools'));import astis_publication as pub,astis_semantic_roundtrip as rt
r=root/'runs/20261007-companion-priority/pbps-centered-root64';d=r/'lesson-dependency64';d.mkdir(exist_ok=False)
load=lambda p:json.loads(Path(p).read_bytes())
def pin(p):
 b=p.read_bytes();return dict(path=p.resolve().as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),lf_sha256=hashlib.sha256(b.replace(b'\r\n',b'\n')).hexdigest(),bytes=len(b))
slug='pbps-centered-root-order-inverse';aid='ASTIS-RT-20261009-PBPSCenteredRootOrderInverse'
lp=root/'website/content/declaration_lessons'/f'{slug}.json';ap=root/'research-wiki/semantic-roundtrip/audits'/f'{aid}.json'
prior=[]
for p in [lp,ap]:
 sp=d/(p.parent.name+'-'+p.name+'.before.exactraw.snapshot');sp.write_bytes(p.read_bytes());prior.append(dict(original=pin(p),explicit_exact_raw_snapshot=pin(sp)))
codefiles=load(r/'claim.json')['proposed_files'];before=[pin(root/p) for p in codefiles]
x=load(lp);decl='AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareOrder.positive_square_order';assert decl not in x['units'][0]['astis_dependencies'];x['units'][0]['astis_dependencies'].append(decl)
lp.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
pub.inputs.cache_clear();pub.load.cache_clear();data=pub.inputs();item=next(x for x in pub.load() if x['id']==slug);binding=item['bindings'][0]
a=load(ap);assert a['state']=='draft';a['publication_binding_sha256']=pub.binding_digest(item,binding,data);a['publication_context']=pub.review_context(item,binding,data)
assert rt.decoder_packet(a)==load(root/'.astis/decoder-64/packet1.json')
ap.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
assert before==[pin(root/p) for p in codefiles]
(d/'supplement.json').write_text(json.dumps(dict(status='PUBLICATION_DEPENDENCY_LIST_COMPLETED_ONLY',reason='The actual reader must name its newly compiled shared positive-square-order ingredient as an exact dependency. Production import and connected frontier parent were already present. No proof/header/statement/formula/3+9 excerpt changed.',original_freeze=pin(r/'math-freeze.json'),finite_historical_maps=prior,current=[pin(lp),pin(ap)],production_unchanged=before,anonymous_packet_unchanged=pin(root/'.astis/decoder-64/packet1.json'),new_assumption=False),indent=2)+'\n',encoding='utf-8',newline='\n')
pub.check_advance(load(r/'publication-plan.json')['mathematical_declarations'],reviewed=False)
print('Reader dependency supplement PASS; all three Lean files, exact statements and anonymous packet unchanged; two prior metadata bytes retained by qualified snapshots.')
