from pathlib import Path
import json,hashlib
d=Path('runs/20261007-companion-priority/pbps-actual-physical-time-law81/integration81/static-svg')
r=json.loads((d/'render.json').read_bytes())
assert hashlib.sha256(Path(r['input']).read_bytes()).hexdigest()==r['input_sha256']
assert hashlib.sha256(Path(r['output']).read_bytes()).hexdigest()==r['output_sha256']
r.update(viewed_by_root=True,inspection='Actually viewed the rendered SVG with view_image. Shared canonical roots/technical leaves and legend readable; paper consumers intentionally excluded in this coarse arsenal view. IdealHalfTurnKernel exact dependencies belong to separately generated underlying graph.',page_visual_acceptance=False,interactive_branch_visual_pending=True)
(d/'viewed.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf8',newline='\n')
