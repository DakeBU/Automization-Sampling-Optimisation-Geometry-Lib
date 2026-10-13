import subprocess,sys
py=sys.executable
def run(label,*args):
 subprocess.run([py,'-B','-X','utf8','.astis/pbps-bounce74/foreground74.py','integration74/'+label,*args],check=True)
def script(label,file,*args):run(label,py,'-B','-X','utf8',file,*args)
stage=sys.argv[1]
if stage=='aggregate':
 subprocess.run([py,'-B','-X','utf8','.astis/pbps-bounce74/foreground74.py','prepare-serialized-integration74',py,'-B','-X','utf8','.astis/pbps-bounce74/integrate74.py'],check=True)
 script('bounded-gates','.astis/pbps-bounce74/small-gates74.py')
 script('prepare-generated-scope','.astis/pbps-bounce74/prepare-generated-scope74.py')
 script('mandatory-astis-check-final','tools/astis.py','check')
 script('python-compile','-m','py_compile','tools/astis.py')
 script('module-graph-refresh','tools/astis.py','module-graph-refresh')
 script('narrow-generated-scope','.astis/pbps-bounce74/narrow-generated-scope74.py')
if stage=='generated-resume':
 script('narrow-generated-scope-diagnostic-recheck','.astis/pbps-bounce74/narrow-generated-scope74.py')
if stage in ['aggregate','generated-resume']:
 script('regression-reuse','.astis/pbps-bounce74/reuse-regression74.py')
 script('website-ci-build','website/scripts/build_site.py')
 script('official-graph-before-visual','website/scripts/underlying_lean_graph.py')
 node='C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe'
 run('reader-render-current',node,'.astis/pbps-bounce74/inspect-cdp74.mjs')
 run('reader-copy-download',node,'.astis/pbps-bounce74/inspect-copy74.mjs')
elif stage=='final':
 script('record-final-admin','.astis/pbps-bounce74/record-integration74.py','admin')
 script('final-gates','.astis/pbps-bounce74/final-gates74.py')
 script('record-final','.astis/pbps-bounce74/record-integration74.py','final')
 script('pr-body','.astis/pbps-bounce74/write-pr74.py')
 script('freeze-final-reader','.astis/pbps-bounce74/freeze-final-reader74.py')
else:raise ValueError(stage)
