from pathlib import Path
import os,sys,json,hashlib,subprocess,re,datetime,traceback
ROOT=Path('E:/Samplinglib')
R=ROOT/'runs/20261007-companion-priority/pbps-unit-exponential-product77'
OWN=R/'independent-math77'
PY='C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
BIN=ROOT/'.astis/toolchain/lean-4.33.0-windows/bin'
LEAN=BIN/'lean.exe'; LAKE=BIN/'lake.exe'
MOD=ROOT/'AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean'
SEAL=ROOT/'runs/20261007-companion-priority/pbps-iid-product-preproof77/root.statement-seal77.json'
PARENT='10ca06b04634e95ff67b461c7b37c9cee0931998'
TARGET='AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws'
ACTOR='/root/exact_science63'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def load(p):return json.loads(Path(p).read_bytes())
def pin(p):
 p=Path(p); b=p.read_bytes();lf=b.replace(b'\r\n',b'\n')
 return dict(path=p.relative_to(ROOT).as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_bytes=len(lf),LF_sha256=sha(lf))
def check(r):assert pin(ROOT/r['path'])==r,r['path']
def write(n,x):
 assert not (OWN/'lease.final.json').exists()
 (OWN/n).write_bytes((json.dumps(x,ensure_ascii=False,indent=2,sort_keys=True)+'\n').encode('utf-8'))
def process(label,argv,env=None):
 assert not (OWN/(label+'.receipt.json')).exists()
 pre=pin(MOD); st=now()
 with (OWN/(label+'.stdout.RAW')).open('wb') as o,(OWN/(label+'.stderr.RAW')).open('wb') as e:
  p=subprocess.Popen([str(x) for x in argv],cwd=ROOT,env=env,stdout=o,stderr=e)
  print(json.dumps(dict(status='FOREGROUND_RUNNING',label=label,actual_PID=p.pid)),flush=True); code=p.wait()
 rec=dict(label=label,actual_PID=p.pid,command=[str(x) for x in argv],started_utc=st,ended_utc=now(),exit_code=code,terminal_closed=True,stdout=pin(OWN/(label+'.stdout.RAW')),stderr=pin(OWN/(label+'.stderr.RAW')),module_pre=pre,module_post=pin(MOD))
 write(label+'.receipt.json',rec); assert code==0 and pre==rec['module_post'],(label,code)
 return rec
