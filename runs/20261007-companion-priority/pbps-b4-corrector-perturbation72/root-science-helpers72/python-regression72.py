from pathlib import Path
import re, subprocess, sys
text=Path('.github/workflows/blueprint-site.yml').read_text(encoding='utf8')
section=text.split('python3 -m unittest \\',1)[1].split('node --check',1)[0]
modules=re.findall(r'tools\.tests\.\w+',section)
assert len(modules)==20 and len(set(modules))==20
print('Fresh complete CI Python suite:',len(modules),'modules',flush=True)
subprocess.run([sys.executable,'-X','utf8','-m','unittest',*modules],check=True)
node='C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe'
for name in re.findall(r'node --check (website/static/[^\s]+)',text):
 subprocess.run([node,'--check',name],check=True)
print('PASS full Python CI suite and six JavaScript syntax checks',flush=True)
