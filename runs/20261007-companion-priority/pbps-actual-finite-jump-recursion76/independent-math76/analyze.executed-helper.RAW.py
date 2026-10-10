from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,re,subprocess,sys,traceback
ROOT=Path('E:/Samplinglib');R=ROOT/'runs/20261007-companion-priority/pbps-actual-finite-jump-recursion76';OWN=R/'independent-math76'
PY='C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';ACTOR='/root/exact_science63';BASE='54620175c56e7db191bcebe7bb010edda1744894'
MODULE=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteJumpRecursion.lean';DECL='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteJumpRecursion.actual_fixed_reference_finite_jump_recursion'
RECIPE='Replace CRLF byte pairs with LF only; preserve bare CR and all other bytes.'
def now():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(d):return json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def load(p):return json.loads(p.read_bytes())
def read(n):return load(OWN/n)
def write(n,d):
 p=OWN/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2).encode()+b'\n')
def pin(p):
 b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_bytes=len(b.replace(b'\r\n',b'\n')),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
def path(s):
 p=Path(s);return p if p.is_absolute() else ROOT/p
def check(row):
 q=pin(path(row['path']))
 for k in ['RAW_bytes','RAW_sha256','LF_bytes','LF_sha256']:
  if k in row:assert q[k]==row[k],(q,k,row[k])
 return q
def git(args):return subprocess.run(['git',*args],cwd=ROOT,capture_output=True,check=True).stdout
def recheck():
 assert git(['rev-parse','HEAD']).decode().strip()==BASE
 for row in read('inputs.manifest.json')['inputs']+read('inputs.manifest.json')['supplemental_inputs']:
  check(row['original'])
  if 'snapshot' in row:check(row['snapshot'])
def freeze():
 dispatch=load(R/'independent-math.dispatch76.json');assert len(dispatch['inputs'])==12 and dispatch['checked_parent']==BASE and git(['rev-parse','HEAD']).decode().strip()==BASE
 rows=[]
 for i,row in enumerate(dispatch['inputs']):
  check(row);p=path(row['path']);rec=dict(original=pin(p))
  if 'primary-pbps.exactraw.snapshot.html' in p.name:rec['storage']='Immutable fixed primary source reference; no duplicate whole paper; exact source regions saved separately.'
  else:
   out=OWN/'inputs'/('%02d.'%i+p.name+'.RAW');out.parent.mkdir(exist_ok=True);out.write_bytes(p.read_bytes());rec['snapshot']=pin(out)
  if p in [ROOT/'lean-toolchain',ROOT/'lake-manifest.json'] or p.parent==MODULE.parent and p!=MODULE:
   b=git(['show',BASE+':'+p.relative_to(ROOT).as_posix()]);rec['Git_parent_RAW_sha256']=sha(b);rec['Git_parent_RAW_bytes']=len(b);rec['Git_parent_RAW_equal']=b==p.read_bytes();assert rec['Git_parent_RAW_equal'] or b.replace(b'\r\n',b'\n')==p.read_bytes().replace(b'\r\n',b'\n');rec['Git_parent_CRLF_only_qualification']=not rec['Git_parent_RAW_equal']
  rows.append(rec)
 supplemental=[]
 for n in ['independent-math.dispatch76.json','mathematics-freeze76.json']:
  p=R/n;out=OWN/'inputs'/n;out.write_bytes(p.read_bytes());supplemental.append(dict(original=pin(p),snapshot=pin(out),role='Dispatch itself' if n.startswith('independent') else 'Later root control-plane freeze; only its stable source/toolchain facts used, no header/source verdict consumption.'))
 write('inputs.manifest.json',dict(dispatch_input_count=12,supplemental_input_count=2,total_input_rows=14,inputs=rows,supplemental_inputs=supplemental,checked_parent=BASE,candidate_uncommitted=True,LF_recipe=RECIPE))
 write('lease.open.json',dict(status='OPEN_WHOLE_MATHEMATICS76',actor=ACTOR,actual_PID=os.getpid(),opened_utc=now(),checked_parent=BASE,no_canonical_shared_Git_ledger_writes=True))
 print(json.dumps(dict(status='FROZEN',actual_PID=os.getpid(),dispatch_inputs=12,supplemental_inputs=2,module=pin(MODULE))))
