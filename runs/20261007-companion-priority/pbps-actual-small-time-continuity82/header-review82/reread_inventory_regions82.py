from pathlib import Path
from html.parser import HTMLParser
import ast,json,hashlib,re,datetime
R=Path('E:/Samplinglib');O=R/'runs/20261007-companion-priority/pbps-actual-small-time-continuity82/header-review82';S=R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html';I=R/'runs/20261007-companion-priority/pbps-process-regularity-preread82/source_inventory82.json'
tree=ast.parse((O/'reread_primary82.py').read_text(encoding='utf8'));node=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='Parser');exec(compile(ast.Module(body=[node],type_ignores=[]),'own-parser-only82','exec'))
p=Parser();p.feed(S.read_text(encoding='utf8'));idx={n['id']:n for n in p.nodes};inventory=json.loads(I.read_text(encoding='utf8'));out=[]
for item in inventory['items']:
 assert item['source_id'] in idx,item['source_id']
 n=idx[item['source_id']];e=dict(inventory_id=item['id'],source_id=item['source_id'],primary_tag=n['tag'],own_direct_primary_text=n['text'],own_text_utf8_sha256=hashlib.sha256(n['text'].encode()).hexdigest());out.append(e);print(item['id'],item['source_id'],n['text'])
with (O/'independent-inventory-region-readback82.json').open('x',encoding='utf8',newline='\n') as f:json.dump(dict(status='ALL36_SOURCE_REGIONS_REREAD_DIRECTLY_FROM_PRIMARY',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),reviewer='/root/exact_verify77',source_RAW_sha256=hashlib.sha256(S.read_bytes()).hexdigest(),inventory_RAW_sha256=hashlib.sha256(I.read_bytes()).hexdigest(),regions=out,parser='Only own earlier stdlib Parser class reused; no extractor private freeze script/rationale/verdict read.'),f,ensure_ascii=False,indent=2);f.write('\n')
