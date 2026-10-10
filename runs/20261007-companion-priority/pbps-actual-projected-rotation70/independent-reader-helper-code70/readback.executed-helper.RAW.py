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
def browser_fixture(version,target=None):
 from fixture_dom import Page
 path=Path(target) if target else ROOT/'website/scripts/check_cross_domain_browser.py';tree=ast.parse(path.read_bytes());main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main');loop=next(n for n in ast.walk(main) if isinstance(n,ast.For) and isinstance(n.target,ast.Name) and n.target.id=='rel' and any(isinstance(m,ast.Name) and m.id=='proof_names' for m in ast.walk(n)))
 code=compile(ast.Module(body=[loop],type_ignores=[]),str(path),'exec');rel='example-cases/samplewiki/companions/minimal-fixture.html';names=['Demo.actual','Demo.actual_statement'];items=[dict(chapter_path=rel,bindings=[dict(declaration=names[0])])];lessons={names[0]:dict(helpers=[names[1]])}
 def panel(name,open_attr='',inside=''):
  return f'<details class="inline-lean inline-lean-proof" data-inline-lean="{name}" {open_attr}><summary>{name}</summary><pre><code class="language-lean">exact source {name}</code></pre>{inside}</details>'
 base='<article data-authored-declaration="Demo.actual"><details class="inline-lean inline-lean-statement" data-inline-lean="Demo.actual"><summary>Statement</summary><code class="language-lean">statement</code></details>'+panel(names[0],inside=panel(names[1]))+'</article>'
 fixtures=[('valid-direct-helper',base,True),('wrong-helper-same-count',base.replace('data-inline-lean="Demo.actual_statement"','data-inline-lean="Demo.wrong"'),False),('missing-helper',base.replace(panel(names[1]),''),False),('extra-closed-sibling',base+panel('Demo.extra'),False),('extra-initially-open-sibling',base+panel('Demo.extra','open'),None)]
 if version!='v1':
  fixtures += [('extra-initially-open-statement',base+'<details class="inline-lean inline-lean-statement" open><summary>Unexpected</summary></details>',False),('expected-helper-initially-open',base.replace(panel(names[1]),panel(names[1],'open')),False),('nested-helper-prevents-opening',base.replace('<summary>'+names[1]+'</summary>','<summary onclick="event.preventDefault()">'+names[1]+'</summary>'),None)]
 results=[]
 if True:
  page=Page()
  for label,fixture,expected in fixtures:
   fixture_path=O/f'fixtures-{version}/{label}.html';fixture_path.parent.mkdir(exist_ok=True);fixture_path.write_text(fixture,encoding='utf-8')
   evidence=O/f'fixture-browser-{version}/{label}';evidence.mkdir(parents=True,exist_ok=True);report=dict(companion_publications=[])
   env=dict(items=items,lesson_units=lessons,args=type('Args',(),dict(offline_dom=True))(),page=page,Counter=Counter,Path=Path,evidence=evidence,report=report,goto=lambda _:page.set_content(fixture,wait_until='domcontentloaded'))
   try:exec(code,env);passed=True;error=None
   except AssertionError as e:passed=False;error=repr(e)
   results.append(dict(label=label,fixture=pin(fixture_path),gate_fragment_accepted=passed,expected_acceptance=expected,error=error,actual_initially_open_panels=fixture.count(' open'),actual_browser=False))
   if expected is not None:assert passed==expected,(label,passed,expected)
 save(f'fixture-results-{version}.json',dict(actual_PID=os.getpid(),utc=now(),target_script=pin(path),exact_companion_loop_AST_executed=True,source_start_line=loop.lineno,source_end_line=loop.end_lineno,fixture_method='Actual AST companion loop executed against stdlib HTMLParser DOM test double. Exact inventory/open assertions and summary toggle/preventDefault semantics only; layout/visibility/real-browser interactions are untested. No screenshot fabricated.',fixture_adapter=pin(O/'fixture_dom.py'),actual_browser=False,first_browser_attempt_failure=pin(O/'negative.failure.json'),cases=results,extra_initially_open_accepted=next(q['gate_fragment_accepted'] for q in results if q['label']=='extra-initially-open-sibling')))
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
def freeze_final():
 old=get('inputs-v1.manifest.json')
 for i,q in enumerate(old['inputs']):
  check(q['RAW_snapshot']);check(q['LF_snapshot'])
  if i not in [0,1]:check(q['original'])
 maps=[read(C/n) for n in ['V2.open-panel-repair.json','V2.Prop-guard-repair.json','V3.open-count-repair.json']]
 for m in maps:assert pin(ROOT/m['exact_before'])['raw_sha256']==m['before_RAW_sha256']
 assert maps[0]['before_RAW_sha256']==old['inputs'][1]['original']['raw_sha256'] and maps[0]['after_RAW_sha256']==maps[2]['before_RAW_sha256']
 assert maps[1]['before_RAW_sha256']==old['inputs'][0]['original']['raw_sha256']
 assert pin(ROOT/'website/scripts/inline_lean.py')['raw_sha256']==maps[1]['after_RAW_sha256'] and pin(ROOT/'website/scripts/check_cross_domain_browser.py')['raw_sha256']==maps[2]['after_RAW_sha256']
 paths=[ROOT/'website/scripts/inline_lean.py',ROOT/'website/scripts/check_cross_domain_browser.py']+[C/n for n in ['V2.open-panel-repair.json','V2.Prop-guard-repair.json','V3.open-count-repair.json']]+[ROOT/m['exact_before'] for m in maps]+[R/'remote-int69-snapshot2'/n for n in ['stdout.log','receipt.json']]
 rows=[]
 for i,p in enumerate(paths):
  q=dict(original=pin(p))
  for k,b in [('RAW',p.read_bytes()),('LF',p.read_bytes().replace(b'\r\n',b'\n'))]:
   dest=O/f'inputs-final/{i:02}.{k}.snapshot';dest.parent.mkdir(exist_ok=True);dest.write_bytes(b);q[k+'_snapshot']=pin(dest)
  rows.append(q)
 # Preserve the exact adapter used for the original successful V1 negative.
 b=(O/'fixture_dom.py').read_bytes();before=b.replace(b"  if self.nodes[0].attrs.get('onclick')=='event.preventDefault()':return\n",b'').replace(b"  elif css=='details.inline-lean-statement':out=[n for n in nodes if statement(n)]\n",b'');assert sha(before)=='32590648bf6471640592554b4bed0f985ca9575ff36faade19383501c89b9b95'
 (O/'fixture_dom.v1.RAW.py').write_bytes(before)
 save('finite-historical-maps.json',dict(status='EXACT_FINITE_MAPS_ONLY',script_maps=maps,original_script_rows_qualified_as_V1=[dict(row_index=i,original=q['original'],exact_snapshot=q['RAW_snapshot']) for i,q in enumerate(old['inputs']) if i in [0,1]],own_original_fixture_adapter=dict(original_pin=get('fixture-results-v1.json')['fixture_adapter'],exact_snapshot=pin(O/'fixture_dom.v1.RAW.py'),reason='Only two narrowly supported selector/toggle cases added for V2/V3 fixtures. Original V1 adapter bytes retained exactly; old negative result not rewritten.'),no_other_historical_fallback=True))
 save('inputs-final.manifest.json',dict(input_count=len(rows),inputs=rows,LF_recipe=old['LF_recipe'],current_inputs_must_remain_equal=True,finite_history_map=pin(O/'finite-historical-maps.json')))
 print(json.dumps(dict(status='FINAL_SCRIPTS_PIN_COMPLETE',actual_PID=os.getpid(),final_input_count=len(rows),script_RAW=[q['original']['raw_sha256'] for q in rows[:2]])))
