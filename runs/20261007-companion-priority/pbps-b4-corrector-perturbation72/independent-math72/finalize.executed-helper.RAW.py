from pathlib import Path
import ast,builtins,difflib,hashlib,json,os,re,subprocess,sys
from datetime import datetime,timezone

ROOT=Path('E:/Samplinglib');R=ROOT/'runs/20261007-companion-priority/pbps-b4-corrector-perturbation72';O=R/'independent-math72'
PY='C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
ACTOR='/root/exact_science63'
FILES=['AutoSamplingTheory/TechnicalLemmas/Analysis/HilbertCorrectorPerturbation.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCorrectorPerturbation.lean']
DECLS=['AutoSamplingTheory.TechnicalLemmas.Analysis.HilbertCorrectorPerturbation.quadratic_corrector_perturbation','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualCorrectorPerturbation.actual_corrector_perturbation']
EXPECTED=['d61e3b78418f95f8c9ff74983050f9f9d2805dcce58f78633afe671827edda43','6e2b75712d441241c773e01b1f42993de527694144463fb10d9579181f291d09']
PARENT='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCorrectorChange.lean'
PRE=ROOT/'runs/20261007-companion-priority/pbps-b4-perturbation-preproof72'
def now():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def can(d):return json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def load(p):return json.loads(Path(p).read_bytes())
def abs(p):
 p=Path(str(p).replace('\\','/'));return p if p.is_absolute() else ROOT/p
def pin(p):
 p=abs(p);b=p.read_bytes();lf=b.replace(b'\r\n',b'\n')
 return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_bytes=len(lf),LF_sha256=sha(lf))
def save(n,d):
 assert not (O/'lease.final.json').exists(),'CLOSED_LAST'
 p=O/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(d if isinstance(d,bytes) else json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2).encode()+b'\n');return pin(p)
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def terminal(label,cmd):
 assert not (O/f'{label}.receipt.json').exists()
 start=now();out=O/f'{label}.stdout.log';err=O/f'{label}.stderr.log'
 with out.open('wb') as fo,err.open('wb') as fe:
  p=subprocess.Popen(cmd,cwd=ROOT,stdout=fo,stderr=fe)
  print(json.dumps(dict(started=label,actual_foreground_PID=p.pid,command=cmd)),flush=True);ec=p.wait()
 d=dict(label=label,actual_foreground_PID=p.pid,actual_parent_PID=os.getpid(),command=cmd,started_utc=start,finished_utc=now(),exit_code=ec,terminal_closed=True,stdout=pin(out),stderr=pin(err))
 save(label+'.receipt.json',d);print(json.dumps(dict(finished=label,PID=p.pid,exit_code=ec)),flush=True);return d
