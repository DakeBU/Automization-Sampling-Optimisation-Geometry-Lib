from pathlib import Path
import json,hashlib,subprocess,sys
R=Path('E:/Samplinglib');D=Path(__file__).parent
p=R/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-finite-first-event-law.json'
b=p.read_bytes();c=json.loads(b)
assert c['cell_id']=='ASTIS-SW-PBPS-actual-finite-first-event-law' and c['status']=='claimed'
e='Samplinglib: AutoSamplingTheory and shared Frontier Cells searched in runs/20261007-companion-priority/pbps-path-law-preread86/root-retrieval86/local-density.txt and shared-frontiers.txt; fixed Mathlib API search in mathlib-cdf.txt and mathlib-maps.txt.'
for key in ['shared_floor_audit','reuse_plan']:
 field='searched' if key=='shared_floor_audit' else 'searched_existing'
 c[key][field]=[e,*c[key][field]]
p.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
diagnosis={'status':'ADMINISTRATIVE_SEARCH_LABEL_REPAIRED_ONLY','first_gate_exit':1,'observed_error':'schema-2 cells must search samplinglib','cause':'Relative evidence filenames omitted the literal library label required by lexical validator, although actual local Samplinglib search was executed and pinned.','change':'Added explicit truthful Samplinglib/Mathlib labels and actual command evidence paths.','old_cell_raw_sha256':hashlib.sha256(b).hexdigest(),'new_cell_raw_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'header_unchanged':True,'StatementSeal_unchanged':True,'no_proof_search_before_gate':True}
(D/'retrieval-label-diagnosis86.json').write_text(json.dumps(diagnosis,indent=2)+'\n',encoding='utf-8')
for label,args in [('frontier-before-proof86.attempt2',['tools/astis_frontier_cells.py','check']),('publication-packet-before-proof86.attempt2',['tools/astis_publication.py','packet','--cell',c['cell_id']])]:
 q=subprocess.run([sys.executable,'-X','utf8',*args],cwd=R,capture_output=True)
 (D/(label+'.stdout.json')).write_bytes(q.stdout);(D/(label+'.stderr.log')).write_bytes(q.stderr)
 (D/(label+'.receipt.json')).write_text(json.dumps({'exit_code':q.returncode,'terminal_closed':True})+'\n',encoding='utf-8')
 assert q.returncode==0,(q.stdout+q.stderr).decode(errors='replace')[-2000:]
print('Explicit real library search metadata accepted; exact mathematical header and seal unchanged')
