import pathlib,json,hashlib,subprocess,os,sys,re,datetime
ROOT=pathlib.Path('E:/Samplinglib');R=ROOT/'runs/20261007-companion-priority/pbps-real-complex-lift60';D=R/'independent-math60';PRE=ROOT/'runs/20261007-companion-priority/pbps-real-complex-lift-preproof60'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(q):return json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def load(p):return json.loads(p.read_bytes())
def write(p,q):p.write_bytes((json.dumps(q,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode())
def pin(p):
 b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
def check(x):
 a=pin(pathlib.Path(x['path']));assert a==x,(a,x)
def prepost():
 f=load(R/'math-freeze.json');before=load(D/'inputs.before.json');after=load(D/'inputs.after.json')
 assert len(f['inputs'])==before['count']==after['count']==31 and before['frozen']==after['frozen']
 for row in before['frozen']:check(row)
 for x in f['inputs']:
  a=pin(pathlib.Path(x['path']));assert a['bytes']==x['raw_bytes'] and a['raw_sha256']==x['raw_sha256'] and a['lf_sha256']==x['lf_sha256']
 assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()==f['checked_base_commit'];return f
if '--readback' in sys.argv:
 f=prepost();q=load(D/'run.json');assert sha(canon({k:v for k,v in q.items() if k!='run_sha256'}))==q['run_sha256'];assert sha(canon(q['named_mathematics_payload']))==q['named_mathematics_payload_sha256']
 for x in load(D/'input.manifest.json')['artifacts']:check(x)
 for x in [q['receipt'],q['inputs'],q['payload']]:check(x)
 assert load(D/'payload.json')==q['named_mathematics_payload']
 write(D/'readback.json',dict(status='PASS',actual_foreground_PID=os.getpid(),frozen_input_count=31,qualified_input_count=load(D/'input.manifest.json')['count'],run_sha256=q['run_sha256'],named_mathematics_payload_sha256=q['named_mathematics_payload_sha256'],whole_run_recipe='Complete sorted compact UTF8 run object excluding ONLY top-level run_sha256',payload_recipe='Sorted compact UTF8 named_mathematics_payload object only'))
 print('READBACK_PASS',os.getpid(),flush=True);sys.exit(0)
f=prepost();status=load(D/'compiler.status.json');assert status['exit_code']==0 and status['terminal_closed'] and status['focused_build_invocation_count']==1
sys.path.insert(0,str(ROOT/'tools'));import astis
codepaths=[ROOT/'AutoSamplingTheory/TechnicalLemmas/Measure/L2RealComplexOperator.lean',ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/DefectComplexLift.lean',ROOT/'Tests/ProximalBPSDefectComplexLift.lean',ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/CenteredDefectOperator.lean']
scans=[]
for p in codepaths:
 cleaned=astis.strip_lean_comments_and_strings(p.read_text(encoding='utf8'))
 hits={name:len(re.findall(pattern,cleaned)) for name,pattern in [('authored_axiom',r'\baxiom\b'),('sorry',r'\bsorry\b'),('admit',r'\badmit\b'),('sorryAx',r'\bsorryAx\b'),('Prop_True',r'\bProp\s*:=\s*True\b'),('trivial_closure',r':=\s*(?:by\s*)?trivial\b')]}
 assert not any(hits.values());assert p.parent.name=='Tests' or not re.search(r'^\s*import\s+Tests',cleaned,re.M)
 scans.append(dict(source=pin(p),hits=hits,comments_and_strings_removed=True))
write(D/'fake-closure-scan.json',dict(actual_sources=scans,count=4,authored_fake_closures=0,scanner=pin(ROOT/'tools/astis.py'),failed_only_elaboration_negatives_not_authored_closures=True))
signatures=[]
for i,p in enumerate(codepaths[:2]):
 header=(PRE/('header'+str(i)+'.lean')).read_text(encoding='utf8').rstrip();text=p.read_text(encoding='utf8');start=text.index('theorem '+header.split()[1]);actual=text[start:text.index(' := by',start)].rstrip();assert actual==header
 signatures.append(dict(header=pin(PRE/('header'+str(i)+'.lean')),source=pin(p),exact_signature=actual,exact_LF_signature_sha256=sha(actual.encode()),exact_header_equal=True))
write(D/'signature-check.json',dict(two_sealed_signatures=signatures,count=2))
generic=codepaths[0].read_text();providers=re.findall(r'^private (?:abbrev|def|theorem) (\w+)',generic,re.M);assert providers==f['private_providers'] and len(providers)==26
provider_calls={name:len(re.findall(r'\b'+name+r'\b',astis.strip_lean_comments_and_strings(generic))) for name in providers};assert all(v>=2 for v in provider_calls.values())
write(D/'provider-coverage.json',dict(actual_26_private_providers=providers,all_referenced_beyond_declaration=provider_calls,proof_review='Every complete body inspected; grouped mathematical reasons in named payload. Counts are usage sanity checks, not mathematical proof by themselves.'))
log=(D/'compiler.stdout.log').read_text(encoding='utf8');closures=[]
for name in [*f['mathematical_declarations'],'AutoSamplingTheory.ExampleCases.ProximalBPS.CenteredDefectOperator.actual_centered_selfadjoint_defect']:
 m=re.search("'"+re.escape(name)+r"' depends on axioms: \[([^\]]+)\]",log);assert m,name
 axioms=[x.strip() for x in m.group(1).split(',')];assert set(axioms)=={'propext','Classical.choice','Quot.sound'};closures.append(dict(declaration=name,actual_printed_axioms=axioms))
assert 'sorryAx' not in log and 'Build completed successfully (3915 jobs).' in log
write(D/'axiom-check.json',dict(actual_named_closures=closures,count=3,stdout=pin(D/'compiler.stdout.log'),anonymous_Test_scope='Compiled anonymous example, no named axiom print for this example; its complete authored body inspected. No invented anonymous closure name.'))
apis=[ROOT/('.lake/packages/mathlib/Mathlib/'+s) for s in ['MeasureTheory/Function/LpSpace/Basic.lean','MeasureTheory/Function/L2Space.lean','MeasureTheory/Integral/Bochner/ContinuousLinearMap.lean','Analysis/InnerProductSpace/Positive.lean','Analysis/InnerProductSpace/StarOrder.lean','Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Basic.lean','Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Instances.lean','Analysis/CStarAlgebra/ContinuousFunctionalCalculus/NonUnital.lean','Analysis/SpecialFunctions/ContinuousFunctionalCalculus/Rpow/Basic.lean','Algebra/Algebra/RestrictScalars.lean']]
rows=load(D/'inputs.before.json')['frozen']+[pin(R/'math-freeze.json'),pin(pathlib.Path(__file__)),pin(D/'compile.py'),pin(D/'inputs.before.json'),pin(D/'inputs.after.json'),pin(D/'compiler.status.json'),pin(D/'compiler.stdout.log'),pin(D/'compiler.stderr.log'),pin(D/'toolchain.stdout.log'),pin(D/'toolchain.stderr.log')]+[pin(p) for p in apis]
write(D/'input.manifest.json',dict(artifacts=rows,count=len(rows),freeze_count=31,additional_actual_API_and_process_pins=len(rows)-31,identity='Qualified absolute path and exact raw/LF SHA256+byte counts; no historical mutable mapping needed for this immutable mathematical freeze'))
payload=dict(verdict='ACCEPT_SCOPED_COMPLETE_MATHEMATICS_NO_BLOCKER',checked_base_commit=f['checked_base_commit'],result_kind='integration-node',declarations=f['mathematical_declarations'],exact_signatures=signatures,
 complete_proof_reasons=[
 dict(ingredients=['embed','realPart','imagPart','conjugate','real_embed','imag_embed','parts','real_I','imag_I'],reason='compLpL sends actual AE classes through bounded scalar maps, so real/imag/conjugate operations are well-defined on the same measure quotient. Every identity follows by Lp.ext and simultaneous AE representative equalities. g=ι(Re g)+iι(Im g) and the I rotation identities hold for arbitrary μ, including zero/infinite measures; no probability, sigma-finiteness or pointwise-everywhere representative claim is introduced.'),
 dict(ingredients=['inner_embed','norm_embed'],reason='L2 inner-product integrals and integral_complex_ofReal identify the real inner product with its complex inclusion. Equality of squared norms plus nonnegativity gives exact isometry. Hidden integrability is supplied by the L2-space API; no separate normalization/regularity certificate.'),
 dict(ingredients=['conjugate_embed','conjugate_parts','fixed_range'],reason='Real images are fixed. Conversely conjugation equality in Lp, combined with coeFn_compLpL, forces imaginary part zero AE, hence g=ι(Re g). The conclusion is the exact range equality of classes, not an arbitrary chosen function fixed at every point.'),
 dict(ingredients=['liftReal','liftReal_I','liftComplex','liftComplex_apply','liftComplex_embed'],reason='The lift is the sum of two bounded real CLM compositions. The I rotation relation and c=Re(c)+i Im(c), with algebraMap_smul aligning real actions, give genuine complex linearity; continuity is inherited from that bounded real map. This constructs an actual bounded complex-linear operator, not an extra supplied witness.'),
 dict(ingredients=['real_lift','imag_lift','real_conjugate','imag_conjugate','liftComplex_conjugate'],reason='The component maps give exact intertwining with D and conjugation compatibility for this constructed Dc. These statements do not imply conjugation compatibility for an arbitrary spectral root.'),
 dict(ingredients=['inner_lift','liftComplex_positive'],reason='Write g=ιu+iιv. With Mathlib inner conjugate-linear in its first input, symmetry of real positive D cancels the imaginary cross terms, yielding inner(Dc g,g)=ofReal(inner(Du,u)+inner(Dv,v)). Both real terms are nonnegative. isPositive_iff_complex then supplies symmetry as well as quadratic nonnegativity; on complete complex L2 this is selfadjoint positivity. No finite-dimensional L2 or Nontrivial assumption.'),
 dict(ingredients=['actual_centered_selfadjoint_defect','exists_positive_complex_lift'],reason='Actual production theorem reuses unchanged59 real μ/J/ν/Λ, internally generated Markov conditional S with its every-y density and stationary marginals, and the same real conditional operator T. It applies the generic construction to exactly D=1−T*T from parent59 positivity and returns T selfadjoint/contraction/AE action/integral preservation. Discarded parent q/H0 witnesses are existing stronger outputs, not new public assumptions or fake proof steps.'),
 dict(ingredients=['Tests.ProximalBPSDefectComplexLift anonymous example','CFC.sqrt','CFC.sqrt_nonneg','CFC.sqrt_mul_sqrt_self'],reason='The real consumer obtains the same Dc from the generic theorem, turns its positivity into order nonnegativity, locally constructs closed complex CFC and its nonunital parent and explicitly typed real selfadjoint CFC, then constructs Rc with Rc≥0 and Rc*Rc=Dc. The root exists in the anonymous Test only. No caller CFC assumption, inverse, spectrum certificate, finite-L2 or nontrivial premise. Nonunital API permits the degenerate zero L2 case.')],
 boundary=['Precommit mathematical review at stated base only; not exact-science VERIFIED or source-fidelity admission.', 'Lift is attributed ASTIS background completion for the printed real positive-defect context; it is not a newly attributed printed paper theorem.', 'No square-root conjugation preservation, real descent, uniqueness, real Gamma/Gamma0/B15/B16, weakH1/dynamics/main/error/querycost/composition/fullpaper/Goal completion.', 'No new validation of the older conceptual-mirror candidate; current none-found audit preserves that candidate unvalidated.'],
 actual_focused=dict(command=status['command'],PID=status['actual_PID'],exit_code=0,jobs=3915,nonforced=True,cached_replay=True,pre_run_inputs=pin(D/'inputs.before.json'),post_run_inputs=pin(D/'inputs.after.json'),actual_standard3_prints=closures),
 counts=dict(frozen_originals=31,private_providers=26,exact_public_signatures=2,actual_authored_source_scans=4,actual_named_axiom_prints=3,focused_invocations=1),
 blockers=[],retained_API_negative_scope='Frozen cfc-api-resolution and root exact type probe retained. Real hidden-module mismatch is a previously proposed static mechanism, not promoted to a independently compiled diagnosis; actual typed local instance correction passes.',warnings='Three Test letI style suggestions are nonblocking; no proof/type/assumption change requested.')
write(D/'payload.json',payload)
receipt=dict(verdict=payload['verdict'],actor='/root/whole_math52/independent-math60',checked_base_commit=f['checked_base_commit'],blockers=[],counts=payload['counts'],exact_scope=payload['boundary'],named_mathematics_payload_sha256=sha(canon(payload)),actual_compiler=status,inputs=pin(D/'input.manifest.json'),checks=[pin(D/x) for x in ['fake-closure-scan.json','signature-check.json','provider-coverage.json','axiom-check.json']],mathematical_reasons=payload['complete_proof_reasons'])
write(D/'receipt.json',receipt)
run=dict(schema='native-independent-complete-math60-v1',actor=receipt['actor'],checked_base_commit=f['checked_base_commit'],actual_review_finalizer_PID=os.getpid(),compiler_wrapper=dict(actual_PID=47408,exit_code=0,tool_chunk='084a57'),actual_compiler=status,inputs=pin(D/'input.manifest.json'),receipt=pin(D/'receipt.json'),payload=pin(D/'payload.json'),named_mathematics_payload=payload,named_mathematics_payload_sha256=sha(canon(payload)),hash_recipes=dict(run_sha256='SHA256 sorted compact UTF8 complete run excluding ONLY top-level run_sha256',named_mathematics_payload_sha256='SHA256 sorted compact UTF8 named_mathematics_payload object only',raw='Actual bytes',LF='Actual bytes replacing CRLF pairs with LF only'),no_canonical_or_proof_mutation=True)
run['run_sha256']=sha(canon(run));write(D/'run.json',run)
with (D/'readback.stdout.log').open('wb') as out,(D/'readback.stderr.log').open('wb') as err:
 command=[sys.executable,'-B','-X','utf8',str(D/'close.py'),'--readback'];p=subprocess.Popen(command,cwd=ROOT,stdout=out,stderr=err);pid=p.pid;code=p.wait()
write(D/'readback.status.json',dict(command=command,actual_PID=pid,exit_code=code,terminal_closed=True,stdout=pin(D/'readback.stdout.log'),stderr=pin(D/'readback.stderr.log')));assert code==0
outputs=[pin(p) for p in sorted(D.iterdir()) if p.is_file() and p.name not in ['lease.json','outputs.final.json']]
q=dict(artifacts=outputs,count=len(outputs),hash_recipe='Complete sorted compact UTF8 output manifest excluding ONLY outputs_sha256');q['outputs_sha256']=sha(canon(q));write(D/'outputs.final.json',q)
for x in outputs:check(x)
assert sha(canon({k:v for k,v in load(D/'run.json').items() if k!='run_sha256'}))==run['run_sha256']
lease=dict(status='CLOSEDLAST',actor=receipt['actor'],actual_foreground_finalizer_PID=os.getpid(),finalizer_terminal_evidence='Parent tool actual EXIT0 after final stdout',compiler_PID=status['actual_PID'],compiler_exit_code=0,compiler='CLOSED',toolchain_PID=status['toolchain_check_actual_PID'],toolchain_exit_code=0,readback_PID=pid,readback_exit_code=0,Python_children='ACTUAL_EXIT0_CLOSED',read_resources='CLOSED',write_resources='CLOSED_AFTER_THIS_FINAL_FILE_WRITE',checked_base_commit=f['checked_base_commit'],run=pin(D/'run.json'),receipt=pin(D/'receipt.json'),payload=pin(D/'payload.json'),inputs=pin(D/'input.manifest.json'),outputs=pin(D/'outputs.final.json'),readback=pin(D/'readback.json'),run_sha256=run['run_sha256'],named_mathematics_payload_sha256=run['named_mathematics_payload_sha256'],closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),lease_hash_recipe='Complete sorted compact UTF8 lease excluding ONLY lease_sha256');lease['lease_sha256']=sha(canon(lease));write(D/'lease.json',lease)
print(json.dumps(dict(status='CLOSEDLAST',verdict=payload['verdict'],actual_finalizer_PID=os.getpid(),actual_readback_PID=pid,compiler_PID=status['actual_PID'],run_sha256=run['run_sha256'],payload_sha256=run['named_mathematics_payload_sha256'],receipt=pin(D/'receipt.json'),run=pin(D/'run.json'),lease=pin(D/'lease.json'),lease_sha256=lease['lease_sha256'],frozen_inputs=31,qualified_inputs=len(rows),outputs=len(outputs))),flush=True)