def freeze():
 save('lease.open.json',dict(status='OPEN',actor=ACTOR,scope=O.as_posix(),utc=now(),allowed_writes='own scope only; no canonical/Git/ledger/Goal/VERIFIED',source_decoder_header_verdicts_not_consumed=True))
 f=load(R/'mathematics-freeze72.json');rows=[]
 for i,e in enumerate(f['inputs']):
  p=abs(e['path']);z=pin(p)
  assert z['RAW_sha256']==e['RAW_sha256'] and z['RAW_bytes']==e['RAW_bytes'] and z['LF_sha256']==e['LF_sha256']
  opaque=p.name in ['root.header-math72.adoption.json','root.header-source72.adoption.json']
  raw=save(f'inputs/{i:02d}.exactraw.snapshot',p.read_bytes());lf=save(f'inputs/{i:02d}.LF.snapshot',p.read_bytes().replace(b'\r\n',b'\n'))
  rows.append(dict(original=z,RAW_snapshot=raw,LF_snapshot=lf,exposure='opaque RAW integrity only; not decoded, parsed or used as verdict' if opaque else 'exact mathematical/type/compiler input'))
 for p in [R/'mathematics-freeze72.json',PRE/'header72.actual.named-literal.proposed.lean',PRE/'header72.generic.proposed.lean',ROOT/'tools/astis.py',ROOT/'runs/20261007-companion-priority/pbps-actual-corrector-change71/verified.json']:
  i=len(rows);rows.append(dict(original=pin(p),RAW_snapshot=save(f'inputs/{i:02d}.exactraw.snapshot',p.read_bytes()),LF_snapshot=save(f'inputs/{i:02d}.LF.snapshot',p.read_bytes().replace(b'\r\n',b'\n')),exposure='bounded exact input'))
 for p,e in zip(FILES,EXPECTED):assert pin(p)['RAW_sha256']==e
 save('inputs.manifest.json',dict(status='FROZEN',actual_PID=os.getpid(),root_frozen_input_count=10,input_count=len(rows),inputs=rows,RAW_LF_recipe='replace ONLY byte CRLF with LF; preserve bare CR and every other byte',header_math_source_adopters_opaque_hash_only=True,no72_decoder_or_source_verdict_read=True,no_historical_directory_copy=True))
 save('git.baseline.json',dict(HEAD=git('rev-parse','HEAD').decode().strip(),parent71_exact_science='4e7ce5d2996ffe1d1b0ab570778e02425c6be34e',parent71_science_Git_RAW_sha256=sha(git('show','4e7ce5d2996ffe1d1b0ab570778e02425c6be34e:'+PARENT)),new72_not_exact_science_commit_review=True,tracked_working_changes=git('diff','--name-only','HEAD').decode().splitlines()))
 print(json.dumps(dict(status='FROZEN',inputs=len(rows),modules=2)),flush=True)
def check_current():
 for row in load(O/'inputs.manifest.json')['inputs']:
  assert pin(row['original']['path'])==row['original']
def compiler():
 check_current();pre=[pin(p) for p in [*FILES,PARENT,'lean-toolchain','lake-manifest.json']]
 receipts=[];results=[]
 for i,(file,decl) in enumerate(zip(FILES,DECLS)):
  receipt=terminal(f'fresh-lean{i}', ['lake','env','lean',file]);receipts.append(receipt)
  text=(O/f'fresh-lean{i}.stdout.log').read_text(encoding='utf-8-sig')+(O/f'fresh-lean{i}.stderr.log').read_text(encoding='utf-8-sig')
  rows=re.findall(r"'"+re.escape(decl)+r"' depends on axioms:\s*\[([^\]]*)\]",text)
  assert receipt['exit_code']==0,(file,'compile failed')
  assert len(rows)==1 and set(x.strip() for x in rows[0].split(','))=={'propext','Classical.choice','Quot.sound'}
  assert 'error:' not in text
  results.append(dict(file=file,declaration=decl,actual_foreground_PID=receipt['actual_foreground_PID'],exit_code=0,standard_axioms=[x.strip() for x in rows[0].split(',')],axiom_output_instances=1,fresh_source_elaboration=True,Lake_cache_replay=False,output_olean_requested=False,warnings_present='warning:' in text,receipt=pin(O/f'fresh-lean{i}.receipt.json')))
 post=[pin(p) for p in [*FILES,PARENT,'lean-toolchain','lake-manifest.json']];assert pre==post;check_current()
 manifest=load(ROOT/'lake-manifest.json');ml=next(x for x in manifest['packages'] if x['name']=='mathlib')
 actual=git('-C',str(ROOT/'.lake/packages/mathlib'),'rev-parse','HEAD').decode().strip();assert actual==ml['rev']
 assert (ROOT/'lean-toolchain').read_bytes().replace(b'\r\n',b'\n')==b'leanprover/lean4:v4.33.0\n'
 save('compiler.result.json',dict(status='PASS',results=results,pre_pins=pre,post_pins=post,pins_unchanged=True,Lean='4.33.0',Mathlib_revision=actual,dependencies_reused=True,new_source_elaborated_without_requested_olean=True,full_root_site_not_run=True))
 print(json.dumps(dict(status='FRESH_BOTH_PASS',actual_PIDs=[x['actual_foreground_PID'] for x in receipts],standard3=True)),flush=True)
def literal_expression(text,name):
 a=text.index('private def '+name);b=text.index(': Prop :=\n',a)+len(': Prop :=\n');end=text.index('\n\ntheorem ',b)
 return text[b:end]
