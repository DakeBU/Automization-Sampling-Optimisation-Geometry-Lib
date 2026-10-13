from pathlib import Path
import json,hashlib,os,sys,traceback
ROOT=Path('E:/Samplinglib');RUN=ROOT/'runs/20261007-companion-priority/pbps-harmonic-flow-preproof73';OWN=RUN/'independent-header-source73';DEST=OWN/'sourcegraph-edge-overlay73'
GRAPH=ROOT/'runs/20261007-companion-priority/pbps-harmonic-flow-sourcegraph73'
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_sha256':sha(b.replace(b'\r\n',b'\n')),'LF_recipe':'CRLF-to-LF only'}
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
code=0
try:
 assert not DEST.exists();DEST.mkdir()
 g=json.loads((GRAPH/'source-proof-graph.json').read_bytes());nodes={x['id']:x for x in g['nodes']}
 primary=ROOT/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html';raw=primary.read_bytes();assert sha(raw)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
 sources=[]
 for i,(source,a,b) in enumerate([('S4.E5.m1',379913,382301),('A1.Ex4',550763,552476),('S2.SS2.p1.1',95559,96221)]):
  f=DEST/f'{i}.source.exactraw.html';f.write_bytes(raw[a:b]);lf=DEST/f'{i}.source.LF.html';lf.write_bytes(raw[a:b].replace(b'\r\n',b'\n'))
  sources.append({'source_anchor':source,'primary_RAW_start_inclusive':a,'primary_RAW_end_exclusive':b,'RAW':pin(f),'LF':pin(lf)})
 edges=[{'producer':'SCALE','consumer':'GROUP','consumer_source_use_site':'S4.E5.m1','edge_layer':'source reconstructed obligation, not compiled Lean dependency','use':'η>0 gives sqrtη nonzero and sqrtη*(sqrtη)^−1=1; expanding both components of Φ_s(Φ_t z) requires these reciprocal cancellations to match Φ_(s+t) z.','justification':'The printed restart equations use sqrtη and η^−1/2. At η=0 the totalized explicit formula generally fails the group law (in R, center0, initial(1,0), s=t=π/2: two composed maps send position to0, while Φπ sends it to−1). η=0 is outside the original source; this example explains why the already-present SCALE ingredient must be an edge rather than a new premise.','exact_source_fragment_indices':[0,2]}, {'producer':'ENERGY','consumer':'ENERGY-NONNEG','consumer_source_use_site':'A1.Ex4','edge_layer':'source reconstructed obligation, not compiled Lean dependency','use':'Nonnegativity refers to the SAME literal H=(η^−1*‖x−c‖²+‖p‖²)/2; use this definition, nonnegative squares and original η>0.','justification':'STAND-STEP alone does not identify an arbitrary scalar H as nonnegative. This edge exposes the source-defined weighted SUM energy as the internal ingredient; it adds no result certificate and does not replace E norms by product max norm.','exact_source_fragment_indices':[1,2]}]
 assert all(not any(e['producer']==z['producer'] and e['consumer']==z['consumer'] for z in g['edges']) for e in edges)
 proposal={'schema':'source73-two-edge-topology-overlay-proposal-v1','status':'FROZEN_PROPOSAL_ONLY_AWAITING_DISTINCT_REVIEWER','proposal_author':'independent_primary69','source_graph_input':pin(GRAPH/'source-proof-graph.json'),'source_graph_lease':pin(GRAPH/'lease.final.json'),'primary':pin(primary),'original_nodes':[nodes[x] for x in ['SCALE','GROUP','ENERGY','ENERGY-NONNEG']],'add_only_edges':edges,'original_edge_count':35,'proposed_edge_count':37,'node_count_unchanged':23,'source_gap_count_unchanged':7,'coverage79_and_binder20_unchanged':True,'exact_source_fragments':sources,'binder_formula_Lean_canonical_changes':False,'independent_overlay_approval_by_author':False,'73_header_or_hash_read':False,'proof_compile_SAU_VERIFIED_fullpaper_credit':False,'old_CLOSED_input_rewritten':False,'actual_pid':os.getpid()}
 write(DEST/'proposal.json',proposal)
 print(json.dumps({'actual_pid':os.getpid(),'exit_code':0,'proposal_path':(DEST/'proposal.json').relative_to(ROOT).as_posix(),'proposal_RAW_sha256':sha((DEST/'proposal.json').read_bytes()),'edges_added':2,'self_approved':False},indent=2))
except BaseException:code=1;traceback.print_exc()
finally:write(OWN/'StageA.edge-overlay-proposal.terminal.json',{'actual_pid':os.getpid(),'exit_code':code,'argv':sys.argv,'background':False})
sys.exit(code)
