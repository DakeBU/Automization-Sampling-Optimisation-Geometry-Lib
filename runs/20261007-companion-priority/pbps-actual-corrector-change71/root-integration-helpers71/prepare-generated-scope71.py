from pathlib import Path
import hashlib,json,subprocess
r=Path('runs/20261007-companion-priority/pbps-actual-corrector-change71/integration71')
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
assert head=='4e7ce5d2996ffe1d1b0ab570778e02425c6be34e'
paths=subprocess.check_output(['git','-c','core.autocrlf=false','diff','--name-only'],text=True).splitlines()
keep={'AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl','runs/substantive_advances.jsonl','research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-corrector-change.json','conversion-windows/ASTIS-SW-PBPS-2026.md','docs/module-graph.svg','docs/assets/astis_lean_arsenal_module_graph.svg','research-wiki/sampling-sde-library/lean-leaf-module-graph.md','research-wiki/retrieval-index/astis-lean-arsenal-module-graph.json','research-wiki/sampling-sde-library/cards/AutoSamplingTheory.ExampleCases.ProximalBPS.ActualCorrectorChange.md'}
assert set(paths)<=keep,set(paths)-keep
out=r/'before-generator-state.json';assert not out.exists()
out.write_text(json.dumps(dict(head=head,preexisting_tracked_changes=paths,keep=sorted(keep),untracked_cards=subprocess.check_output(['git','ls-files','--others','--exclude-standard','research-wiki/sampling-sde-library/cards'],text=True).splitlines()),indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS captured exact pre-generator clean scope and existing cards; only root-owned aggregate paths currently changed.')
