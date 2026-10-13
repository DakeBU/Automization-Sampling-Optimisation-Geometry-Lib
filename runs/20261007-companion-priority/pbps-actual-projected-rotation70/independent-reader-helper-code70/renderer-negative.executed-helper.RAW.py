import os,sys,json,hashlib,datetime,traceback,ast,difflib,subprocess,html
from pathlib import Path
from collections import Counter
ROOT=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;R=O.parent;C=R/'reader-helper-contract70';ACTOR='/root/exact_science63'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(Path(p).read_bytes())
def get(n):return read(O/n)
def save(n,x):
 assert not(O/'lease.final.json').exists();p=O/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((json.dumps(x,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode())
def pin(p):
 p=Path(p);b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),raw_bytes=len(b),raw_sha256=sha(b),lf_bytes=len(lf),lf_sha256=sha(lf))
def check(q):assert pin(q['path'])==q,('RAW/LF mismatch',q['path'])
def logical(r):return sha(json.dumps({k:v for k,v in r.items() if k!='run_sha256'},sort_keys=True,ensure_ascii=False,separators=(',',':')).encode())
def files():return sorted(p for p in O.rglob('*') if p.is_file())
def freeze():
 save('lease.open.json',dict(status='OPEN',actor=ACTOR,actual_PID=os.getpid(),utc=now(),owned_scope=O.as_posix(),scope='Bounded two-script code review and focused isolated DOM fixture checks only; no theorem/source verdict or fullsite/aggregate/canonical writes.'))
 paths=[ROOT/'website/scripts/inline_lean.py',ROOT/'website/scripts/check_cross_domain_browser.py',C/'inline_lean.py.before.exactraw.snapshot',C/'check_cross_domain_browser.py.before.exactraw.snapshot',C/'repair.notes.json']
 for dirname in ['reader-helper-targeted-tests70','reader-helper-pycompile70','remote-int69-site-failure-log1']:
  paths += [R/dirname/n for n in ['receipt.json','stdout.log','stderr.log']]
 paths += [ROOT/'tools/tests/test_proof_readers.py',ROOT/'tools/tests/test_declaration_lesson_kind.py',ROOT/'website/scripts/declaration_lessons.py',ROOT/'website/scripts/proof_readers.py',ROOT/'tools/astis_site.py']
 assert len(paths)==19;rows=[]
 for i,p in enumerate(paths):
  row=dict(original=pin(p))
  for k,b in [('RAW',p.read_bytes()),('LF',p.read_bytes().replace(b'\r\n',b'\n'))]:
   dest=O/f'inputs-v1/{i:02}.{k}.snapshot';dest.parent.mkdir(exist_ok=True);dest.write_bytes(b);row[k+'_snapshot']=pin(dest)
  rows.append(row)
 save('inputs-v1.manifest.json',dict(input_count=len(rows),inputs=rows,LF_recipe='Replace ONLY CRLF with LF; preserve bare CR and all other bytes. RAW authoritative.',finite_historical_rows='The exact two before snapshots and immutable historical receipts/logs are historical authority, not current script equality claims.',script_row_indices=[0,1],current_input_drift_allowed=False))
 print(json.dumps(dict(status='V1_PIN_COMPLETE',actual_PID=os.getpid(),input_count=len(rows),current_script_RAW=[r['original']['raw_sha256'] for r in rows[:2]])))
def browser_fixture(version):
 from fixture_dom import Page
 path=ROOT/'website/scripts/check_cross_domain_browser.py';tree=ast.parse(path.read_bytes());main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main');loop=next(n for n in ast.walk(main) if isinstance(n,ast.For) and isinstance(n.target,ast.Name) and n.target.id=='rel' and any(isinstance(m,ast.Name) and m.id=='proof_names' for m in ast.walk(n)))
 code=compile(ast.Module(body=[loop],type_ignores=[]),str(path),'exec');rel='example-cases/samplewiki/companions/minimal-fixture.html';names=['Demo.actual','Demo.actual_statement'];items=[dict(chapter_path=rel,bindings=[dict(declaration=names[0])])];lessons={names[0]:dict(helpers=[names[1]])}
 def panel(name,open_attr='',inside=''):
  return f'<details class="inline-lean inline-lean-proof" data-inline-lean="{name}" {open_attr}><summary>{name}</summary><pre><code class="language-lean">exact source {name}</code></pre>{inside}</details>'
 base='<article data-authored-declaration="Demo.actual"><details class="inline-lean inline-lean-statement" data-inline-lean="Demo.actual"><summary>Statement</summary><code class="language-lean">statement</code></details>'+panel(names[0],inside=panel(names[1]))+'</article>'
 fixtures=[('valid-direct-helper',base,True),('wrong-helper-same-count',base.replace('data-inline-lean="Demo.actual_statement"','data-inline-lean="Demo.wrong"'),False),('missing-helper',base.replace(panel(names[1]),''),False),('extra-closed-sibling',base+panel('Demo.extra'),False),('extra-initially-open-sibling',base+panel('Demo.extra','open'),None)]
 results=[]
 if True:
  page=Page()
  for label,fixture,expected in fixtures:
   fixture_path=O/f'fixtures-{version}/{label}.html';fixture_path.parent.mkdir(exist_ok=True);fixture_path.write_text(fixture,encoding='utf-8')
   evidence=O/f'fixture-browser-{version}/{label}';evidence.mkdir(parents=True,exist_ok=True);report=dict(companion_publications=[])
   env=dict(items=items,lesson_units=lessons,args=type('Args',(),dict(offline_dom=True))(),page=page,Counter=Counter,Path=Path,evidence=evidence,report=report,goto=lambda _:page.set_content(fixture,wait_until='domcontentloaded'))
   try:exec(code,env);passed=True;error=None
   except AssertionError as e:passed=False;error=repr(e)
   results.append(dict(label=label,fixture=pin(fixture_path),gate_fragment_accepted=passed,expected_acceptance=expected,error=error,actual_initially_open_panels=1 if label=='extra-initially-open-sibling' else 0,actual_browser=False))
   if expected is not None:assert passed==expected,(label,passed,expected)
 save(f'fixture-results-{version}.json',dict(actual_PID=os.getpid(),utc=now(),target_script=pin(path),exact_companion_loop_AST_executed=True,source_start_line=loop.lineno,source_end_line=loop.end_lineno,fixture_method='Actual AST companion loop executed against stdlib HTMLParser DOM test double. Exact inventory/open assertions and summary toggle semantics only; layout/visibility/real-browser interactions are untested. No screenshot fabricated.',fixture_adapter=pin(O/'fixture_dom.py'),actual_browser=False,first_browser_attempt_failure=pin(O/'negative.failure.json'),cases=results,extra_initially_open_accepted=results[-1]['gate_fragment_accepted']))
 return results
