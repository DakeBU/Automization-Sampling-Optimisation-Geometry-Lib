import sys, os, json, hashlib, subprocess, re, datetime, traceback
from pathlib import Path
ROOT = Path('E:/Samplinglib')
P = ROOT/'runs/20261007-companion-priority/pbps-sharp-energy-preproof68'
O = P/'independent-header-math68'
PR = ROOT/'runs/20261007-companion-priority/pbps-first-corrector-energy-preproof67'
M = ROOT/'runs/20261007-companion-priority/pbps-root-commutation67/independent-math67'
ACTOR = '/root/exact_science63'
BASE = 'eb3d5ffbb6853f2a0aa4a8c66aefce19d8050176'
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def raw(p):
 p=Path(p); b=p.read_bytes(); lf=b.replace(b'\r\n',b'\n')
 return dict(path=p.as_posix(),raw_bytes=len(b),raw_sha256=sha(b),lf_bytes=len(lf),lf_sha256=sha(lf))
def save(n,v):
 p=O/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((json.dumps(v,ensure_ascii=False,indent=2,sort_keys=True)+'\n').encode())
def read(n): return json.loads((O/n).read_text(encoding='utf-8'))
def logical(v): return sha(json.dumps({k:x for k,x in v.items() if k!='run_sha256'},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def pincheck():
 m=read('inputs.manifest.json')
 maps=read('qualified.alpha-renaming.maps.json')['maps'] if (O/'qualified.alpha-renaming.maps.json').exists() else []
 for x in m['inputs']:
  if raw(x['path'])!=x['original']:
   q=[q for q in maps if q['path']==x['path']];assert len(q)==1,('unqualified current input changed',x['path'])
   assert raw(x['path'])==q[0]['after'] and q[0]['before_sha256']==x['original']['raw_sha256']
  assert raw(x['RAW_snapshot'])['raw_sha256']==x['original']['raw_sha256']
  assert raw(x['LF_snapshot'])['raw_sha256']==x['original']['lf_sha256']
 if maps:
  for x in read('qualified.alpha-renaming.maps.json')['authority_and_snapshot_pins']:assert raw(x['path'])==x
 return m
def resolution():
 authority=P/'alpha-renaming-weight68/applied.json';a=json.loads(authority.read_text(encoding='utf-8'))
 assert len(a['maps'])==2 and not a['source_mathematical_repair'] and not a['proof_search']
 initial=read('inputs.manifest.json');maps=[];pins=[raw(authority)]
 for q in a['maps']:
  p=ROOT/q['path'];before=authority.parent/q['before_snapshot'];after=authority.parent/q['after_snapshot']
  old=[x for x in initial['inputs'] if x['path']==p.as_posix()];assert len(old)==1
  bb=before.read_bytes();ab=after.read_bytes();assert sha(bb)==q['before_raw_sha256']==old[0]['original']['raw_sha256']
  assert bb==Path(old[0]['RAW_snapshot']).read_bytes();assert sha(ab)==q['after_raw_sha256']==raw(p)['raw_sha256']
  assert bb.count('ω'.encode())==q['bound_identifier_occurrences']==6
  assert ab==bb.replace('ω'.encode(),b'omegaWeight')
  maps.append(dict(path=p.as_posix(),before_sha256=sha(bb),after=raw(p),before_snapshot=raw(before),after_snapshot=raw(after),exact_byte_substitution='six Unicode omega -> omegaWeight, only bound-name alpha-renaming'))
  pins.extend([raw(before),raw(after)])
 save('qualified.alpha-renaming.maps.json',dict(status='PASS',actual_pid=os.getpid(),finite_explicit_maps_only=True,mathematical_repair=False,maps=maps,authority_and_snapshot_pins=pins))
 pincheck()
 prefix,name,caller,body=split_header((P/'header2-expanded.lean').read_text(encoding='utf-8'))
 dn,dc,db=split_def((P/'statement2.definition.lean').read_text(encoding='utf-8'));assert caller==dc and db==body+'\n'
 old=[x for x in initial['inputs'] if x['path']==(P/'header2-expanded.lean').as_posix()][0]
 _,_,oc,_=split_header(Path(old['RAW_snapshot']).read_text(encoding='utf-8'));assert caller==oc
 t=prefix+'private def repaired_expanded2\n'+caller+' : Prop :=\n'+body+'\n'+(P/'statement2.definition.lean').read_text(encoding='utf-8')+'\n#check repaired_expanded2\n#check genuine_actual_modified_energy_equivalence_statement\n'
 (O/'repaired-header2-elaboration.lean').write_text(t,encoding='utf-8',newline='\n')
 print(json.dumps(dict(status='PASS',actual_pid=os.getpid(),finite_maps=2,only_bound_identifier_changed=True)))
def repair_compile():
 pincheck();cmd=['lake','env','lean',str(O/'repaired-header2-elaboration.lean')]
 pre=[raw(P/'header2-expanded.lean'),raw(P/'statement2.definition.lean')]
 with (O/'repair-elaboration.stdout.log').open('wb') as a,(O/'repair-elaboration.stderr.log').open('wb') as b:
  start=now();p=subprocess.Popen(cmd,cwd=ROOT,stdout=a,stderr=b);print(json.dumps(dict(event='FRESH_REPAIRED_PROP_START',launched_lake_PID=p.pid)),flush=True);code=p.wait()
 post=[raw(P/'header2-expanded.lean'),raw(P/'statement2.definition.lean')];assert pre==post
 txt=(O/'repair-elaboration.stdout.log').read_text(encoding='utf-8')+(O/'repair-elaboration.stderr.log').read_text(encoding='utf-8')
 save('repair-elaboration.terminal.json',dict(command=cmd,actual_runner_pid=os.getpid(),launched_lake_PID=p.pid,exit_code=code,started_utc=start,finished_utc=now(),terminal_closed=True,fresh_Lean_Prop_typecheck=True,no_target_proof=True,no_generic_actual_or_API_repeat=True,pre_pins=pre,post_pins=post,stdout_RAW=raw(O/'repair-elaboration.stdout.log'),stderr_RAW=raw(O/'repair-elaboration.stderr.log')))
 assert code==0 and not re.search(r': error:|error\(|sorryAx',txt)
 print(json.dumps(dict(status='PASS',launched_lake_PID=p.pid,exit_code=0)))
def split_header(t):
 m=re.search(r'(?m)^theorem ',t);assert m is not None
 a,b=t[:m.start()],t[m.end():]; name,tail=b.split('\n',1)
 marker=') :\n'
 i=tail.index(marker)+1
 return a+'\n',name.strip(),tail[:i],tail[i+len(' :\n'):]
def split_def(t):
 a,b=t.split('\n',1); name=a.removeprefix('private def ').strip()
 marker=') : Prop :=\n';i=b.index(marker)+1
 return name,b[:i],b[i+len(' : Prop :=\n'):]
def freeze():
 O.mkdir(parents=True,exist_ok=True)
 assert not (O/'lease.final.json').exists()
 save('lease.open.json',dict(status='OPEN',actor=ACTOR,actual_pid=os.getpid(),utc=now(),owned_scope=O.as_posix(),no_proof_search=True,no_canonical_writes=True))
 paths=[P/'draft68.json',*[P/f'header{i}-expanded.lean' for i in range(3)],*[P/f'statement{i}.definition.lean' for i in (1,2)],
  PR/'header1-expanded.lean',PR/'header2-expanded.lean',PR/'root.primary67.adoption.json',
  PR/'independent-primary67/source-proof-graph.json',PR/'independent-primary67/source-coverage-inventory.json',
  PR/'independent-primary67/source.corrector-sharp-energy-and-consumers-B3.rendered.txt',
  PR/'independent-primary67/source.corrector-sharp-energy-and-consumers-B3.RAW.html',
  PR/'independent-primary67/literal-formulas-and-conditions.json',PR/'independent-primary67/lease.final.json',
  M/'lease.final.json',M/'mathematical-review.json',M/'mathematical-review.named.raw.json',M/'run.json',
  ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualRootCommutation.lean',ROOT/'Tests/ProximalBPSActualRootCommutation.lean',
  ROOT/'lean-toolchain',ROOT/'lake-manifest.json',
  ROOT/'.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Basic.lean',
  ROOT/'.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Adjoint.lean',
  ROOT/'.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/ProdL2.lean',
  ROOT/'.lake/packages/mathlib/Mathlib/Analysis/Normed/Lp/ProdLp.lean',
  ROOT/'.lake/packages/mathlib/Mathlib/Analysis/Normed/Operator/Basic.lean']
 items=[]
 for i,p in enumerate(paths):
  b=p.read_bytes();rp=O/f'inputs/{i:03}.RAW.snapshot';lp=O/f'inputs/{i:03}.LF.snapshot';rp.parent.mkdir(exist_ok=True)
  rp.write_bytes(b);lp.write_bytes(b.replace(b'\r\n',b'\n'))
  items.append(dict(path=p.as_posix(),original=raw(p),RAW_snapshot=rp.as_posix(),LF_snapshot=lp.as_posix()))
 head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();assert head==BASE
 draft=json.loads((P/'draft68.json').read_text(encoding='utf-8'))
 assert draft['status']=='HEADER68_DRAFT_NOT_SEALED_NOT_CLAIMED_NO_PROOF_SEARCH'
 for h in draft['headers']: assert raw(ROOT/h['path'])['raw_sha256']==h['RAW_sha256']
 save('inputs.manifest.json',dict(status='PINNED',actual_pid=os.getpid(),utc=now(),checked_base=BASE,headers_unsealed_unclaimed=True,inputs=items,finite_historical_maps=[],recursive_history_scan=False))
 save('observer-console-truncation.json',dict(status='PRESERVED_OBSERVER_LIMITATION',failure_class='NONE',description='Initial console displayed truncation on combined source/old math verdict reads; exact complete necessary files are now RAW/LF pinned, and bounded source regions and verdict scalar fields are used. No compiler or mathematical failure.'))
 print(json.dumps(dict(status='PINNED',actual_pid=os.getpid(),inputs=len(items),base=BASE)))
def structural():
 pincheck();out=[];gen=[];common=None
 for i in range(3):
  t=(P/f'header{i}-expanded.lean').read_text(encoding='utf-8');prefix,name,caller,body=split_header(t)
  if common is None: common=prefix
  assert prefix==common
  assert not re.search(r'\b(sorry|admit|axiom|opaque|native_decide|run_tac)\b',t)
  d=f'private def expanded{i}\n'+caller+' : Prop :=\n'+body
  gen.append(d)
  entry=dict(header=i,name=name,header_RAW=raw(P/f'header{i}-expanded.lean'),caller_RAW_sha256=sha(caller.encode()),body_RAW_sha256=sha(body.encode()),no_target_proof=True)
  if i:
   dt=(P/f'statement{i}.definition.lean').read_text(encoding='utf-8');dn,dc,db=split_def(dt)
   assert dc==caller,('private caller mismatch',i)
   assert db==body or (i==2 and db==body+'\n'),('private full Prop BODY mismatch',i)
   entry.update(private_name=dn,literal_private_caller_equal=True,literal_private_body_RAW_equal=(db==body),all_Lean_tokens_equal=True,exact_difference=('one additional trailing empty line in private definition BODY' if db!=body else None),private_definition_RAW=raw(P/f'statement{i}.definition.lean'))
   _,_,oldcaller,_=split_header((PR/f'header{i}-expanded.lean').read_text(encoding='utf-8'))
   assert oldcaller==caller,('original67 caller drift',i)
   assert not re.search(r'Nontrivial|IsProbabilityMeasure|Commute|IsUnit|Inv|Γ|hNorm',caller)
   entry['original67_caller_exact_equal']=True
   gen.append(dt)
  out.append(entry)
 assert 'Nontrivial' not in out[0].get('caller','')
 generic=(P/'header0-expanded.lean').read_text(encoding='utf-8')
 assert '[FiniteDimensional' not in generic and 'Nontrivial' not in generic and '(hc : 0 ≤ c)' in generic and '1 ≤ c' not in generic
 assert '‖u‖^2+‖v‖^2' in generic and 'H × H' not in generic
 test=(P/'header2-expanded.lean').read_text(encoding='utf-8')
 actual=(P/'header1-expanded.lean').read_text(encoding='utf-8')
 assert '0<ω → ω≤γ' in test and '‖fP‖^2+‖fV‖^2≤‖f‖^2' in actual
 checks='\n'.join(['#check expanded0','#check expanded1','#check expanded2','#check actual_sharp_corrector_bound_statement','#check genuine_actual_modified_energy_equivalence_statement',
 '#check norm_add_sq_real','#check norm_sub_sq_real','#check real_inner_self_eq_norm_sq','#check real_inner_comm','#check abs_real_inner_le_norm',
 '#check ContinuousLinearMap.isSelfAdjoint_iff_isSymmetric','#check ContinuousLinearMap.apply_norm_sq_eq_inner_adjoint_left','#check ContinuousLinearMap.le_opNorm',
 '#check WithLp.prod_norm_sq_eq_of_L2','#check WithLp.prod_inner_apply',
 '#check AutoSamplingTheory.ExampleCases.ProximalBPS.ActualRootCommutation.actual_same_root_inverse_commutation',
 'section','variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℝ H] [CompleteSpace H]',
 '#synth InnerProductSpace ℝ (WithLp 2 (H × H))','#synth CompleteSpace (WithLp 2 (H × H))','end'])
 # Definitions return Prop expressions; none asserts or proves a target theorem.
 (O/'header-elaboration.lean').write_text(common.replace('import AutoSamplingTheory','import Mathlib.Analysis.InnerProductSpace.ProdL2\nimport AutoSamplingTheory',1)+'\n\n'.join(gen)+'\n'+checks+'\n',encoding='utf-8',newline='\n')
 save('structural.result.json',dict(status='PASS_WITH_ONE_TRAILING_EMPTY_LINE_DELTA',actual_pid=os.getpid(),headers=out,full_private_definition_token_equality=2,private_math_providers=0,original_callers_preserved=True,pair_norm='explicit sum of squared Hilbert norms; no Prod max-norm',rank0_legal=True,alpha_eta_one_legal=True,no_extra_public_premise=True,no_proof_search=True))
 save('observer.failures.qualification.json',dict(status='RETAINED',first_parser_failure='Old67 header starts directly with theorem, not import-prefixed. Initial actual24828 EXIT1 exact structural.stderr.log,stdout,terminal and executed-helper snapshot retained.',summary_overwrite='structural.failure.json was initially overwritten by second observer comparison failure; the original complete stderr/terminal/executed-helper bytes remain losslessly retained. No reconstruction of that overwritten JSON is claimed.',second_comparison_failure='Actual52304 EXIT1 found exact extra trailing empty line. Full stderr/terminal/helper and structural-v2.failure.json retained. No mathematical or compiler failure.',format_delta='statement2 BODY equals header2 BODY plus one newline, all Lean tokens equal. Canonical drafts untouched.'))
 print(json.dumps(dict(status='PASS_WITH_ONE_TRAILING_EMPTY_LINE_DELTA',actual_pid=os.getpid(),header_count=3,private_token_equal=2)))
def compile_headers():
 pincheck();before=[raw(p) for p in [P/f'header{i}-expanded.lean' for i in range(3)]]
 cmd=['lake','env','lean',str(O/'header-elaboration.lean')]
 with (O/'elaboration.stdout.log').open('wb') as a,(O/'elaboration.stderr.log').open('wb') as b:
  start=now();proc=subprocess.Popen(cmd,cwd=ROOT,stdout=a,stderr=b);pid=proc.pid;print(json.dumps(dict(event='LEAN_START',actual_compiler_pid=pid)),flush=True);code=proc.wait()
 text=(O/'elaboration.stdout.log').read_text(encoding='utf-8')+(O/'elaboration.stderr.log').read_text(encoding='utf-8')
 after=[raw(p) for p in [P/f'header{i}-expanded.lean' for i in range(3)]];assert before==after
 save('elaboration.terminal.json',dict(command=cmd,actual_runner_pid=os.getpid(),actual_compiler_pid=pid,started_utc=start,finished_utc=now(),exit_code=code,terminal_closed=True,fresh_compiler=True,target_theorem_proof=False,pre_pins=before,post_pins=after,stdout_RAW=raw(O/'elaboration.stdout.log'),stderr_RAW=raw(O/'elaboration.stderr.log')))
 assert code==0,('header/API elaboration failed',code)
 assert not re.search(r'error:|error\(|sorryAx|declaration uses .sorry.',text)
 save('elaboration.result.json',dict(status='PASS',actual_pid=os.getpid(),actual_compiler_pid=pid,only_Prop_definitions_and_existing_API_checks=True,no_theorem_proof_credit=True))
 print(json.dumps(dict(status='PASS',actual_compiler_pid=pid,exit_code=code)))
def verdict():
 pincheck();et=read('elaboration.terminal.json');assert et['exit_code']==1
 assert read('repair-elaboration.terminal.json')['exit_code']==0
 log=(O/'elaboration.stdout.log').read_text(encoding='utf-8')
 errors=[s for s in log.splitlines() if ': error:' in s]
 assert len(errors)==2 and all("unexpected token 'ω'" in s for s in errors)
 ft=ROOT/'.lake/packages/mathlib/Mathlib/Analysis/Calculus/ContDiff/FTaylorSeries.lean'
 fb=ft.read_bytes();(O/'ContDiff.FTaylorSeries.RAW.snapshot').write_bytes(fb);(O/'ContDiff.FTaylorSeries.LF.snapshot').write_bytes(fb.replace(b'\r\n',b'\n'))
 fl=fb.splitlines(keepends=True);notation=[i for i,s in enumerate(fl) if b'scoped[ContDiff] notation3' in s and 'ω'.encode() in s];assert len(notation)==1
 ix=notation[0]
 original=[x['original'] for x in read('inputs.manifest.json')['inputs'] if Path(x['path']).name in ['header2-expanded.lean','statement2.definition.lean']]
 save('header2.parse-obstruction.json',dict(status='RETAINED_SYNTAX_FAILURE_RESOLVED_BY_EXACT_ALPHA_RENAMING',failure_class='API_BLOCKED',exact_errors=errors,actual_Lean_child_PID=35028,foreground_lake_EXIT=1,scope_source_RAW=raw(ft),scope_source_snapshot_RAW=raw(O/'ContDiff.FTaylorSeries.RAW.snapshot'),scope_source_snapshot_LF=raw(O/'ContDiff.FTaylorSeries.LF.snapshot'),source_line=ix+1,exact_RAW_line_sha256=sha(fl[ix]),literal_notation=fl[ix].decode(),affected_original_files=original,smallest_correction='Rename exactly six occurrences of bound weight omega to ASCII omegaWeight in each file. Preserve caller, conditions, scopes and mathematical target.',mathematical_repair=False,root_only_alpha_renaming_applied=True,qualified_finite_maps=read('qualified.alpha-renaming.maps.json'),fresh_repaired_full_Prop_terminal=read('repair-elaboration.terminal.json'),header0_header1_and_APIs='No errors reported on their full Prop definitions/API checks in original run; original overall EXIT1 preserved. Only repaired Test full Prop rerun, no target proof credit.',failed_error_recovery_declarations_not_accepted=True))
 processes=json.loads((O/'compiler.live-process-observation.json').read_text(encoding='utf-8-sig'))
 lean=[p for p in processes if p['Name']=='lean.exe'];assert len(lean)==1 and lean[0]['ProcessId']==35028
 assert lean[0]['ParentProcessId']==39056
 save('compiler.PID.qualification.json',dict(status='ACTUAL_LIVE_PROCESS_TREE_PINNED',launched_lake_shim_PID=33452,toolchain_lake_PID=39056,actual_Lean_child_PID=35028,original_receipt_field='actual_compiler_pid=33452 names the launched Lake shim; not the Lean child',terminal_outcome='Fresh Lean child failure propagated through foreground lake env lean EXIT1; no separate direct child exit code claimed',no_build_or_olean_output=True,observation_RAW=raw(O/'compiler.live-process-observation.json')))
 a=json.loads((PR/'root.primary67.adoption.json').read_text(encoding='utf-8'))
 assert a['classified_math_items']==344
 inventory=json.loads((PR/'independent-primary67/source-coverage-inventory.json').read_text(encoding='utf-8'))
 assert inventory['count']==344 and len(inventory['math_items'])==344 and inventory['all_classified'] and inventory['missing_items']==0
 assert raw(PR/'independent-primary67/source-proof-graph.json')['raw_sha256']==a['source_graph_sha256']
 assert raw(M/'lease.final.json')['raw_sha256']=='e98cc7a699edf6827583c6d40a00505445cd033588693788b152afddc9b66425'
 prior=json.loads((M/'mathematical-review.json').read_text(encoding='utf-8'))
 assert prior['status']=='ACCEPTED_MATHEMATICS_WITH_PRESENTATION_RESOLUTION_REQUIRED'
 source=(PR/'independent-primary67/source.corrector-sharp-energy-and-consumers-B3.rendered.txt').read_bytes().decode('utf-8')
 rows=[]
 lines=source.splitlines(keepends=True)
 for key in ['A2.E19.m1','A2.E20.m1','A2.E22.m1','A2.E23.m1','A2.E24.m1','A2.E24.m2','A2.Ex19.m1','A2.Ex20.m1','A2.Ex21.m1','A2.Ex22.m1']:
  ids=[i for i,l in enumerate(lines) if key in l];assert len(ids)==1
  i=ids[0];j=i+1
  while j<len(lines) and ']' not in ''.join(lines[i:j]):j+=1
  b=''.join(lines[i:j]).encode();rows.append(dict(id=key,start_line=i+1,end_line=j,exact_region_RAW_sha256=sha(b),literal=b.decode()))
 save('source.B3.bounded-regions.json',dict(whole_rendered_RAW=raw(PR/'independent-primary67/source.corrector-sharp-energy-and-consumers-B3.rendered.txt'),line_span_hashes_distinct_from_whole_file=True,regions=rows))
 v=dict(status='ACCEPTED_REPAIRED_HEADER_DRAFTS_MATHEMATICALLY_FEASIBLE',actor=ACTOR,actual_review_pid=os.getpid(),checked_base=BASE,
  scope='Unsealed/unclaimed statement and type/API review only. No theorem implementation, proof search, SCI68 exact-commit review, VERIFIED or source67 final decision.',
  headers=read('structural.result.json')['headers'],
  source_authority=dict(primary67_items=344,inventory_all_classified=True,inventory_missing_items=0,source_graph_RAW=a['source_graph_sha256'],source_before67_implementation=True,final_candidate_source67_verdict_consumed=False,numbering='B20 definition, B23 sharp bound, B19 Lyapunov definition, B22/B24 equivalence; B21 and B4 independent'),
  seven_slots=dict(objects='Same original μ,J,ν,S,e,U,T,A,B,Γ,ΓP,q,qP,HP0,ΓP0,Inv,A0,B0,V0,R, actual fP/fperp/fV; C defined from same A0 Inv.',domains='Generic arbitrary complete real Hilbert H. Actual original finite-dimensional real E with Borel measure, true HP/ker inner qP and kerP. Inv acts only on HP0.',quantifiers='Generic forall K,D,c,u,v under listed operator hypotheses; actual existential same witnesses followed by all u,v HP0 and all globally centered joint f; Test additionally all 0<ω≤γ.',assumptions='Actual caller RAW equals67 original caller: C2 V,0<α≤β, two global Hessian bounds,η>0,βη≤1. Probability/range/root/inverse/gap/commutation/norm estimates remain internally derived conclusions.',conclusion='Exact sharp pair C and global B23, then same-f Lω B19 with B22 half/three-halves bounds and B24 absolute perturbation chain.',senses='Real inner product; pair energy explicitly norm-square sum, not default Prod max norm. Actual centered global integral and conditional kernel distinguished.',constants='c≥0 and normD≤c only; c≥1/Nontrivial absent. Actual c=1/γ from same inverse, γ>0 internally; rank0 and αη=1 legal; ω=γ endpoint included.'),
  mathematical_feasibility=[
   'For the generic leaf, the formal block on the sum Hilbert space is [[I,-K],[-K,-I]]. Its quadratic form is twice the displayed corrector, using hK symmetry.',
   'Algebraic feasibility audit: the sum squared output norm is ||u-Kv||²+||Ku+v||²; cross terms cancel by selfadjoint K. hSquare and selfadjoint D identify the remaining sum with ||Du||²+||Dv||². This is a mathematical audit, not a Lean proof artifact.',
   'Cauchy-Schwarz in the genuine Hilbert sum and normD≤c yield the sharp c/2 constant. A direct scalar two-component Cauchy-Schwarz route can avoid constructing a block CLM; no theorem implementation is supplied.',
   'No c≥1 argument or nonzero vector selection is required. The zero Hilbert space satisfies the target for every c≥0, including c=0; on nontrivial spaces hSquare would imply a lower norm bound, but it need not become a caller premise.',
   'Actual67 Test supplies same K=A0 Inv selfadjoint and I+K²=Inv², while actual67 main supplies same inverse and global decomposition budget. These are internal dependency edges, not added paper inputs.',
   'Production68 must derive the K selfadjoint/square identities internally from the accepted actual67 main ingredients; the preceding genuine Test witnesses their feasibility and must not become a production import or public caller premise.',
   'The Test B19/B22/B24 tail follows arithmetically from sharp B23 and 0<ω≤γ. No idealized rotation B21 or dynamics B4 is needed for these statements.'],
  representation=dict(two_private_full_Props_literal_tokens=True,caller_RAW_equal=True,entire_BODY_RAW_equal=False,generated_differences=['statement2.definition.lean has exactly one extra trailing empty line versus header2-expanded BODY; all Lean tokens equal. statement1 BODY RAW equal.'],mathematical_difference=False,new_provider=False),
  API_retrieval=dict(existing=['real_inner_self_eq_norm_sq','norm_add_sq_real','norm_sub_sq_real','real_inner_comm','abs_real_inner_le_norm','ContinuousLinearMap.isSelfAdjoint_iff_isSymmetric','ContinuousLinearMap.apply_norm_sq_eq_inner_adjoint_left','ContinuousLinearMap.le_opNorm','WithLp.prod_norm_sq_eq_of_L2','WithLp.prod_inner_apply'],additional_minimal_import='Mathlib.Analysis.InnerProductSpace.ProdL2 only if implementation chooses actual WithLp2 block; direct scalar sum route can reuse existing imports',actual_fresh_elaboration=read('elaboration.terminal.json'),PID_qualification=read('compiler.PID.qualification.json'),catalogue_is_not_formal_dependency_credit=True),
  blockers=[],retained_resolved_parse_failure=read('header2.parse-obstruction.json'),proposed_mathematical_repairs=[],accepted_bound_alpha_renaming=read('qualified.alpha-renaming.maps.json'),sealing_conditions=['Root must seal exact reviewed repaired draft bytes before any proof search; original draft68.json historical header2 hash remains original and is not silently treated as current.','Actual source67 final review/publication attribution overlay remains independently pending, not inherited as completed source acceptance.','Fresh final mathematical/source/publication review required after any68 implementation; this header feasibility verdict proves no target theorem.'],
  remaining_boundary=['B21 actual idealized rotation/corrector change','B2 weak H1','B4 one-step Lyapunov decay and dynamics','full main theorem','errors/caps/expected costs','actual-input composition','full Exposition/PURIFIED/paper/Goal completion'],
  fake_closure=dict(status='NO_AUTHORED_FAKE_CLOSURE; FAILED_ELABORATION_NOT_ACCEPTED',no_authored_sorry_axiom_or_target_assumption=True,no_target_theorem_declared_in_typecheck=True,error_recovery_Prop_definitions_never_given_theorem_credit=True),
  conceptual_mirror=dict(status='not_promoted',reason='Statement/API review only; no new mathematical mechanism discovery or source/mirror certification.'),
  canonical_writes=False,SAU_transition=False,Statement_Seal=False,proof_search=False,full_Exposition=False,PURIFIED=False,utc=now())
 save('header-mathematical-review.json',v);print(json.dumps(dict(status=v['status'],actual_pid=os.getpid(),remaining_blockers=0,resolved_parse_failure=1,harmless_trailing_empty_line_difference=1)))
def owned(): return [p for p in sorted(O.rglob('*')) if p.is_file()]
def terminal_ok(n):
 t=read(n+'.terminal.json');assert t['exit_code']==(1 if n=='compile' else 0) and t['terminal_closed'];return t
def finalize():
 pincheck();v=read('header-mathematical-review.json');assert v['status']=='ACCEPTED_REPAIRED_HEADER_DRAFTS_MATHEMATICALLY_FEASIBLE'
 ts={n:terminal_ok(n) for n in ['freeze','structural-v3','compile','resolution','repair-compile','verdict']}
 excludes={'finalize.stdout.log','finalize.stderr.log'}
 pre=[raw(p) for p in owned() if p.name not in excludes]
 payload=dict(full_verdict=v,inputs=read('inputs.manifest.json'),structural=read('structural.result.json'),source_regions=read('source.B3.bounded-regions.json'),complete_pre_finalizer_owned_outputs=pre,observer_limitations=read('observer-console-truncation.json'),observer_failure_qualification=read('observer.failures.qualification.json'),stage_terminals=ts,failed_stage_records=[json.loads(p.read_text(encoding='utf-8')) for p in O.glob('*.failure.json')])
 save('complete.named-review.RAW.json',payload)
 run=dict(schema=1,actor=ACTOR,status=v['status'],base=BASE,actual_finalizer_pid=os.getpid(),utc=now(),complete_named_RAW=raw(O/'complete.named-review.RAW.json'),simple_verdict_RAW=raw(O/'header-mathematical-review.json'),whole_hash_rule='canonical UTF8 logical JSON removing ONLY top-level run_sha256',input_count=len(read('inputs.manifest.json')['inputs']),no_proof_search=True,no_VERIFIED=True,pre_finalizer_owned=pre)
 run['run_sha256']=logical(run);save('run.json',run);save('finalizer.result.json',dict(status='PASS',actual_pid=os.getpid(),whole_logical=run['run_sha256'],complete_named_RAW=run['complete_named_RAW']))
 print(json.dumps(dict(status='PASS',whole_logical=run['run_sha256'],namedRAW=run['complete_named_RAW'])))
def readback():
 pincheck();r=read('run.json');assert logical(r)==r['run_sha256'];assert raw(O/'complete.named-review.RAW.json')==r['complete_named_RAW'];assert raw(O/'header-mathematical-review.json')==r['simple_verdict_RAW']
 for x in r['pre_finalizer_owned']:assert raw(x['path'])==x
 t=terminal_ok('finalize');save('readback.result.json',dict(status='PASS',actual_pid=os.getpid(),whole_logical=r['run_sha256'],actual_finalizer=t));print(json.dumps(dict(status='PASS',actual_pid=os.getpid())))
def close():
 pincheck();r=read('run.json');assert logical(r)==r['run_sha256'];assert read('readback.result.json')['status']=='PASS';t=terminal_ok('readback');f=terminal_ok('finalize')
 save('close.result.json',dict(status='PASS',actual_pid=os.getpid(),utc=now(),whole_logical=r['run_sha256'],all_sessions_closed=True))
 m=[raw(p) for p in owned()];save('final.manifest.json',dict(status='ALL_OWNED_BEFORE_FINAL_LEASE',files=m,manifest_excludes_only_self_and_future_lease=True))
 allpins=[raw(p) for p in owned()]
 lease=dict(status='CLOSED_LAST',actor=ACTOR,actual_close_pid=os.getpid(),utc=now(),owned_count_including_lease=len(allpins)+1,all_owned_except_final_lease=allpins,whole_logical_run_sha256=r['run_sha256'],complete_named_RAW=r['complete_named_RAW'],simple_verdict_RAW=r['simple_verdict_RAW'],actual_finalizer_pid=f['actual_worker_pid'],actual_finalizer_exit=0,actual_readback_pid=t['actual_worker_pid'],actual_readback_exit=0,no_proof_search=True,no_VERIFIED=True,final_owned_write=True)
 save('lease.final.json',lease);print(json.dumps(dict(status='CLOSED_LAST',actual_close_pid=os.getpid(),owned_count=lease['owned_count_including_lease'],whole_logical=r['run_sha256'],namedRAW=r['complete_named_RAW'],leaseRAW=raw(O/'lease.final.json'))))
def postclose():
 pincheck();l=read('lease.final.json');assert l['status']=='CLOSED_LAST';assert len(owned())==l['owned_count_including_lease']
 for x in l['all_owned_except_final_lease']:assert raw(x['path'])==x
 assert max(p.stat().st_mtime_ns for p in owned())==(O/'lease.final.json').stat().st_mtime_ns
 r=read('run.json');assert logical(r)==r['run_sha256'];print(json.dumps(dict(status='READ_ONLY_POSTCLOSE_PASS',actual_pid=os.getpid(),owned_count=len(owned()),whole_logical=r['run_sha256'],complete_named_RAW=r['complete_named_RAW'],leaseRAW=raw(O/'lease.final.json'),owned_writes=0)))
if __name__=='__main__':
 mode=sys.argv[1]
 try: {'freeze':freeze,'structural':structural,'compile':compile_headers,'resolution':resolution,'repair-compile':repair_compile,'verdict':verdict,'finalize':finalize,'readback':readback,'close':close,'postclose':postclose}[mode]()
 except Exception as e:
  if mode not in ['close','postclose'] and not (O/'lease.final.json').exists():save((sys.argv[2] if len(sys.argv)>2 else mode)+'.failure.json',dict(mode=mode,actual_pid=os.getpid(),utc=now(),error=repr(e),traceback=traceback.format_exc()))
  raise
