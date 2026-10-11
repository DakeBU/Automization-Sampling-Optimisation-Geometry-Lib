from pathlib import Path
import hashlib,json,datetime
R=Path('E:/Samplinglib');D=R/'runs/20261007-companion-priority/pbps-actual-prescribed-path-density94/independent-whole-math94/exposition94'
def sha(b):return hashlib.sha256(b).hexdigest()
def info(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=sha(b),bytes=len(b))
def write(n,b):
 p=D/n;assert not p.exists();p.write_bytes(b);return p
freeze=R/'runs/20261007-companion-priority/pbps-actual-prescribed-path-density94/publication-freeze94.json'
pub=R/'website/content/publications/pbps-actual-prescribed-path-density.json'
lesson=R/'website/content/declaration_lessons/pbps-actual-prescribed-path-density.json'
prod=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPrescribedPathDensity.lean'
inputs=[info(p) for p in [pub,lesson,prod,freeze]]
for p in [pub,lesson,freeze]:write(('publication' if p==pub else 'lesson' if p==lesson else 'freeze')+'.initial.exactraw.json',p.read_bytes())
u=json.loads(lesson.read_bytes())['units'][0];p=json.loads(pub.read_bytes())['items'][0]
assert u['statement']==u['lean_statement']==p['statement']
assert u['assumptions']==p['assumptions']
lines=prod.read_bytes().splitlines(keepends=True);rows=[]
for i,s in enumerate(u['steps'],1):
 r=s['lean_source_region'];raw=b''.join(lines[r['start_line']-1:r['end_line']]);code=s['lean'].encode()
 assert r['source_raw_sha256']==sha(prod.read_bytes())
 assert r['exact_code_raw_sha256']==sha(code)
 assert raw.decode().replace('\r\n','\n')==s['lean']
 rows.append(dict(step=i,title=s['title'],start_line=r['start_line'],end_line=r['end_line'],source_raw_sha256=sha(prod.read_bytes()),physical_region_raw_sha256=sha(raw),embedded_code_utf8_sha256=sha(code),embedded_equals_source_after_CRLF_to_LF=True,embedded_is_physical_raw_bytes=(raw==code)))
report=dict(kind='EXPOSITION_INITIAL_REGION_CHECK',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),inputs=inputs,regions=rows,statement_and_assumptions_consistent=True,normalization_disclosure='Embedded JSON code uses LF while physical source uses CRLF; exact_code_raw_sha256 hashes embedded code UTF8, not physical CRLF slice. Each entire source RAW and physical region RAW independently pinned here.')
write('initial-region-check94.native.json',(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps(report,ensure_ascii=False,indent=2))
