from common import *
import gzip
m=J(R/'integration62/generated-context-preservation-data/manifest.json');assert len(m['preserved_canonical_metadata'])==67 and len(m['emitted_snapshots'])==88 and len(m['new_actual_modules'])==2
tree=J(P/'integration.tree.index.json')['files'];old=subprocess.check_output(['git','ls-tree','-r',SCI],cwd=ROOT).decode().splitlines();old={s.split('\t',1)[1]:s.split()[2] for s in old};rows=[]
for q in m['preserved_canonical_metadata']:
 p=q['canonical_card'];assert tree[p]==old[p];assert pin(p)['raw_sha256']==q['card_raw_sha256'];rows.append(pin(p))
restored=0
for q in m['emitted_snapshots']:
 raw=gzip.decompress(path(q['emitted_snapshot']).read_bytes());assert H(raw)==q['emitted_raw_sha256'];rows.append(pin(q['emitted_snapshot']))
 if q['action'].startswith('restored'):
  restored+=1;assert tree[q['path']]==old[q['path']];rows.append(pin(q['path']))
assert restored==84
newcards=[p for p in tree if p.startswith('research-wiki/sampling-sde-library/cards/') and tree.get(p)!=old.get(p)];assert len(newcards)==2
for p in newcards:rows.append(pin(p));assert 'joint GammaP/ontoM/typed B*B' in path(p).read_text(encoding='utf8')
controls=[]
for name in ['preserve-generated-context-v2','cache-pure-generated-cards']:
 p=R/'integration62'/name/'receipt.json';q=J(p);assert q['exit_code']==0 and q['terminal_closed'];controls.append(dict(receipt=pin(p),actual_PID=q['actual_foreground_pid'],exit_code=0));rows.extend([pin(p),q['stdout'],q['stderr']])
tracked=J(R/'integration62/tracked-whitespace/diagnosis.json');assert tracked['full_tracked_exit']==0 and tracked['full_tracked_called_PASS'];rows.append(pin(R/'integration62/tracked-whitespace/diagnosis.json'))
index=J(P/'integration.tree.index.json');production_subdirectory=index['production_module_count'];tests_subdirectory=sum(s.startswith('Tests/') and s.endswith('.lean') for s in tree)
assert production_subdirectory==514 and tests_subdirectory==415
W(P/'preservation.check.json',dict(status='PASS',preserved_canonical_cards=67,restored_unrelated_exact_Git_paths=84,new_enriched_cards=newcards,generator_controls=controls,tracked_whitespace_PASS=True,staged_whitespace_PASS=False,inventory_contract=dict(production_subdirectory=514,production_root_file=1,total_production_modules=515,Tests_subdirectory=415,Tests_root_file=1,total_Lean_modules=931,native_graph_source_paths_including_lake_pins=934),clarification='Opening index production_module_count counts directory leaves only; root515 inventory includes AutoSamplingTheory.lean. Graph509 registry_declarations is generated scan count, not compiled formalizedTechnicalLemmaCount507. No numerical substitution or extra theorem credit.',actual_pin_rows=rows))
print('PRESERVATION62_PASS67/84/2;514+root=515production;trackedPASS/stagedNEGATIVE')
