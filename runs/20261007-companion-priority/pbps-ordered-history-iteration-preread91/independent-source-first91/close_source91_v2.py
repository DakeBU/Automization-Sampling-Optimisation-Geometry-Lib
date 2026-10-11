from pathlib import Path
import json,hashlib,datetime
ROOT=Path('E:/Samplinglib');OUT=ROOT/'runs/20261007-companion-priority/pbps-ordered-history-iteration-preread91/independent-source-first91'
def raw(p):
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def read(n):return json.loads((OUT/n).read_text(encoding='utf8'))
def write(n,x):
 p=OUT/n;assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8');return raw(p)
g=read('source-proof-graph91.native.json');original=raw(OUT/'source-proof-graph91.native.json')
g['authored_successor_provenance']={'predecessor':original,'reason':'Resolve textual AND-parent shorthand into explicit open proof nodes and route-indexed AND junctions. No new source premise, theorem target, closure or independent topology approval. Original retained immutable.','creator_self_independent_approval':False}
g['nodes'] += [
 {'id':'S91-REL','kind':'alternative-source-implicit-induction','claim':'Alternative finite-depth positive relative-wait vector density multiplication from90, before cumulative-sum substitution','anchors':['P91-A7'],'status':'OPEN_OR_ROUTE_NOT_REQUIRED_FOR_PREFERRED91'},
 {'id':'S91-TRI','kind':'alternative-source-implicit-coordinate-ingredient','claim':'Full finite-dimensional cumulative-sum triangular transport of the relative-wait joint density to strict ordered absolute times','anchors':['P91-A1','P91-A7'],'status':'OPEN_OR_ROUTE_NOT_REQUIRED_FOR_PREFERRED91'},
 {'id':'S91-ALG','kind':'source-implicit-path-hazard-algebra','claim':'Sum integrated hazards over consecutive flow segments, including final segment, equals the rate integral along the prescribed path; pre-bounce factors match','anchors':['P91-A7'],'status':'OPEN_FUTURE_CONSUMER'},
 {'id':'S91-PATH','kind':'source-implicit-path-measurability-identification','claim':'Borel prescribed-path observables and compatibility with the actual globally reconstructed path on its finite-count event','anchors':['P91-A7','P91-A2'],'status':'OPEN_FUTURE_CONSUMER'}]
for e in g['edges']:
 if e['id']=='E08':e.update({'to':'S91-REL','justification':'Alternative: first iterate90 in relative waits; global cumulative-sum substitution follows. Not an AND parent in the preferred conditional absolute-time91 route.'})
g['edges'] += [
 {'id':'E20','from':'S91-REL','to':'S91-J','relation':'alternative-relative-induction','justification':'The relative-vector density is transported by S91-TRI in the alternative sufficient route.'},
 {'id':'E21','from':'S91-TRI','to':'S91-J','relation':'alternative-global-coordinate-route','justification':'Together with relative induction and Borel finite constructors, yields ordered absolute-time density; OR with conditional91 route.'},
 {'id':'E22','from':'S91-ALG','to':'S91-F','relation':'path-hazard-algebra','justification':'Actual finite factors plus final survival still require segment-to-full-path rate integral algebra.'},
 {'id':'E23','from':'S91-PATH','to':'S91-P','relation':'actual-prescribed-path-observables','justification':'Half-open count coverage must be connected to Borel actual/prescribed full-path tests.'}]
g['AND_junctions']=[
 {'target':'S91-C','parents':['S90-E','S91-T'],'route':'preferred actual90 coordinate route','direct89_note':'S89-D is transitive; optional direct Borel/fiber reuse is E06, not a duplicated independent probability AND.'},
 {'target':'S91-J','parents':['S91-M','S91-C'],'route':'preferred conditional absolute-time induction'},
 {'target':'S91-J','parents':['S91-M','S91-REL','S91-TRI'],'route':'alternative relative induction then triangular transport; OR with preceding junction'},
 {'target':'S91-F','parents':['S91-J','S88-S','S91-ALG'],'route':'finite factors, final survival and hazard algebra all required'},
 {'target':'S91-P','parents':['S79-COVER','S91-J','S91-PATH'],'route':'conditional extra S91-B only if endpoint conventions are equated'},
 {'target':'S91-A7','parents':['S91-F','S91-P','S91-AC'],'route':'full A7'}]
