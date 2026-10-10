import subprocess,sys
py=sys.executable
def run(label,*args):
 subprocess.run([py,'-B','-X','utf8','.astis/pbps-harmonic73/foreground73.py','integration73/'+label,*args],check=True)
def script(label,file,*args):run(label,py,'-B','-X','utf8',file,*args)
stage=sys.argv[1]
if stage=='aggregate':
 subprocess.run([py,'-B','-X','utf8','.astis/pbps-harmonic73/foreground73.py','prepare-serialized-integration73',py,'-B','-X','utf8','.astis/pbps-harmonic73/integrate73.py'],check=True)
 script('bounded-gates','.astis/pbps-harmonic73/small-gates73.py')
 script('prepare-generated-scope','.astis/pbps-harmonic73/prepare-generated-scope73.py')
 script('mandatory-astis-check-final','tools/astis.py','check')
 script('python-compile','-m','py_compile','tools/astis.py')
 script('module-graph-refresh','tools/astis.py','module-graph-refresh')
 script('narrow-generated-scope','.astis/pbps-harmonic73/narrow-generated-scope73.py')
if stage=='generated-resume':
 script('narrow-generated-scope-diagnostic-recheck','.astis/pbps-harmonic73/narrow-generated-scope73.py')
if stage in ['aggregate','generated-resume']:
 script('regression-reuse','.astis/pbps-harmonic73/reuse-regression73.py')
 script('website-ci-build','website/scripts/build_site.py')
 script('official-graph-before-visual','website/scripts/underlying_lean_graph.py')
 node='C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe'
 run('reader-render-current',node,'.astis/pbps-harmonic73/inspect-cdp73.mjs')
 run('reader-copy-download',node,'.astis/pbps-harmonic73/inspect-copy73.mjs')
elif stage=='final':
 script('record-final-admin','.astis/pbps-harmonic73/record-integration73.py','admin')
 script('final-gates','.astis/pbps-harmonic73/final-gates73.py')
 script('record-final','.astis/pbps-harmonic73/record-integration73.py','final')
 script('pr-body','.astis/pbps-harmonic73/write-pr73.py')
 script('freeze-final-reader','.astis/pbps-harmonic73/freeze-final-reader73.py')
else:raise ValueError(stage)