APIS=[
('Probability/ProductMeasure.lean',352,389),('Probability/ProductMeasure.lean',470,484),
('Probability/Independence/InfinitePi.lean',120,136),('Probability/Independence/Basic.lean',449,461),('Probability/Independence/Basic.lean',664,679),
('Probability/Distributions/Exponential.lean',89,101),('Probability/Distributions/Exponential.lean',159,169),('Probability/CDF.lean',78,87),
('MeasureTheory/Measure/Real.lean',35,45),('MeasureTheory/Measure/Real.lean',405,418),('MeasureTheory/OuterMeasure/AE.lean',93,103),('MeasureTheory/Measure/Map.lean',245,254),
('Data/NNReal/Defs.lean',151,168),('MeasureTheory/Constructions/BorelSpace/Real.lean',139,155),('MeasureTheory/Integral/Bochner/Set.lean',530,539),
('MeasureTheory/Integral/Bochner/Basic.lean',1040,1057),('Probability/IdentDistrib.lean',66,115),('Probability/StrongLaw.lean',590,613),
('Topology/Algebra/Order/Field.lean',28,52),('Order/Filter/AtTopBot/Tendsto.lean',63,77)]
def freeze():
 assert not (OWN/'inputs.manifest.json').exists()
 write('lease.open.json',dict(status='OPEN',actor=ACTOR,created_utc=now(),actual_PID=os.getpid(),scope='Whole mathematics77 only; no canonical/shared/ledger/Git/Goal writes; no source/decoder verdict or VERIFIED.',prior_header50_immutable=True))
 f=load(R/'mathematics-freeze77.json')
 for row in f['inputs']:
  p=Path(row['path']);b=p.read_bytes();assert len(b)==row['RAW_bytes'] and sha(b)==row['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==row['LF_sha256']
 assert MOD.read_bytes()==(R/'canonical77.frozen.exactraw.lean').read_bytes()
 assert sha(MOD.read_bytes())=='c4a93999f287008d9ddb3f3624f52f302df122e5e007a54fd427a9985edc5ec0'
 paths=[R/'mathematics-freeze77.json',R/'canonical77.frozen.exactraw.lean',R/'expanded77.frozen.header.lean',MOD,SEAL,ROOT/'lean-toolchain',ROOT/'lake-manifest.json',LEAN,LAKE]
 paths += [ROOT/x for x in ['.agents/skills/astis-substantive-advance/SKILL.md','docs/contributor-codex-contract.md','docs/theorem-publication-protocol.md','docs/proof-digestion-protocol.md','docs/evidence-routed-memory-protocol.md']]
 paths += [ROOT/'.lake/packages/mathlib/Mathlib'/x for x in sorted(set(a for a,_,_ in APIS))]
 rows=[pin(p) for p in paths]
 write('inputs.manifest.json',dict(input_count=len(rows),LF_recipe='Replace CRLF byte pairs with LF ONLY; preserve bare CR and all other bytes.',inputs=rows,storage='Finite RAW/LF references plus exact module/header/freeze snapshots; no recursive historical copies.',source_decoder_final_verdicts_read=False))
 (OWN/'module77.exactraw.lean').write_bytes(MOD.read_bytes())
 (OWN/'expanded77.exactraw.header.lean').write_bytes((R/'expanded77.frozen.header.lean').read_bytes())
 (OWN/'mathematics-freeze77.exactraw.json').write_bytes((R/'mathematics-freeze77.json').read_bytes())
 regions=[]
 for a,start,end in APIS:
  p=ROOT/'.lake/packages/mathlib/Mathlib'/a;b=b''.join(p.read_bytes().splitlines(keepends=True)[start-1:end])
  regions.append(dict(source=pin(p),start_line=start,end_line=end,RAW_region_sha256=sha(b),RAW_region_bytes=len(b),literal_RAW_UTF8=b.decode('utf-8')))
 write('API-regions.json',dict(region_count=len(regions),regions=regions,region_hash_is_not_whole_file_hash=True))
 head=process('git-head',['git','rev-parse','HEAD']);actual=(OWN/'git-head.stdout.RAW').read_text().strip();assert actual==PARENT
 status=process('git-module-status',['git','status','--porcelain','--',str(MOD.relative_to(ROOT))]);assert '??' in (OWN/'git-module-status.stdout.RAW').read_text()
 seal=load(SEAL); code=MOD.read_text(encoding='utf-8');literal=code.split('private def unit_exponential_product_statement : Prop :=\n',1)[1].split('\n\n/--',1)[0]
 expanded=(R/'expanded77.frozen.header.lean').read_text(encoding='utf-8').split('theorem unit_exponential_product_laws :\n',1)[1].strip()
 strip=lambda s:re.sub(r'\s+','',s)
 assert strip(literal)==strip(seal['expanded_literal_Prop'])==strip(expanded)
 assert sha(seal['expanded_literal_Prop'].encode())==seal['expanded_literal_Prop_UTF8_sha256']
 assert re.search(r'theorem unit_exponential_product_laws\s*:\s*unit_exponential_product_statement\s*:= by',code)
 assert len(re.findall(r'^private def ',code,re.M))==1 and len(re.findall(r'^theorem ',code,re.M))==1
 write('statement-and-parent.json',dict(checked_parent=actual,module_uncommitted=True,exact_SCI77_commit_exists_or_reviewed=False,module=pin(MOD),line_count=len(MOD.read_bytes().splitlines()),module_frozen_equal=True,public_parameter_binders=0,logical_premises=0,fixed_literal_definitions=['P=infinitePi(expMeasure1)','X=actual evaluation','epsilon=Real.toNNReal(X)'],conclusion_groups=5,private_statement_only=True,private_proof_providers=0,sealed_literal_text=seal['expanded_literal_Prop'],actual_private_literal_text=literal,expanded_header=pin(R/'expanded77.frozen.header.lean'),equivalence_recipe='Delete only syntactic whitespace for literal equality; no term/formula/binder change.',semantic_alias_expansion_complete=True,source_exposure_qualification='Required statement seal contains earlier header-admission labels and binder inventory, which were seen for exact contract identification only. No source/decoder final verdict, graph/coverage outcome, private final packet or reconstruction was opened or used as proof evidence. Prior header review is not evidence for this proof.'))
 write('frozen.json',dict(status='FROZEN_BEFORE_INDEPENDENT_COMPILER',actual_PID=os.getpid(),input_count=len(rows),inputs_manifest=pin(OWN/'inputs.manifest.json'),checked_parent=actual,module=pin(MOD),expanded_header=pin(R/'expanded77.frozen.header.lean'),current_to_historical_maps=[],all_input_equalities_current=True,stage='precommit mathematical review'))
 print(json.dumps(dict(status='FROZEN',actual_PID=os.getpid(),input_count=len(rows),module=pin(MOD))),flush=True)
def recheck():
 for row in load(OWN/'inputs.manifest.json')['inputs']:check(row)
 assert MOD.read_bytes()==(OWN/'module77.exactraw.lean').read_bytes()
 assert subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,capture_output=True,text=True,check=True).stdout.strip()==PARENT
 return True
