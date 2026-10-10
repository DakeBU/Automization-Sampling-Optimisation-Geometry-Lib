import datetime,json,os,re,sys
sys.dont_write_bytecode=True
from review76 import ROOT,OWN,HEADER,EXPECTED,ACTOR,SPEC,PUBLIC,sha,can,load,pin,check,save

assert not (OWN/'lease.final.json').exists()
inputs=load(OWN/'inputs.manifest.json')
for z in inputs['inputs']:assert check(z['original'])==check(z['snapshot'])
original=HEADER.read_bytes();accepted=OWN/'header76.v3.proposed.lean';source=accepted.read_bytes().decode();overlay=load(OWN/'exact-minimal-type-overlay.v3.proposal.json');expected=original.decode()
for z in overlay['exact_replacements']:assert expected.count(z['before'])==z['occurrences']==1;expected=expected.replace(z['before'],z['after'])
assert source==expected and sha(original)==EXPECTED and pin(accepted)['RAW_sha256']=='996b8a89ffe84cfef8faf75551f962f2378db221841f5e1a38137eb81281d015'
assert source[source.index('\ntheorem '+PUBLIC):]==original.decode()[original.decode().index('\ntheorem '+PUBLIC):]
prefix=source[:source.index('\ntheorem '+PUBLIC)];defs=re.findall(r'^    let (\S+)\s*:',prefix,re.M);assert defs==['c','Φ','S','rate','H','C','Λ','τ','next','record','eventTime']
private_tel=prefix[prefix.index('private def '+SPEC):prefix.index(' : Prop :=')];public_tel=source[source.index('\ntheorem '+PUBLIC):];callers=re.findall(r'\((h(?:αβ|α|V|H|βη|η))\s*:',private_tel);assert callers==re.findall(r'\((h(?:αβ|α|V|H|βη|η))\s*:',public_tel)==['hα','hαβ','hV','hH','hη','hβη']
sys.path.insert(0,str(ROOT/'tools'));import astis
stripped=astis.strip_lean_comments_and_strings(source);forbidden=[dict(line=i,text=s) for i,s in enumerate(stripped.splitlines(),1) if astis.FORBIDDEN_REGEX.search(s)];assert not forbidden
assert source.endswith(' := by\n') and 'WellFoundedLT' not in stripped
v3=load(OWN/'typechecks.v3.json');negative=load(OWN/'typechecks.json');v2=load(OWN/'typechecks.v2.json');assert v3['status']=='PASS' and negative['status']==v2['status']=='FAIL_TYPE_CONTRACT'
for result in v3['results']:assert result['terminal_EXIT']==0 and load(result['receipt']['path'])['terminal_closed']
for result in negative['results']+v2['results']:assert result['terminal_EXIT']==1 and load(result['receipt']['path'])['terminal_closed']
audit=dict(status='PASS_PROSPECTIVE_LITERAL_AUDIT',actual_audit_and_close_PID=os.getpid(),original_header=pin(HEADER),accepted_header=pin(accepted),exact_overlay=pin(OWN/'exact-minimal-type-overlay.v3.proposal.json'),original_six_callers=callers,literal_definition_names=defs,definitions=11,conclusion_groups=10,public_telescope_exact_unchanged=True,all_non_overlay_bytes_exact=True,forbidden_closure_hits=forbidden,full_target_body_present=False,full_target_proved=False,source_review=False,VERIFIED=False)
save('literal-and-type-audit.json',audit)
decision=dict(status='ACCEPTED_V3_PROSPECTIVE_HEADER_ONLY_ORIGINAL_REQUIRES_TYPE_REPAIR',actor=ACTOR,reviewer=ACTOR,
 accepted_prospective_header_only=True,accepted_header_SHA256=pin(accepted)['RAW_sha256'],accepted_header=pin(accepted),
 original_header_typecheck_failed=True,original_header_not_accepted_as_typed=True,original_header_SHA256=EXPECTED,
 ten_clauses_mathematically_correct=True,minimum_mathematical_repair=[],minimum_type_repair=overlay['exact_replacements'],
 intermediate_default_only_v2_rejected=True,exact_two_inner_ascriptions_only=True,
 original_six_callers_preserved=True,literal_definitions=11,conclusion_groups=10,new_public_premises=[],arbitrary_provider=False,
 native_Sum_active_finite_stopped_Unit=True,no_phase_at_infinity=True,joint_product_sequence_Borel_for_every_finite_n=True,
 original_energy_H_z0_inherited=True,uniform_waiting_increment_includes_stopped_infinity=True,
 zero_C_positive_threshold_stop=True,zero_threshold_legal=True,non_strict_event_times_for_arbitrary_thresholds=True,
 rank_zero_allowed=True,alphaeta_one_allowed=True,zero_energy_allowed=True,hidden_almost_sure_finite_premise=False,
 full_target_proved=False,full_target_proof_search=False,SAU=False,PROVED_LOCAL=False,VERIFIED=False,source_review=False,decoder_review=False,
 reader_acceptance=False,PURIFIED=False,full_Exposition_Seal=False,Goal_complete=False,main=False,live=False,whole_paper=False,
 true_parent75_source_admission_pending=True,source_overlay_adoption_pending=True,
 open_boundaries=['iid Exp sequence/product law and support/mean/SLLN','nonaccumulation/nonexplosion','stitched all-time phase/process','Markov/invariance/terminal kernel','main/error/cost/composition/full paper and Goal'],
 metadata_debts=['selected source-only contract retains historical prospective75/no-header76 stage wording; no mathematical effect'],
 actual_typechecks=dict(original=[dict(PID=z['PID'],EXIT=z['terminal_EXIT']) for z in negative['results']],insufficient_v2=[dict(PID=z['PID'],EXIT=z['terminal_EXIT']) for z in v2['results']],accepted_v3=[dict(PID=z['PID'],EXIT=z['terminal_EXIT']) for z in v3['results']]))
