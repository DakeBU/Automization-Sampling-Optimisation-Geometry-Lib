from pathlib import Path
import json,hashlib
r=Path(__file__).parent;out=r/'integration82/static-svg'
x=json.loads((out/'render.json').read_bytes())
for p,h in [(x['input'],x['input_sha256']),(x['output'],x['output_sha256'])]:
    assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h
x.update(viewed_by_root=True,inspection='Actually viewed current raster through view_image. Shared root, local module labels, arrows and legend readable; coarse module-import view, not a claim of conceptual implication or paper completion. Precise actual82 branch separately generated and checked.',page_visual_acceptance=False,browser_used=False)
(out/'viewed.json').write_text(json.dumps(x,indent=2)+'\n',encoding='utf8',newline='\n')
print('Current affected SVG actually viewed and RAW-pinned; browser page visual pending')
