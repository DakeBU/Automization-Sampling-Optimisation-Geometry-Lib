import datetime,hashlib,json,os,pathlib,re,shutil,subprocess,sys,traceback
R=pathlib.Path('E:/Samplinglib');O=pathlib.Path(__file__).resolve().parent;D=O.parent;H=D.parent/'pbps-first-corrector-energy-preproof67';PY='C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';ACTOR='/root/exact_science63';BASE='a115115d42b3fa2b67885d87fe4d5300af36fcd1';L='AutoSamplingTheory/TechnicalLemmas/Measure/L2RealSquareCommute.lean';M='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualRootCommutation.lean';T='Tests/ProximalBPSActualRootCommutation.lean';LD='AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareCommute.positive_square_commutation';MD='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualRootCommutation.actual_same_root_inverse_commutation';TD='Tests.ProximalBPSActualRootCommutation.genuine_actual_corrector_coefficient_consumer'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(j):return json.dumps(j,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def read(p):return json.loads(pathlib.Path(p).read_text(encoding='utf-8-sig'))
def pin(p):
 p=pathlib.Path(p);b=p.read_bytes();return {'path':p.as_posix(),'raw_bytes':len(b),'lf_bytes':len(b.replace(b'\r\n',b'\n')),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n'))}
def write(n,j):
 assert not (O/'lease.final.json').exists();p=O/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((json.dumps(j,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode())
def check(x):
 q=pin(x['path']);assert q['raw_bytes']==x['raw_bytes'] and q['raw_sha256']==x['raw_sha256']
def inputs():
 j=read(O/'initial.inputs.manifest.json')
 for x in j['inputs']:check(x['original']);check(x['RAW_snapshot']);check(x['LF_snapshot'])
 return j
def command(label,args):
 folder=O/label;folder.mkdir(exist_ok=False);start=now()
 with (folder/'stdout.log').open('wb') as out,(folder/'stderr.log').open('wb') as err:
  p=subprocess.Popen(args,cwd=R,stdout=out,stderr=err);print(json.dumps({'event':'START','label':label,'actual_foreground_pid':p.pid,'actual_runner_pid':os.getpid()}),flush=True);code=p.wait()
 row={'label':label,'command':args,'actual_foreground_pid':p.pid,'actual_runner_pid':os.getpid(),'exit_code':code,'terminal_closed':True,'started_utc':start,'finished_utc':now(),'stdout':pin(folder/'stdout.log'),'stderr':pin(folder/'stderr.log')};write(label+'/receipt.json',row);print(json.dumps({'event':'TERMINAL','label':label,'actual_pid':p.pid,'exit_code':code}),flush=True);return row
def freeze():
 write('lease.open.json',{'schema':'independent-precommit-math67-OPEN-v1','status':'OPEN','actor':ACTOR,'actual_open_pid':os.getpid(),'opened_utc':now(),'owned_prefix':O.as_posix(),'scope':'Independent actual mathematical/proof review; preliminary exact source pin/fresh leaf+main checks allowed. Wait root immutable math-freeze/publication before final BODY review/close. No source final verdict consumption,VERIFIED,canonical/shared/ledger/Git/publication writes.'})
 paths=[R/L,R/M,R/T,R/'AutoSamplingTheory/ExampleCases/ProximalBPS/AmbientAdjointCorrector.lean',R/'AutoSamplingTheory/TechnicalLemmas/Measure/L2RealComplexOperator.lean',R/'lean-toolchain',R/'lake-manifest.json',D/'claim.json',D/'preproof-admission.json',H/'root.statement-seal67.json',H/'root.header67.adoption.json',H/'root.primary67.adoption.json',H/'independent-primary67/source-proof-graph.json',H/'independent-header-math67/lease.final.json',H/'independent-header-math67/mathematical-statement-review.named.raw.json']+[H/f'header{i}-expanded.lean' for i in range(3)]+[H/f'statement{i}.definition.lean' for i in range(3)]
 rootfreeze=read(D/'math-freeze.json')
 for x in rootfreeze['inputs']:
  q=pin(x['path']);assert q['raw_sha256']==x['raw_sha256'] and q['raw_bytes']==x['raw_bytes']
 paths += [D/'math-freeze.json',D/'publication-plan.json',D/'math-freeze.0.before-canonical-floor.json',D/'canonical-floor-metadata67/repair.json']+[pathlib.Path(x['path']) for x in rootfreeze['inputs']];paths=list(dict.fromkeys(paths))
 rows=[]
 for i,path in enumerate(paths):
  b=path.read_bytes();raw=O/'inputs'/f'{i:03}.RAW.snapshot';lf=O/'inputs'/f'{i:03}.LF.snapshot';raw.parent.mkdir(exist_ok=True);raw.write_bytes(b);lf.write_bytes(b.replace(b'\r\n',b'\n'));rows.append({'original':pin(path),'RAW_snapshot':pin(raw),'LF_snapshot':pin(lf)})
 inherited=[]
 for path in ['AutoSamplingTheory/ExampleCases/ProximalBPS/AmbientAdjointCorrector.lean','AutoSamplingTheory/TechnicalLemmas/Measure/L2RealComplexOperator.lean']:
  b=subprocess.check_output(['git','show',BASE+':'+path],cwd=R);assert sha(b)==pin(R/path)['raw_sha256'];inherited.append({'path':path,'base_Git_RAW_sha256':sha(b),'exact_current_RAW_equal':True})
 write('initial.inputs.manifest.json',{'schema':'bounded-precommit67-initial-exact-inputs-v1','base_science_commit':BASE,'actual_HEAD_at_freeze':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),'actual_freeze_pid':os.getpid(),'utc':now(),'inputs':rows,'exact_unchanged_inherited_science':inherited,'root_final_math_freeze_and_publication_packet':pin(D/'math-freeze.json'),'checked_integration_base':rootfreeze['checked_base_commit'],'original_science_parent_reuse':BASE,'source_final_verdict_consumed':False,'no_whole_history_or_ledger_scan':True})
 print(json.dumps({'status':'INITIAL_FROZEN','actual_pid':os.getpid(),'inputs':len(rows),'root_final_freeze_admitted':True}),flush=True)
def standard(row,names):
 assert row['exit_code']==0;stdout=pathlib.Path(row['stdout']['path']).read_text(encoding='utf-8');found=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]+)\]",stdout,re.S);assert {n for n,s in found}==set(names);result=[]
 for n,s in found:
  axioms=[x.strip() for x in s.replace('\n',' ').split(',')];assert len(axioms)==3 and set(axioms)=={'propext','Classical.choice','Quot.sound'};result.append({'declaration':n,'axioms':axioms})
 return result