def compile():
 recheck();env=dict(os.environ);env['PATH']=str(BIN)+os.pathsep+env.get('PATH','');env['PYTHONDONTWRITEBYTECODE']='1'
 process('Lean-version',[LEAN,'--version'],env)
 er=process('Lake-environment',[LAKE,'env',PY,'-B','-X','utf8','-c',"import os,json; print(json.dumps({k:os.environ[k] for k in ['LEAN_PATH','LEAN_SRC_PATH'] if k in os.environ}))"],env)
 env.update(json.loads((OWN/'Lake-environment.stdout.RAW').read_bytes()))
 suffix=('\n/- Independent fresh whole-module elaboration and axiom inspection; no new proof. -/\n#print axioms '+TARGET+'\n#check '+TARGET+'\n').encode('utf-8')
 probe=OWN/'FreshWholeModuleAxioms77.lean';probe.write_bytes(MOD.read_bytes()+suffix)
 assert probe.read_bytes()[:-len(suffix)]==MOD.read_bytes()
 rec=process('fresh-whole-module-and-axioms',[LEAN,probe],env)
 text=(OWN/'fresh-whole-module-and-axioms.stdout.RAW').read_text(encoding='utf-8')
 match=re.search(r'depends on axioms:\s*\[([^\]]+)\]',text);assert match,text
 axioms=[x.strip() for x in match.group(1).split(',')];assert set(axioms)=={'propext','Classical.choice','Quot.sound'} and len(axioms)==3
 assert 'error' not in text.lower() and 'sorryAx' not in text
 code=MOD.read_text(encoding='utf-8');stripped=re.sub(r'/-.*?-/', '',code,flags=re.S);stripped=re.sub(r'--[^\n]*','',stripped)
 patterns=[r'\baxiom\b',r'\bsorry\b',r'\badmit\b',r'\bsorryAx\b',r'Prop\s*:=\s*True',r':=\s*trivial\b',r'\bunsafe\b',r'\bimplemented_by\b',r'\bextern\b']
 hits=[dict(pattern=p,match=m.group(),offset=m.start()) for p in patterns for m in re.finditer(p,stripped)]
 assert not hits
 write('fake-closure-scan.json',dict(status='PASS',actual_PID=os.getpid(),module=pin(MOD),patterns=patterns,hits=hits,scan_recipe='Strip block/doc and single-line comments, then scan whole actual128-line module; compiler axiom result independently excludes sorryAx.',provider_inventory=dict(private_literal_Prop_def=1,private_proof_provider=0,public_theorem=1,other_authored_declarations=0)))
 write('compiler.json',dict(status='PASS_FRESH_WHOLE_MODULE_STANDARD3',actual_PID=os.getpid(),actual_Lean_PID=rec['actual_PID'],exit_code=rec['exit_code'],receipt=pin(OWN/'fresh-whole-module-and-axioms.receipt.json'),probe=pin(probe),actual_module=pin(MOD),prefix_exact_to_current_and_frozen=True,only_appended=suffix.decode(),axioms=axioms,fresh_full_source_elaboration=True,Lake_target_cache_replay=False,dependencies_reused_from_fixed_Lake_environment=True,canonical_olean_written=False,new_proof_written=False))
 recheck(); print(json.dumps(dict(status='COMPILER_PASS',actual_Lean_PID=rec['actual_PID'],EXIT=0,axioms=axioms)),flush=True)
