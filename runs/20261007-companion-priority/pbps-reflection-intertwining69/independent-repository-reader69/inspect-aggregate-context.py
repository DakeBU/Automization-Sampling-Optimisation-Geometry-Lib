import json,pathlib,sys
sys.stdout.reconfigure(encoding='utf-8')
out=pathlib.Path(__file__).resolve().parent
cell=json.loads((out/'current.020.ASTIS-SW-PBPS-actual-reflection-intertwining.json').read_text(encoding='utf-8'))
print(json.dumps({k:cell[k] for k in ['status','parents','consumers','reader_contract','graph_contribution','evidence','blocked','purification']},ensure_ascii=True,indent=2))
print('\n'.join((out/'current.029.stdout.log').read_text(encoding='utf-8').splitlines()[-32:]))
graph=json.loads((out/'current.015.underlying-lean-graph.json').read_text(encoding='utf-8'))
print(json.dumps({'graph_keys':list(graph)},ensure_ascii=True))
print(json.dumps(json.loads((out/'current.086.render-branch-actual-consumer.inspect.json').read_text(encoding='utf-8')),ensure_ascii=True,indent=2))