def audit():
 check_current();texts=[(ROOT/p).read_text(encoding='utf-8') for p in FILES];parent=(ROOT/PARENT).read_text(encoding='utf-8')
 gen,actual=texts;seal=load(PRE/'root.statement-seal72.json')
 for e in seal['exact_headers']:
  assert pin(e['path'])['RAW_sha256']==e['RAW_sha256']
 actual_header=(PRE/'header72.actual.named-literal.proposed.lean').read_text(encoding='utf-8')
 assert actual.startswith(actual_header)
 generic_header=(PRE/'header72.generic.proposed.lean').read_text(encoding='utf-8')
 # The sealed generic header omits only the separately admitted tactic import.
 gi=gen.index('theorem quadratic_corrector_perturbation');gh=generic_header.index('theorem quadratic_corrector_perturbation')
 assert gen[gi:].startswith(generic_header[gh:])
 expr=literal_expression(actual,'actual_corrector_perturbation_statement')
 old=literal_expression(parent,'actual_corrector_change_statement')
 delta=' ∧\n                                (∀ u v r : HP0,\n                                  C (u+ΓP0 r) (v-A0 r)-C u v=\n                                    inner ℝ u (Inv r)+‖r‖^2/2)'
 assert delta in expr and expr.replace(delta,'',1)==old
 expanded=(R/'expanded72.actual.frozen.header.lean').read_text(encoding='utf-8')
 # Expansion is the exact original six callers followed by the complete literal body.
 assert expr in expanded
 def binders(t,name):
  a=t.index('theorem '+name);b=t.index(' : actual_',a);return t[a:b].replace(name,'PUBLIC_TARGET',1)
 assert binders(actual,'actual_corrector_perturbation')==binders(parent,'actual_corrector_change')
 witness_names=re.findall(r'obtain ⟨([^,]+), parentSlice',actual)
 assert witness_names==['S','e','U','T','Γ','q','ΓP0','Inv','A0','B0','V0','R']
 assert 'exact AutoSamplingTheory.TechnicalLemmas.Analysis.HilbertCorrectorPerturbation.quadratic_corrector_perturbation\n      A0 ΓP0 Inv hA0self hΓself hInvSelf hCommInv hLeft hRight hSquare0 u v r' in actual
 tree=ast.parse((ROOT/'tools/astis.py').read_text(encoding='utf-8-sig'));nodes=[]
 for n in tree.body:
  if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='FORBIDDEN_REGEX' for t in n.targets):nodes.append(n)
  if isinstance(n,ast.FunctionDef) and n.name=='strip_lean_comments_and_strings':nodes.append(n)
 env={'re':re};exec(builtins.compile(ast.Module(body=nodes,type_ignores=[]),'pinned-fakeclosure-scan','exec'),env)
 scans=[]
 for p,t in zip(FILES,texts):
  s=env['strip_lean_comments_and_strings'](t);hits=[dict(match=m.group(),line=s[:m.start()].count('\n')+1) for m in env['FORBIDDEN_REGEX'].finditer(s)];assert not hits
  scans.append(dict(file=pin(p),line_count=len(t.splitlines()),hits=hits,public_theorems=len(re.findall(r'^theorem ',t,re.M)),private_full_literal_Prop_definitions=len(re.findall(r'^private def ',t,re.M)),imports=re.findall(r'^import (.+)$',t,re.M)))
 assert [x['line_count'] for x in scans]==[54,440] and [x['public_theorems'] for x in scans]==[1,1] and [x['private_full_literal_Prop_definitions'] for x in scans]==[0,1]
 save('statement-and-parent-retention.json',dict(status='PASS',full_private_literal_matches_sealed_expansion=True,exact_original_public_binders_same_as71=True,source_analytic_callers=['hα','hαβ','hV','hH','hη','hβη'],same_common_witnesses=witness_names,strip_only_new_delta_recovers_entire_parent71_literal_exactly=True,removed_delta_utf8=delta,parent71=pin(PARENT),parent71_verified=pin(ROOT/'runs/20261007-companion-priority/pbps-actual-corrector-change71/verified.json'),generic_sealed_seven_hypotheses=['hA','hG','hInv','hAInv','hInvG','hGInv','hSquares'],actual_internally_produced_hypotheses=dict(hA='parent71 hA0self',hG='same GammaP0.IsPositive -> isSelfAdjoint',hInv='parent71 hInvSelf',hAInv='parent71 hCommInv',hInvG='parent71 hLeft',hGInv='parent71 hRight',hSquares='parent71 hSquare0'),generic_actual_call_exact=True,arbitrary_centered_r=True,r_is_not_actual_r_rho=True,no_B27_H_K_B28_inference=True,rank_zero_alphaeta_one_legal=True))
 save('fake-closure-and-import-scan.json',dict(status='PASS',scanner=pin(ROOT/'tools/astis.py'),files=scans,total_hits=0,private_proof_providers=0,public_theorems=2,source_final_verdict_not_read=True))
 negdir=R/'typed-inner-repair';diag=load(negdir/'diagnosis.json');negative=load(R/'focused-generic-first/receipt.json')
 assert negative['exit_code']==1 and negative['actual_foreground_PID']==13416
 before=negdir/'generic-first.exactraw.lean';assert pin(before)['RAW_sha256']==diag['old_RAW_sha256'] and pin(FILES[0])['RAW_sha256']==diag['new_RAW_sha256']
 oldg=before.read_text(encoding='utf-8');oldtype=oldg[oldg.index('theorem quadratic_corrector_perturbation'):oldg.index(' := by')]
 newtype=gen[gen.index('theorem quadratic_corrector_perturbation'):gen.index(' := by')];assert oldtype==newtype
 save('typed-inner-repair.exact.diff',''.join(difflib.unified_diff(oldg.splitlines(keepends=True),gen.splitlines(keepends=True),fromfile='retained-first-negative',tofile='compiled-current')).encode())
 save('retained-negatives.json',dict(first_generic_failure=[pin(R/'focused-generic-first'/n) for n in ['receipt.json','stdout.log','stderr.log']],diagnosis=pin(negdir/'diagnosis.json'),before=pin(before),exact_statement_unchanged=True,typed_ha_hg_hi_repair_only=True,failed_sorryAx_or_no_axioms_print_not_certificate=True,negative_as_proof_credit=False))
 regions=[]
 for index,start,end,role in [(0,1,54,'whole generic module'),(1,1,19,'actual imports/namespace/options'),(1,20,141,'complete literal private Prop'),(1,142,152,'public six callers and literal unfold'),(1,153,313,'same parent71 extraction and Hilbert type adapters'),(1,314,320,'seven internal generic hypotheses and genuine invocation'),(1,321,349,'append arbitrary-r tail while retaining actual global conclusion'),(1,350,375,'retained all-micro and actual-global final conjunction'),(1,376,435,'complete same-witness outer reconstruction'),(1,436,440,'end and axiom inspection')]:
  b=b''.join((ROOT/FILES[index]).read_bytes().splitlines(keepends=True)[start-1:end]);regions.append(dict(file=FILES[index],start_line=start,end_line=end,RAW_bytes=len(b),RAW_sha256=sha(b),role=role))
 save('proof-region-coverage.json',dict(status='WHOLE_494_LINES_READ',regions=regions,local_generic_facts=['ha/hg/hi','Inv G x=x','A²x+G²x=x','norm-square energy','Inv A²x+Gx=Invx','mixed linear term','full norm/inner expansion'],scope='whole implementations read independently; exact full RAW snapshots and these literal line-span hashes are distinct from whole-file digests'))
 print(json.dumps(dict(status='AUDIT_PASS',whole_module_lines=494,sealed=True,same6callers12witnesses=True,fake_closure_hits=0)),flush=True)