def final_stable():
 old=get('inputs-v1.manifest.json')
 for i,q in enumerate(old['inputs']):
  check(q['RAW_snapshot']);check(q['LF_snapshot'])
  if i not in [0,1]:check(q['original'])
 for q in get('inputs-final.manifest.json')['inputs']:
  for k in ['original','RAW_snapshot','LF_snapshot']:check(q[k])
 check(get('finite-historical-maps.json')['own_original_fixture_adapter']['exact_snapshot'])
def final_checks():
 final_stable();mid=browser_fixture('intermediate-v2',ROOT/read(C/'V3.open-count-repair.json')['exact_before']);assert next(q for q in mid if q['label']=='nested-helper-prevents-opening')['gate_fragment_accepted'] and not next(q for q in mid if q['label']=='extra-initially-open-sibling')['gate_fragment_accepted']
 final=browser_fixture('final-v3');assert not next(q for q in final if q['label']=='nested-helper-prevents-opening')['gate_fragment_accepted'] and not next(q for q in final if q['label']=='extra-initially-open-sibling')['gate_fragment_accepted']
 from types import SimpleNamespace
 from unittest.mock import patch
 sys.path[:0]=[str(ROOT/'website/scripts'),str(ROOT/'tools')]
 import inline_lean
 fixtures=[('literal_statement','private def literal_statement : Prop := ∀ x : Nat, x=x',True),('number_statement','def number_statement : Nat := 7',False),('inferred_statement','private def inferred_statement := (0 : Nat)',False),('parenthesized_statement','private def parenthesized_statement : (Prop) := ∀ x : Nat, x=x',False),('commented_statement','private def commented_statement : Nat /- : Prop -/ := 7',False),('trailing_statement','private def trailing_statement : Prop /- comment -/ := ∀ x : Nat, x=x',True)]
 values={n:SimpleNamespace(full_name=n,short_name=n,kind='def',source_text=s,source_file='Fixture.lean') for n,s,_ in fixtures};values['result']=SimpleNamespace(full_name='result',short_name='result',kind='theorem',source_text='theorem result : literal_statement := existing_proof',source_file='Fixture.lean');results=[]
 with patch.object(inline_lean,'declarations',return_value=values),patch.object(inline_lean.base,'source_href',return_value=('Fixture.lean','')),patch.object(inline_lean.base,'lean_source_actions',return_value=''):
  for n,s,expected in fixtures:
   rendered=inline_lean.disclosure(n,role='proof',explanation='Authored construction explanation',page='fixture.html');is_prop='Full Lean proposition (definition)' in rendered;assert is_prop==expected,(n,is_prop,expected)
   assert html.escape(s) in rendered and '<details ' in rendered and ' open' not in rendered
   if expected:assert 'no mathematical proof or additional hypothesis' in rendered
   else:assert 'Lean construction' in rendered and 'Authored construction explanation' in rendered
   dest=O/f'renderer-final/{n}.html';dest.parent.mkdir(exist_ok=True);dest.write_text(rendered,encoding='utf-8');results.append(dict(name=n,expected_full_proposition_label=expected,actual_full_proposition_label=is_prop,exact_complete_code_preserved=True,initially_folded=True,output=pin(dest)))
  rendered=inline_lean.disclosure('result',role='proof',explanation='Original theorem explanation',page='fixture.html',helpers=('literal_statement',));assert 'Lean proof' in rendered and 'Original theorem explanation' in rendered and 'Full Lean proposition (definition)' in rendered;assert rendered.count('data-lean-code-panel')==2
  dest=O/'renderer-final/theorem-with-literal-helper.html';dest.write_text(rendered,encoding='utf-8')
 save('renderer-final.results.json',dict(status='PASS',actual_PID=os.getpid(),current_script=pin(ROOT/'website/scripts/inline_lean.py'),case_count=len(results),cases=results,nested_helper=pin(dest),theorem_proof_label_preserved=True,full_literal_not_proof_provider=True,unrecognized_codomains_conservatively_use_construction_label=True,actual_browser=False))
 # Explicit py_compile writes ONLY task-owned pyc destinations.
 import py_compile
 syntaxes=[]
 for q in get('inputs-final.manifest.json')['inputs'][:2]:
  p=Path(q['original']['path']);dest=O/'syntax'/str(p.name+'.pyc');dest.parent.mkdir(exist_ok=True);py_compile.compile(str(p),cfile=str(dest),doraise=True);syntaxes.append(dict(input=pin(p),owned_pyc=pin(dest)))
 save('syntax.receipt.json',dict(status='PY_COMPILE_PASS',actual_foreground_PID=os.getpid(),exit_code=0,terminal_closed=True,command_api='py_compile.compile(input,cfile=owned_prefix,doraise=True)',scripts=syntaxes,no_canonical_pyc_written=True))
 cmd=[sys.executable,'-B','-X','utf8','-m','unittest','tools.tests.test_proof_readers','tools.tests.test_declaration_lesson_kind'];start=now();pre=[pin(ROOT/'website/scripts'/n) for n in ['inline_lean.py','check_cross_domain_browser.py']]
 with (O/'focused31.stdout.log').open('wb') as out,(O/'focused31.stderr.log').open('wb') as err:
  p=subprocess.Popen(cmd,cwd=ROOT,stdout=out,stderr=err);code=p.wait()
 receipt=dict(command=cmd,actual_foreground_PID=p.pid,actual_parent_PID=os.getpid(),started_utc=start,finished_utc=now(),exit_code=code,terminal_closed=True,script_pre_pins=pre,script_post_pins=[pin(q['path']) for q in pre],stdout=pin(O/'focused31.stdout.log'),stderr=pin(O/'focused31.stderr.log'),limitation='Existing31 focused unit regressions run on observed workspace content; not an exhaustive or hermetically frozen whole-site data inventory. No real browser/CDN/layout checks.')
 save('focused31.receipt.json',receipt);assert code==0 and 'Ran 31 tests' in (O/'focused31.stderr.log').read_text() and receipt['script_pre_pins']==receipt['script_post_pins'];final_stable()
 print(json.dumps(dict(status='FINAL_FOCUSED_CHECKS_PASS',actual_PID=os.getpid(),focused31_PID=p.pid,focused31_exit=code,fixture_cases_current=len(final),renderer_cases=len(results),py_compile_scripts=2)))
