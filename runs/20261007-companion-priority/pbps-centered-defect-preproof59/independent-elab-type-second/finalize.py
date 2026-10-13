import pathlib,json,hashlib,sys,os,subprocess,datetime,re
ROOT=pathlib.Path('E:/Samplinglib');R=ROOT/'runs/20261007-companion-priority/pbps-centered-defect-preproof59';D=R/'independent-elab-type-second';P=ROOT/'.astis/pbps-centered-defect59/independent-elab-type-second'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(q):return json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def load(p):return json.loads(pathlib.Path(p).read_bytes())
def write(p,q):pathlib.Path(p).write_bytes((json.dumps(q,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode())
def pin(p):
 p=pathlib.Path(p);b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
results=[];inputs={}
for phase in [D,D/'phase1',D/'phase2']:
 q=load(phase/'compiler.results.json');assert q['all_compiler_leases']=='CLOSED'
 for row in q['inputs']:assert pin(row['path'])==row;inputs[row['path']]=row
 for result in q['results']:
  for k in ['source','stdout','stderr']:assert pin(result[k]['path'])==result[k]
  assert result['compiler_status']=='CLOSED' and any(p['exe'].lower()=='lean.exe' for p in result['observed_processes'])
  results.append(result);inputs[result['source']['path']]=result['source']
assert len(results)==8
byname={x['name']:x for x in results}
before_body=['full-type-baseline','full-type-expected-Prop','full-type-recdepth','consumer-complete-type']
reached_body=['full-type-inline-kernel','full-type-no-centered-tail','consumer-inline-kernel-type']
for name in before_body:
 x=byname[name];s=pathlib.Path(x['stdout']['path']).read_text(encoding='utf8');assert x['actual_exit_code']==1 and 'unknown free variable' in s and 'HEADER_ELABORATED_INTENTIONAL_NO_PROOF' not in s
for name in reached_body:
 x=byname[name];s=pathlib.Path(x['stdout']['path']).read_text(encoding='utf8');assert x['actual_exit_code']==1 and 'HEADER_ELABORATED_INTENTIONAL_NO_PROOF' in s and 'unknown free variable' not in s
control=byname['full-inline-definition-equality-and-kernel-controls'];assert control['actual_exit_code']==0
s=pathlib.Path(control['stdout']['path']).read_text(encoding='utf8');assert 'sorryAx' not in s and all(f'kernel_signatures{n}_definitionally_equal' in s and f'diagnostic_named_full_type{n}' in s for n in [0,1])
rootprobe=ROOT/'.astis/pbps-centered-defect59/full-header-negative-probe.lean'
inputs[rootprobe.as_posix()]=pin(rootprobe);assert rootprobe.read_bytes()==pathlib.Path(byname['full-type-baseline']['source']['path']).read_bytes()
rows=[]
for n in [0,1]:
 old=R/f'independent-elab-review/header{n}.successor-proposed.lean';new=D/f'header{n}.inline-kernel-proposed.lean'
 a=old.read_text(encoding='utf8');b=new.read_text(encoding='utf8')
 lines=a.splitlines(keepends=True);removed=[l for l in lines if 'let H0 : Submodule ℝ (Lp ℝ 2 ν) := (innerSL ℝ q).ker' in l];assert len(removed)==1
 line=removed[0];without=a.replace(line,'',1);expected=without.replace('H0','((innerSL ℝ q).ker)');assert expected==b
 offset=a.index(line);reverse=b.replace('((innerSL ℝ q).ker)','H0');reverse=reverse[:offset]+line+reverse[offset:];assert reverse==a
 row=dict(index=n,parent=pin(old),successor=pin(new),deleted_let_definition=line,deleted_definition_start_original_LF_character=offset,exact_kernel_inline_replacements=without.count('H0'),reverse_reconstruction_raw_LF_match=True,quantified_binders_unchanged=True,declaration_name_unchanged=True)
 rows.append(row);inputs[old.as_posix()]=pin(old);inputs[new.as_posix()]=pin(new)
 for suffix,data in [('parent',old.read_bytes()),('successor',new.read_bytes())]:(D/f'header{n}.{suffix}.qualified.raw.snapshot').write_bytes(data)
 # No proposal introduces any new witness, certificate, instance or hypothesis.
 assert 'H0' not in b
oldrun=R/'independent-elab-review/run.json';oldlease=R/'independent-elab-review/lease.json'
for p in [oldrun,oldlease]:inputs[p.as_posix()]=pin(p)
q=load(oldrun);assert sha(canon({k:v for k,v in q.items() if k!='run_sha256'}))==q['run_sha256'] and load(oldlease)['status']=='CLOSED'
for x in results:
 assert not re.search(r'\b(sorry|admit|axiom)\b',pathlib.Path(x['source']['path']).read_text(encoding='utf8'))
proposal=dict(schema_version=1,created_by='/root/whole_math52',status='PROPOSED_REQUIRES_DISTINCT_SOURCE_SYNTAX_REVIEW',repair_kind='Definitionally equal elimination of dependent let-H0 abbreviation in complete theorem types',
 headers=rows,exact_rule='Remove the single local let H0 := (innerSL ℝ q).ker and substitute that exact value for each H0 use. Retain all previously accepted explicit operator identity annotations.',
 unchanged='All theorem names, quantified binders and their order/types, hypotheses, q witness, AE classes, kernel/domain, quantifiers, operators, constants and conclusions. A let abbreviation is unfolded; no premise or instance is added.',
 producer_named_type_probe=byname['full-type-inline-kernel'],consumer_named_type_probe=byname['consumer-inline-kernel-type'],
 complete_rfl_and_kernel_declaration_controls=control,scope='TYPE elaboration only; intentional-fail probes EXIT1 by design. Kernel controls use an extra input solely to check declaration typing; that diagnostic input is not in either proposed header and gives no theorem proof admission.')
write(D/'exact-proposal.json',proposal);inputs[(D/'exact-proposal.json').as_posix()]=pin(D/'exact-proposal.json')
payload=dict(payload_name='independent-full-theorem-type-elaboration59-second',verdict='DEFINITIONALLY_EQUAL_TYPE_SYNTAX_CLARIFICATION_ISOLATED',
 precise_reducer='Both full let-H0 theorem types fail before any body with unknown free variable. Producer with centered operator tail removed reaches its body. Fully substituting the exact kernel for H0 lets BOTH complete unchanged theorem conclusions reach their intentional body. Expected Prop and maxRecDepth10000 fail unchanged.',
 mechanism_boundary='Observed failure concerns dependent let-H0/centered operator type elaboration. We do not claim a proved Lean-internal caching mechanism or a mathematical defect.',
 parent_review_scope_correction='Previous CLOSED statement-valued Prop definitions/rfl equalities and partial positive fragment remain valid. They did not establish direct complete named theorem TYPE elaboration; this stage supplies that missing check.',
 headers=rows,proposal=pin(D/'exact-proposal.json'),before_body_negatives=[byname[x] for x in before_body],intentional_body_reached=[byname[x] for x in reached_body],complete_definitionally_equal_controls=control,
 actual_operator_types=dict(H0='Exact subtype of (innerSL ℝ q).ker in Lp ℝ 2 ν',T0='((innerSL ℝ q).ker) →L[ℝ] ((innerSL ℝ q).ker)',D0='(1 : ((innerSL ℝ q).ker) →L[ℝ] ((innerSL ℝ q).ker)) - T0*T0'),
 source_binder_or_assumption_repair=False,full_theorem_proof_admission=False,original_closed_artifacts_preserved=True,
 remaining=['Separate independent source/syntax review and root adoption of this exact successor proposal.','Root full theorem and real consumer proof gate remain open.','Gamma/root/weakH1/polar/dynamics/main/cost/composition/fullpaper/PURIFIED remain open.'])
write(D/'type-review.payload.json',payload)
write(D/'inputs.final.json',dict(inputs=list(inputs.values()),count=len(inputs),reviewer_implementation_inputs=[pin(x) for x in sorted(D.glob('*.py'))]))
code="import pathlib,json,hashlib,sys,os;q=json.loads(pathlib.Path(sys.argv[1]).read_bytes())\nfor r in q['inputs']+q['reviewer_implementation_inputs']:\n b=pathlib.Path(r['path']).read_bytes();l=b.replace(b'\\r\\n',b'\\n');assert len(b)==r['bytes'] and len(l)==r['lf_bytes'] and hashlib.sha256(b).hexdigest()==r['raw_sha256'] and hashlib.sha256(l).hexdigest()==r['lf_sha256']\nprint(json.dumps(dict(pid=os.getpid(),all_input_pins_match=True,input_count=len(q['inputs']))))"
cmd=[sys.executable,'-B','-X','utf8','-c',code,str(D/'inputs.final.json')];p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=p.communicate()
(D/'final-readback.stdout.log').write_bytes(out);(D/'final-readback.stderr.log').write_bytes(err)
write(D/'final-readback.status.json',dict(actual_pid=p.pid,actual_exit_code=p.returncode,command=cmd,stdout=pin(D/'final-readback.stdout.log'),stderr=pin(D/'final-readback.stderr.log')));assert p.returncode==0,err.decode()
for phase in [D/'phase1',D/'phase2']:write(phase/'lease.json',dict(status='CLOSED',compiler_results=pin(phase/'compiler.results.json'),compiler='ALL_TERMINAL_CLOSED',Python_runner_observed_exit_code=0))
payload_hash=sha(canon(payload))
receipt=dict(schema_version=1,actor='/root/whole_math52',status='CLOSED_BOUNDED_NAMED_THEOREM_TYPE_REVIEW59',verdict=payload['verdict'],proposal=pin(D/'exact-proposal.json'),
 counts=dict(inputs=len(inputs),compiler_invocations=8,before_body_type_negatives=4,intentional_body_reached_EXIT1=3,successful_kernel_controls_EXIT0=1),
 complete_named_producer_TYPE_body_reached=True,complete_named_consumer_TYPE_body_reached=True,complete_forward_definition_equality='Named rfl EXIT0',reverse_reconstruction='Both exact parent LF bytes reconstructed',
 kernel_controls_scope='Additional diagnostic-input binder only on kernel typing controls; not part of either proposal, no source theorem proof credit',
 type_review_payload_sha256=payload_hash,full_theorem_proof_admitted=False,remaining=payload['remaining'])
write(D/'receipt.json',receipt)
run=dict(schema_version=1,actor='/root/whole_math52',status='COMPLETE_PREPROOF_TYPE_DIAGNOSIS',inputs=load(D/'inputs.final.json'),receipt=pin(D/'receipt.json'),compiler_results=results,
 type_review_payload=payload,type_review_payload_sha256=payload_hash,readback_status=pin(D/'final-readback.status.json'),
 native_recipes=dict(run_sha256='SHA256 sorted compact UTF8 complete run excluding ONLY top-level run_sha256; ensure_ascii=False, allow_nan=False, no newline',type_review_payload_sha256='SHA256 same canonical encoding of distinct complete named type_review_payload object',raw_lf='Exact bytes; replace CRLF pairs only for LF; exact bytes lengths and hashes both recorded'))
run['run_sha256']=sha(canon(run));write(D/'run.json',run)
q=load(D/'run.json');assert sha(canon({k:v for k,v in q.items() if k!='run_sha256'}))==q['run_sha256'] and q['type_review_payload']==load(D/'type-review.payload.json') and sha(canon(q['type_review_payload']))==payload_hash
outputs=[pin(x) for x in sorted(D.rglob('*')) if x.is_file() and x not in [D/'lease.json',D/'outputs.final.json',D/'readback.json']]
manifest=dict(artifacts=outputs,count=len(outputs));manifest['outputs_sha256']=sha(canon(manifest));write(D/'outputs.final.json',manifest)
for row in outputs:assert pin(row['path'])==row
read=dict(status='ALL_INPUT_OUTPUT_NATIVE_SELF_DISTINCT_PAYLOAD_READBACKS_PASS',actual_readback_pid=p.pid,actual_readback_exit_code=0,run=pin(D/'run.json'),receipt=pin(D/'receipt.json'),outputs_manifest=pin(D/'outputs.final.json'),input_count=len(inputs),output_count=len(outputs))
write(D/'readback.json',read);assert load(D/'readback.json')==read
lease=dict(schema_version=1,actor='/root/whole_math52',status='CLOSED',closure_order='LAST filesystem write after actual foreground compiler/Python/readback exits and all input/output/native validations',
 actual_finalizer_pid=os.getpid(),actual_readback_pid=p.pid,actual_readback_exit_code=0,actual_compiler_Lean_pids=[z['pid'] for r in results for z in r['observed_processes'] if z['exe'].lower()=='lean.exe'],
 resources=dict(compiler='ALL8_TERMINAL_CLOSED',Python_diagnostic_runners='ALL3_OBSERVED_EXIT0_CLOSED',readback='EXIT0_CLOSED',read_handles='CLOSED',write_handles='CLOSED',Python_finalizer='Immediate successful EXIT0 after last lease write/precomputed stdout; no subsequent filesystem operations'),
 run=pin(D/'run.json'),receipt=pin(D/'receipt.json'),outputs_manifest=pin(D/'outputs.final.json'),readback=pin(D/'readback.json'),run_sha256=run['run_sha256'],type_review_payload_sha256=payload_hash,output_count=len(outputs)+2,closed_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
lease['lease_sha256']=sha(canon(lease));b=(json.dumps(lease,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
summary=dict(status='CLOSED',verdict=receipt['verdict'],inputs=len(inputs),outputs=lease['output_count'],actual_finalizer_pid=os.getpid(),actual_readback_pid=p.pid,receipt_raw_lf=lease['receipt']['raw_sha256'],run_raw_lf=lease['run']['raw_sha256'],run_sha256=run['run_sha256'],type_review_payload_sha256=payload_hash,lease_raw_lf=sha(b),lease_sha256=lease['lease_sha256'],proposal_raw_lf=receipt['proposal']['raw_sha256'],successor_headers=[r['successor'] for r in rows])
(D/'lease.json').write_bytes(b)
print(json.dumps(summary))