def verdict():
 assert load(O/'compiler.result.json')['status']=='PASS';check_current()
 actual=(ROOT/FILES[1]).read_text(encoding='utf-8');expr=literal_expression(actual,'actual_corrector_perturbation_statement')
 expanded=(R/'expanded72.actual.frozen.header.lean').read_text(encoding='utf-8')
 assert expanded.split(' :\n',1)[1].rstrip('\n')==expr
 verified=load(ROOT/'runs/20261007-companion-priority/pbps-actual-corrector-change71/verified.json')
 assert verified['status']=='VERIFIED' and verified['verified_commit']=='4e7ce5d2996ffe1d1b0ab570778e02425c6be34e'
 parentraw=git('show',verified['verified_commit']+':'+PARENT);assert parentraw==(ROOT/PARENT).read_bytes()
 aux=[pin(R/'focused-generic-typed-inner/receipt.json'),pin(R/'focused-actual-first/receipt.json'),pin(R/'focused-generic-first/receipt.json'),pin(R/'typed-inner-repair/diagnosis.json'),pin(R/'typed-inner-repair/generic-first.exactraw.lean')]
 for path,expected in [('focused-generic-typed-inner/receipt.json',9564),('focused-actual-first/receipt.json',37484)]:
  q=load(R/path);assert q['actual_foreground_PID']==expected and q['exit_code']==0
 save('auxiliary.inputs.manifest.json',dict(input_count=len(aux),inputs=aux,scope='exact original positive/negative focused compiler and typed-coercion repair authorities only; no source/decoder verdicts'))
 save('final-parent-and-seal-readback.json',dict(parent_verified_commit=verified['verified_commit'],parent_science_Git_RAW_bytes=len(parentraw),parent_science_Git_RAW_sha256=sha(parentraw),current_parent_exact_Git_RAW=True,whole_literal_equals_entire_expanded_result=True,expanded_header=pin(R/'expanded72.actual.frozen.header.lean'),exact_parent_verified_record=pin(ROOT/'runs/20261007-companion-priority/pbps-actual-corrector-change71/verified.json'),no_exact_SCI72_commit_review=True))
 proof='''Independent mathematics72, whole generic54 and actual440 lines.

Let H be any complete real Hilbert space, including the zero space. Write I=Inv and K=A I. The generic sealed assumptions give A and G selfadjoint, I selfadjoint, I G=G I=id, A I=I A, and A²+G²=id. This is not an assertion that K is invertible. The implementation's actual algebra uses A/G/I symmetry, I G=id and the square identity; the supplied reverse inverse and A/I commutation are redundant in this particular identity. They remain the fixed generic contract, and add no analytic caller premise to the actual theorem.

First test A²r+G²r=r against r. Selfadjointness gives ||Ar||²+||Gr||²=||r||². Applying I to the same vector identity and using I G(Gr)=Gr gives I A²r+Gr=Ir. Therefore <K u,Ar>+<u,Gr>=<Iu,A²r>+<u,Gr>=<u,I A²r+Gr>=<u,Ir>. These are precisely hEnergy, hLinear and hMixed; they do not use source estimates or a supplied corrector certificate.

Define C(u,v)=(||u||²-||v||²)/2-<Ku,v>. For u'=u+Gr and v'=v-Ar, the norm contribution to C(u',v')-C(u,v) is <u,Gr>+<v,Ar>+(||Gr||²-||Ar||²)/2. Since K G r=A r, the cross contribution is <Ku,Ar>-<Ar,v>+||Ar||². The v cross terms cancel by real symmetry. The total is <u,Gr>+<Ku,Ar>+(||Gr||²+||Ar||²)/2=<u,Ir>+||r||²/2. Signs, order of A I and coefficient one-half agree exactly. This is the complete mathematical proof; no finite-dimensionality, nontriviality, norm-gap, positivity premise on G or new inverse/root is used in the generic leaf.

For the actual theorem, reuse SAME actual parent71 witnesses S,e,U,T,Gamma,q,GammaP0,Inv,A0,B0,V0,R before every globally centered input f. The exact centered space HP0 is the kernel of the constant functional on the actual conditional macro space. Its norm, inner product and complete structure are inherited internally; it is not finite-dimensional L2. Parent71 supplies selfadjoint A0, positivity of the SAME GammaP0, selfadjoint Inv, A0/Inv commutation, both inverse products and A0²+GammaP0²=id. Positivity supplies the seventh required interface component, selfadjoint GammaP0, internally. The actual proof explicitly invokes the generic theorem with these exact seven proofs and unchanged operators.

The new universally quantified u,v,r:HP0 identity is appended to each actual-f conclusion. Deleting only that appended identity recovers the entire parent71 literal proposition byte-for-byte. Its placement does not assert a residual r_rho exists or equals any algorithmic error: r is arbitrary. Actual conditional fP/gP and fV/gV, internal mean(g), rotation, energy and prior B21 all remain inherited unchanged. Every original probability/kernel/range/root/inverse/polar/intertwining clause survives the outer reconstruction. Six original analytic callers and twelve witnesses persist; no parent conclusion is promoted to a public caller premise or private provider.

Rank-zero E and alpha eta=1 are admitted by the parent and unchanged binders. In the zero centered space all vectors and operator expressions vanish and the identity is 0=0; the proof divides only by real 2, never a vector norm or additional gap. There is no onto-V0, actual-residual, H/K/B27/B28, full B4, dynamics, H1, main, error/cap/query-cost or composition conclusion. This review is mathematical implementation only; no72 source/header verdict/decoder/publication conclusion is consumed or certified.

The retained first generic compile failed typed/coerced symmetry rw matching. Typed local equalities ha,hg,hi expose identical CLM applications; exact generic statement equality before/after is checked. Failed axiom output is not a proof certificate. Fresh independent source elaboration and standard3 for both exact files are separately required and recorded.
'''
 save('independent-mathematics.utf8.txt',proof.encode())
 d=dict(status='ACCEPTED_LOCAL_TWO_THEOREM_IMPLEMENTATIONS_MATHEMATICS_ONLY',actor=ACTOR,checked_HEAD=load(O/'git.baseline.json')['HEAD'],candidate_files=[pin(p) for p in FILES],declarations=DECLS,whole_lines=494,mathematical_repairs=[],nonblocking_contract_observation='Generic hAInv and hGInv are not needed by this proof; sealed contract retained, actual derives both internally, no new analytic caller premise.',original_analytic_callers=6,common_witnesses=12,parent71_literal_all_clauses_retained=True,fresh_compiler_results=load(O/'compiler.result.json')['results'],fake_closure_hits=0,private_providers=0,rank_zero_alphaeta_one_legal=True,conceptual_mirror_audit=dict(status='none-found',reason='Exact same-Hilbert quadratic corrector expansion; no new cross-domain hypothesis/conclusion transport certified in this bounded delta.'),source_fidelity_review=False,decoder_or72_header_verdict_consumed=False,VERIFIED=False,exact_SCI72_review=False,full_paper=False,Goal_complete=False,remaining_boundary='Arbitrary centered r perturbation identity only; genuine actual r_rho/H/K/B27/B28, full B4/H1/dynamics/main/errors/caps/query costs/composition and reader/PURIFIED/main/live/Goal remain open.')
 save('mathematical-verdict.json',d);print(json.dumps(dict(status=d['status'],whole_lines=494,repairs=0)),flush=True)