def negative():
 for q in get('inputs-v1.manifest.json')['inputs']:check(q['original']);check(q['RAW_snapshot']);check(q['LF_snapshot'])
 results=browser_fixture('v1');assert results[-1]['gate_fragment_accepted']
 save('V1.typed-obstruction.json',dict(status='CONFIRMED_DEFAULT_FOLD_GATE_GAP',actual_PID=os.getpid(),utc=now(),test=pin(O/'fixture-results-v1.json'),smallest_negative='One expected declaration + one expected nested helper, both folded, plus one extra already-open sibling proof panel. Actual companion loop accepts all assertions, then toggles the extra open sibling closed.',cause='Initial Counter is formed only from :not([open]) panels and no total-panel or initially-open-zero assertion exists. Clicking every summary can hide an extra initially-open sibling before final open-code count.',smallest_repair=['Assert total proof-panel count and Counter over ALL proof panels equal the exact authored declaration+helper multiset.','Assert initially-open proof panels count is zero before clicking.','Retain folded count and later-open checks; verify all proof details themselves open after clicking.'],preexisting_limit='Older count-only gate also had this hole; the new helper-aware repair must not claim all panels initially folded while it remains.',code_writes=False))
 print(json.dumps(dict(status='CONFIRMED_DEFAULT_FOLD_GATE_GAP',actual_PID=os.getpid(),negative_fixture_accepted=True)))
def renderer_negative():
 from types import SimpleNamespace
 from unittest.mock import patch
 sys.path[:0]=[str(ROOT/'website/scripts'),str(ROOT/'tools')]
 import inline_lean
 values={n:SimpleNamespace(full_name=n,short_name=n.split('.')[-1],kind=k,source_text=s,source_file='Fixture.lean') for n,k,s in [('Demo.literal_statement','def','private def literal_statement : Prop := ∀ x : Nat, x=x'),('Demo.number_statement','def','def number_statement : Nat := 7'),('Demo.result','theorem','theorem result : literal_statement := existing_proof')]}
 with patch.object(inline_lean,'declarations',return_value=values),patch.object(inline_lean.base,'source_href',return_value=('Fixture.lean','')),patch.object(inline_lean.base,'lean_source_actions',return_value=''),patch.object(inline_lean.base,'code_html',side_effect=lambda s:'<pre><code class="language-lean">'+html.escape(s)+'</code></pre>'):
  rendered={n:inline_lean.disclosure(n,role='proof',explanation='Authored explanation',page='fixture.html') for n in values}
 for n,b in rendered.items():(O/(n.split('.')[-1]+'.renderer-v1.html')).write_text(b,encoding='utf-8')
 assert 'Full Lean proposition (definition)' in rendered['Demo.literal_statement'] and 'no mathematical proof or additional hypothesis' in rendered['Demo.literal_statement']
 assert 'Lean proof' in rendered['Demo.result'] and 'Authored explanation' in rendered['Demo.result']
 false_positive='Full Lean proposition (definition)' in rendered['Demo.number_statement'];assert false_positive
 save('renderer-v1.finding.json',dict(status='CONFIRMED_SUFFIX_ONLY_LITERAL_CLASSIFICATION_FALSE_POSITIVE',actual_PID=os.getpid(),current_script=pin(ROOT/'website/scripts/inline_lean.py'),proper_Prop_label_pass=True,theorem_label_unchanged=True,non_Prop_Nat_definition_falsely_labelled_full_proposition=True,fixture=pin(O/'number_statement.renderer-v1.html'),scope='Independent renderer fixture, not existing canonical declaration or mathematical counterexample.',smallest_repair='Require a recognized Prop-valued literal definition in addition to the _statement suffix; e.g. exact parsed signature ends in : Prop. Private-marker qualification can further match intended protocol. Preserve construction label for unrecognized definitions.',actual_browser=False))
 print(json.dumps(dict(status='CONFIRMED_SUFFIX_ONLY_LITERAL_CLASSIFICATION_FALSE_POSITIVE',actual_PID=os.getpid())))
if __name__=='__main__':
 try:globals()[sys.argv[1]]()
 except Exception as e:
  if not(O/'lease.final.json').exists():save((sys.argv[2] if len(sys.argv)>2 else sys.argv[1])+'.failure.json',dict(actual_PID=os.getpid(),utc=now(),error=repr(e),traceback=traceback.format_exc()))
  raise
