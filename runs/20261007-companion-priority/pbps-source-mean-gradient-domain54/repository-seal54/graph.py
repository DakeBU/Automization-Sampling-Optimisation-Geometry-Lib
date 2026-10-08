from common import *
sys.path[:0]=[str(R/'tools'),str(R/'website/scripts'),str(R)]
readpaths=set(); collecting=False
def observed_reads(event,args):
 if collecting and event=='open' and args and isinstance(args[0],(str,bytes,os.PathLike)):
  p=pathlib.Path(os.fsdecode(args[0])).resolve()
  try: p.relative_to(R)
  except ValueError: return
  if p.is_file(): readpaths.add(p)
sys.addaudithook(observed_reads)
import publication_reader as reader
import astis_publication as publication
import astis_site
helper=path('website/scripts/publication_reader.py'); raw=helper.read_bytes(); selected=b''.join(raw.splitlines(keepends=True)[182:187])
assert selected.startswith(b'def graph_input_digest()') and b'publication.digest' in selected
(O/'graph_input_digest.183-187.raw.snapshot.py').write_bytes(selected)
collecting=True
actual=reader.graph_input_digest()
data=publication.inputs(); lean=astis_site.source_digest(); items=publication.load()
payload={'lean':lean,'items':items,'cells':{b['cell']:data['cells'].get(b['cell']) for i in items for b in i['bindings']}}
recomputed=publication.digest(payload)
collecting=False
assert actual==recomputed
g=load('_site/data/underlying-lean-graph.json'); assert g['publication_inputs_sha256']==actual
tid='decl:'+TARGET; nodes=[n for n in g['nodes'] if n['id']==tid]; incident=[e for e in g['edges'] if e['source']==tid or e['target']==tid]
assert len(nodes)==1 and nodes[0]['status']=='compiled' and len(incident)==7
official=load(B/'integration.0.graph.log'); c=official['contributions']; assert len(c)==1 and c[0]['node']==tid and len(c[0]['connections'])==7
project=lambda es: sorted((x['source'],x['target'],x['relation']) for x in es)
assert project(incident)==project(c[0]['connections'])
assert any(e['source'].endswith('LogConcaveOn.prod') and e['relation']=='source reference (scanner)' for e in incident)
assert not any('WeightedC1GradientDomain' in e['source'] for e in incident)
pins=[pin(p) for p in sorted(readpaths)]
assert not guard_denied
dump('graph.binding.payload.actual.json',dict(status='PASS',actual_full_normative_payload=payload,publication_inputs_sha256=actual,recipe='Actual complete publication_reader.graph_input_digest: publication.digest({lean:astis_site.source_digest(),items:publication.load(),cells:all bound cells from publication.inputs()}); sorted compact UTF8 ensure_ascii=False. No projected replacement.'))
dump('graph.exact54.slice.json',dict(schema_version=g['schema_version'],publication_inputs_sha256=actual,reference_contract=g['reference_contract'],target_nodes=nodes,actual_7_incident_edges=incident,native_exact_cell_report=pin(B/'integration.0.graph.log'),scope='Bounded header/one exact54 node/7 incident edges only; no provenance inventories inspected. Solid module/import ownership and dashed incomplete name/source references are not certified theorem implication.'))
dump('graph.checks.json',dict(status='PASS_SCOPED',checked_integration=HEAD,native_graph_input_digest=actual,helper_whole=pin(helper),helper_selected=pin(O/'graph_input_digest.183-187.raw.snapshot.py'),selected_lines=[183,187],whole_helpers=[pin('tools/astis_publication.py'),pin('tools/astis_site.py')],actual_normative_canonical_input_count=len(pins),actual_normative_canonical_input_pins=pins,generated_graph=pin('_site/data/underlying-lean-graph.json'),exact_target=TARGET,actual_incident_edges=7,bounded_slice=pin(O/'graph.exact54.slice.json'),normative_complete_payload=pin(O/'graph.binding.payload.actual.json'),compiler_started=False,future55_directory_guard='Installed before helper imports/calls; blocks runs/*55 directories and private.future55. Bytecode disabled.',guard_denied=guard_denied,graph_truth='Seven graph incident edges are correspondence/ownership/incomplete source-name scan. LogConcaveOn.prod lexical name reference is not an actual parent proof edge; WeightedC1 adapter missing from scan. Actual four parents established by immutable reviewed body/imports, not scanner.'))
print(json.dumps(dict(status='PASS_SCOPED',publication_inputs_sha256=actual,actual_canonical_input_count=len(pins),exact_target_nodes=1,incident_edges=7,guard_denied=guard_denied)))