def finalize():
 files=['inputs.manifest.json','auxiliary.inputs.manifest.json','git.baseline.json','final-parent-and-seal-readback.json','compiler.result.json','statement-and-parent-retention.json','fake-closure-and-import-scan.json','retained-negatives.json','proof-region-coverage.json','mathematical-verdict.json']
 p={n:load(O/n) for n in files};p['complete_written_independent_mathematics']=(O/'independent-mathematics.utf8.txt').read_text(encoding='utf-8')
 p['own_negative_terminals']=[pin(f) for f in sorted(O.glob('*.receipt.json')) if load(f)['exit_code']!=0]
 named=save('complete-named-mathematical-review.payload.json',p)
 rows=[pin(p) for p in sorted(O.rglob('*')) if p.is_file() and p.name not in ['finalize.stdout.log','finalize.stderr.log','finalize.receipt.json','outputs.manifest.json','run.json','lease.final.json']]
 manifest=save('outputs.manifest.json',dict(entries=rows,entry_count=len(rows),entries_logical_sha256=sha(can(rows)),deferred_final_lease_bindings='active finalizer stdout/stderr/receipt, own run/manifest, readback/close terminal layers, only lease self observed externally'))
 run=dict(actor=ACTOR,status='ACCEPTED_MATHEMATICS_ONLY',checked_HEAD=load(O/'git.baseline.json')['HEAD'],candidate_files=[pin(p) for p in FILES],complete_named_RAW_payload=named,input_manifest=pin(O/'inputs.manifest.json'),output_manifest=manifest,verdict=pin(O/'mathematical-verdict.json'),compiler=pin(O/'compiler.result.json'),whole_logical_recipe='canonical sorted JSON ensure_ascii=False comma/colon; remove ONLY top-level run_sha256',canonical_Git_ledger_Goal_writes=False,VERIFIED=False,source_review=False)
 run['run_sha256']=sha(can(run));save('run.json',run)
 print(json.dumps(dict(status='FINALIZED',whole_logical_run_sha256=run['run_sha256'],complete_named_RAW=named)),flush=True)
