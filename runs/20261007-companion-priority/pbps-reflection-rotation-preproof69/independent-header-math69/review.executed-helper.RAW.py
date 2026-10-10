import sys,os,json,hashlib,subprocess,datetime,re,traceback
from pathlib import Path
ROOT=Path('E:/Samplinglib');P=ROOT/'runs/20261007-companion-priority/pbps-reflection-rotation-preproof69';O=P/'independent-header-math69';ACTOR='/root/exact_science63';BASE='38e5f34c6b2c82612459d54d6288a15e20d9deab';NAME='actual_reflection_intertwining';PARENT=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualRootCommutation.lean'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 p=Path(p);b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),raw_bytes=len(b),raw_sha256=sha(b),lf_bytes=len(l),lf_sha256=sha(l))
def save(n,v):
 p=O/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((json.dumps(v,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode())
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def get(n):return read(O/n)
def raw(path):
 q=next(x for x in get('inputs.manifest.json')['inputs'] if x['original']['path']==Path(path).as_posix());return Path(q['RAW_snapshot']['path']).read_bytes()
def stable():
 for q in get('inputs.manifest.json')['inputs']:
  assert pin(q['original']['path'])==q['original'],('current frozen header input changed',q['original']['path'])
  assert pin(q['RAW_snapshot']['path'])==q['RAW_snapshot'] and pin(q['LF_snapshot']['path'])==q['LF_snapshot']
 assert sha(subprocess.check_output(['git','show',BASE+':'+PARENT.relative_to(ROOT).as_posix()],cwd=ROOT))==pin(PARENT)['raw_sha256']
def freeze():
 assert not (O/'lease.final.json').exists();draft=read(P/'header-draft69.json');assert draft['checked_parent']==BASE and not draft['proof_search'] and not draft['SAU_claim']
 paths=[P/'header-draft69.json',P/'header0-expanded.lean',P/'header0-public.lean',P/'statement0.definition.lean',P/'root.primary69.adoption.json',P/'independent-primary69/source-expectations.json',P/'independent-primary69/source-proof-graph.json',P/'independent-primary69/lease.final.json',PARENT,P/'existing-parent67-statement.exactraw.fragment.lean',P/'existing-parent67-statement.fragment-map.json',ROOT/'lean-toolchain',ROOT/'lake-manifest.json',ROOT/'tools/astis.py']
 rows=[]
 for i,path in enumerate(paths):
  b=path.read_bytes();rp=O/f'inputs/{i:03}.RAW.snapshot';lp=O/f'inputs/{i:03}.LF.snapshot';rp.parent.mkdir(exist_ok=True);rp.write_bytes(b);lp.write_bytes(b.replace(b'\r\n',b'\n'));rows.append(dict(original=pin(path),RAW_snapshot=pin(rp),LF_snapshot=pin(lp)))
 save('lease.open.json',dict(status='OPEN_HEADER_ONLY_REVIEW',actor=ACTOR,actual_PID=os.getpid(),utc=now(),owned_scope=O.as_posix(),no_proof_search=True,no_SAU_claim=True,canonical_Git_ledger_writes=False))
 save('inputs.manifest.json',dict(input_count=len(rows),inputs=rows,actual_PID=os.getpid(),utc=now(),checked_parent=BASE,observed_HEAD=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),finite_historical_maps=[],before_fresh_type_compiler=True))
 stable();print(json.dumps(dict(status='PINNED',actual_PID=os.getpid(),input_count=len(rows))))
def generate():
 stable();expanded=raw(P/'header0-expanded.lean').decode();public=raw(P/'header0-public.lean').decode();definition=raw(P/'statement0.definition.lean').decode()
 expandeddef=expanded.replace('theorem '+NAME,'def expanded_header_expression69',1).replace(' :\n    let μ',' : Prop :=\n    let μ',1)
 publicdef=public.replace('theorem '+NAME,'def public_header_expression69',1).replace(' : '+NAME+'_statement',' : Prop := '+NAME+'_statement',1)
 prefix='import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualRootCommutation\nopen MeasureTheory ProbabilityTheory InnerProductSpace\nopen scoped RealInnerProductSpace ContDiff NNReal Topology ENNReal\nnamespace HeaderOnly69\nnoncomputable section\nset_option autoImplicit false\nset_option maxHeartbeats 2000000\n\n'
 checks='\n#check '+NAME+'_statement\n#check expanded_header_expression69\n#check public_header_expression69\n#check ContinuousLinearMap.comp\n#check ContinuousLinearMap.adjoint\n#check Submodule.subtypeL\n#check LinearIsometry.toContinuousLinearMap\n#check AutoSamplingTheory.ExampleCases.ProximalBPS.ActualRootCommutation.actual_same_root_inverse_commutation\nend\nend HeaderOnly69\n'
 text=prefix+definition+'\n'+expandeddef+'\n'+publicdef+'\n'+checks
 sys.path.insert(0,str(ROOT/'tools'));import astis
 stripped=astis.strip_lean_comments_and_strings(text);assert not re.search(r'(?m)^\s*(theorem|lemma|axiom|opaque|constant)\b',stripped) and not astis.FORBIDDEN_REGEX.search(stripped)
 (O/'HeaderOnlyCheck69.lean').write_bytes(text.encode());save('generated-type-check.map.json',dict(actual_PID=os.getpid(),generated=pin(O/'HeaderOnlyCheck69.lean'),transformations=['Exact private full Prop retained','Expanded header theorem keyword replaced by a named Prop-valued def and outer result colon replaced by : Prop :=','Public caller theorem header replaced by a Prop-valued def whose body is the exact private statement application'],target_proof_assumed=False,target_proof_credit=False,theorem_declarations=0,axiom_declarations=0,sorry_admit=0))
 print(json.dumps(dict(status='GENERATED_LEGAL_PROP_EXPRESSIONS',actual_PID=os.getpid())))
def compile_header():
 stable();cmd=['lake','env','lean',(O/'HeaderOnlyCheck69.lean').relative_to(ROOT).as_posix()]
 with (O/'compiler.stdout.log').open('wb') as out,(O/'compiler.stderr.log').open('wb') as err:
  start=now();p=subprocess.Popen(cmd,cwd=ROOT,stdout=out,stderr=err);print(json.dumps(dict(event='FRESH_TYPE_COMPILER_START',actual_foreground_lake_PID=p.pid)),flush=True);code=p.wait()
 save('compiler.receipt.json',dict(actual_parent_PID=os.getpid(),actual_foreground_lake_PID=p.pid,command=cmd,started_utc=start,finished_utc=now(),exit_code=code,terminal_closed=True,fresh_Lean=True,olean_output_requested=False,header_type_check_only=True,stdout=pin(O/'compiler.stdout.log'),stderr=pin(O/'compiler.stderr.log')))
 t=(O/'compiler.stdout.log').read_text(encoding='utf-8')+(O/'compiler.stderr.log').read_text(encoding='utf-8');assert code==0 and not re.search(r': error:|error\(|sorryAx',t)
 for name in ['expanded_header_expression69','public_header_expression69','ContinuousLinearMap.comp','ContinuousLinearMap.adjoint','Submodule.subtypeL','LinearIsometry.toContinuousLinearMap']:assert name in t
 stable();save('compiler.result.json',dict(status='PASS_TYPE_ELABORATION_ONLY',actual_PID=os.getpid(),receipt=get('compiler.receipt.json'),diagnostic_warnings=[q for q in t.splitlines() if ': warning:' in q],no_theorem_proof_credit=True));print(json.dumps(dict(status='PASS_TYPE_ELABORATION_ONLY',actual_PID=os.getpid(),actual_foreground_lake_PID=p.pid)))
def review():
 stable();assert get('compiler.result.json')['status']=='PASS_TYPE_ELABORATION_ONLY'
 expanded=raw(P/'header0-expanded.lean').decode();public=raw(P/'header0-public.lean').decode();definition=raw(P/'statement0.definition.lean').decode()
 caller,body=expanded.split('theorem '+NAME,1)[1].split(' :\n',1);dc,db=definition.split('private def '+NAME+'_statement',1)[1].split(' : Prop :=\n',1);pc=public.split('theorem '+NAME,1)[1].split(' : '+NAME+'_statement',1)[0]
 assert caller==dc==pc and body==db
 fm=json.loads(raw(P/'existing-parent67-statement.fragment-map.json'));fragment=raw(P/'existing-parent67-statement.exactraw.fragment.lean');parentraw=raw(PARENT);start,end=fm['RAW_range_end_exclusive'];assert parentraw[start:end]==fragment and sha(fragment)==fm['fragment_RAW_sha256'] and sha(parentraw)==fm['parent_RAW_sha256']
 parentdef=fragment.decode();oldcaller,oldbody=parentdef.split('private def actual_same_root_inverse_commutation_statement',1)[1].split(' : Prop :=\n',1)
 assert caller==oldcaller
 addition='                          let D : Hperp →L[ℝ] Hperp :=\n                            R ∘L U.toContinuousLinearMap ∘L Hperp.subtypeL\n                          (∀ h : Hperp, (D h : Lp ℝ 2 J)=\n                            U (h : Lp ℝ 2 J)-P (U (h : Lp ℝ 2 J))) ∧\n                          V0.adjoint ∘L D = -(A0 ∘L V0.adjoint) ∧\n'
 assert body.count(addition)==1 and body.replace(addition,'',1).rstrip('\n')==oldbody.rstrip('\n')
 draft=json.loads(raw(P/'header-draft69.json'));adopt=json.loads(raw(P/'root.primary69.adoption.json'));expect=json.loads(raw(P/'independent-primary69/source-expectations.json'));graph=json.loads(raw(P/'independent-primary69/source-proof-graph.json'))
 assert sha(raw(P/'independent-primary69/source-expectations.json'))==adopt['source_expectations_sha256'] and sha(raw(P/'independent-primary69/source-proof-graph.json'))==adopt['source_graph_sha256']==draft['source_graph_SHA256']
 assert pin(P/'independent-primary69/lease.final.json')['raw_sha256']==adopt['native_lease']['RAW_sha256']
 p11=next(q for q in graph['nodes'] if q['id']=='P11');assert p11==expect['target']['intertwining']
 assert not any(s in caller for s in ['Nontrivial','Inv','IsSelfAdjoint','IsPositive','Commute','IsProbabilityMeasure','CFC','omega','ρ','γ'])
 v=dict(status='HEADER69_ACCEPTED_TYPECHECKED_NO_TARGET_PROOF',actor=ACTOR,actual_review_PID=os.getpid(),utc=now(),checked_parent=BASE,header_RAW=pin(P/'header0-expanded.lean'),public_header_RAW=pin(P/'header0-public.lean'),private_definition_RAW=pin(P/'statement0.definition.lean'),exact_private_full_Prop_expansion=True,public_original_caller_exact=True,unchanged_parent=dict(full_RAW=pin(PARENT),body_free_fragment=pin(P/'existing-parent67-statement.exactraw.fragment.lean'),fragment_map=pin(P/'existing-parent67-statement.fragment-map.json'),original_definition_and_all_old_conclusions_exact_after_only_new_D_fragment_removed=True,terminal_newline_map=dict(candidate_old_tail_LF=len(body.replace(addition,''))-len(body.replace(addition,'').rstrip('\n')),parent_tail_LF=len(oldbody)-len(oldbody.rstrip('\n')))),exact_new_fragment=addition,
  mathematical_statement_audit=[
   'Original caller remains finite real Hilbert/Borel E, C² potential,0<α≤β, both global Hessian bounds,η>0 and βη≤1. Probability,onto pullback,root/order/inverse/polar facts remain conclusions; no new public operator/regularity premise appears.',
   'D is a let-defined bounded operator Hperp→Hperp equal to R∘U∘Hperp.subtypeL, using the SAME R and reflection U selected with the SAME parent witnesses. It is not a free operator or a supplied relation.',
   'Its concluded all-h semantics is inclusion(D h)=U(inclusion h)−P(U(inclusion h)), exactly the micro-to-micro compression of the actual reflection. This equality concerns L² classes, not selected pointwise representatives.',
   'V0:HP0→Hperp, so V0.adjoint:Hperp→HP0; both V0.adjoint∘D and A0∘V0.adjoint are bounded maps Hperp→HP0. Their negated equality is exactly for ALL h:kerP; the statement imposes no range(V0) restriction and no onto/coisometry claim.',
   'HP0 is exactly the inherited macroscopic mean-zero closed subspace; the SAME centered inverse acts only there. Hperp is exactly ker conditional P, not just global mean-zero. No inverse of the full root across constants is requested.',
   'The preceding existential witnesses and all global-centered observable conclusions are preserved literally after deleting only the added D block. No sharp-energy68 dependency is inserted; actual67 is the sole actual production parent.',
   'Rank-zero E and αη=1 remain legal. There is no Nontrivial,strict cap,γ<1,ρ,ω,small universal step,H1 or extra smooth observable binder. Both sides have meaningful zero-space interpretations; no endpoint denominator is introduced.',
   'This is the independently source-backed P11 operator-intertwining statement. Actual projected rotation and B21 corrector-change for g=U(P−Pperp)f, plus B4 error/dynamics consumers, remain later obligations; no right-hand-side-defined fake rotation is substituted.'],
  independently_frozen_source_slice=dict(primary_adoption=pin(P/'root.primary69.adoption.json'),source_expectations=pin(P/'independent-primary69/source-expectations.json'),SPG=pin(P/'independent-primary69/source-proof-graph.json'),P11=p11,parents=[q for q in graph['nodes'] if q['id'] in ['P7','P9','P10']],source_graph_not_Lean_graph=True,primary_source_items_reported_by_source_only_adoption=419,source_inventory_not_reaudited_as_candidate_proof=True),
  type_elaboration=get('compiler.result.json'),generated_type_check=get('generated-type-check.map.json'),typed_header_blockers=[],mathematical_statement_repairs_required=[],private_mathematical_providers=0,finite_historical_maps=[],
  remaining_boundary=['Unsealed statement draft only','No target theorem implementation or proof search','No SAU claim or VERIFIED','No B21 actual rotation/corrector change','No B4/dynamics/main/errors/cost/composition','No full source/publication/reader admission,Exposition Seal,PURIFIED,whole-paper or Goal credit'],canonical_Lean_Git_ledger_writes=False,target_theorem_proved=False,SAU_claim=False,VERIFIED=False,PURIFIED=False)
 save('header-review.json',v);print(json.dumps(dict(status=v['status'],actual_PID=os.getpid(),blockers=0,proof_credit=False)))
if __name__=='__main__':
 try:{'freeze':freeze,'generate':generate,'compile':compile_header,'review':review}[sys.argv[1]]()
 except Exception as e:
  if not (O/'lease.final.json').exists():save((sys.argv[2] if len(sys.argv)>2 else sys.argv[1])+'.failure.json',dict(actual_PID=os.getpid(),utc=now(),error=repr(e),traceback=traceback.format_exc()))
  raise