def multiplicity():
 final_stable();from fixture_dom import Page
 path=ROOT/'website/scripts/check_cross_domain_browser.py';tree=ast.parse(path.read_bytes());main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main');loop=next(n for n in ast.walk(main) if isinstance(n,ast.For) and isinstance(n.target,ast.Name) and n.target.id=='rel' and any(isinstance(m,ast.Name) and m.id=='proof_names' for m in ast.walk(n)));code=compile(ast.Module(body=[loop],type_ignores=[]),str(path),'exec');rel='example-cases/samplewiki/companions/multiplicity.html'
 def panel(n,inside=''):return f'<details class="inline-lean-proof" data-inline-lean="{n}"><summary>{n}</summary><code class="language-lean">{n}</code>{inside}</details>'
 prefix='<article data-authored-declaration="D"><details class="inline-lean-statement"><summary>Statement</summary></details>'
 cases=[('two-authored-occurrences',prefix+panel('D',panel('H')+panel('H'))+'</article>',True),('one-replaced-occurrence-same-count',prefix+panel('D',panel('H')+panel('X'))+'</article>',False),('one-missing-occurrence',prefix+panel('D',panel('H'))+'</article>',False)];results=[]
 for label,fixture,expected in cases:
  p=O/f'multiplicity/{label}.html';p.parent.mkdir(exist_ok=True);p.write_text(fixture,encoding='utf-8');page=Page();evidence=O/'multiplicity/no-visual';evidence.mkdir(exist_ok=True)
  env=dict(items=[dict(chapter_path=rel,bindings=[dict(declaration='D')])],lesson_units={'D':dict(helpers=['H','H'])},args=type('Args',(),dict(offline_dom=True))(),page=page,Counter=Counter,Path=Path,evidence=evidence,report=dict(companion_publications=[]),goto=lambda _:page.set_content(fixture))
  try:exec(code,env);accepted=True
  except AssertionError:accepted=False
  assert accepted==expected;results.append(dict(label=label,fixture=pin(p),expected=expected,accepted=accepted))
 save('multiplicity.results.json',dict(status='PASS',actual_PID=os.getpid(),target_script=pin(path),authored_expected_multiset=['D','H','H'],cases=results,actual_companion_loop_AST=True,actual_browser=False,scope='Multiset multiplicity and mismatched repeated-helper identity only. Same HTMLParser assertion test double; no layout credit.'))
 print(json.dumps(dict(status='EXACT_COUNTER_MULTIPLICITY_PASS',actual_PID=os.getpid(),cases=3)))