def toolchain_readback():
 recheck();version=(OWN/'Lean-version.stdout.RAW').read_text(encoding='utf-8');assert '4.33.0' in version
 manifest=load(ROOT/'lake-manifest.json');expected=next(x['rev'] for x in manifest['packages'] if x['name']=='mathlib')
 rec=process('Mathlib-revision',['git','-C',ROOT/'.lake/packages/mathlib','rev-parse','HEAD']);actual=(OWN/'Mathlib-revision.stdout.RAW').read_text().strip();assert actual==expected
 files=sorted(set('Mathlib/'+a for a,_,_ in APIS))
 clean=process('Mathlib-finite-API-diff',['git','-C',ROOT/'.lake/packages/mathlib','diff','--name-only','HEAD','--']+files)
 assert not (OWN/'Mathlib-finite-API-diff.stdout.RAW').read_bytes().strip()
 write('toolchain-readback.json',dict(status='PASS',actual_PID=os.getpid(),Lean_version=version.strip(),Lean=pin(LEAN),lake_manifest=pin(ROOT/'lake-manifest.json'),Mathlib_manifest_revision=expected,actual_Mathlib_revision=actual,revision_receipt=pin(OWN/'Mathlib-revision.receipt.json'),finite_inspected_API_files=len(files),finite_API_source_equals_pinned_revision=True,finite_API_diff_receipt=pin(OWN/'Mathlib-finite-API-diff.receipt.json'),full_Mathlib_rebuild=False))
 print(json.dumps(dict(status='TOOLCHAIN_READBACK_PASS',actual_PID=os.getpid(),Mathlib_revision=actual)),flush=True)
