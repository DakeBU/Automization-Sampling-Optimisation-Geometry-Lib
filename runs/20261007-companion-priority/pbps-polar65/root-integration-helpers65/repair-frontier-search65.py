from pathlib import Path
import json,hashlib,sys,subprocess
root=Path.cwd();sys.path.insert(0,str(root/'tools'));import astis_publication as pub
r=root/'runs/20261007-companion-priority/pbps-polar65';d=r/'exact-science-verification';lease=json.loads((d/'lease.final.json').read_bytes())
assert lease['status']=='CLOSED_LAST'
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()=='dad6e38c9beed3476cb5d1db06eb57b955c8e3eb'
p=root/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-polar-isometry.json';old=p.read_bytes();x=json.loads(old);before=json.loads(old)
pub.inputs.cache_clear();pub.load.cache_clear();item=next(i for i in pub.load() if i['id']=='pbps-actual-polar-isometry');binding=item['bindings'][0];b0=pub.binding_digest(item,binding);c0=pub.digest(pub.review_context(item,binding))
assert len(x['reuse_plan']['searched_existing'])==1 and 'samplinglib' not in x['reuse_plan']['searched_existing'][0].lower()
x['reuse_plan']['searched_existing'][0]='Samplinglib: '+x['reuse_plan']['searched_existing'][0]
out=r/'frontier-search-repair65';out.mkdir(exist_ok=False);(out/'cell.before.exactraw.snapshot.json').write_bytes(old)
nl=b'\r\n' if b'\r\n' in old else b'\n';p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode().replace(b'\n',nl))
pub.inputs.cache_clear();pub.load.cache_clear();assert pub.binding_digest(item,binding)==b0 and pub.digest(pub.review_context(item,binding))==c0
check=json.loads(p.read_bytes());check['reuse_plan']['searched_existing'][0]=before['reuse_plan']['searched_existing'][0];assert check==before
row=dict(status='PROCESS_ONLY_RETRIEVAL_LIBRARY_LABEL_CORRECTED',failed_exact_commit='dad6e38c9beed3476cb5d1db06eb57b955c8e3eb',failed_gate='astis_frontier_cells.py check: schema-2 cells must search samplinglib',changed_field='reuse_plan.searched_existing[0]',change='Prefix existing recorded actual64/PolarIsometry Samplinglib reuse search with its explicit library name.',before_RAW_sha256=hashlib.sha256(old).hexdigest(),after_RAW_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),publication_binding_sha256=b0,publication_review_context_sha256=c0,publication_binding_and_context_unchanged=True,Lean_source_lesson_audit_changed=False,mathematical_repair=False,VERIFIED=False,remaining='Fresh frontier PASS and new exact SCI65b independent verification required; dad6e38 is not VERIFIED.')
(out/'diagnosis.json').write_text(json.dumps(row,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Corrected one process-only Samplinglib retrieval label; exact publication binding/context and all mathematics unchanged. New commit verification required.')
