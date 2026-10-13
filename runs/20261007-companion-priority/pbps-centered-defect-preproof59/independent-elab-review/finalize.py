import pathlib,json,hashlib,sys,os,subprocess,re,datetime
ROOT=pathlib.Path('E:/Samplinglib');R=ROOT/'runs/20261007-companion-priority/pbps-centered-defect-preproof59';D=R/'independent-elab-review'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(q):return json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def load(p):return json.loads(pathlib.Path(p).read_bytes())
def write(p,q):pathlib.Path(p).write_bytes((json.dumps(q,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode())
def pin(p):
 p=pathlib.Path(p);b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
def annotated(s):return s.replace('(1-T*T)','((1 : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν)-T*T)').replace('(1-T0*T0)','((1 : H0 →L[ℝ] H0)-T0*T0)')
phase_dirs=[D,D/'phase1',D/'phase2',D/'phase3',D/'phase4'];results=[]
inputs={}
for phase in phase_dirs:
 q=load(phase/'compiler.results.json');assert q['all_compiler_leases']=='CLOSED'
 for row in q['inputs']:assert pin(row['path'])==row;inputs[row['path']]=row
 for row in q['results']:
  assert row['compiler_status']=='CLOSED'
  for k in ['source','stdout','stderr']:assert pin(row[k]['path'])==row[k]
  assert any(p['exe'].lower()=='lean.exe' for p in row['observed_processes'])
  results.append(row);inputs[row['source']['path']]=row['source']
assert len(results)==11 and sum(x['actual_exit_code']==0 for x in results)==5 and sum(x['actual_exit_code']==1 for x in results)==6
final=next(x for x in results if x['name']=='positive-typed-actual-one-API');assert final['actual_exit_code']==0
assert 'sorryAx' not in pathlib.Path(final['stdout']['path']).read_text(encoding='utf8')
eq=next(x for x in results if x['name']=='sealed-successor-definitional-equality');assert eq['actual_exit_code']==0
assert 'sorryAx' not in pathlib.Path(eq['stdout']['path']).read_text(encoding='utf8')
eq_text=pathlib.Path(eq['stdout']['path']).read_text(encoding='utf8')
assert 'signatures0_definitionally_equal' in eq_text and 'signatures1_definitionally_equal' in eq_text
failed_print=next(x for x in results if x['name']=='positive-all-identities-typed')
assert failed_print['actual_exit_code']==1 and 'sorryAx' in pathlib.Path(failed_print['stdout']['path']).read_text(encoding='utf8')
api=ROOT/'.lake/packages/mathlib/Mathlib/Algebra/Star/SelfAdjoint.lean';inputs[api.as_posix()]=pin(api)
api_lines=api.read_text(encoding='utf8').splitlines();assert 'protected theorem one' in api_lines[184]
header_changes=[]
for n in [0,1]:
 old=R/f'header{n}.lean';new=D/f'header{n}.successor-proposed.lean'
 s=old.read_text(encoding='utf8');t=new.read_text(encoding='utf8');assert annotated(s)==t
 changes=[]
 for pattern in ['(1-T*T)','(1-T0*T0)']:
  for m in re.finditer(re.escape(pattern),s):changes.append(dict(start_original_LF_character=m.start(),end_original_LF_character=m.end(),original=pattern,replacement=annotated(pattern)))
 changes.sort(key=lambda x:x['start_original_LF_character'])
 header_changes.append(dict(index=n,original=pin(old),successor=pin(new),annotation_occurrences=len(changes),changes=changes))
 inputs[new.as_posix()]=pin(new)
 assert not re.search(r'\(1-T(?:0)?\*T(?:0)?\)',t)
assert [x['annotation_occurrences'] for x in header_changes]==[7,4]
for result in results:
 source=pathlib.Path(result['source']['path']).read_text(encoding='utf8')
 assert not re.search(r'\b(sorry|admit|axiom)\b',source)
proposal=dict(schema_version=1,created_by='/root/whole_math52',status='PROPOSED_SYNTAX_OVERLAY_REQUIRES_DISTINCT_REVIEW',repair_kind='definitionally-equal elaboration annotation; no mathematical/source-assumption repair',
 headers=header_changes,unchanged='All declaration names, binder order/types, hypotheses, definitions, quantifiers, conclusions and formula operands; only explicit types on eleven operator identity numerals.',
 exact_compiled_equality=eq,scope='Separate reviewer must admit this syntax overlay before root changes sealed code; not a proof/body/source-fidelity admission.')
write(D/'exact-proposal.json',proposal);inputs[(D/'exact-proposal.json').as_posix()]=pin(D/'exact-proposal.json')
payload=dict(payload_name='independent-declaration-elaboration-diagnosis59',verdict='ELABORATION_CLARIFICATION_ISOLATED_NO_MATHEMATICAL_STATEMENT_REPAIR',
 diagnosis='Bare overloaded identity numerals in dependent positivity targets cause actual larger-fragment generalization/kernel-free-variable failures. Removing dsimp or disabling zeta does not fix them. Explicit endomorphism types remove these failures. Qualification of IsPositive alone is insufficient and produces HSub Nat/operator instance failure. This is observed elaboration behavior; no claim about Lean internal root cause is required.',
 actual_operator_types=dict(full='ContinuousLinearMap ℝ ℝ (Lp ℝ 2 ν) (Lp ℝ 2 ν)',centered='ContinuousLinearMap ℝ ℝ H0 H0',H0='Submodule.ker (innerSL ℝ q); induced real Hilbert subtype',full_defect='(1 : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν) - T*T',centered_defect='(1 : H0 →L[ℝ] H0) - T0*T0',positivity='ContinuousLinearMap.IsPositive on that exact real continuous endomorphism; symmetry and nonnegative real quadratic form; no extra completeness or finite-L2 premise'),
 independent_controls=['Minimal dependent-kernel positivity compiles with and without dsimp.','Complete original and explicitly annotated header propositions compile; both complete rfl equality theorems print standard3.','All-identity-typed positive fragment with correct explicit-ring IsSelfAdjoint.one compiles EXIT0 and prints standard3.'],
 exact_one_API=dict(path=api.as_posix(),line=185,declaration='protected theorem IsSelfAdjoint.one (R : Type*) [MulOneClass R] [StarMul R] : IsSelfAdjoint (1 : R)',usage='(IsSelfAdjoint.one (H →L[ℝ] H) : IsSelfAdjoint (1 : H →L[ℝ] H)).sub ...',negative='No global isSelfAdjoint_one identifier; IsSelfAdjoint.one requires explicit ring type R.'),
 proposed_headers=header_changes,proposal=pin(D/'exact-proposal.json'),compiled_equality=eq,compiled_positive_fragment=final,
 retained_negatives=[x for x in results if x['actual_exit_code']==1],failed_only_sorryAx=dict(diagnostic=failed_print['name'],stdout=failed_print['stdout'],exit_code=1,authored_placeholder=False,not_admitted=True),
 original_fragments=dict(mean=pin(ROOT/'.astis/pbps-centered-defect59/mean-fragment.lean'),centered=pin(ROOT/'.astis/pbps-centered-defect59/centered-fragment.lean'),status='Root-reported EXIT0 partials preserved unchanged; no whole theorem credit'),
 scope='Bounded declaration/typeclass/API diagnosis only. No full59 theorem/Test proof, source-fidelity verdict, state transition, production/canonical write, Gamma/root/weakH1/dynamics/main/cost/PURIFIED admission.',
 residuals=['Distinct independent review and root adoption of the proposed complete syntax overlay.','Root must pass actual complete theorem and real consumer later; compiled positive fragment is only a partial control.'])
write(D/'declaration-review.payload.json',payload)
write(D/'operational-reader-negative.json',dict(status='RETAINED_NONMATHEMATICAL_OPERATIONAL_NEGATIVE',tool_chunks=['d5c8ea','c6a0dd'],cause='PowerShell inline Python quoting failed before phase1 preparation; missing generated script invocation failed. Corrected with owned prepare_phase1.py. No original input or proof changed.'))
write(D/'inputs.final.json',dict(inputs=list(inputs.values()),count=len(inputs),implementation_inputs=[pin(x) for x in sorted(D.glob('*.py'))]))
read_code="import json,pathlib,hashlib,sys,os; q=json.loads(pathlib.Path(sys.argv[1]).read_bytes()); [(assertion if False else None) for assertion in []];\nfor r in q['inputs']+q['implementation_inputs']:\n b=pathlib.Path(r['path']).read_bytes();l=b.replace(b'\\r\\n',b'\\n');assert len(b)==r['bytes'] and len(l)==r['lf_bytes'] and hashlib.sha256(b).hexdigest()==r['raw_sha256'] and hashlib.sha256(l).hexdigest()==r['lf_sha256']\nprint(json.dumps(dict(actual_pid=os.getpid(),inputs=len(q['inputs']),implementation_inputs=len(q['implementation_inputs']),all_pins_pass=True)))"
cmd=[sys.executable,'-B','-X','utf8','-c',read_code,str(D/'inputs.final.json')]
p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=p.communicate()
(D/'final-readback.stdout.log').write_bytes(out);(D/'final-readback.stderr.log').write_bytes(err)
write(D/'final-readback.status.json',dict(actual_pid=p.pid,actual_exit_code=p.returncode,command=cmd,stdout=pin(D/'final-readback.stdout.log'),stderr=pin(D/'final-readback.stderr.log')))
assert p.returncode==0,err.decode()
for phase in phase_dirs[1:]:
 q=load(phase/'compiler.results.json');lease=dict(status='CLOSED',compiler_results=pin(phase/'compiler.results.json'),all_actual_compiler_exits=[r['actual_exit_code'] for r in q['results']],all_compiler_processes='TERMINAL',python_runner_pid=q['python_pid'],python_runner_observed_exit_code=0,closed_in_finalization=True)
 write(phase/'lease.json',lease)
payload_hash=sha(canon(payload))
receipt=dict(schema_version=1,actor='/root/whole_math52',status='CLOSED_BOUNDED_ELABORATION_REVIEW59',verdict=payload['verdict'],proposal=pin(D/'exact-proposal.json'),
 counts=dict(inputs=len(inputs),compiler_diagnostics=11,EXIT0=5,EXIT1_retained=6,header_annotation_occurrences=[7,4],readback_pid=p.pid),
 explicit_types=payload['actual_operator_types'],API=payload['exact_one_API'],declaration_review_payload_sha256=payload_hash,
 focused_positive_Lean_PID=next(x['pid'] for x in final['observed_processes'] if x['exe'].lower()=='lean.exe'),focused_positive_exit_code=0,
 equality_Lean_PID=next(x['pid'] for x in eq['observed_processes'] if x['exe'].lower()=='lean.exe'),equality_exit_code=0,axioms='propext, Classical.choice, Quot.sound only for successful positive fragment and complete equality controls',
 original_headers_unchanged=True,authored_placeholder_scan='ZERO',failed_only_sorryAx_preserved=True,residuals=payload['residuals'],scope=payload['scope'])
write(D/'receipt.json',receipt)
run=dict(schema_version=1,actor='/root/whole_math52',status='COMPLETE_BOUNDED_ELABORATION_REVIEW',inputs=load(D/'inputs.final.json'),receipt=pin(D/'receipt.json'),compiler_results=results,
 declaration_review_payload=payload,declaration_review_payload_sha256=payload_hash,final_input_readback=pin(D/'final-readback.status.json'),
 native_recipes=dict(run_sha256='SHA256 sorted compact UTF8 entire run excluding ONLY top-level run_sha256; ensure_ascii=False, allow_nan=False, no newline',declaration_review_payload_sha256='SHA256 same canonical encoding of distinct complete named declaration_review_payload object',raw_lf='Exact bytes; LF replaces CRLF pairs only; exact bytes/length/SHA256 for both'))
run['run_sha256']=sha(canon(run));write(D/'run.json',run)
q=load(D/'run.json');assert sha(canon({k:v for k,v in q.items() if k!='run_sha256'}))==q['run_sha256'] and q['declaration_review_payload']==load(D/'declaration-review.payload.json') and sha(canon(q['declaration_review_payload']))==payload_hash
outputs=[pin(x) for x in sorted(D.rglob('*')) if x.is_file() and x not in [D/'lease.json',D/'outputs.final.json',D/'readback.json']]
manifest=dict(artifacts=outputs,count=len(outputs));manifest['outputs_sha256']=sha(canon(manifest));write(D/'outputs.final.json',manifest)
for row in outputs:assert pin(row['path'])==row
read=dict(status='ALL_NATIVE_INPUT_OUTPUT_SELF_PAYLOAD_READBACKS_PASS',inputs=len(inputs),outputs=len(outputs),actual_readback_pid=p.pid,actual_readback_exit_code=0,run=pin(D/'run.json'),receipt=pin(D/'receipt.json'),outputs_manifest=pin(D/'outputs.final.json'))
write(D/'readback.json',read);assert load(D/'readback.json')==read
lease=dict(schema_version=1,actor='/root/whole_math52',status='CLOSED',closure_order='LAST filesystem write after actual foreground compiler/Python/readback EXIT and all raw/LF/native-self/payload/output validations',
 actual_finalizer_pid=os.getpid(),actual_readback_pid=p.pid,actual_readback_exit_code=0,actual_compiler_lean_pids=[x['pid'] for r in results for x in r['observed_processes'] if x['exe'].lower()=='lean.exe'],
 resources=dict(compiler='ALL11_TERMINAL_CLOSED',Python_diagnostic_runners='ALL5_EXIT0_CLOSED',readback='EXIT0_CLOSED',read_handles='CLOSED',write_handles='CLOSED',Python_finalizer='Immediate successful EXIT0 after last lease write and precomputed stdout; no later filesystem operation'),
 run=pin(D/'run.json'),receipt=pin(D/'receipt.json'),outputs_manifest=pin(D/'outputs.final.json'),readback=pin(D/'readback.json'),run_sha256=run['run_sha256'],declaration_review_payload_sha256=payload_hash,output_count=len(outputs)+2,closed_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
lease['lease_sha256']=sha(canon(lease));b=(json.dumps(lease,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
summary=dict(status='CLOSED',verdict=receipt['verdict'],inputs=len(inputs),outputs=lease['output_count'],actual_finalizer_pid=os.getpid(),actual_readback_pid=p.pid,receipt_raw_lf=lease['receipt']['raw_sha256'],run_raw_lf=lease['run']['raw_sha256'],run_sha256=run['run_sha256'],declaration_review_payload_sha256=payload_hash,lease_raw_lf=sha(b),lease_sha256=lease['lease_sha256'],proposal_raw_lf=receipt['proposal']['raw_sha256'],successor_headers=[r['successor'] for r in header_changes])
(D/'lease.json').write_bytes(b)
print(json.dumps(summary))
