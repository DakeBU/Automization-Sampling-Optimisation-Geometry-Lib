from pathlib import Path
import json,subprocess
r=Path('runs/20261007-companion-priority/pbps-b4-corrector-perturbation72');plan=json.loads((r/'publication-plan.json').read_bytes())
v=json.loads((r/'root.exact-verification72.adoption.json').read_bytes());head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();assert v['native_verified'] and v['verified_commit']==head
paths=subprocess.check_output(['git','-c','core.autocrlf=false','diff','--name-only'],text=True).splitlines()
keep={'AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl','runs/substantive_advances.jsonl','conversion-windows/ASTIS-SW-PBPS-2026.md','docs/module-graph.svg','docs/assets/astis_lean_arsenal_module_graph.svg','research-wiki/sampling-sde-library/lean-leaf-module-graph.md','research-wiki/retrieval-index/astis-lean-arsenal-module-graph.json'}
keep.update('research-wiki/frontier-cells/'+c+'.json' for c in plan['active_cells'])
keep.update('research-wiki/sampling-sde-library/cards/'+d.rsplit('.',1)[0]+'.md' for d in plan['mathematical_declarations'])
assert set(paths)<=keep,set(paths)-keep
out=r/'integration72/before-generator-state.json';assert not out.exists()
out.write_text(json.dumps(dict(head=head,preexisting_tracked_changes=paths,keep=sorted(keep),untracked_cards=subprocess.check_output(['git','ls-files','--others','--exclude-standard','research-wiki/sampling-sde-library/cards'],text=True).splitlines()),indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS captured pre-generator72 exact current dirty scope; original collaborator/untracked cards preserved.')
