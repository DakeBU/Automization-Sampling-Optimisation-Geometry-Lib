from pathlib import Path
import json
r=Path('runs/20261007-companion-priority/pbps-centered-defect59');p=Path('docs/companion-papers-handoff.md');b=p.read_bytes();anchor=b'## Actual PBPS centered squared defect (2026-10-08)\n\n';assert b.count(anchor)==1
extra="""Actual serialized aggregate passes: root9163, Tests9454, Registry501, current
contributor/publication/semantic/frontier/site gates and both affected graph
checks. Eight native desktop views of both statements, ten formula steps and
exact branches were inspected; original reader debts remain explicit. Science
2d6cd016 was safely pushed to PR315 after a fetch confirmed unchanged main
c05de12e and preserved all working edits. Its remote contributor CI succeeds;
Lean/site terminal acceptance and the successor integration commit remain
separate. Push each meaningful reviewed science/integration milestone.

""".encode()
p.write_bytes(b.replace(anchor,anchor+extra,1))
n=json.loads((r/'integration.notes.json').read_bytes());n['final_administrative_gate_receipts']=[str(r/'integration59'/label/'receipt.json') for label in ['publication-final-admin','contributor-final-admin','frontier-final-admin']];(r/'integration.notes.json').write_text(json.dumps(n,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Handoff records actual aggregate and milestone push with CI boundary explicit.')
