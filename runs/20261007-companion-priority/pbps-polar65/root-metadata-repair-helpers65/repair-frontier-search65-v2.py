from pathlib import Path
import hashlib,json,sys
root=Path.cwd();sys.path.insert(0,str(root/'tools'));import astis_publication as pub
r=root/'runs/20261007-companion-priority/pbps-polar65';assert (r/'root.exact65-blocker.adoption.json').exists()
p=root/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-polar-isometry.json';raw=p.read_bytes();x=json.loads(raw);before=json.loads(raw)
assert x['reuse_plan']['searched_existing'][0].startswith('Samplinglib: ')
assert 'samplinglib' not in x['shared_floor_audit']['searched'][0].lower()
pub.inputs.cache_clear();pub.load.cache_clear();item=next(i for i in pub.load() if i['id']=='pbps-actual-polar-isometry');binding=item['bindings'][0];b0=pub.binding_digest(item,binding);c0=pub.digest(pub.review_context(item,binding))
x['shared_floor_audit']['searched'][0]='Samplinglib: '+x['shared_floor_audit']['searched'][0]
assert x['shared_floor_audit']['searched']==x['reuse_plan']['searched_existing']
out=r/'frontier-search-repair65-v2';out.mkdir(exist_ok=False);(out/'cell.before.exactraw.snapshot.json').write_bytes(raw)
nl=b'\r\n' if b'\r\n' in raw else b'\n';p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode().replace(b'\n',nl))
pub.inputs.cache_clear();pub.load.cache_clear();assert pub.binding_digest(item,binding)==b0 and pub.digest(pub.review_context(item,binding))==c0
again=json.loads(p.read_bytes());again['shared_floor_audit']['searched']=before['shared_floor_audit']['searched'];assert again==before
row=dict(status='PROCESS_ONLY_CANONICAL_RETRIEVAL_LABEL_CORRECTED',previous_failed_root_gate='frontier-repair-gate65/receipt.json',failure_diagnosis='Native suggested reuse_plan field is a duplicate; exact validator actually reads shared_floor_audit.searched. Both existing descriptions now consistently identify Samplinglib.',exact_validator='tools/astis_frontier_cells.py:156-163 and 191-195',changed_field='shared_floor_audit.searched[0]',source_mathematical_repair=False,publication_binding_sha256=b0,publication_context_sha256=c0,publication_binding_and_context_unchanged=True,before_RAW_sha256=hashlib.sha256(raw).hexdigest(),after_RAW_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),VERIFIED=False)
(out/'diagnosis.json').write_text(json.dumps(row,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Corrected canonical shared_floor_audit search label and kept duplicate reuse plan consistent; exact mathematics/binding/context unchanged. Fresh required frontier gate follows.')
