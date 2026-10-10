from pathlib import Path
import hashlib,json
r=Path(__file__).parent;out=r/'integration89/static-svg'
source=Path('docs/module-graph.svg');png=out/'module-graph.png';sha=lambda b:hashlib.sha256(b).hexdigest()
p=out/'viewed-or-reused.json';assert not p.exists()
p.write_text(json.dumps(dict(status='CURRENT_CHANGED_SHARED_SVG_ACTUALLY_VIEWED',input=source.as_posix(),input_RAW_sha256=sha(source.read_bytes()),output=png.as_posix(),output_RAW_sha256=sha(png.read_bytes()),renderer='bundled sharp/libvips',viewed_by_root=True,inspection='Root viewed actual current1780x980 raster through view_image: labels, shared-root boxes, arrows and legend readable, no clipping. Shared overview excludes paper consumers; no fine consumer branch/page visual credit.',page_visual_acceptance=False,fine_branch_visual_acceptance=False,browser_used=False),indent=2)+'\n',encoding='utf8',newline='\n')
