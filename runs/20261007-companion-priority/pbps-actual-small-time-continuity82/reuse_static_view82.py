from pathlib import Path
import hashlib,json
r=Path(__file__).parent;out=r/'integration82/static-svg';out.mkdir(exist_ok=False)
prior=Path('runs/20261007-companion-priority/pbps-actual-physical-time-law81/integration81/static-svg/viewed.json')
x=json.loads(prior.read_bytes());assert x['viewed_by_root']
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(x['input'])==x['input_sha256'],'Changed SVG requires a fresh raster and actual view, cannot reuse.'
assert sha(x['output'])==x['output_sha256']
x.update(status='REUSED_UNCHANGED_ACTUALLY_VIEWED_STATIC_SVG',reuse_evidence=dict(path=prior.as_posix(),RAW_sha256=sha(prior)),reuse_reason='Current SVG byte-identical to previously actually viewed shared-root SVG; new precise actual-process dependency node is separately generated, graph-checked and not visually certified by this reuse.')
(out/'viewed.json').write_text(json.dumps(x,indent=2)+'\n',encoding='utf8',newline='\n')
print('Exact unchanged static SVG view reused; actual page/interactive new branch remains pending')
