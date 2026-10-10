from pathlib import Path
import json,hashlib
r=Path(__file__).parent;out=r/'integration87/static-svg';x=json.loads((out/'render.json').read_bytes())
for p,h in [(x['input'],x['input_sha256']),(x['output'],x['output_sha256'])]:assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h
x.update(viewed_by_root=True,inspection='Actually viewed the current SVG raster with view_image. Coarse shared-root module-import view: readable labels, arrows and legend. Paper consumer modules are explicitly excluded, so ActualFiniteHistoryTailLaw87 is NOT claimed visible in this coarse SVG. Its fine reference graph and actual audited kernel closure remain separate evidence.',new_paper_branch_visually_inspected=False,page_visual_acceptance=False,browser_used=False)
p=out/'viewed.json';assert not p.exists();p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf8',newline='\n');print('Coarse SVG actually viewed; exact consumer branch/browser visual remains pending.')
