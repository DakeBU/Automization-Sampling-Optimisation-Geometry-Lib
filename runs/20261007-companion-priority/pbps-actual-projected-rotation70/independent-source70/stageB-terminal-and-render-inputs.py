import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,os
O=pathlib.Path(__file__).resolve().parent;R=O.parent;ROOT=pathlib.Path('E:/Samplinglib')
H=lambda b:hashlib.sha256(b).hexdigest()
paths=[(R/'focused-canonical-v2/receipt.json','root70.focused-canonical-v2.receipt.exactraw.json'),(R/'focused-canonical-v2/stdout.log','root70.focused-canonical-v2.stdout.exactraw.log'),(R/'focused-canonical-v2/stderr.log','root70.focused-canonical-v2.stderr.exactraw.log'),(ROOT/'tools/astis_source.py','reader.astis_source.exactraw.py'),(ROOT/'website/scripts/source_lineage.py','reader.source_lineage.exactraw.py'),(ROOT/'lean-toolchain','current70.lean-toolchain.exactraw.txt'),(ROOT/'lake-manifest.json','current70.lake-manifest.exactraw.json')]
out=[]
for p,n in paths:
 b=p.read_bytes();l=b.replace(b'\r\n',b'\n');assert not (O/n).exists();(O/n).write_bytes(b);(O/(n+'.LF')).write_bytes(l)
 out.append({'original_path':str(p),'snapshot':n,'RAW_bytes':len(b),'RAW_sha256':H(b),'LF_snapshot':n+'.LF','LF_bytes':len(l),'LF_sha256':H(l),'LF_recipe':'replace ONLY CRLF bytes with LF','original_mtime_ns':p.stat().st_mtime_ns})
r=json.loads((O/'root70.focused-canonical-v2.receipt.exactraw.json').read_bytes())
assert r['actual_foreground_PID']==9524 and r['exit_code']==0 and r['terminal_closed']
for k in ('stdout','stderr'):
 b=(O/('root70.focused-canonical-v2.'+k+'.exactraw.log')).read_bytes();assert H(b)==r[k]['RAW_sha256'] and len(b)==r[k]['RAW_bytes']
assert b'Build completed successfully (3949 jobs)' in (O/'root70.focused-canonical-v2.stdout.exactraw.log').read_bytes()
result={'schema':'source70-actual-terminal-and-scoped-render-inputs-v1','actual_pid':os.getpid(),'inputs':out,'input_count':len(out),'owner_focused_PID':9524,'owner_focused_EXIT':0,'jobs':3949,'compile_by_source_reviewer':False,'independent_math_verdict_read':False}
(O/'stageB.terminal-and-render-input-manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');print(json.dumps(result,ensure_ascii=False))
