from pathlib import Path
import os, subprocess, sys
runtime=Path('.astis/browser-runtime70').resolve();assert (runtime/'playwright').is_dir()
env=dict(os.environ);env['PYTHONPATH']=str(runtime)+os.pathsep+env.get('PYTHONPATH','')
cmd=[sys.executable,'-X','utf8','website/scripts/check_cross_domain_browser.py','--browser-channel','chrome','--evidence','.astis/pbps-perturbation72/browser-full-current']
print('Task-local Playwright1.57.0 with installed Chrome, isolated owned headless profile; online MathJax; no global environment change.',flush=True)
child=subprocess.Popen(cmd,env=env);print('actual browser-check Python PID',child.pid,flush=True);code=child.wait();print('browser-check EXIT',code,flush=True);sys.exit(code)
