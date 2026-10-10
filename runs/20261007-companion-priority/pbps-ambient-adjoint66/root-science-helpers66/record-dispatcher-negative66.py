from pathlib import Path
import json,hashlib
r=Path('runs/20261007-companion-priority/pbps-ambient-adjoint66')
old=r/'synchronous-elaboration66/production.before.exactraw.lean'
g=json.loads((r/'focused-main-sync-v4/receipt.json').read_bytes());assert g['exit_code']==1
matches=[x for x in g['inputs'] if x['path'].endswith('/AmbientAdjointCorrector.lean')];assert len(matches)==1
sha=lambda b:hashlib.sha256(b).hexdigest()
assert matches[0]['raw_sha256']==sha(old.read_bytes()) and b'set_option Elab.async false' not in old.read_bytes()
out=r/'synchronous-dispatch66.negative.json';assert not out.exists()
out.write_text(json.dumps(dict(kind='ROOT_DISPATCH_GUARD_AND_SCRATCH_NAME_ASSERTION',failed_helper_expression='assert header in new and header in scratch',helper_failure='Renamed scratch theorem intentionally lacks original theorem name; assertion should compare the conclusion expression only.',root_dispatch_failure='PowerShell continued to the following build after helper EXIT1; sync-v4 therefore compiled the OLD inline default-async bytes. This accidental unchanged retry is retained and provides no new mathematical information.',native_compiler_receipt=(r/'focused-main-sync-v4/receipt.json').as_posix(),native_compiler_pid=g['actual_foreground_pid'],old_RAW_sha256=sha(old.read_bytes()),async_false_present=False,correction='Corrected expression-only assertion. Apply helper EXIT0 inspected in a separate exec_command result before dispatching the new sync-v5 build. Future dependent calls must use this explicit exit-code guard.',route_progress_claim=False),indent=2)+'\n',encoding='utf-8',newline='\n')
print('Preserved accidental old-byte retry and corrected dependent exit-code dispatch; no async-route or theorem credit from sync-v4.')
