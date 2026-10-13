from pathlib import Path
import hashlib,json,os,sys
sys.path.insert(0,str(Path.cwd()/'tools'));import astis as a
r=Path('runs/20261007-companion-priority/pbps-actual-finite-jump-recursion76')
out=Path(os.environ['ASTIS_FOREGROUND_OBSERVER_DIR'])
v=json.loads((r/'root.exact-verification76.adoption.json').read_bytes());assert v['native_verified']
records=a.lean_module_records();name='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteJumpRecursion'
selected=[x for x in records if x['module']==name];assert len(selected)==1
graph=a.arsenal_module_graph_svg(records)
payload={'generated':a.now_stamp(),'module_graph_svg':'docs/module-graph.svg','ledger':a.rel(a.SAMPLING_LIBRARY_DIR/'lean-leaf-module-graph.md'),'modules':records}
targets={
 Path('docs/module-graph.svg'):graph,
 Path('docs/assets/astis_lean_arsenal_module_graph.svg'):graph,
 a.SAMPLING_LIBRARY_DIR/'lean-leaf-module-graph.md':a.arsenal_module_graph_markdown(records),
 a.RETRIEVAL_INDEX_DIR/'astis-lean-arsenal-module-graph.json':json.dumps(payload,indent=2,sort_keys=True,ensure_ascii=False)+'\n',
 a.SAMPLING_LIBRARY_DIR/'cards'/f'{a.slugify(name)}.md':a.arsenal_module_card_text(selected[0])
}
rows=[]
for i,(p,text) in enumerate(targets.items()):
 if p.exists():(out/f'{i}.before.exactraw.snapshot').write_bytes(p.read_bytes())
 # Trim generator trailing ASCII whitespace before freezing the affected outputs.
 text='\n'.join(line.rstrip(' \t\r') for line in text.split('\n'))
 p.write_text(text,encoding='utf8',newline='\n');b=p.read_bytes()
 rows.append(dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest()))
(out/'affected-graph.receipt.json').write_text(json.dumps(dict(status='AFFECTED_MODULE_GRAPH_AND_ONE_CARD_REFRESH_WITH_EXISTING_PURE_GENERATORS',actual_root_PID=os.getpid(),canonical_tool_source_changed=False,official_whole_module_graph_refresh_command_run=False,used_existing_APIs=['lean_module_records','arsenal_module_graph_svg','arsenal_module_graph_markdown','arsenal_module_card_text'],outputs=rows,unrelated_cards_external_indexes_leaf_docs_and_manifest_untouched=True,reason='Regenerate only the affected existing graph views and one actual module card; avoid whole-site external-card/leaf-document side effects. Underlying formal dependency graph and cell graph-check are separate required gates.',mathematical_credit=False,Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS76 existing graph generators refreshed five affected views/card only; no unrelated library or source changes.')
