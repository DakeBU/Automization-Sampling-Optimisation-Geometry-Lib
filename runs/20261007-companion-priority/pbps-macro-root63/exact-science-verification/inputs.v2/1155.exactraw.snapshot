import hashlib,json,os,subprocess,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
p=subprocess.run([sys.executable,'-X','utf8',str(OUT/'finalize63.py')],capture_output=True)
(OUT/'finalizer.stdout.txt').write_bytes(p.stdout)
(OUT/'finalizer.stderr.txt').write_bytes(p.stderr)
(OUT/'finalizer.process.receipt.json').write_bytes((json.dumps({'foreground_capture_pid':os.getpid(),'command':[sys.executable,'-X','utf8',str(OUT/'finalize63.py')],'actual_exit_code':p.returncode,'stdout_RAW_sha256':hashlib.sha256(p.stdout).hexdigest(),'stderr_RAW_sha256':hashlib.sha256(p.stderr).hexdigest(),'background':False},indent=2)+'\n').encode('utf-8'))
sys.stdout.buffer.write(p.stdout);sys.stderr.buffer.write(p.stderr)
sys.exit(p.returncode)
