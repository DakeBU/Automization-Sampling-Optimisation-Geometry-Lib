from pathlib import Path
import hashlib, json, os, sys, traceback
ROOT=Path('E:/Samplinglib')
OWN=ROOT/'runs/20261007-companion-priority/pbps-b4-perturbation-preproof72/b27-dependency-diagnosis'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def write(name,x):
 (OWN/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def pin(path):
 b=path.read_bytes();lf=b.replace(b'\r\n',b'\n')
 return {'path':path.relative_to(OWN).as_posix(),'raw_bytes':len(b),'raw_sha256':sha(b),'lf_bytes':len(lf),'lf_sha256':sha(lf),'lf_recipe':'CRLF-to-LF only'}
try:
 assert not (OWN/'lease.final.json').exists(),'never reopen CLOSED'
 inputs=json.loads((OWN/'inputs.finite-pins.json').read_text(encoding='utf-8'))
 assert inputs['content_files_read']==7
 for p in inputs['files']:
  b=(ROOT/p['path']).read_bytes();assert len(b)==p['raw_bytes'] and sha(b)==p['raw_sha256']
  assert sha(b.replace(b'\r\n',b'\n'))==p['lf_sha256']
 cleanup=[]
 for name in ['primary.search-contexts.json','selected-six.line-readview.txt']:
  target=(OWN/name).resolve();assert target.parent==OWN.resolve()
  if target.exists():
   cleanup.append({'removed_owned_redundant_scratch':name,**{k:v for k,v in pin(target).items() if k!='path'},'reason':'derived display-only duplicates; no RAW input/canonical/old-CLOSED file removed'})
   target.unlink()
 write('bounded-scratch-cleanup.json',{'actual_pid':os.getpid(),'scope':str(OWN),'removed':cleanup})
 decision={
  'schema':'bounded-source-dependency-diagnosis-v1',
  'status':'diagnosis-complete-only',
  'target':'PBPSv1 actual B27/H/K/r_rho boundary',
  'content_inputs':7,
  'smallest_missing_real_producer':'Jointly Borel law of Algorithm1 terminal position x_pi, internally constructed from same-J conditional reference law, independent Gaussian momentum and integrated-hazard nonexplosive trajectory; conditional detailed balance/invariance and same-J L2 lift are required to obtain actual B27.',
  'selected_conditional_kernel_supplies_actual_Q_density_or_J_disintegration':False,
  'reference_adapter_status':'open unproved adapter Q_y = map(z -> (y+z)/2)(S y); imported implementations not inspected',
  'reused_actual_api':'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualCorrectorChange.actual_corrector_change',
  'abstract_interfaces':['ConditionalKernel conditional-integral/version adapter','KernelMixture supplied-component Markov/invariance results'],
  'inapplicable_generalization':'KernelReversibility singleton-balance requires Countable E and cannot be imposed on source continuous E',
  'next_candidate_edges':[
   {'order':1,'classification':['internal-paper-step','local-lemma'],'edge':'Actual Algorithm1 endpoint kernel with internal same-J reference-law density/disintegration adapter, nonexplosion and joint Borelness','claims_now':False},
   {'order':2,'classification':['internal-paper-step','local-lemma'],'edge':'Terminal-time reversal, independent Gaussian/reference averaging, same-J A9 L2 self-adjoint Markov contraction and all-kerP restriction','claims_now':False},
   {'order':3,'classification':['local-lemma'],'edge':'Actual mixture/reflection transition, B7 observable identity, actual r/r_rho and B27 components using inherited71 witnesses','claims_now':False}
  ],
  'forbidden_extra_callers':['arbitrary H or Hmicro','invariance','nonexplosion','joint measurability','mean(Kf)=0','cost bounds','onto V','higher smoothness'],
  'source_inputs_unchanged':True,
  'source_graph_rebuilt_or_expanded':False,
  'read72_implementation_body_decoder_mathverdict_or_other_sourceplan':False,
  'prior_exposure':'70/71 complete implementations and prospective72 headers already seen; not sourceblind',
  'canonical_git_ledger_goal_old_closed_writes':False,
  'lean_compile_or_proof_search':False,
  'new_source_fidelity_sau_sci_verified_completion_credit':False,
  'remaining':'B27/B28/fullB4/dynamics/main/implementation/errors/caps/costs/composition/fullpaper remain open here',
  'evidence':'b27-dependency.memo.md',
  'source_math_and_offsets':'primary.final-exact-source-anchors.json',
  'finite_input_manifest':'inputs.finite-pins.json'
 }
 write('b27-dependency.decision.json',decision)
 receipt={'actual_pid':os.getpid(),'exit_code':0,'argv':sys.argv,'background':False,'checks':['exactly seven content inputs','all RAW/LF/size pins current','cleanup confined to new owned scratch files','no old CLOSED/canonical/Git/ledger/Goal writes','finite native closure'],'lease_written_last':True}
 write('close-diagnosis.terminal.json',receipt)
 memo=(OWN/'b27-dependency.memo.md').read_text(encoding='utf-8')
 run={'schema':'bounded-source-dependency-run-v1','run_sha256':None,'target':decision['target'],'decision':decision,'memo':pin(OWN/'b27-dependency.memo.md'),'input_manifest':pin(OWN/'inputs.finite-pins.json'),'foreground_terminals':[json.loads((OWN/n).read_text(encoding='utf-8')) for n in ['inspect-bounded.terminal.json','inspect-details.terminal.json','final-source-extract.terminal.json','close-diagnosis.terminal.json']],'observer_failures':json.loads((OWN/'observer-failures.json').read_text(encoding='utf-8')),'truth_boundary':decision['remaining']}
 logical=dict(run);del logical['run_sha256'];run['run_sha256']=sha(canon(logical))
 write('diagnosis.run.json',run)
 payload={'schema':'small-complete-named-diagnosis-payload-v1','complete_named_review':{'name':'b27-dependency.memo.md','text':memo},'complete_named_decision':{'name':'b27-dependency.decision.json','value':decision},'complete_finite_input_manifest':{'name':'inputs.finite-pins.json','value':inputs,'raw_sha256':sha((OWN/'inputs.finite-pins.json').read_bytes())},'native_run':{'name':'diagnosis.run.json','raw_sha256':sha((OWN/'diagnosis.run.json').read_bytes()),'whole_logical_sha256':run['run_sha256'],'logical_recipe':'canonical JSON UTF8 ensure_ascii=false sort_keys=true separators=(comma,colon), deleting ONLY top-level run_sha256'},'large_or_historical_RAW_base64_copies':False}
 write('complete-named-diagnosis-input-payload.json',payload)
 rows=[pin(p) for p in sorted(OWN.rglob('*')) if p.is_file() and p.name not in ['owned-manifest.json','lease.final.json']]
 write('owned-manifest.json',{'schema':'finite-owned-manifest-v1','file_count':len(rows),'files':rows,'self_exclusion':['owned-manifest.json','lease.final.json'],'scope':str(OWN)})
 manifest=pin(OWN/'owned-manifest.json')
 lease={'schema':'bounded-diagnosis-CLOSED_LAST-v1','state':'CLOSED_LAST','last_write':'lease.final.json','actual_close_pid':os.getpid(),'exit_code_confirmed_by_foreground_tool':0,'owned_scope':str(OWN),'manifest':manifest,'payload':pin(OWN/'complete-named-diagnosis-input-payload.json'),'native_run':pin(OWN/'diagnosis.run.json'),'whole_logical_sha256':run['run_sha256'],'logical_recipe':'delete ONLY top-level run_sha256; canonical JSON UTF8 sort_keys=true ensure_ascii=false compact separators','manifest_member_count':len(rows),'closure_files_excluding_lease':len(rows)+1,'total_closed_files_including_lease':len(rows)+2,'finite_content_inputs':7,'canonical_or_old_closed_mutation':False,'no_theorem_or_source_completion_credit':True,'postclose_policy':'read-only verification only; zero writes to this tree after lease'}
 write('lease.final.json',lease)
 print(json.dumps({'actual_pid':os.getpid(),'exit_code':0,'decision_raw_sha256':sha((OWN/'b27-dependency.decision.json').read_bytes()),'memo_raw_sha256':sha((OWN/'b27-dependency.memo.md').read_bytes()),'whole_logical_sha256':run['run_sha256'],'payload':lease['payload'],'manifest':manifest,'lease_raw_sha256':sha((OWN/'lease.final.json').read_bytes()),'total_files':len(rows)+2,'total_bytes':sum(p.stat().st_size for p in OWN.rglob('*') if p.is_file())},ensure_ascii=True,indent=2))
except BaseException:
 traceback.print_exc();sys.exit(1)