def decision():
 recheck(); c=load(OWN/'compiler.json');assert c['status']=='PASS_FRESH_WHOLE_MODULE_STANDARD3';assert load(OWN/'toolchain-readback.json')['status']=='PASS'
 proof=[
 dict(id='P01',lines=[17,27],claim='Exact fixed model and sealed proposition',argument='The only private declaration is the full literal Prop. P is the fixed countable product of rate-one exponential measures on native Real sequences; X_k is evaluation and epsilon_k is toNNReal(X_k). The public theorem has no binders or logical assumptions. Its expanded private target is whitespace-identical to the sealed five groups; no characterized object or provider is hidden.'),
 dict(id='P02',lines=[47,54],claim='Probability, measurability and exact raw marginals',argument='Positive rate1 gives each factor IsProbabilityMeasure by the exponential theorem. Only then does infinitePi probability inference apply. The product default-zero branch is therefore not used. Evaluation is measurable on the product sigma algebra; measurable toNNReal gives measurable epsilon. Evaluation pushforward is exactly expMeasure1 for every index.'),
 dict(id='P03',lines=[55,57],claim='Actual mutual independence',argument='iIndepFun_infinitePi is instantiated with the identity on each Real factor, not an assumed iid sequence or an independent witness. The resulting family is definitionally the actual X. This establishes mutual independence and permits pairwise extraction only for distinct indices.'),
 dict(id='P04',lines=[59,75],claim='Zero-null support and common AE positive event',argument='At0 the rate1 CDF is1-exp(0)=0. Probability finiteness makes measure.real(Iic0)=0 equivalent to measure(Iic0)=0. Thus x>0 almost everywhere. Pullback along each measurable evaluation using its exact marginal law transfers support to each coordinate. ae_all_iff uses Countable Nat to obtain one full-probability event for all k. On that event toNNReal coercion equals X_k by positivity; no pointwise positivity assumption is introduced.'),
 dict(id='P05',lines=[77,87],claim='Indicator integrability and iid laws',argument='b(x)=1_{x>1} is measurable. B_k=b(X_k) is the actual coordinate transform. B_0 is the indicator of measurable evaluation preimage of Ioi1, so it is integrable as an indicator of the constant1 on the now proved probability space. Measurable composition preserves actual mutual independence. Exact coordinate marginal equality plus both AEMeasurable witnesses constructs IdentDistrib(X_k,X_0), then composition yields IdentDistrib(B_k,B_0).'),
 dict(id='P06',lines=[88,99],claim='Actual indicator expectation is exp(-1)>0',argument='Ioi1 is the complement of Iic1. For the factor probability, its real measure is1-CDF(1)=exp(-1). integral_map transfers the actual B_0 integral to the raw marginal without assuming a moment of X. The measurable indicator-one integral equals the real measure of Ioi1. This proves the exact expectation internally; positivity is Real.exp_pos(-1).'),
 dict(id='P07',lines=[100,104],claim='Real SLLN hypotheses are all discharged',argument='The real strong law is instantiated with B, its internally proved integrable B_0, pairwise independence extracted from actual mutual independence, and IdentDistrib(B_k,B_0) for every k. Rewriting the integral with the computed mean gives almost-sure averages converging to exp(-1). Neither integrability nor a positive mean is a caller premise.'),
 dict(id='P08',lines=[106,117],claim='Positive average implies real partial-sum divergence',argument='On the SLLN event, a_n=(sum_{k<n}B_k)/n tends to positive p=exp(-1), while real n tends to atTop. pos_mul_atTop therefore makes a_n*n tend to atTop. The proof cancels the denominator for n!=0 and explicitly treats n=0, where both the empty sum and Lean total division produce0. This yields divergence of the actual indicator sums. Equivalently, eventually a_n>=p/2, so sums grow at least np/2.'),
 dict(id='P09',lines=[118,125],claim='Pointwise domination includes negative and zero samples',argument='For x>1, b(x)=1<=x<=coe(toNNReal x). For x<=1, b(x)=0<=coe(toNNReal x). This inequality is pointwise on the full Real sequence carrier, independently of the support event and including negative/zero x. Finite-sum monotonicity and tendsto_atTop_mono transfer indicator-sum divergence to the exact epsilon sums. It is not a claim of pointwise divergence: the zero sequence is still a null exceptional sample.'),
 dict(id='P10',lines=[34,126],claim='No missing premise or fake mathematical closure',argument='Probability, measurability, laws, support, countable event, integrability, common law, independence, mean and SLLN conditions are all constructed in the body from fixed library results. There are zero public assumptions and zero proof providers. A fresh full-source elaboration with exact canonical prefix succeeds and the actual public theorem uses precisely the three standard axioms.'),
 dict(id='P11',lines=[17,126],claim='Exact exported and remaining boundary',argument='Exported groups are product probability; coordinate/clamp measurability and raw X marginal laws; mutual independence of X; simultaneous AE positivity/clamp equality; AE divergence of real epsilon partial sums. No separate epsilon map-law/independence group, Exp first moment or normalized Exp sum limit is exported. The indicator argument is an ASTIS sufficient route, not evidence of the paper proof topology. No geometric V/Hessian/dimension premise appears, so later rank0/alphaeta1/zero-cap cases remain legal. Actual finite-recursion nonaccumulation still requires a separate consumer joining76 increments to these iid thresholds. No global PDMP/path/Markov/invariance/terminal kernel/main/cost/composition/full-paper conclusion follows from this review.')]
 write('independent-mathematical-proof.json',dict(status='ACCEPTED_WHOLE_IMPLEMENTATION',actor=ACTOR,module=pin(MOD),checked_parent=PARENT,source_boundary='Only mathematical truth of the concrete iid realization and its sufficient indicator/SLLN proof. No independent source-fidelity/coverage verdict.',proof=proof,strict_blockers=[],repair_required=False,proof_reviewer_did_not_edit_production=True))
 d=dict(schema='independent-math77/decision-v1',status='ACCEPTED_WHOLE_FROZEN_IMPLEMENTATION_MATH_ONLY',accepted_whole_mathematics=True,actual_PID=os.getpid(),actor=ACTOR,checked_parent=PARENT,checked_uncommitted_module=pin(MOD),module_lines=len(MOD.read_bytes().splitlines()),production_Lean_declarations=[TARGET],public_parameter_binders=0,logical_premises=0,literal_definitions=3,conclusion_groups=5,private_literal_statement_defs=1,private_proof_providers=0,compiler=pin(OWN/'compiler.json'),fresh_Lean_PID=c['actual_Lean_PID'],fresh_Lean_EXIT=0,axioms=c['axioms'],fake_closure_scan=pin(OWN/'fake-closure-scan.json'),mathematical_proof=pin(OWN/'independent-mathematical-proof.json'),seal_and_parent=pin(OWN/'statement-and-parent.json'),strict_blockers=[],source_verdict=False,decoder_verdict=False,exact_SCI77_verification=False,VERIFIED=False,PROVED_LOCAL_transition=False,canonical_Git_ledger_writes=False,aggregate_reader=False,PURIFIED=False,main=False,full_paper=False,Goal_complete=False,prior_header_approval_used_as_proof=False,remaining_boundary='Separate source/decoder/exact-commit admission and actual76 nonaccumulation/global path/PDMP/Markov/invariance/kernel/main/cost/composition remain pending.')
 write('decision.json',d)
 payload=dict(payload_name='COMPLETE_INDEPENDENT_WHOLE_MATHEMATICS77',decision=d,independent_mathematical_proof=load(OWN/'independent-mathematical-proof.json'),inputs_manifest=load(OWN/'inputs.manifest.json'),frozen=load(OWN/'frozen.json'),statement_and_parent=load(OWN/'statement-and-parent.json'),compiler=c,fake_closure_scan=load(OWN/'fake-closure-scan.json'),API_regions=load(OWN/'API-regions.json'),toolchain_readback=load(OWN/'toolchain-readback.json'),full_module_RAW_UTF8=MOD.read_bytes().decode('utf-8'),retained_own_negatives=[pin(p) for p in sorted(OWN.glob('negative.*.json'))])
 write('complete-named-math.payload.json',payload)
 run=dict(schema='independent-math77/run-v1',status=d['status'],actor=ACTOR,checked_parent=PARENT,uncommitted_module=pin(MOD),decision=pin(OWN/'decision.json'),inputs_manifest=pin(OWN/'inputs.manifest.json'),complete_named_RAW_payload=pin(OWN/'complete-named-math.payload.json'),compiler=pin(OWN/'compiler.json'),VERIFIED=False,source_verdict=False,canonical_Git_ledger_writes=False,wholelogical_recipe='Canonical UTF8 JSON ensure_ascii=false sort_keys=true separators comma/colon; remove ONLY the top-level run_sha256.')
 run['run_sha256']=sha(canon(run));write('run.json',run)
 print(json.dumps(dict(status=d['status'],actual_PID=os.getpid(),whole_logical_run_sha256=run['run_sha256'],complete_named_RAW_payload=run['complete_named_RAW_payload']['RAW_sha256'])),flush=True)
