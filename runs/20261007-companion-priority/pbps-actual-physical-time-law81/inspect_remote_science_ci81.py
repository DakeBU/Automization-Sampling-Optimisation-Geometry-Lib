from pathlib import Path
import subprocess,json,hashlib
r=Path('runs/20261007-companion-priority/pbps-actual-physical-time-law81')
p=subprocess.run(['gh','run','view','38057308993','--repo','DakeBU/Automization-Sampling-Optimisation-Geometry-Lib','--log-failed'],capture_output=True)
(r/'remote-science-ci81.stdout.log').write_bytes(p.stdout);(r/'remote-science-ci81.stderr.log').write_bytes(p.stderr)
assert p.returncode==0
lines=p.stdout.decode('utf8',errors='replace').splitlines()
hits=[(i,x) for i,x in enumerate(lines) if any(s in x.lower() for s in ['##[error]','error:','failed','exception','traceback'])]
for i,x in hits:
 print('\n'.join(lines[max(0,i-4):min(len(lines),i+7)]))
(r/'remote-science-ci81.observed.json').write_text(json.dumps(dict(run=38057308993,head='7f815975f0ac55a211af4a4ba8c446b0d7f69a9f',gh_log_exit=p.returncode,log_RAW_sha256=hashlib.sha256(p.stdout).hexdigest(),error_lines=hits,local_math_compile_is_separate=True),indent=2)+'\n',encoding='utf8',newline='\n')
