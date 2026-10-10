from pathlib import Path
import json,copy,sys,hashlib
sys.path.insert(0,str(Path('tools').resolve()))
import astis_publication as pub
from astis_frontier import load_cells,validate_cells
R=Path('runs/20261007-companion-priority');r=R/'pbps-macroscopic-centered-range58';pre=R/'pbps-macro-range-preproof58'
j=lambda p:json.loads(Path(p).read_text(encoding='utf-8'))
def w(p,d):Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=Path('.astis/pbps-marginal-gradient51/author-publication58.py');(r/'publication.0.failed.raw.snapshot.py').write_bytes(p.read_bytes())
w(r/'publication.0.diagnosis.json',dict(classification='canonical-declaration-mapping',error='Publication requires one exact canonical declaration per bound Frontier Cell. Three target declarations were mapped to one shared-floor generic canonical declaration.',proof_or_statement_change=False,strict_repair='Retain one SAU and one owner; register three distinct declaration mappings within the connected frontier using existing cells, not a parallel ledger. Rebind current publication context before reviews.'))
plan=j(r/'publication-plan.json');decls=plan['mathematical_declarations'];ids=['ASTIS-SHARED-l2-pullback-range','ASTIS-SW-PBPS-macroscopic-centered-range','ASTIS-SW-PBPS-centered-macro-defect-gap'];sigfiles=['generic-prospective-statement.txt','prospective-statement.txt','consumer-prospective-statement.txt']
basepath=Path('research-wiki/frontier-cells')/(ids[1]+'.json');base=j(basepath);(r/'before-canonical-map58.raw.snapshot.cell.json').write_bytes(basepath.read_bytes())
new=[]
for i,(cid,decl,sf) in enumerate(zip(ids,decls,sigfiles)):
 cell=copy.deepcopy(base);cell['cell_id']=cid;cell['title']=j(Path('website/content/publications')/(plan['slugs'][i]+'.json'))['items'][0]['title'];cell['target_statement']=(pre/sf).read_text(encoding='utf-8');cell['shared_floor_audit']['canonical_declaration']=decl;cell['shared_floor_audit']['canonical_shared_cell']=ids[0];cell['shared_floor_audit']['decision']='new_canonical_shared' if i==0 else 'reuse';cell['reuse_plan']['new_shared_declarations']=[decls[0]];cell['reuse_plan']['reused_declarations']=[] if i==0 else [decls[0]]+base['reuse_plan']['reused_declarations'];cell['parents']=[] if i==0 else ([ids[0]]+base['parents'] if i==1 else [ids[1],'ASTIS-SW-PBPS-l2-macroscopic-mean','ASTIS-SHARED-gaussian-marginal-poincare']);cell['graph_contribution']['focus_targets']=[decl];cell['statement_seal']['signature_digest']=hashlib.sha256((pre/sf).read_bytes().replace(b'\r\n',b'\n')).hexdigest();new.append(cell)
errors=validate_cells([x for x in load_cells() if x['cell_id']!=ids[1]]+new);assert not errors,errors
for cell in new:
 path=Path('research-wiki/frontier-cells')/(cell['cell_id']+'.json');assert cell['cell_id']==ids[1] or not path.exists();w(path,cell)
for i,slug in enumerate(plan['slugs']):
 path=Path('website/content/publications')/(slug+'.json');d=j(path);item=d['items'][0];item['bindings'][0]['cell']=ids[i]
 for k in ['statement_seal','proof_digestion','purification']:item[k]=copy.deepcopy(new[i][k])
 if i==0:
  item['bindings'][0]['assumption_deltas'][0]=dict(source='Source macro space uses a real L2 pullback factorization under its probability law.',lean='Arbitrary measurable spaces and measures; only the genuine measure-preserving map is an input.',classification='generalization',reason='Independent general background proved using fixed Mathlib real-valued measurable factorization and pushforward MemLp; no probability/StandardBorel/finite-dimensional requirement is added.')
 w(path,d)
pub.inputs.cache_clear();pub.load.cache_clear();data=pub.inputs()
for slug,aid in zip(plan['slugs'],plan['audit_ids']):
 bound=next(x for x in pub.load() if x['id']==slug);binding=bound['bindings'][0];p=Path('research-wiki/semantic-roundtrip/audits')/(aid+'.json');a=j(p);assert a['state']=='draft' and a['source_review']['state']=='pending';a['publication_binding_sha256']=pub.binding_digest(bound,binding,data);a['publication_context']=pub.review_context(bound,binding,data);w(p,a)
plan['active_cells']=ids;w(r/'publication-plan.json',plan);w(r/'canonical-mapping58.json',dict(advance_id=j(r/'claim.json')['advance_id'],one_owner=j(r/'claim.json')['owner'],mappings=[dict(cell=cid,declaration=decl) for cid,decl in zip(ids,decls)],boundary='Distinct exact declaration mappings for the same connected SAU. No additional theorem/Goal/owner/ledger or proof change.'))
pub.inputs.cache_clear();pub.load.cache_clear();pub.check_advance(decls,reviewed=False)
print('Three exact canonical mappings; one SAU/owner; actual base publication gate PASS.')
