from pathlib import Path
import hashlib,json,os
pre=Path('runs/20261007-companion-priority/pbps-bounce-rate-preproof74');p=pre/'header74.typecheck.lean';b=p.read_bytes()
assert hashlib.sha256(b).hexdigest()=='1dd0d07c3d21fd3e5c0e1989755d15103ad495852defb1ce261484fc7f12c672'
anchor=b'end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBounceRate\n';assert b.count(anchor)==1
fixed=b.replace(anchor,b'end\n'+anchor);q=pre/'header74.typecheck-closed-sections.lean';assert not q.exists();q.write_bytes(fixed)
d=dict(status='TYPECHECK_DRIVER_SCOPE_CLOSE_REPAIR_ONLY_NOT_STATEMENT',actual_root_PID=os.getpid(),original_predicate_file=p.as_posix(),original_RAW_sha256=hashlib.sha256(b).hexdigest(),fixed_predicate_file=q.as_posix(),fixed_RAW_sha256=hashlib.sha256(fixed).hexdigest(),difference='One end inserted to close noncomputable section before named namespace end.',original_failed_PID=52824,original_terminal_EXIT=1,all_predicate_bytes_unchanged=True,sealed_header_unchanged=True,no_theorem_proof=True,Goal_complete=False)
(pre/'typecheck-driver-diagnosis74.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf8',newline='\n');print(json.dumps(d))
