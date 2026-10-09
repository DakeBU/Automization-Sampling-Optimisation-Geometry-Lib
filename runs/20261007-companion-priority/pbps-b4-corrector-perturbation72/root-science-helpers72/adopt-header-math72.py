from pathlib import Path
import hashlib,json,os,subprocess,sys
r=Path('runs/20261007-companion-priority/pbps-b4-perturbation-preproof72');o=r/'independent-header-math72'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
q=subprocess.run([sys.executable,'-X','utf8',str(o/'verify72.py')],capture_output=True,check=True)
receipt=json.loads(q.stdout);assert receipt['verification']=='PASS' and receipt['writer_terminated'] and receipt['owned_manifest_and_last_write_valid']
assert receipt['run_sha256']=='8f25b5e473acb5b91ffffbf5e2309be4c462cadcb84dec38cba3db19b84918e2'
run=load(o/'run72.json');assert run['minimum_mathematical_repair'] is None
assert set(run['prospective_header_verdict'].values())=={'ACCEPT_PROSPECTIVE_HEADER_MATH'}
assert run['literal_checks']['removing_only_added_tail_and_renaming_private_def_restores_current71_literal']
assert not run['compiled'] and not run['proved'] and not run['source_fidelity_review_completed']
assert all(not z['returned_to_original_caller'] for z in run['derived_assumptions_audit'])
p=r/'root.header-math72.adoption.json';assert not p.exists()
p.write_text(json.dumps(dict(status='INDEPENDENT_PROSPECTIVE72_HEADERS_MATH_ONLY_ADOPTED',actual_root_PID=os.getpid(),native_owned_files=13,native_inputs=5,native_whole_logical_run_sha256=run['run_sha256'],native_closed_marker_RAW_sha256=sha((o/'CLOSED_LAST.json').read_bytes()),named_complete_review_RAW_sha256=sha((o/'review72.named.md').read_bytes()),fresh_root_readonly_verifier=receipt,actual_verifier_terminal_exit=q.returncode,mathematical_repairs=[],source_verdict=False,statement_seal=False,claimed=False,proved=False,VERIFIED=False),ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS72 independent prospective header mathematics CLOSED13/5inputs; fresh readonly verifier PID',receipt['readonly_verifier_pid'],'EXIT0; source/Seal/claim/proof pending.')
