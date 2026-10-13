from pathlib import Path
import hashlib,json,os,re,xml.etree.ElementTree as ET
r=Path('runs/20261007-companion-priority/pbps-actual-projected-rotation70');dest=r/'integration70/generated-whitespace';dest.mkdir(exist_ok=False)
sha=lambda b:hashlib.sha256(b).hexdigest();packet=json.loads((r/'final-reader-repository-packet70.json').read_bytes())
old={Path(z['path']).resolve():z for z in packet['inputs']}
paths=['docs/module-graph.svg','docs/assets/astis_lean_arsenal_module_graph.svg','research-wiki/sampling-sde-library/cards/AutoSamplingTheory.ExampleCases.ProximalBPS.ActualProjectedRotation.md']
def structure(e):
 text=e.text if e.text and e.text.strip() else None
 tail=e.tail if e.tail and e.tail.strip() else None
 return [e.tag,sorted(e.attrib.items()),text,tail,[structure(x) for x in e]]
rows=[]
for i,name in enumerate(paths):
 p=Path(name);before=p.read_bytes();assert sha(before)==old[p.resolve()]['RAW_sha256']
 after=re.sub(rb'(?m)[ \t]+(?=\r?$)',b'',before)
 changed=[j+1 for j,(x,y) in enumerate(zip(before.splitlines(),after.splitlines())) if x!=y]
 assert changed==([313] if p.suffix=='.svg' else [5,6])
 assert before.replace(b'\r\n',b'\n').count(b'\n')==after.replace(b'\r\n',b'\n').count(b'\n')
 if p.suffix=='.svg':assert structure(ET.fromstring(before))==structure(ET.fromstring(after))
 (dest/f'{i}.before.exactraw.snapshot').write_bytes(before);(dest/f'{i}.after.exactraw.snapshot').write_bytes(after)
 p.write_bytes(after)
 rows.append(dict(path=p.as_posix(),before_snapshot=(dest/f'{i}.before.exactraw.snapshot').as_posix(),before_RAW_bytes=len(before),before_RAW_sha256=sha(before),after_snapshot=(dest/f'{i}.after.exactraw.snapshot').as_posix(),after_RAW_bytes=len(after),after_RAW_sha256=sha(after),changed_lines=changed,only_ASCII_EOL_whitespace_removed=True))
assert sum(z['before_RAW_bytes']-z['after_RAW_bytes'] for z in rows)==6
other=[z for z in packet['inputs'] if Path(z['path']).resolve() not in old.keys()-set(old.keys()) and Path(z['path']).resolve() not in {Path(p).resolve() for p in paths}]
for z in other:assert sha(Path(z['path']).read_bytes())==z['RAW_sha256'],z['path']
(dest/'proposal.json').write_text(json.dumps(dict(status='THREE_GENERATED_READER_ASSETS_WHITESPACE_ONLY_NOT_NEW_MATHEMATICS',actual_root_PID=os.getpid(),rows=rows,total_ASCII_bytes_removed=6,original_CLOSED213_preserved=True,other_frozen_current_inputs_unchanged=len(other),original_review_packet_RAW_sha256=sha((r/'final-reader-repository-packet70.json').read_bytes()),independent_overlay_pending=True),indent=2)+'\n',encoding='utf8')
print('PASS exactly six ASCII trailing-space bytes/four lines/three generated assets; SVG structure and other137 frozen inputs unchanged.')