def readback():
 recheck();run=load(OWN/'run.json');h=run.pop('run_sha256');assert sha(canon(run))==h
 for k in ['decision','inputs_manifest','complete_named_RAW_payload','compiler']:check(run[k])
 assert load(OWN/'decision.json')['accepted_whole_mathematics'] and not run['VERIFIED']
 print(json.dumps(dict(status='READONLY_READBACK_PASS',actual_PID=os.getpid(),whole_logical_run_sha256=h)),flush=True)
def launch(action):
 assert not (OWN/'lease.final.json').exists();(OWN/(action+'.executed-helper.RAW.py')).write_bytes(Path(__file__).read_bytes())
 with (OWN/(action+'.stdout.RAW')).open('wb') as o,(OWN/(action+'.stderr.RAW')).open('wb') as e:
  p=subprocess.Popen([PY,'-B','-X','utf8',str(Path(__file__)),'_child',action],cwd=ROOT,stdout=o,stderr=e);print(json.dumps(dict(status='FOREGROUND_RUNNING',action=action,actual_PID=p.pid,runner_PID=os.getpid())),flush=True);code=p.wait()
 write(action+'.receipt.json',dict(action=action,actual_PID=p.pid,runner_PID=os.getpid(),exit_code=code,terminal_closed=True,stdout=pin(OWN/(action+'.stdout.RAW')),stderr=pin(OWN/(action+'.stderr.RAW')),executed_helper=pin(OWN/(action+'.executed-helper.RAW.py'))));print(json.dumps(dict(status='TERMINAL',action=action,actual_PID=p.pid,exit_code=code)),flush=True);return code
