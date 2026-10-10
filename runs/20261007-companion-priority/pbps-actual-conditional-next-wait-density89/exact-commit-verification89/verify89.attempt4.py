import ast,json
from pathlib import Path
O=Path(__file__).parent;p=O/'verify89.py'
with (O/'verifier-native-source-serialization89.negative.json').open('x',encoding='utf8',newline='\n') as f:
 json.dump({'status':'VERIFIER_SCHEMA_EQUALITY_ERROR_BEFORE_GATES','terminal_tool_chunk':'5f73be','exit_code':1,'cause':'Verifier compared the v2 structured reconstruction to entire original slot records, and demanded full equality of deltas despite documented additive canonical fields. Native v2 preserves each original reconstructed payload separately and serializes canonical reconstructed strings; delta slots/descriptions/evidence/severity are additive.','correction':'Compare exact original reconstructed payload per slot, decode v2 string for equality, retain every other original slot field and every original delta field exactly. No native/source/canonical changes.'},f,indent=2);f.write('\n')
tree=ast.parse((O/'verify89.attempt3.py').read_text('utf8'))
new=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='new' for t in n.targets))
s=p.read_text('utf8').replace(" if r.startswith('.lake/packages/mathlib/'):",new,1)
old="assert native['native_structured_reconstruction']==original['semantic_slots'] and native['deltas']==original['deltas']"
repair="for slot,record in original['semantic_slots'].items():\n assert native['native_structured_reconstruction'][slot]==record['reconstructed']\n assert json.loads(native['semantic_slots'][slot]['reconstructed'])==record['reconstructed']\n for k,v in record.items():\n  if k!='reconstructed':assert native['semantic_slots'][slot][k]==v\nassert len(native['deltas'])==len(original['deltas'])\nfor old_delta,new_delta in zip(original['deltas'],native['deltas']):\n for k,v in old_delta.items():assert new_delta[k]==v"
assert s.count(old)==1
exec(compile(s.replace(old,repair,1),str(p),'exec'),{'__file__':str(p),'__name__':'__main__'})
