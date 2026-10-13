import json,hashlib,difflib
from pathlib import Path
R=Path('E:/Samplinglib');x=json.loads((R/'website/content/declaration_lessons/pbps-sharp-corrector-energy.json').read_text(encoding='utf-8'));s=x['units'][0]['steps'][4];q=s['lean_source_region'];raw=(R/q['path']).read_bytes();span=b''.join(raw.splitlines(keepends=True)[q['start_line']-1:q['end_line']]);code=s['lean'].encode()
print(json.dumps(dict(expected_region=q,whole_sha=hashlib.sha256(raw).hexdigest(),span_sha=hashlib.sha256(span).hexdigest(),code_sha=hashlib.sha256(code).hexdigest(),span_bytes=len(span),code_bytes=len(code),span_tail=repr(span[-200:]),code_tail=repr(code[-200:])),ensure_ascii=False,indent=2))
print(''.join(difflib.unified_diff(code.decode().splitlines(keepends=True),span.decode().splitlines(keepends=True),fromfile='lesson-step5',tofile='literal-span')))
