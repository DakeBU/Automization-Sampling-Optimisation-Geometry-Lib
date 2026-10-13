from pathlib import Path
import gzip,hashlib,json,re,subprocess,sys
root=Path.cwd();r=Path('runs/20261007-companion-priority/pbps-centered-defect59');out=r/'integration59/generated-context-preservation';out.mkdir(exist_ok=False)
sha=lambda b:hashlib.sha256(b).hexdigest()
plan=json.loads((r/'publication-plan.json').read_bytes())
owned={'AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl','runs/substantive_advances.jsonl'}|{'research-wiki/frontier-cells/'+x+'.json' for x in plan['active_cells']}
graphpaths={'docs/module-graph.svg','docs/assets/astis_lean_arsenal_module_graph.svg','research-wiki/sampling-sde-library/lean-leaf-module-graph.md','research-wiki/retrieval-index/astis-lean-arsenal-module-graph.json'}
changed=subprocess.check_output(['git','diff','--name-only'],text=True).splitlines();rows=[]
for name in changed:
 if name in owned:continue
 assert name in graphpaths or name=='MANIFEST.md' or name.startswith(('agent-briefs/','docs/assets/','research-wiki/')),name
 p=Path(name);current=p.read_bytes();baseline=subprocess.check_output(['git','show','HEAD:'+name]);snapshot=out/(sha(name.encode())+'.emitted.raw.gz');snapshot.write_bytes(gzip.compress(current,mtime=0));rows.append(dict(path=name,emitted_raw_sha256=sha(current),baseline_raw_sha256=sha(baseline),emitted_snapshot=snapshot.as_posix(),action='retained affected aggregate then enriched from canonical cards' if name in graphpaths else 'restored root-generated unrelated changes to exact HEAD bytes'))
 if name not in graphpaths:p.write_bytes(baseline)
index=Path('research-wiki/retrieval-index/astis-lean-arsenal-module-graph.json');data=json.loads(index.read_bytes());preserved=[]
for item in data['modules']:
 name='research-wiki/sampling-sde-library/cards/'+item['module']+'.md';q=subprocess.run(['git','show','HEAD:'+name],capture_output=True)
 if q.returncode:continue
 text=q.stdout.decode('utf-8');old={}
 for label,key in [('Layer','layer'),('Purpose','summary'),('Mathlib-quality status','status')]:
  match=re.search(r'^- '+re.escape(label)+r': (.*)$',text,re.M)
  if match and match.group(1).strip():old[key]=match.group(1).rstrip('\r')
 for key,value in old.items():item[key]=value
 if old:preserved.append(dict(module=item['module'],canonical_card=name,card_raw_sha256=sha(q.stdout),metadata=old))
name='AutoSamplingTheory.ExampleCases.ProximalBPS.CenteredDefectOperator';item=next(x for x in data['modules'] if x['module']==name);item.update(layer='SampleWiki paper route',summary='Actual stationary reflected Gaussian kernel yields the same selfadjoint real L2 mean operator, canonical constant and closed mean-zero restriction; full and centered squared defects are positive.',status='Independent exact-science59 verified at 2d6cd016; sharp coercivity and centered squared-defect unit are exercised in the real Test. Gamma/root/dynamics/main/error/cost/composition remain open.')
data['ledger']='research-wiki/sampling-sde-library/lean-leaf-module-graph.md';index.write_text(json.dumps(data,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
sys.path.insert(0,str(root/'tools'));import astis
for name in ['docs/module-graph.svg','docs/assets/astis_lean_arsenal_module_graph.svg']:Path(name).write_text(astis.arsenal_module_graph_svg(data['modules']),encoding='utf-8',newline='\n')
Path(data['ledger']).write_text(astis.arsenal_module_graph_markdown(data['modules']),encoding='utf-8',newline='\n')
Path('research-wiki/sampling-sde-library/cards/'+item['module']+'.md').write_text(astis.arsenal_module_card_text(item),encoding='utf-8',newline='\n')
(out/'manifest.json').write_text(json.dumps(dict(scope='Preserve existing collaborator purposes/source boundaries and unrelated legacy frontiers after actual generator commands; keep exact current source/import/declaration inventory and affected graph views',emitted_snapshots=rows,preserved_canonical_metadata=preserved,new_actual_module=item,all_existing_cards_retained_from_HEAD=True,no_Lean_or_source_review_changes=True),ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Restored',len(rows)-len(graphpaths),'unrelated generated files; preserved canonical module metadata for',len(preserved),'nodes; retained current',len(data['modules']),'module scan inventory and actual59 module card. No mathematical status inferred from graph scan.')
