from pathlib import Path
import base64,hashlib,json,os
root=Path.cwd();r=root/'runs/20261007-companion-priority/pbps-reflection-rotation-preproof69'
load=lambda p:json.loads(p.read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def lower_pin(row):
 p=Path(row['path']);b=p.read_bytes();lf=b.replace(b'\r\n',b'\n')
 assert len(b)==row['raw_bytes'] and sha(b)==row['raw_sha256'] and len(lf)==row['lf_bytes'] and sha(lf)==row['lf_sha256']
 return b
def upper_check(b,row):
 lf=b.replace(b'\r\n',b'\n')
 assert len(b)==row['RAW_bytes'] and sha(b)==row['RAW_sha256'] and sha(lf)==row['LF_sha256']
 if 'LF_bytes' in row:assert len(lf)==row['LF_bytes']
def pin(p):
 b=p.read_bytes();return dict(path=p.relative_to(root).as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
s=r/'independent-header-source69';m=r/'independent-header-math69'
sl=load(s/'lease.final.json');ml=load(m/'lease.final.json')
assert sha((s/'lease.final.json').read_bytes())=='a3b1cfecdc7d0bb7d9a33a8360658ed8ba9f2d8913e857ad0cdada008b28f4ee'
assert sha((m/'lease.final.json').read_bytes())=='7ff2b645d2c6a4b857889d557ad076a2f50b0d1e868d6125baf0d96c44b53ffa'
assert sl['status']==ml['status']=='CLOSED_LAST' and sl['owned_file_count']==84 and ml['owned_file_count_including_self']==77
sm=load(s/'owned-manifest.json');assert len(sm['regular_file_entries'])==82
sf={p.relative_to(s).as_posix():p for p in s.rglob('*') if p.is_file()}
assert len(sf)==84 and set(sf)=={row['name'] for row in sm['regular_file_entries']}|{'owned-manifest.json','lease.final.json'}
assert sha(can(sm['regular_file_entries']))==sl['finite_owned_closure_sha256']==sm['closure_entries_canonical_sha256']
assert sha((s/'owned-manifest.json').read_bytes())==sl['manifest_RAW_sha256']
for row in sm['regular_file_entries']:upper_check(sf[row['name']].read_bytes(),row)
mf={p.resolve() for p in m.rglob('*') if p.is_file()}
assert len(mf)==77 and mf=={Path(row['path']).resolve() for row in ml['all_owned_outputs_except_only_self']}|{(m/'lease.final.json').resolve()}
for row in ml['all_owned_outputs_except_only_self']:lower_pin(row)
assert (s/'lease.final.json').stat().st_mtime_ns>=max(p.stat().st_mtime_ns for p in sf.values())
assert (m/'lease.final.json').stat().st_mtime_ns>=max(p.stat().st_mtime_ns for p in mf)
for d,lease,name,expected in [(s,sl,'review-run.json','4f683c9f0c59e846516870b33b0eeefffb550797d80676b0ba640c084e92a7bd'),(m,ml,'run.json','77418f40f25b284b431d9f87c64d2703f78e2532aea644c129372ce4e1132fb1')]:
 run=load(d/name);assert sha(can({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']==lease['whole_logical_run_sha256']==expected
for key in ['COMPLETE_NAMED_REVIEW','COMPLETE_RAW_REVIEW','COMPLETE_RAW_DECISION','FINITE_COVERAGE','SEPARATE_COMPLETE_RAW_LF_INPUT']:
 upper_check((s/sl[key]['name']).read_bytes(),sl[key])
assert sha(lower_pin(ml['named_complete_RAW_review']))=='454b28b9bc96e3cee5d2a90909a574e4cb7dbaae3f3fbaaf464e8d3b64c5e36c'
source_inputs=load(s/'RAW-input-payload.json')
assert source_inputs['count']==len(source_inputs['inputs'])
for row in source_inputs['inputs']:
 b=base64.b64decode(row['complete_RAW_bytes_base64']);upper_check(b,row)
 assert base64.b64decode(row['complete_LF_bytes_base64'])==b.replace(b'\r\n',b'\n')
 assert Path(row['original_path'].replace('\\','/')).read_bytes()==b
math_inputs=load(m/'inputs.manifest.json');assert math_inputs['input_count']==len(math_inputs['inputs'])==14
for row in math_inputs['inputs']:
 b=lower_pin(row['original']);assert lower_pin(row['RAW_snapshot'])==b and lower_pin(row['LF_snapshot'])==b.replace(b'\r\n',b'\n')
sd=load(s/'header-source-decision.json');md=load(m/'header-review.json');mr=load(m/'run.json')
assert sd['verdict']==sl['verdict']=='ADMIT_HEADER_ONLY_FOR_STATEMENT_SEAL_CONSIDERATION'
assert not sd['missing_source_premises'] and not sd['extra_public_premises'] and not sd['source_semantic_repairs_required']
assert md['status']==mr['status']=='HEADER69_ACCEPTED_TYPECHECKED_NO_TARGET_PROOF'
assert not md['typed_header_blockers'] and not md['mathematical_statement_repairs_required'] and not md['private_mathematical_providers']
assert sl['source_math_count']==419 and sl['expanded_header_lines']==107 and sl['expanded_header_segments']==10
assert [sl[key] for key in ['actual_source_reviewer_pid','actual_finalizer_pid','actual_readback_pid','actual_close_validator_pid','actual_lease_writer_pid']]==[51488,30932,17364,14624,52240]
assert all(sl[key]==0 for key in ['actual_source_reviewer_exit','actual_finalizer_exit','actual_readback_exit','actual_close_validator_exit'])
draft=load(r/'header-draft69.json')
for row in draft['headers']:upper_check((root/row['path']).read_bytes(),row)
assert sha((r/'header0-expanded.lean').read_bytes())==sd['exact_candidate_expanded_RAW_sha256']==sl['candidate_expanded_RAW_sha256']=='391ccc5bbf0978aa342269eb96c2dc4c9c23ae7865e6d9152959fc4df26f468b'
out=dict(status='INDEPENDENT_HEADER69_MATH_AND_SOURCE_ACCEPTED',actual_read_only_adopter_pid=os.getpid(),math_owned_files=77,source_owned_files=84,source_only_parent_owned_files=82,math_whole_logical_run_sha256=ml['whole_logical_run_sha256'],source_whole_logical_run_sha256=sl['whole_logical_run_sha256'],math_complete_named_RAW_review=ml['named_complete_RAW_review'],source_complete_named_RAW_review=sl['COMPLETE_NAMED_REVIEW'],math_lease=pin(m/'lease.final.json'),source_lease=pin(s/'lease.final.json'),math_current_RAW_LF_inputs=14,source_current_RAW_LF_inputs=len(source_inputs['inputs']),header_expanded=pin(r/'header0-expanded.lean'),private_literal_Prop=pin(r/'statement0.definition.lean'),public_header=pin(r/'header0-public.lean'),source_expectations_frozen_before_candidate=True,fresh_type_compiler_PID_EXIT0=35056,source_compiler=False,target_proof=False,SAU_claim=False,VERIFIED=False,Goal_complete=False)
p=r/'root.header69.adoption.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
seal=dict(status='STATEMENT69_SEALED_NOT_CLAIMED_NOT_PROVED',source_first_adoption=pin(r/'root.primary69.adoption.json'),independent_header_admission=pin(p),exact_target=draft['target_declaration'],planned_file=draft['proposed_file'],statement_seal=out['header_expanded'],private_literal_Prop=out['private_literal_Prop'],public_original_caller=out['public_header'],original_caller_conditions='Finite real Hilbert/Borel E; C2 V;0<alpha<=beta;two global Hessian bounds;eta>0,beta eta<=1.',exact_delta=draft['exact_source_delta'],source_consumers=draft['source_consumers'],real_parent='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualRootCommutation.actual_same_root_inverse_commutation',no_sharp_energy68_proof_dependency=True,all_source_ingredients_are_obligations_or_internal_parents_not_public_binders=True,definition_semantics='D=R U inclusion is exact actual conditional-complement compression; SAME centered root/inverse/polar. One literal full Prop only; no provider.',remaining_truth_boundary=draft['truth_boundary'],SAU_claim=False,proof_search=False,compiled_target=False,whole_paper=False,Goal_complete=False)
p=r/'root.statement-seal69.json';assert not p.exists();p.write_text(json.dumps(seal,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS69 header math77/source84/current inputs adopted; exact actual-intertwining Statement Seal created. NO SAU claim, target proof or Goal completion.')