def process(label,argv,env=None):
 pre=pin(MODULE);f=OWN/'terminals';f.mkdir(exist_ok=True);out=f/(label+'.stdout.RAW');err=f/(label+'.stderr.RAW');started=now()
 with out.open('wb') as o,err.open('wb') as e:
  p=subprocess.Popen(argv,cwd=ROOT,stdout=o,stderr=e,env=env);print(json.dumps(dict(status='FOREGROUND_RUNNING',label=label,actual_PID=p.pid)),flush=True);code=p.wait()
 rec=dict(label=label,actual_PID=p.pid,command=argv,started_utc=started,ended_utc=now(),exit_code=code,terminal_closed=True,stdout=pin(out),stderr=pin(err),module_pre=pre,module_post=pin(MODULE));write('terminals/'+label+'.receipt.json',rec);assert code==0 and rec['module_post']==pre,(label,code);return rec
def compile():
 recheck();envrec=process('fixed-Lake-environment',['lake','env',PY,'-B','-X','utf8','-c',"import os,json;print(json.dumps({k:os.environ.get(k,'') for k in ['LEAN_PATH','LEAN_SRC_PATH']}))"])
 lakeenv=json.loads(path(envrec['stdout']['path']).read_bytes());env=os.environ.copy();env.update(lakeenv);lean=ROOT/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe';version=process('fixed-Lean-version',[str(lean),'--version'],env);assert '4.33.0' in path(version['stdout']['path']).read_text()
 out=OWN/'output/ActualFiniteJumpRecursion.olean';out.parent.mkdir(exist_ok=True);rec=process('fresh-whole-canonical-module',[str(lean),'-o',str(out),str(MODULE)],env)
 driver=OWN/'inputs/ActualFiniteJumpRecursion.axiom-audit.lean';suffix='\n#print axioms '+DECL+'\n';driver.write_bytes(MODULE.read_bytes()+suffix.encode());ax=process('fresh-whole-source-standard3',[str(lean),str(driver)],env)
 text=path(ax['stdout']['path']).read_text(encoding='utf8');matches=re.findall(r'depends on axioms:\s*\[([^\]]+)\]',text,re.S);assert len(matches)==1;axioms=[x.strip() for x in matches[0].split(',')];assert set(axioms)=={'propext','Classical.choice','Quot.sound'} and len(axioms)==3
 write('fresh-compiler.json',dict(status='PASS',checked_parent=BASE,module=pin(MODULE),fresh_source_elaboration=True,Lake_build_cache_replay=False,actual_foreground_Lean_PID=rec['actual_PID'],axioms_PID=ax['actual_PID'],terminal_EXIT=0,standard_axioms=axioms,compiler_receipt=pin(OWN/'terminals/fresh-whole-canonical-module.receipt.json'),axiom_receipt=pin(OWN/'terminals/fresh-whole-source-standard3.receipt.json'),real_Lean_executable=pin(lean),version_receipt=pin(OWN/'terminals/fixed-Lean-version.receipt.json'),Lake_environment_receipt=pin(OWN/'terminals/fixed-Lake-environment.receipt.json'),fixed_environment=lakeenv,output_olean=pin(out),canonical_olean_written=False,axiom_driver=pin(driver),axiom_driver_only_suffix=suffix,axiom_driver_exact_module_prefix=True))
 recheck();print(json.dumps(dict(status='FRESH_SOURCE_AND_AXIOMS_PASS',actual_PID=os.getpid(),Lean_PID=rec['actual_PID'],axioms_PID=ax['actual_PID'],standard3=True)))
def launch(action):
 assert not (OWN/'lease.final.json').exists();p=Path(__file__);(OWN/(action+'.executed-helper.RAW.py')).write_bytes(p.read_bytes());argv=[PY,'-B','-X','utf8',str(p),'_child',action]
 with (OWN/(action+'.stdout.log')).open('wb') as o,(OWN/(action+'.stderr.log')).open('wb') as e:
  proc=subprocess.Popen(argv,cwd=ROOT,stdout=o,stderr=e);print(json.dumps(dict(status='RUNNING',action=action,actual_PID=proc.pid,runner_PID=os.getpid())),flush=True);code=proc.wait()
 write(action+'.receipt.json',dict(action=action,actual_PID=proc.pid,runner_PID=os.getpid(),command=argv,exit_code=code,terminal_closed=True,stdout=pin(OWN/(action+'.stdout.log')),stderr=pin(OWN/(action+'.stderr.log')),executed_helper=pin(OWN/(action+'.executed-helper.RAW.py'))));print(json.dumps(dict(status='TERMINAL',action=action,actual_PID=proc.pid,exit_code=code)));return code

