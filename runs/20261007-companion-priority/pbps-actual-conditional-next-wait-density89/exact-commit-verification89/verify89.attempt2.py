import json,hashlib
from pathlib import Path
O=Path(__file__).parent;p=O/'verify89.py'
negative={'status':'VERIFIER_RUNTIME_BINDING_CLASSIFICATION_ERROR_BEFORE_GATES','terminal_tool_chunk':'b1f29a','exit_code':1,'original_script_RAW_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'cause':'Historical complete header manifest includes pinned local lake.exe, which is intentionally not a repository Git blob. Runtime binary was RAW-validated before the mistaken Git-binding demand.','correction':'Classify only the two explicitly pinned local Lean4.33 binaries as local runtime evidence, retain exact historical RAW check, and independently record runtime version output. No source/proof/metadata target changes.'}
with (O/'verifier-runtime-classification89.negative.json').open('x',encoding='utf8',newline='\n') as f:json.dump(negative,f,indent=2);f.write('\n')
s=p.read_text('utf8');old=" if r.startswith('.lake/packages/mathlib/'):"
new=" if r in ['.astis/toolchain/lean-4.33.0-windows/bin/lake.exe','.astis/toolchain/lean-4.33.0-windows/bin/lean.exe']:\n  version=subprocess.check_output([str(p),'--version'],cwd=R).decode().strip();assert '4.33.0' in version,version\n  local[r]=dict(**info(p),binding='Pinned local Lean4.33 runtime binary; exact historical RAW checked, not repository source content.',version=version);return\n if r.startswith('.lake/packages/mathlib/'):"
assert s.count(old)==1
exec(compile(s.replace(old,new,1),str(p),'exec'),{'__file__':str(p),'__name__':'__main__'})
