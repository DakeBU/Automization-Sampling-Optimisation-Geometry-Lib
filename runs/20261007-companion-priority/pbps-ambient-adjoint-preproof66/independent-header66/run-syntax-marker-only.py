import subprocess,json,datetime,os,hashlib
from pathlib import Path
O=Path(__file__).parent
H=lambda b:hashlib.sha256(b).hexdigest()
for label in ['main','test']:
 p=O/('syntax-'+label+'-marker-only.lean');start=datetime.datetime.now(datetime.timezone.utc).isoformat();proc=subprocess.Popen(['lake','env','lean',str(p)],cwd='E:/Samplinglib',stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=proc.communicate();(O/('syntax-'+label+'.stdout.log')).write_bytes(out);(O/('syntax-'+label+'.stderr.log')).write_bytes(err)
 d=dict(schema='header66-owned-TYPE-only-syntax-terminal-v1',actual_foreground_pid=proc.pid,actual_exit_code=proc.returncode,terminal_closed=True,started_utc=start,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),command=['lake','env','lean',str(p)],candidate_RAW_sha256=H(p.read_bytes()),stdout_RAW_sha256=H(out),stderr_RAW_sha256=H(err),header_changed=False,only_intentional_BODY_error_marker_changed=True,proof_credit=False,observer_pid=os.getpid());(O/('syntax-'+label+'.receipt.json')).write_bytes((json.dumps(d,sort_keys=True,indent=2)+'\n').encode());print(json.dumps(d,sort_keys=True),flush=True);print(out.decode('utf-8')[:5000],flush=True)
