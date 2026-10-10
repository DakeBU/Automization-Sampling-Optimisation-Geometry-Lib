import json,os,pathlib,sys
sys.dont_write_bytecode=True
from compare_bounded_dom import compare
out=pathlib.Path(__file__).resolve().parent
expected=json.loads((out/'expected-code-and-reader-payload.before-final-packet.json').read_text(encoding='utf-8'))
result=compare((out/'current.016.proximal-bouncy-particle.html').read_text(encoding='utf-8'),expected)
result.update(schema='repository-reader69-current-scoped-DOM-comparison-v1',actual_pid=os.getpid())
(out/'current-scoped-DOM-comparison.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,sort_keys=True))
assert result['authored_article_count']==1 and result['scoped_panel_count']==3
assert all(x['exact'] for x in result['panel_checks']) and result['helper_nested_in_public_proof']
assert result['scoped_BODY_count']==6 and all(x['code_exact'] and x['formula_exact'] and x['initially_closed'] for x in result['BODY_checks'])
assert result['complete_natural_statement_exact'] and result['full_assumptions_exact'] and result['assumptions_initially_closed']