def validate(closed=False):
 run=load(O/'run.json');assert sha(can({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']
 for field in ['complete_named_RAW_payload','input_manifest','output_manifest','verdict','compiler']:
  e=run[field];assert pin(e['path'])==e
 for e in load(O/'outputs.manifest.json')['entries']:assert pin(e['path'])==e
 check_current()
 for e in load(O/'auxiliary.inputs.manifest.json')['inputs']:assert pin(e['path'])==e
 if closed:
  l=load(O/'lease.final.json');assert l['status']=='CLOSED_LAST'
  actual={p.as_posix() for p in O.rglob('*') if p.is_file()};expected={e['path'] for e in l['all_owned_outputs_except_only_self']}|{(O/'lease.final.json').as_posix()};assert actual==expected and len(actual)==l['owned_count']
  for e in l['all_owned_outputs_except_only_self']:assert pin(e['path'])==e
  assert sha(can(l['all_owned_outputs_except_only_self']))==l['closure_manifest_logical_sha256']
  assert all(abs(e['path']).stat().st_mtime_ns<=(O/'lease.final.json').stat().st_mtime_ns for e in l['all_owned_outputs_except_only_self'])
 print(json.dumps(dict(status='READ_ONLY_PASS',actual_PID=os.getpid(),owned_writes=0,closed=closed,owned_count=len([p for p in O.rglob('*') if p.is_file()]),whole_logical_run_sha256=run['run_sha256'],named_complete_RAW=run['complete_named_RAW_payload'],lease=pin(O/'lease.final.json') if closed else None)),flush=True)
def close():
 rec=terminal('close-readonly',[PY,'-B','-X','utf8',str(O/'math72.py'),'validate']);assert rec['exit_code']==0
 rows=[pin(p) for p in sorted(O.rglob('*')) if p.is_file()];run=load(O/'run.json')
 save('lease.final.json',dict(status='CLOSED_LAST',actor=ACTOR,actual_last_writer_PID=os.getpid(),actual_close_probe=rec,owned_count=len(rows)+1,all_owned_outputs_except_only_self=rows,closure_manifest_logical_sha256=sha(can(rows)),whole_logical_run_sha256=run['run_sha256'],complete_named_RAW=run['complete_named_RAW_payload'],last_owned_write=True,no_more_owned_writes=True,canonical_Git_ledger_Goal_writes=False,VERIFIED=False,postclose='external read-only terminal validator only'))
 print(json.dumps(dict(status='CLOSED_LAST',actual_close_writer_PID=os.getpid(),owned_count=len(rows)+1,whole_logical_run_sha256=run['run_sha256'],complete_named_RAW=run['complete_named_RAW_payload'],lease=pin(O/'lease.final.json'),closure_manifest_logical_sha256=sha(can(rows)))),flush=True)
if __name__=='__main__':
 os.chdir(ROOT);{'freeze':freeze,'compiler':compiler,'audit':audit,'verdict':verdict,'finalize':finalize,'validate':validate,'postclose':lambda:validate(True),'close':close}[sys.argv[1]]()