def analyze():
 from html.parser import HTMLParser
 recheck();b=MODULE.read_bytes();text=b.decode();assert len(b)==22655 and len(b.splitlines())==412 and sha(b)=='1f1ebc187676e0481247bc2f58ec0bf94b2fc6f02a563b87009a0fe7bfb4910c'
 header=ROOT/'runs/20261007-companion-priority/pbps-recursive-preproof76/header76.v3.proposed.lean';h=header.read_bytes().decode();private=text[text.index('private def '):text.index('set_option maxHeartbeats')].strip();old=h[h.index('private def '):h.index('\ntheorem ')].strip();assert private==old
 pubstart=text.index('\ntheorem ')+1;pubend=text.index(':= by',pubstart)+len(':= by');pub=text[pubstart:pubend];assert pub==h[h.index('\ntheorem ')+1:].strip()
 args,body=private.split(' : Prop :=',1);expanded=args.replace('private def actual_fixed_reference_finite_jump_recursion_statement','theorem actual_fixed_reference_finite_jump_recursion',1)+' :'+body
 ep=R/'expanded76.frozen.header.lean';assert expanded.split()==ep.read_bytes().decode().split()
 lets=body[:body.index('    (∀ y xRef')];local=text[text.index('  let c',pubend):text.index('  change',pubend)];assert lets.split()==local.split()
 seal=load(ROOT/'runs/20261007-companion-priority/pbps-recursive-preproof76/root.statement-seal76.json');inventory=seal['binder_inventory'];assert inventory['counts']==dict(callers=6,conclusion_groups=10,literal_definitions=11,typing=5)
 for category in ['callers','conclusion_groups','literal_definitions']:
  for row in inventory[category]:
   literal=row['header_literal'] if category=='callers' else row['literal'];start,end=row['header_RAW_range'];assert header.read_bytes()[start:end].decode()==literal
   assert literal.strip() in private
 sys.path[:0]=[str(ROOT),str(ROOT/'tools')];import astis
 stripped=astis.strip_lean_comments_and_strings(text);hits=[dict(line=i+1,text=line) for i,line in enumerate(stripped.splitlines()) if astis.FORBIDDEN_REGEX.search(line)];assert not hits
 declared=re.findall(r'^(private )?(def|theorem|lemma|axiom|opaque)\s+([^\s:]+)',stripped,re.M);assert declared==[('private ','def','actual_fixed_reference_finite_jump_recursion_statement'),('','theorem','actual_fixed_reference_finite_jump_recursion')]
 parents=[]
 for name,target in [('ActualHarmonicFlow','actual_harmonic_flow_laws'),('ActualBounceRate','actual_bounce_rate_energy_laws'),('ActualHazardClock','actual_integrated_hazard_clock_laws')]:
  assert text.count(name+'.'+target+' hα hαβ hV hH hη hβη')==1;p=MODULE.parent/(name+'.lean');parents.append(dict(declaration='AutoSamplingTheory.ExampleCases.ProximalBPS.'+name+'.'+target,module=pin(p),Git_parent_exact_RAW=True))
 # Only bounded source/API references used; no prospective sourcegraph or later source/decoder verdict.
 apis=[]
 for n,start,end in [('MeasureTheory/Constructions/BorelSpace/WithTop.lean',31,68),('MeasureTheory/MeasurableSpace/Embedding.lean',443,466),('Probability/Process/HittingTime.lean',61,79)]:
  p=ROOT/'.lake/packages/mathlib/Mathlib'/n;data=p.read_bytes();lines=data.splitlines(keepends=True);raw=b''.join(lines[start-1:end]);out=OWN/'API'/p.name;out.parent.mkdir(exist_ok=True);out.write_bytes(raw);apis.append(dict(original=pin(p),exact_lines_start=start,exact_lines_end_inclusive=end,fragment=pin(out),whole_file_vs_span_digests_distinguished=True))
 apis.append(dict(original=pin(ROOT/'tools/astis.py'),role='Fake-closure scanner implementation'))
 api_manifest=dict(api_input_count=4,other_required_input_count=1,API_inputs=apis,expanded_header_input=pin(ep),LF_recipe=RECIPE);write('analysis.inputs.manifest.json',api_manifest)
 primary=path(read('inputs.manifest.json')['inputs'][11]['original']['path']);raw=primary.read_bytes();source=[]
 class Extract(HTMLParser):
  def __init__(self):super().__init__();self.parts=[]
  def handle_data(self,d):self.parts.append(d)
 for anchor in ['A1.E2','A1.Ex4','A1.Ex5','A1.Ex6','A1.Ex7','A1.Ex8']:
  pos=raw.index(('id="'+anchor+'"').encode());start=raw.rfind(b'<table',0,pos);end=raw.index(b'</table>',pos)+len(b'</table>');fragment=raw[start:end];out=OWN/'source'/(anchor+'.exactraw.html');out.parent.mkdir(exist_ok=True);out.write_bytes(fragment);parser=Extract();parser.feed(fragment.decode());source.append(dict(anchor=anchor,original=pin(primary),start_RAW_offset=start,end_RAW_offset_exclusive=end,fragment=pin(out),exact_alttext=re.findall(r'alttext="([^"]+)"',fragment.decode()),readable=' '.join(' '.join(parser.parts).split())))
 # Preserve the finite/empty-set/stopped and future SLLN/Markov prose separately, by exact offsets.
 start=raw.index(b'id="A1.SS1"');start=raw.rfind(b'<section',0,start);end=raw.index(b'With the process now constructed',start);end=raw.rfind(b'<',start,end);out=OWN/'source/finite-construction-and-future-boundary.exactraw.html';out.write_bytes(raw[start:end]);source.append(dict(anchor='A1.1 well-posedness proof through its end; future probabilistic steps explicitly uncredited',original=pin(primary),start_RAW_offset=start,end_RAW_offset_exclusive=end,fragment=pin(out)))
 write('source-anchors.json',dict(status='BOUNDED_MATHEMATICAL_SCOPE_ONLY_NOT_SOURCE_ADMISSION',primary=pin(primary),source_regions=source,numbering='A1.E2 contains printed(A.1)+(A.2); A1.Ex4-8 are unnumbered energy/cap/wait displays. Printed(A.4)-(A.8) are later reversal/invariance and receive no credit.'))
 write('statement-and-fakeclosure.json',dict(status='PASS',actual_PID=os.getpid(),checked_parent=BASE,module=pin(MODULE),module_lines=412,exact_sealed_private_literal=True,exact_sealed_public_signature=True,expanded_complete_private_result_token_equal=True,expanded_header=pin(ep),same11_local_and_private_definitions=True,callers=6,typing_classes=5,literal_definitions=[x['name'] for x in inventory['literal_definitions']],conclusion_groups=10,private_providers=0,declaration_inventory=declared,fake_closure_hits=hits,actual_producers=parents,source_graph_or_source_decoder_verdicts_consumed=False,representation_note='One full private Prop is literal specification; its public caller invokes exactly hα hαβ hV hH hη hβη. The public BODY constructs all10 conclusion groups; no theorem/provider assumption.',documentation_debt='Opening comment still says Prospective header76 only; this understates the compiled theorem and must not become an unfinished-proof or full-completion claim. No mathematical statement repair.'))
 print(json.dumps(dict(status='WHOLE_STATEMENT_SCAN_SOURCE_SCOPE_PASS',actual_PID=os.getpid(),callers=6,definitions=11,conclusion_groups=10,source_regions=7,API_inputs=4)))

if __name__=='__main__':
 try:
  action=sys.argv[-1]
  if sys.argv[1]=='_child':sys.exit(globals()[action]() or 0)
  elif action in ['close','postclose']:globals()[action]()
  else:sys.exit(launch(action))
 except BaseException as e:
  if not isinstance(e,SystemExit) and not (OWN/'lease.final.json').exists():write('negative.'+sys.argv[-1]+'.'+str(os.getpid())+'.json',dict(actual_PID=os.getpid(),action=sys.argv[-1],error=repr(e),traceback=traceback.format_exc(),canonical_mutation=False))
  raise
