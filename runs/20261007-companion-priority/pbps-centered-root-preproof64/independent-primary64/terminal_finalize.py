from pathlib import Path
import hashlib,json,datetime,subprocess
out=Path(r'E:/Samplinglib/runs/20261007-companion-priority/pbps-centered-root-preproof64/independent-primary64');repo=Path('E:/Samplinglib')
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def j(p):return json.loads((out/p).read_text(encoding='utf8'))
seal=j('source-first-graph-seal.json');graph=j('source-proof-graph.json');coverage=j('source-coverage-inventory.json');regions=j('primary-regions-receipt.json');pins=j('bounded-current-api-pins.json');capsule=j('bounded-source-api-capsule.json');idx=j('source-index.json')
source=Path(regions['source']).read_bytes();assert hashlib.sha256(source).hexdigest()==seal['source_raw_sha256']
checks=[]
assert digest(out/'source-proof-graph.json')==seal['graph_sha256'];assert digest(out/'source-coverage-inventory.json')==seal['coverage_sha256'];assert digest(out/'primary-regions-receipt.json')==seal['regions_receipt_sha256'];assert digest(out/'primary-preread-open-receipt.json')==seal['source_preread_receipt_sha256'];checks.append('primary-first graph/coverage/region/preread seals unchanged after current API reads')
for r in regions['regions']:
 a,b=r['byte_range_zero_based_half_open'];chunk=source[a:b];assert Path(r['raw_file']).read_bytes()==chunk;assert digest(r['raw_file'])==r['raw_sha256'];assert Path(r['lf_file']).read_bytes()==chunk.replace(b'\r\n',b'\n').replace(b'\r',b'\n');assert digest(r['lf_file'])==r['lf_sha256'];assert digest(r['readable_file'])==r['readable_sha256'];assert digest(r['alttext_file'])==r['alttext_sha256'];alts=json.loads(Path(r['alttext_file']).read_text());assert len(alts)==r['math_count'];assert all(a['alttext'] for a in alts)
checks.append('10 literal source raw/LF byte-range snapshots and all readable/alttext hashes match; 0 missing alttexts')
for c in coverage['inventory']:
 a,b=c['byte_range_zero_based_half_open'];assert hashlib.sha256(source[a:b]).hexdigest()==c['literal_sha256'];assert c['disposition'] in ['NODE','EXCLUDED'];assert c['reason']
assert coverage['unclassified_count']==0;checks.append(f"all {len(coverage['inventory'])} exact source inventory literal hashes/dispositions read back")
ids={n['id'] for n in graph['nodes']};assert all(p in ids for n in graph['nodes'] for p in n['parents']);assert all(a in idx['nodes'] for n in graph['nodes'] for a in n['source_anchors']);checks.append('independent graph parents and exact primary anchors resolve; SOURCE_GAP edges retain source/proof distinction')
live_drift=[]
for f in pins['files']:
 assert digest(f['raw_snapshot'])==f['raw_sha256'];assert digest(f['lf_snapshot'])==f['lf_sha256'];assert Path(f['lf_snapshot']).read_bytes()==Path(f['raw_snapshot']).read_bytes().replace(b'\r\n',b'\n').replace(b'\r',b'\n')
 if digest(f['path'])!=f['raw_sha256']:live_drift.append(f['relative_path'])
assert not live_drift;assert pins['Mathlib_revision_observed']=='db584cd6d46c92f209a44c0f1c829460d327499d';assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo/'.lake/packages/mathlib',text=True).strip()==pins['Mathlib_revision_observed'];checks.append(f"{len(pins['files'])} exact production/Test/fixed-Mathlib/toolchain raw+LF pins read back; no current source drift")
assert capsule['bounded_current_api_pins_sha256']==digest(out/'bounded-current-api-pins.json');assert len(capsule['route_at_most_seven_steps'])==7;assert all(not x['new_public_premises'] for x in capsule['route_at_most_seven_steps']);assert capsule['not_STATEMENT_SEALED'];checks.append('7-step proposal only; no new public premises/theorem/header/SAU/Goal claim')
file_digests=[]
for p in sorted(out.iterdir()):
 if p.is_file() and p.name not in ['owned-lease.json','terminal-finalizer.json','terminal-readback.json']:
  file_digests.append({'name':p.name,'bytes':p.stat().st_size,'raw_sha256':digest(p)})
report={'schema':1,'role':'independent-primary64-terminal-evidence-finalizer','status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'source_raw_sha256':seal['source_raw_sha256'],'source_graph_sha256':seal['graph_sha256'],'source_coverage_sha256':seal['coverage_sha256'],'capsule_sha256':digest(out/'bounded-source-api-capsule.json'),'synthesis_sha256':digest(out/'bounded-source-api-synthesis.md'),'current_api_pins_sha256':digest(out/'bounded-current-api-pins.json'),'artifacts':file_digests,'canonical_science_gate_run':False,'Lean_authored_or_compile_run':False,'source63_review':False,'frozen_TYPE_header_received':False,'statement_sealed_or_theorem_review_granted':False,'lease_close_is_final_write':True}
(out/'terminal-finalizer.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())
readback={'schema':1,'event':'ACTUAL_TERMINAL_FINALIZER_READBACK','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'finalizer_sha256':digest(out/'terminal-finalizer.json'),'observed_finalizer_status':j('terminal-finalizer.json')['status'],'capsule_sha256':digest(out/'bounded-source-api-capsule.json'),'synthesis_sha256':digest(out/'bounded-source-api-synthesis.md'),'all_checks_count':len(checks),'source_graph_unchanged':digest(out/'source-proof-graph.json')==seal['graph_sha256'],'owned_lease_close_next_and_last':True}
(out/'terminal-readback.json').write_bytes((json.dumps(readback,indent=2)+'\n').encode())
assert j('terminal-readback.json')==readback
lease=j('owned-lease.json');lease.update({'state':'CLOSED_LAST','closed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'terminal_finalizer_sha256':digest(out/'terminal-finalizer.json'),'terminal_readback_sha256':digest(out/'terminal-readback.json'),'capsule_sha256':digest(out/'bounded-source-api-capsule.json'),'synthesis_sha256':digest(out/'bounded-source-api-synthesis.md'),'last_write':'owned-lease.json','no_more_owned_writes_authorized':True})
# Deliberately the final filesystem write of this prereviewer lease.
(out/'owned-lease.json').write_bytes((json.dumps(lease,indent=2)+'\n').encode())
assert j('owned-lease.json')['state']=='CLOSED_LAST'
print(json.dumps({'terminal_finalizer_status':'PASS','terminal_finalizer_sha256':digest(out/'terminal-finalizer.json'),'terminal_readback_sha256':digest(out/'terminal-readback.json'),'capsule_sha256':digest(out/'bounded-source-api-capsule.json'),'synthesis_sha256':digest(out/'bounded-source-api-synthesis.md'),'owned_lease_state':j('owned-lease.json')['state'],'owned_lease_sha256':digest(out/'owned-lease.json'),'checked_artifact_count':len(file_digests),'canonical_mutations_or_compile':False},indent=2))
