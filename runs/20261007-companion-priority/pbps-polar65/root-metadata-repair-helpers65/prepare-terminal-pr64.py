from pathlib import Path
import hashlib,json
r=Path('runs/20261007-companion-priority/pbps-centered-root64');src=r/'integration64/pr315-body64.md';b=src.read_text(encoding='utf-8');assert b.count('Remote CI must be checked on the integration commit.')==1
assert json.loads((r/'remote-ci64.accepted.json').read_bytes())['status']=='EXACT_INT64_REMOTE_ALL_SUCCESS'
b=b.replace('Remote CI must be checked on the integration commit.','Exact integration commit 0aef19ca2711159eeaec86d42c9be142a94fa402 has terminal SUCCESS for formalization, site and contributor workflows (including the push contributor check). Independent repository/reader admission accepts the bounded integration and preserves the explicit reader/metadata debt.')
p=r/'integration64/pr315-body64-terminal.md';assert not p.exists();p.write_text(b,encoding='utf-8',newline='\n')
(r/'integration64/pr315-body64-terminal.pin.json').write_text(json.dumps(dict(path=p.as_posix(),RAW_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),previous_source_body_preserved=src.as_posix(),scope='Current remote PR branch INT64 only; uncommitted65 results are not claimed by this PR body.'),indent=2)+'\n',encoding='utf-8',newline='\n')
print('Prepared exact INT64 terminal-CI PR body; original frozen body preserved.')