def close():
 assert not (OWN/'lease.final.json').exists();(OWN/'close.executed-helper.RAW.py').write_bytes(Path(__file__).read_bytes());readback();assert launch('readback')==0
 rows=[pin(p) for p in sorted(OWN.rglob('*')) if p.is_file()];run=load(OWN/'run.json')
 write('lease.final.json',dict(status='CLOSED_LAST',actor=ACTOR,actual_last_writer_PID=os.getpid(),closed_utc=now(),owned_count=len(rows)+1,all_owned_outputs_except_only_self=rows,closure_logical_sha256=sha(canon(rows)),whole_logical_run_sha256=run['run_sha256'],complete_named_RAW_payload=run['complete_named_RAW_payload'],all_child_sessions_closed=True,final_writer_terminal_qualification='Actual finalwriter EXIT must be observed by the external foreground tool. No postclose owned receipt is written.',postclose_owned_writes=False,canonical_Git_ledger_writes=False,VERIFIED=False))
 print(json.dumps(dict(status='CLOSED_LAST',actual_PID=os.getpid(),owned_count=len(rows)+1,lease=pin(OWN/'lease.final.json'))),flush=True)
def postclose():
 l=load(OWN/'lease.final.json');rows=[pin(p) for p in sorted(OWN.rglob('*')) if p.is_file() and p.name!='lease.final.json'];assert rows==l['all_owned_outputs_except_only_self'] and sha(canon(rows))==l['closure_logical_sha256'];readback();print(json.dumps(dict(status='READONLY_POSTCLOSE_PASS',actual_PID=os.getpid(),owned_count=len(rows)+1,lease=pin(OWN/'lease.final.json'),closure_logical_sha256=l['closure_logical_sha256'],owned_writes=False)),flush=True)
if __name__=='__main__':
 try:
  a=sys.argv[1]
  if a=='_child':globals()[sys.argv[2]]()
  elif a in ('close','postclose'):globals()[a]()
  else:sys.exit(launch(a))
 except BaseException as e:
  if not isinstance(e,SystemExit) and not (OWN/'lease.final.json').exists():write('negative.'+sys.argv[-1]+'.'+str(os.getpid())+'.json',dict(actual_PID=os.getpid(),error=repr(e),traceback=traceback.format_exc(),typed_failure='OBSERVER_OR_COMPILER_FAILURE_NOT_MATHEMATICAL_CERTIFICATE'))
  raise