def decision():
 final_stable();assert get('final-checks.terminal.json')['exit_code']==0 and get('multiplicity.terminal.json')['exit_code']==0
 before_notes=read(C/'repair.notes.json');old=get('inputs-v1.manifest.json')['inputs'];current=get('inputs-final.manifest.json')['inputs'];diffs=[]
 for index,name in enumerate(['inline_lean.py','check_cross_domain_browser.py']):
  before=Path(old[index+2]['original']['path']);after=ROOT/'website/scripts'/name;v1=Path(old[index]['RAW_snapshot']['path']);note=before_notes['changes'][index];assert pin(before)['raw_sha256']==note['before_RAW_sha256'] and pin(v1)['raw_sha256']==note['after_RAW_sha256']
  part=''.join(difflib.unified_diff(before.read_text(encoding='utf-8').splitlines(keepends=True),after.read_text(encoding='utf-8').splitlines(keepends=True),fromfile=before.as_posix(),tofile=after.as_posix()));dest=O/(name+'.reviewed.diff');dest.write_text(part,encoding='utf-8');diffs.append(dict(before=pin(before),V1=pin(v1),final=pin(after),unified_diff=pin(dest)))
 class Normalize(ast.NodeTransformer):
  def visit_ImportFrom(self,n):return None if n.module=='collections' and [a.name for a in n.names]==['Counter'] else n
  def visit_Assign(self,n):
   if any(isinstance(t,ast.Name) and t.id in ['literal_statement','lesson_units'] for t in n.targets):return None
   return self.generic_visit(n)
  def visit_If(self,n):
   if any(isinstance(q,ast.Name) and q.id=='literal_statement' for q in ast.walk(n.test)):return None
   return self.generic_visit(n)
  def visit_For(self,n):
   if isinstance(n.target,ast.Name) and n.target.id=='rel' and isinstance(n.iter,ast.Call) and isinstance(n.iter.func,ast.Name) and n.iter.func.id=='sorted':return ast.Pass()
   return self.generic_visit(n)
 for index,name in enumerate(['inline_lean.py','check_cross_domain_browser.py']):
  a=Normalize().visit(ast.parse(Path(old[index+2]['original']['path']).read_bytes()));b=Normalize().visit(ast.parse((ROOT/'website/scripts'/name).read_bytes()));assert ast.dump(a,include_attributes=False)==ast.dump(b,include_attributes=False),('Unrelated AST change',name)
 # Bind real retained remote outcome and both older focused-process receipts.
 remote=read(R/'remote-int69-snapshot2/stdout.log');site=next(x for x in remote if x['databaseId']==37949674762);assert site['headSha']=='aa9dd2cf691489535aa8039850c2ee0bcdacdfb4' and site['status']=='completed' and site['conclusion']=='failure'
 historical=[]
 for folder in ['reader-helper-targeted-tests70','reader-helper-pycompile70','remote-int69-site-failure-log1']:
  p=R/folder/'receipt.json';r=read(p);assert r['exit_code']==0 and r['terminal_closed']
  for k in ['stdout','stderr']:
   q=r[k];assert pin(q['path'])['raw_bytes']==q['RAW_bytes'] and pin(q['path'])['raw_sha256']==q['RAW_sha256']
  historical.append(dict(receipt=pin(p),actual_foreground_PID=r['actual_foreground_PID'],exit_code=0,terminal_closed=True,script_inputs_bound=any(q['path'].endswith('/inline_lean.py') for q in r['inputs']),qualification='Historical test/syntax/retrieval receipt; none pins these two changed scripts. Own fresh focused/syntax check supplies exact final-script bindings. Retrieval EXIT0 is not remote CI success.'))
 assert 'Ran 31 tests' in (R/'reader-helper-targeted-tests70/stderr.log').read_text();assert pin(R/'remote-int69-site-failure-log1/stdout.log')['raw_sha256']=='a76c5992abec986a994e923be1f7f53ed2bff9f34688c92268cff90ed8b8ecc2'
 final_fixture=get('fixture-results-final-v3.json');assert len(final_fixture['cases'])==8 and all(q['gate_fragment_accepted']==(q['label']=='valid-direct-helper') for q in final_fixture['cases']);assert get('multiplicity.results.json')['status']=='PASS';assert get('renderer-final.results.json')['case_count']==6
 refs=['inputs-v1.manifest.json','inputs-final.manifest.json','finite-historical-maps.json','V1.typed-obstruction.json','fixture-results-v1.json','fixture-results-intermediate-v2.json','fixture-results-final-v3.json','multiplicity.results.json','renderer-v1.finding.json','renderer-final.results.json','negative.failure.json','focused31.receipt.json','syntax.receipt.json']
 payload=dict(schema='independent-reader-helper-code70-complete-native-review-v1',actor=ACTOR,status='ACCEPTED_BOUNDED_READER_HELPER_CODE_FINAL_INLINE_V2_BROWSER_V3',actual_decision_PID=os.getpid(),utc=now(),checked_scripts=[q['original'] for q in current[:2]],exact_before_vs_final_diffs=diffs,AST_unrelated_code_unchanged=True,AST_allowed_delta='inline literal classification/label block; browser Counter import, authored lesson_units map, companion per-page loop. All other AST exact.',independent_findings=['proof_names includes each publication binding declaration and its directly authored lesson helpers; exact Counter preserves repeated identities and multiplicities. Renderer emits those same direct helper disclosures; no hardcoded declaration count or set-based loss of duplicates.','All statement panels now counted in total and all must start folded. All proof/helper panels must match exact count and Counter, with zero initially open. After summary clicks every proof/helper detail must be open, and exact code-panel count remains checked.','V1 admitted an extra initially-open sibling; intermediate browserV2 still admitted a closed nested helper because its code was below an open parent. Final browserV3 rejects both retained adversarial fixtures.','Suffix-only V1 incorrectly called a Nat definition a full proposition. Final inlineV2 additionally requires sanitized parsed signature ending explicitly : Prop. Nat/inferred/parenthesized-unrecognized codomains conservatively remain Lean construction; genuine explicit Prop with comments is labelled full proposition/no proof/additional hypothesis.','Theorem labels/explanations remain proof labels, full literal code is retained adjacent in the helper fold and no helper definition is presented as a mathematical provider. No theorem/source semantics or proof BODY was reviewed or changed in this code task.'],test_evidence=dict(existing31_fresh=get('focused31.receipt.json'),syntax2_fresh=get('syntax.receipt.json'),final_DOM_assertion_cases=8,additional_multiset_cases=3,renderer_guard_cases=6,nested_theorem_helper_render=True,actual_AST_loop_executed=True,actual_browser=False,fixture_double='stdlib HTMLParser bounded selector/assertion test double; summary default toggle and explicit preventDefault semantics; no screenshot, layout, visibility, browser or CDN evidence.'),retained_negatives=dict(first_real_browser_attempt=get('negative.terminal.json'),first_browser_failure=pin(O/'negative.failure.json'),typed_gate_gap=pin(O/'V1.typed-obstruction.json'),typed_renderer_gap=pin(O/'renderer-v1.finding.json'),intermediate_nested_open_gap=pin(O/'fixture-results-intermediate-v2.json'),all_native_bytes_preserved=True),historical_receipts=historical,remote_INT69=dict(headSha=site['headSha'],run_id=37949674762,conclusion='failure',failure_log=pin(R/'remote-int69-site-failure-log1/stdout.log'),snapshot=pin(R/'remote-int69-snapshot2/stdout.log'),retrieval_actual_PID=36212,retrieval_exit_code=0,old_remote_not_relabelled_success=True),input_counts=dict(original_V1_rows=19,final_revision_rows=10,rows_total=29,distinct_paths=21,qualification='Repeated two current script paths are separately frozen V1/final rows; root revision maps and exact snapshots resolve only named historical versions. Two further remote snapshot paths are new; counts are manifest-row counts.'),LF_recipe=get('inputs-v1.manifest.json')['LF_recipe'],finite_history=pin(O/'finite-historical-maps.json'),required_remaining_checks=['Full real-browser/site integration, genuine nested interaction, MathJax/CDN, mobile layout and current graph/readers acceptance remain pending.','No exact SCI70/source/math/VERIFIED/Exposition/PURIFIED/Goal or live/remote success credit from these code tests.'],canonical_writes=False,whole_site_or_aggregate_writes=False,Lean_runs=False,source_packet_or_ledger_writes=False,evidence=[pin(O/n) for n in refs],closure_contract='Whole logical run drops ONLY top-level run_sha256. Complete named RAW payload distinct. Every owned input/helper/negative/terminal/self layer bound by final manifest and CLOSED_LAST last write; postclose read-only.')
 # Compute distinct locators, never infer them from prompt arithmetic.
 payload['input_counts']['distinct_paths']=len({q['original']['path'] for m in ['inputs-v1.manifest.json','inputs-final.manifest.json'] for q in get(m)['inputs']})
 save('named-review.payload.json',payload);save('decision.json',dict(schema='independent-reader-helper-code70-decision-v1',status=payload['status'],actor=ACTOR,actual_PID=os.getpid(),utc=now(),accepted=True,checked_scripts=payload['checked_scripts'],named_complete_RAW_payload=pin(O/'named-review.payload.json'),scope='Bounded final two-script code review after retained independent counterexamples and exact root repairs.',full_browser_integration=False,final_source_review=False,SAU_VERIFIED=False,canonical_writes=False,remaining=payload['required_remaining_checks']))
 print(json.dumps(dict(status=payload['status'],actual_PID=os.getpid(),input_counts=payload['input_counts'],named_complete_RAW_payload=pin(O/'named-review.payload.json'))))
def finalize():
 import closure
 closure.finalize()
def readback():
 import closure
 closure.readback()
def preclose():
 import closure
 closure.preclose()
def postclose():
 import closure
 closure.postclose()
if __name__=='__main__':
 try:globals()[sys.argv[1]]()
 except Exception as e:
  if not(O/'lease.final.json').exists():save((sys.argv[2] if len(sys.argv)>2 else sys.argv[1])+'.failure.json',dict(actual_PID=os.getpid(),utc=now(),error=repr(e),traceback=traceback.format_exc()))
  raise