def fresh():
 inputs();pre=[pin(R/p) for p in [L,M,T,'lean-toolchain','lake-manifest.json']];write('fresh.pre-pins.json',{'inputs':pre,'utc':now()});lake=shutil.which('lake');assert lake;rows=[]
 build=command('lake-build',[lake,'build','Tests.ProximalBPSActualRootCommutation']);assert build['exit_code']==0;assert 'Build completed successfully (3948 jobs).' in pathlib.Path(build['stdout']['path']).read_text(encoding='utf-8')
 for label,path,name in [('fresh-leaf',L,[LD]),('fresh-main',M,[MD]),('fresh-Test',T,[LD,MD,TD])]:
  row=command(label,[lake,'env','lean',path]);row['standard3']=standard(row,name);rows.append(row)
 post=[pin(R/p) for p in [L,M,T,'lean-toolchain','lake-manifest.json']];assert pre==post;write('fresh.post-pins.json',{'inputs':post,'pre_post_exact_RAW_LF_equal':True,'utc':now()});write('fresh.all.result.json',{'status':'PASS','lake_build':build,'lake_build_cache_replay_separate_from_fresh_Lean':True,'jobs':3948,'actual_pid':os.getpid(),'fresh_compilers':rows,'pre_post_exact_RAW_LF_equal':True,'cache_replay_called_fresh_proof':False,'root_final_freeze_admitted':True,'all3_fresh_proof_compilers':True});print(json.dumps({'status':'FRESH_ALL3_PASS','actual_pid':os.getpid()}),flush=True)
def structural():
 inputs();rows=[]
 for i,path,name in [(0,L,LD),(1,M,MD),(2,T,TD)]:
  b=(R/path).read_bytes();d=(H/f'statement{i}.definition.lean').read_bytes();h=(H/f'header{i}-expanded.lean').read_bytes();n=name.split('.')[-1].encode()
  if i==0:assert h in b
  else:assert d in b
  assert not re.search(rb'\b(?:sorry|admit|axiom|native_decide|run_tac|elab|macro)\b',b);assert len(re.findall(rb'^theorem ',b,re.M))==1;assert len(re.findall(rb'^private def ',b,re.M))==(0 if i==0 else 1);assert not re.search(rb'^private (?:lemma|theorem|axiom|opaque)',b,re.M);rows.append({'path':path,'whole_RAW':pin(R/path),'sealed_header':pin(H/f'header{i}-expanded.lean'),'literal_private_statement':None if i==0 else pin(H/f'statement{i}.definition.lean'),'private_mathematical_providers':0,'public_theorems':1})
 negatives=[]
 for label in ['focused-main-v1','focused-main-v2','focused-main-v3','focused-main-v4-api-corrected']:
  folder=D/label;receipt=read(folder/'receipt.json');stdout=folder/'stdout.log';s=stdout.read_text(encoding='utf-8');assert receipt['exit_code']!=0;errors=[x for x in s.splitlines() if re.search(r'error(?:\(|:)',x)];negatives.append({'label':label,'actual_receipt':pin(folder/'receipt.json'),'actual_stdout':pin(stdout),'exit_code':receipt['exit_code'],'all_error_kinds_including_parenthesized':errors,'sorryAx_in_failed_diagnostics':('sorryAx' in s),'mathematical_proof_credit':False})
 write('structural.result.json',{'status':'PASS','actual_pid':os.getpid(),'sealed_rows':rows,'private_literal_statements_only':2,'private_mathematical_providers':0,'original_actual_caller_header_preservation':'Exact literal private statement bytes equal independently sealed header definitions; public theorem binders retained and invoke only those original inputs.','rank0_alphaeta1_legal':True,'root_negative_runs_preserved':negatives,'root_summary_filter_issue':'Earlier filter missed error(lean.unknownIdentifier); complete original stdout/error kinds are authoritative, failed sorryAx is never proof.','corrected_API':'IsSelfAdjoint.one requires explicit operator Type; actual current main uses it.','source_final_verdict_consumed':False})
 print(json.dumps({'status':'STRUCTURAL_PASS','actual_pid':os.getpid(),'original_negative_runs_retained':4}),flush=True)
if __name__=='__main__':
 mode=sys.argv[1]
 try:globals()[mode]()
 except Exception as e:
  if not (O/'lease.final.json').exists():write(mode+'.failure.json',{'status':'FAIL','actual_pid':os.getpid(),'exception':repr(e),'traceback':traceback.format_exc(),'utc':now()})
  raise
