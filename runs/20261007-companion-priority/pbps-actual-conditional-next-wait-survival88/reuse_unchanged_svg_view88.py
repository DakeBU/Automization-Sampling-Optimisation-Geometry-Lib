from pathlib import Path
import json,hashlib
r=Path(__file__).parent;old=r.parent/'pbps-actual-finite-history-tail-law87/integration87/static-svg/viewed.json'
x=json.loads(old.read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
assert x['viewed_by_root'] and sha(Path(x['input']).read_bytes())==x['input_sha256']
assert sha(Path(x['output']).read_bytes())==x['output_sha256']
out=r/'integration88/static-svg';out.mkdir(exist_ok=False)
p=out/'viewed-or-reused.json'
p.write_text(json.dumps(dict(status='UNCHANGED_RAW_SVG_PREVIOUS_ACTUAL_VIEW_REUSED',input=x['input'],input_RAW_sha256=x['input_sha256'],previous_actual_view=old.as_posix(),previous_evidence_RAW_sha256=sha(old.read_bytes()),unchanged_current_SVG=True,paper_consumer_branch_included=False,page_visual_acceptance=False,fine_branch_visual_acceptance=False,reason='Existing shared-root module overview excludes paper consumers. Its exact unchanged SVG and actual-view evidence are reused; new paper fine graph and page remain visually pending.'),indent=2)+'\n',encoding='utf8',newline='\n')
print('Unchanged shared SVG actual-view audit reused; new paper page/fine graph remains pending.')