ids={n['id'] for n in g['nodes']};assert len(ids)==len(g['nodes'])
assert all(e['from'] in ids and e['to'] in ids for e in g['edges'])
assert all(j['target'] in ids and all(p in ids for p in j['parents']) for j in g['AND_junctions'])
g['structural_check']={'unique_nodes':True,'edge_endpoints_resolve':True,'AND_parents_resolve':True,'mathematical_topology_independently_approved':False}
gd=write('source-proof-graph91.v2.native.json',g)
c=read('source-coverage91.native.json');c['graph']=gd;c['predecessor']=raw(OUT/'source-coverage91.native.json')
for item in c['coverage']:
 if item['id']=='C13':item['nodes']+=['S91-REL']
 if item['id']=='C14':item['nodes']+=['S91-TRI']
 if item['id']=='C17':item['nodes']+=['S91-ALG']
 if item['id']=='C21':item['nodes']+=['S91-PATH']
cd=write('source-coverage91.v2.native.json',c)
p=read('candidate91.source-proposal.native.json');p['source_graph']=gd;p['authored_successor_provenance']={'predecessor':raw(OUT/'candidate91.source-proposal.native.json'),'change':'Only graph binding updated to explicit-node structural successor. Mathematical target unchanged. No independent acceptance.'}
pd=write('candidate91.source-proposal.v2.native.json',p)
chron=write('chronology91.closure-successor.native.json',{'schema':'astis-source-chronology91-successor-v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'previous_chronology':raw(OUT/'chronology91.native.json'),'event':'After initial native closure, creator structural check found three textual AND-parent shorthands. Added four explicit OPEN future/alternative nodes and route-indexed AND junctions; preserved original files. This is authoring/serialization correction only, never self-independent topology acceptance. No source input, chosen mathematical target or original primary-first freeze changed.','outputs':[gd,cd,pd]})
t=write('terminal91.v2.native.json',{'schema':'astis-source-terminal91-v2','terminal_closed':True,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'authoritative_creator_outputs':[gd,cd,pd],'primary_first_freeze_unchanged':raw(OUT/'primary-first91.freeze.native.json'),'retrieval_unchanged':raw(OUT/'retrieval91.native.json'),'chronology':[raw(OUT/'chronology91.native.json'),chron],'status':'CLOSED SOURCE-ONLY PROPOSAL; DISTINCT TOPOLOGY REVIEW REQUIRED','creator_self_independent_approval':False,'nodes':len(g['nodes']),'edges':len(g['edges']),'AND_junctions':len(g['AND_junctions']),'OR_routes':len(g['OR_routes']),'coverage_items':27})
inputs=read('closed-raw-manifest.source-first91.native.json')['inputs']
outputs=[raw(p) for p in sorted(OUT.rglob('*')) if p.is_file()]
m=write('closed-raw-manifest.source-first91.v2.native.json',{'schema':'astis-closed-raw-manifest91-v2','closed':True,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'predecessor':raw(OUT/'closed-raw-manifest.source-first91.native.json'),'inputs':inputs,'outputs':outputs,'authoritative_graph':gd,'authoritative_coverage':cd,'authoritative_candidate':pd,'terminal':t,'manifest_self_hash_omitted':True,'creator_self_independent_approval':False,'scope':'Source-only authored topology proposal; no new math proof/status/canonical write; old source-first and first closure immutable.'})
for d in inputs+outputs+[m]:assert raw(ROOT/d['path'])==d
print(json.dumps({'graph':gd,'coverage':cd,'candidate':pd,'retrieval':raw(OUT/'retrieval91.native.json'),'existing_actual_coverage':raw(OUT/'existing-actual-coverage91.native.json'),'terminal':t,'manifest':m,'inputs':len(inputs),'outputs':len(outputs)},indent=2))
