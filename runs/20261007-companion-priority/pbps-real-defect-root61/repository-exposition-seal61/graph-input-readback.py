from common import *
payload=J(P/'graph.after-native-adapter.input.payload.json'); differences=[]
for cid,expected in payload['cells'].items():
 if expected is not None:
  p=ROOT/expected['__path__']; actual=J(p); actual['__path__']=expected['__path__']
  if actual!=expected: differences.append(dict(cell=cid,input=pin(p),expected=expected,actual=actual))
for q in J(P/'graph.after-native-adapter.diagnosis.json')['source_rows']: matches(q)
W(P/'graph.exact-input-readback.json',dict(actual_PID=os.getpid(),referenced_cells_checked=len(payload['cells']),canonical_current_vs_exactGit_cell_differences=differences,exact_source_rows_unchanged=True,future62_not_read=True))
print('EXACT_REFERENCED_CELL_DIFFS',len(differences)); print([x['cell'] for x in differences])
