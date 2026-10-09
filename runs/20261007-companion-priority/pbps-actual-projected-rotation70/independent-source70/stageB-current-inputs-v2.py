import sys
sys.dont_write_bytecode=True
from pathlib import Path
# Preserve the failed helper unchanged. Correct only its two reader-script paths
# and permit reuse of already captured snapshots after asserting exact equality.
source=(Path(__file__).resolve().parent/'stageB-current-inputs.py').read_text(encoding='utf-8')
source=source.replace("E:/Samplinglib/tools/inline_lean.py", "E:/Samplinglib/website/scripts/inline_lean.py")
source=source.replace("E:/Samplinglib/tools/check_cross_domain_browser.py", "E:/Samplinglib/website/scripts/check_cross_domain_browser.py")
source=source.replace("p=O/name;assert not p.exists();p.write_bytes(raw);(O/(name+'.LF')).write_bytes(lf)", "p=O/name\n if p.exists():\n  assert p.read_bytes()==raw and (O/(name+'.LF')).read_bytes()==lf\n else:\n  p.write_bytes(raw);(O/(name+'.LF')).write_bytes(lf)")
exec(compile(source,'stageB-current-inputs-v2-derived-from-retained-v1','exec'))
