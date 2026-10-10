import subprocess,sys
py=sys.executable
def run(label,*args):subprocess.run([py,'-B','-X','utf8','.astis/pbps-recursion76/foreground76.py','integration76/'+label,*args],check=True)
def script(label,file,*args):run(label,py,'-B','-X','utf8',file,*args)
stage=sys.argv[1]
if stage=='aggregate':
 subprocess.run([py,'-B','-X','utf8','.astis/pbps-recursion76/foreground76.py','prepare-serialized-integration76',py,'-B','-X','utf8','.astis/pbps-recursion76/integrate76.py'],check=True)
 script('bounded-gates','.astis/pbps-recursion76/small-gates76.py')
 script('prepare-generated-scope','.astis/pbps-recursion76/prepare-generated-scope76.py')
 script('mandatory-astis-check-final','tools/astis.py','check')
 script('python-compile','-m','py_compile','tools/astis.py')
 script('affected-module-graph','.astis/pbps-recursion76/refresh-affected-module-graph76.py')
 script('regression-reuse','.astis/pbps-recursion76/reuse-regression76.py')
 script('website-ci-build','website/scripts/build_site.py')
 script('official-graph-before-visual','website/scripts/underlying_lean_graph.py')
 node='C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe'
 run('reader-render-current',node,'.astis/pbps-recursion76/inspect-cdp76.mjs')
 run('reader-copy-download',node,'.astis/pbps-recursion76/inspect-copy76.mjs')
elif stage=='final':
 script('record-final-admin','.astis/pbps-recursion76/record-integration76.py','admin')
 script('final-gates','.astis/pbps-recursion76/final-gates76.py')
 script('record-final','.astis/pbps-recursion76/record-integration76.py','final')
 script('pr-body','.astis/pbps-recursion76/write-pr76.py')
 script('freeze-final-reader','.astis/pbps-recursion76/freeze-final-reader76.py')
else:raise ValueError(stage)
