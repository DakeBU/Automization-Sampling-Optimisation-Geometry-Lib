import subprocess,sys
py=sys.executable
def run(label,*args):subprocess.run([py,'-B','-X','utf8','.astis/pbps-clock75/foreground75.py','integration75/'+label,*args],check=True)
def script(label,file,*args):run(label,py,'-B','-X','utf8',file,*args)
stage=sys.argv[1]
if stage=='aggregate':
 subprocess.run([py,'-B','-X','utf8','.astis/pbps-clock75/foreground75.py','prepare-serialized-integration75',py,'-B','-X','utf8','.astis/pbps-clock75/integrate75.py'],check=True)
 script('bounded-gates','.astis/pbps-clock75/small-gates75.py')
 script('prepare-generated-scope','.astis/pbps-clock75/prepare-generated-scope75.py')
 script('mandatory-astis-check-final','tools/astis.py','check')
 script('python-compile','-m','py_compile','tools/astis.py')
 script('affected-module-graph','.astis/pbps-clock75/refresh-affected-module-graph75.py')
 script('regression-reuse','.astis/pbps-clock75/reuse-regression75.py')
 script('website-ci-build','website/scripts/build_site.py')
 script('official-graph-before-visual','website/scripts/underlying_lean_graph.py')
 node='C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe'
 run('reader-render-current',node,'.astis/pbps-clock75/inspect-cdp75.mjs')
 run('reader-copy-download',node,'.astis/pbps-clock75/inspect-copy75.mjs')
elif stage=='final':
 script('record-final-admin','.astis/pbps-clock75/record-integration75.py','admin')
 script('final-gates','.astis/pbps-clock75/final-gates75.py')
 script('record-final','.astis/pbps-clock75/record-integration75.py','final')
 script('pr-body','.astis/pbps-clock75/write-pr75.py')
 script('freeze-final-reader','.astis/pbps-clock75/freeze-final-reader75.py')
else:raise ValueError(stage)
