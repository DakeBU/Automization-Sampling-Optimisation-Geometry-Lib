import sys,os,json,hashlib,re,subprocess,datetime,traceback
from pathlib import Path
ROOT=Path('E:/Samplinglib');P=ROOT/'runs/20261007-companion-priority/pbps-sharp-energy68';O=P/'independent-math68';PRE=ROOT/'runs/20261007-companion-priority/pbps-sharp-energy-preproof68';BASE='38e5f34c6b2c82612459d54d6288a15e20d9deab';ACTOR='/root/exact_science63'
LEAF=ROOT/'AutoSamplingTheory/TechnicalLemmas/Analysis/HilbertCorrectorBound.lean';NAME='AutoSamplingTheory.TechnicalLemmas.Analysis.HilbertCorrectorBound.quadratic_corrector_bound_of_square_identity'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 p=Path(p);b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),raw_bytes=len(b),raw_sha256=sha(b),lf_bytes=len(l),lf_sha256=sha(l))
def save(n,v):
 p=O/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((json.dumps(v,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode())
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def get(n):return read(O/n)
def leafpins():
 for q in get('leaf.inputs.manifest.json')['inputs']:
  assert pin(q['original']['path'])==q['original'],('leaf-stage input changed',q['original']['path'])
  assert pin(q['RAW_snapshot']['path'])==q['RAW_snapshot'] and pin(q['LF_snapshot']['path'])==q['LF_snapshot']
 assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==BASE
def freeze_leaf():
 O.mkdir(parents=True,exist_ok=True);assert not (O/'lease.final.json').exists()
 assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==BASE
 save('lease.open.json',dict(status='OPEN_STAGED_MATHEMATICS_REVIEW',actor=ACTOR,actual_PID=os.getpid(),utc=now(),base=BASE,owned_scope=O.as_posix(),initial_stage='Shared leaf only; main/Test/source/publication/decoder/current owner verdicts deliberately unread until FINAL INPUTS READY68',canonical_Git_ledger_writes=False,VERIFIED=False))
 paths=[LEAF,ROOT/'lean-toolchain',ROOT/'lake-manifest.json',PRE/'header0-expanded.lean',PRE/'independent-header-math68/lease.final.json',P/'typed-leaf-learning68.json',ROOT/'research-wiki/sampling-sde-library/cards/AutoSamplingTheory.TechnicalLemmas.Analysis.md',ROOT/'.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Adjoint.lean',ROOT/'.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Basic.lean',ROOT/'.lake/packages/mathlib/Mathlib/Analysis/Normed/Operator/Basic.lean']
 for label in ['focused-leaf68-v1','focused-leaf68-v2']:
  paths += [P/label/'receipt.json',P/label/'stdout.log',P/label/'stderr.log']
 rows=[]
 for i,p in enumerate(paths):
  b=p.read_bytes();rp=O/f'leaf-inputs/{i:03}.RAW.snapshot';lp=O/f'leaf-inputs/{i:03}.LF.snapshot';rp.parent.mkdir(exist_ok=True);rp.write_bytes(b);lp.write_bytes(b.replace(b'\r\n',b'\n'));rows.append(dict(original=pin(p),RAW_snapshot=pin(rp),LF_snapshot=pin(lp)))
 save('leaf.inputs.manifest.json',dict(status='PINNED_BEFORE_FRESH_COMPILER',actual_PID=os.getpid(),utc=now(),checked_base=BASE,input_count=len(rows),inputs=rows,finite_historical_maps=[],no_actual_main_Test_source_publication_decoder_read=True))
 print(json.dumps(dict(status='PINNED_LEAF_ONLY',actual_PID=os.getpid(),inputs=len(rows))))
def leaf_compile():
 leafpins();cmd=['lake','env','lean','AutoSamplingTheory/TechnicalLemmas/Analysis/HilbertCorrectorBound.lean']
 with (O/'leaf.compiler.stdout.log').open('wb') as a,(O/'leaf.compiler.stderr.log').open('wb') as b:
  start=now();p=subprocess.Popen(cmd,cwd=ROOT,stdout=a,stderr=b);print(json.dumps(dict(event='FRESH_LEAF_START',actual_foreground_lake_PID=p.pid)),flush=True);code=p.wait()
 txt=(O/'leaf.compiler.stdout.log').read_text(encoding='utf-8')+(O/'leaf.compiler.stderr.log').read_text(encoding='utf-8')
 save('leaf.compiler.receipt.json',dict(command=cmd,actual_parent_PID=os.getpid(),actual_foreground_lake_PID=p.pid,started_utc=start,finished_utc=now(),exit_code=code,terminal_closed=True,fresh_Lean=True,olean_output_requested=False,stdout=pin(O/'leaf.compiler.stdout.log'),stderr=pin(O/'leaf.compiler.stderr.log')))
 assert code==0 and not re.search(r': error:|error\(|sorryAx',txt)
 matches=re.findall(re.escape(NAME)+r"' depends on axioms:\s*\[([^\]]+)\]",txt);assert len(matches)==1
 ax=[x.strip() for x in matches[0].split(',')];assert len(ax)==3 and set(ax)=={'propext','Classical.choice','Quot.sound'}
 leafpins();save('leaf.compiler.result.json',dict(status='PASS',actual_PID=os.getpid(),receipt=get('leaf.compiler.receipt.json'),exact_standard3=ax,pre_post_RAW_LF_unchanged=True))
 print(json.dumps(dict(status='PASS',actual_foreground_lake_PID=p.pid,axioms=ax)))
def leaf_review():
 leafpins();assert get('leaf.compiler.result.json')['status']=='PASS'
 t=LEAF.read_text(encoding='utf-8');h=(PRE/'header0-expanded.lean').read_text(encoding='utf-8');mark='theorem quadratic_corrector_bound_of_square_identity'
 sig=t.split(mark,1)[1].split(' := by',1)[0].rstrip();sealed=h.split(mark,1)[1].rstrip();assert sig==sealed
 assert not re.search(r'\b(sorry|admit|axiom|opaque|native_decide|run_tac|unsafe)\b',t.split('#print axioms')[0])
 assert not re.search(r'(?m)^(private )?(def|axiom|opaque|lemma)\b',t)
 assert len(re.findall(r'(?m)^theorem ',t))==1
 assert 'Nontrivial' not in sig and 'FiniteDimensional' not in sig and '1 ≤ c' not in sig and '(hc : 0 ≤ c)' in sig
 assert 'H × H' not in t and 'Prod.' not in t and 'WithLp' not in t
 neg=read(P/'typed-leaf-learning68.json');negative=[]
 for q in neg['failed_routes']:
  label=q['label'];assert pin(P/label/'receipt.json')['raw_sha256']==q['receipt_RAW_sha256'] and pin(P/label/'stdout.log')['raw_sha256']==q['stdout_RAW_sha256']
  log=(P/label/'stdout.log').read_text(encoding='utf-8');errors=[s for s in log.splitlines() if re.search(r'\berror(?::|\()',s)]
  negative.append(dict(label=label,typed=q['failure_class'],diagnosis=q['diagnosis'],actual_root_PID=q['actual_PID'],actual_error_lines=errors,failed_sorryAx_not_proof=True,receipt=pin(P/label/'receipt.json'),stdout=pin(P/label/'stdout.log')))
 v=dict(status='SHARED_LEAF_MATHEMATICS_ACCEPTED_WAITING_FINAL_INPUTS_READY68',actor=ACTOR,actual_review_PID=os.getpid(),checked_base=BASE,source_file=pin(LEAF),sealed_header0=pin(PRE/'header0-expanded.lean'),signature_RAW_LF_equal=True,compiler=get('leaf.compiler.result.json'),
  exact_claim='Arbitrary complete real Hilbert H; selfadjoint K,D; I+K²=D²; c≥0 and ||D||≤c imply |(1/2)(||u||²−||v||²)−<Ku,v>|≤(c/2)(||u||²+||v||²).',
  proof_audit=[
   'hEnergy applies the exact operator square identity to <A x,x>, and uses selfadjoint K and D to identify <K²x,x>=||Kx||² and <D²x,x>=||Dx||² for every x.',
   'hSym and hSwap use the correct real-inner orientation. Expanding ||u−Kv||²+||Ku+v||² cancels cross terms and gives ||Du||²+||Dv||². No default Prod norm is instantiated.',
   'hForm identifies the scalar block quadratic form with twice the target corrector. abs_sub and two ordinary Hilbert Cauchy-Schwarz inequalities bound its absolute value by a sum of products.',
   'hDx squares ||Dx||≤||D||||x||≤c||x|| only after proving nonnegativity using hc. This remains valid at c=0 and x=0.',
   'hCS is exactly the scalar two-component Lagrange/Cauchy-Schwarz identity: the difference of right and left sides is (||u−Kv||||v||−||Ku+v||||u||)²≥0.',
   'hSquared combines that scalar CS with the sum energy bound. Removing squares uses only nonnegative absolute value and c times nonnegative squared-energy sum; no c≥1, dimension or nonzero-vector argument.',
   'The final factor1/2 is literal algebra plus positivity, preserving the sharp c/2 constant. All nlinarith/ring steps close scalar identities/inequalities, without supplied mathematical providers.'],
  edge_cases=dict(zero_Hilbert_space='All vectors/norms vanish; the same proof handles c=0 without case split or unit-vector selection.',nontriviality_required=False,finite_H_required=False,c_ge_one_required=False,D_positive_required=False,pair_norm='sum of squared H norms, never default max product norm'),
  library_review=dict(home='TechnicalLemmas.Analysis generic reusable leaf',module_card=pin(ROOT/'research-wiki/sampling-sde-library/cards/AutoSamplingTheory.TechnicalLemmas.Analysis.md'),imports=['Mathlib.Analysis.InnerProductSpace.Adjoint','Mathlib.Tactic.Linarith','Mathlib.Tactic.Positivity','Mathlib.Tactic.Ring'],actual_operators='IsSelfAdjoint.isSymmetric, norm_add/sub_sq_real, real_inner_comm, real_inner_self_eq_norm_sq, abs_real_inner_le_norm, ContinuousLinearMap.le_opNorm, sq_le_sq₀; scalar ring/nlinarith',nearby_duplicate_search='Targeted Analysis folder search found no other corrector/square-identity leaf; not a full Mathlib semantic duplicate certificate.'),
  retained_typed_API_negatives=negative,private_math_providers=0,fake_closure_hits=0,mathematical_blockers=[],proof_repairs_required=[],
  stage_boundary='Shared leaf only. Actual main/Test/current publication/source/decoder/opinions unread. Wait FINAL INPUTS READY68 before whole-three-module review and final native closure.',source_fidelity_verdict=False,exact_SCI68_commit_review=False,VERIFIED=False,canonical_Git_ledger_writes=False,full_Exposition=False,PURIFIED=False)
 save('shared-leaf.mathematical-review.json',v)
 save('shared-leaf.ready-capsule.json',dict(status=v['status'],actual_PID=os.getpid(),base=BASE,leaf_RAW=v['source_file'],fresh_compiler=v['compiler']['receipt'],mathematical_verdict=pin(O/'shared-leaf.mathematical-review.json'),lease_status='OPEN_WAITING_FINAL_INPUTS_READY68',canonical_writes=False))
 print(json.dumps(dict(status=v['status'],actual_PID=os.getpid(),leaf_RAW=v['source_file']['raw_sha256'],remaining_math_blockers=0)))
if __name__=='__main__':
 mode=sys.argv[1]
 try:{'freeze-leaf':freeze_leaf,'leaf-compile':leaf_compile,'leaf-review':leaf_review}[mode]()
 except Exception as e:
  if not (O/'lease.final.json').exists():save((sys.argv[2] if len(sys.argv)>2 else mode)+'.failure.json',dict(actual_PID=os.getpid(),utc=now(),mode=mode,error=repr(e),traceback=traceback.format_exc()))
  raise