save('decision.json',decision)
observed=[dict(label='prepare',PID=47428,terminal_EXIT=0),dict(label='original-typecheck-driver',PID=14060,terminal_EXIT=1),dict(label='insufficient-v2-typecheck-driver',PID=45980,terminal_EXIT=1),dict(label='accepted-v3-typecheck-driver',PID=39928,terminal_EXIT=0)]
save('observed-tool-terminals.json',dict(evidence_origin='Actual foreground exec_command completions observed by independent reviewer; individual Lean probes have complete RAW stdout/stderr/closed terminal receipts.',terminals=observed,optional_historical_lookup_negative=pin(OWN/'retrieval-negative.preserved.json')))
payload=dict(name='Complete independent prospective76 mathematical/type decision with exact original and accepted full headers',actor=ACTOR,
 decision=decision,input_manifest=inputs,full_exact_header_UTF8=source,full_original_header_UTF8=original.decode(),
 full_named_review_UTF8=(OWN/'named.prospective-mathematics76.md').read_text(encoding='utf8'),exact_overlay_proposal=overlay,
 typechecks=v3,original_typechecks=negative,insufficient_v2_typechecks=v2,literal_audit=audit,actual_tool_terminal_completions=observed,
 mathematical_proof_implementation=False,full_target_proved=False,source_review=False,VERIFIED=False)
save('complete.named.RAW-payload.json',payload)
run=dict(status='ACCEPTED_V3_PROSPECTIVE_HEADER_ONLY',actor=ACTOR,checked_parent=inputs['checked_parent'],original_header=pin(HEADER),accepted_header=pin(accepted),
 decision=decision,decision_pin=pin(OWN/'decision.json'),input_manifest=inputs,typechecks=v3,
 original_negative_typechecks=pin(OWN/'typechecks.json'),insufficient_v2_negative_typechecks=pin(OWN/'typechecks.v2.json'),
 exact_overlay=pin(OWN/'exact-minimal-type-overlay.v3.proposal.json'),complete_named_RAW_payload=pin(OWN/'complete.named.RAW-payload.json'),
 named_review=pin(OWN/'named.prospective-mathematics76.md'),literal_audit=pin(OWN/'literal-and-type-audit.json'),
 full_target_proved=False,SAU=False,VERIFIED=False,source_review=False,no_canonical_Git_ledger_site_writes=True,
 whole_logical_recipe='SHA256 sorted-key compact UTF8 JSON, ensure_ascii=False, allow_nan=False, removing ONLY top-level run_sha256.',
 LF_pin_recipe='Replace CRLF byte pairs with LF ONLY; RAW authoritative.',actual_close_writer_PID=os.getpid())
run['run_sha256']=sha(can(run));save('run.json',run)
entries=[pin(p) for p in sorted(OWN.rglob('*'),key=lambda p:p.as_posix()) if p.is_file() and p.name not in {'native.manifest.json','lease.final.json'}]
save('native.manifest.json',dict(entries=entries,entry_count=len(entries),logical_entries_sha256=sha(can(entries)),recipe='All owned files except native.manifest.json and final lease; canonical sorted compact UTF8 JSON hash of exact RAW/LF pins.'))
manifest=pin(OWN/'native.manifest.json');files=sorted(entries+[manifest],key=lambda z:z['path'])
lease=dict(status='CLOSED_LAST',actor=ACTOR,reviewer=ACTOR,writer_PID=os.getpid(),writer_terminal_EXIT_contract=0,
 postclose_owned_writes_forbidden=True,final_owned_write=True,files=files,file_count_including_lease=len(files)+1,owned_files=len(files)+1,
 manifest=manifest,closure_logical_sha256=sha(can(files)),run_sha256=run['run_sha256'],full_target_proved=False,VERIFIED=False,
 closed_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),external_readonly_command='review76.py readonly after actual writer terminal EXIT0; no owned writes.')
save('lease.final.json',lease)
print(json.dumps(dict(status='CLOSED_LAST',writer_PID=os.getpid(),file_count_including_lease=len(files)+1,manifest_entries=len(entries),input_count=inputs['input_count'],
 run_sha256=run['run_sha256'],lease_RAW_sha256=sha((OWN/'lease.final.json').read_bytes()),complete_named_RAW_sha256=run['complete_named_RAW_payload']['RAW_sha256'],
 complete_named_RAW_bytes=run['complete_named_RAW_payload']['RAW_bytes'],closure_logical_sha256=lease['closure_logical_sha256'],accepted_header_SHA256=pin(accepted)['RAW_sha256'],terminal_EXIT_contract=0)),flush=True)
