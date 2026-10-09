import json,hashlib
from pathlib import Path
R=Path('E:/Samplinglib')
for slug in ['hilbert-sharp-quadratic-corrector-bound','pbps-sharp-corrector-energy']:
 x=json.loads((R/f'website/content/declaration_lessons/{slug}.json').read_text(encoding='utf-8'))
 for i,s in enumerate(x['units'][0]['steps']):
  q=s['lean_source_region'];raw=(R/q['path']).read_bytes();lines=raw.splitlines(keepends=True);span=b''.join(lines[q['start_line']-1:q['end_line']]);code=s['lean'].encode();print(json.dumps(dict(slug=slug,step=i+1,span_bytes=len(span),code_bytes=len(code),span_sha=hashlib.sha256(span).hexdigest(),code_sha=hashlib.sha256(code).hexdigest(),raw_literal_equal=span==code,code_digest_matches=hashlib.sha256(code).hexdigest()==q['exact_code_raw_sha256'],only_trailing_empty_LF_delta=span.rstrip(b'\n')==code.rstrip(b'\n'),smallest_literal_end_line=q['end_line']-(len(span)-len(code)) if span==code+b'\n' else q['end_line']),ensure_ascii=False))
