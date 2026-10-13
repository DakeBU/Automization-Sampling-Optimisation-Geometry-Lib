"""Distinct exact-overlay review, not approval of this reviewer's original extraction."""
from pathlib import Path
from html.parser import HTMLParser
import ast,copy,datetime,hashlib,json
ROOT=Path('E:/Samplinglib'); BASE=ROOT/'runs/20261007-companion-priority/pbps-transition-kernel-preread85'; OUT=Path(__file__).resolve().parent
def sha(b): return hashlib.sha256(b).hexdigest()
def pin(p):
    p=Path(p); p=p if p.is_absolute() else ROOT/p
    b=p.read_bytes(); return {'path':p.relative_to(ROOT).as_posix(),'raw_sha256':sha(b),'bytes':len(b)}
def put(name,obj):
    p=OUT/name; assert not p.exists(),name
    p.write_bytes((json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode())
    return pin(p)
primary=ROOT/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
assert pin(primary)['raw_sha256']=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
parser_source=BASE/'freeze_preread85.py'
tree=ast.parse(parser_source.read_text(encoding='utf-8'))
cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='SourceHTML')
ns={'HTMLParser':HTMLParser}; exec(compile(ast.Module(body=[cls],type_ignores=[]),str(parser_source),'exec'),ns)
h=ns['SourceHTML'](); h.feed(primary.read_text(encoding='utf-8'))
notes=BASE/'source-first-notes85.json'; assert pin(notes)['raw_sha256']=='9e9e3737db6cc73e351ffe7daa8ad7dbb124e546f1378a25372ae0dab36fa1c1'
for a in json.loads(notes.read_text(encoding='utf-8'))['anchors']:
    assert sha(h.normalized(a['source_id']).encode())==a['normalized_anchor_sha256']
proposal_path=BASE/'independent-topology85/proposed-minimal-topology-overlay85.json'
assert pin(proposal_path)['raw_sha256']=='0d4911d3f7f495bc7b1a8f9c944eaaf64032a0ddc3c62b57266440a13e8441d9'
proposal=json.loads(proposal_path.read_text(encoding='utf-8'))
assert proposal['proposer']=='/root/exact_verify77'
for key in ['exact_original_graph','exact_original_inventory','exact_candidate']:
    expected=proposal[key]; actual=pin(expected['path'])
    assert actual['raw_sha256']==expected['RAW_sha256'] and actual['bytes']==expected['RAW_bytes']
graph=json.loads((BASE/'source-proof-graph85.json').read_text(encoding='utf-8'))
inventory=json.loads((BASE/'source-inventory85.json').read_text(encoding='utf-8'))
candidate=json.loads((BASE/'candidate-recommendation85.json').read_text(encoding='utf-8'))
before={'source-proof-graph85.json':graph,'source-inventory85.json':inventory}
effective=copy.deepcopy(before)
assert len(proposal['operations'])==7
reasons=[
 'Actual iidExp1 P being probability is needed to make the selected constant-clock probability kernel. Qualification to SELECTED_ID_CONST_MAP records sufficiency of this realization; it does not add a source premise or ban direct parameter integration.',
 'Joint actual F measurability is an ingredient of Kernel.map in this selected realization. It remains derived from the actual phase parent, never supplied as an arbitrary-process premise.',
 'Identity-times-constant-clock kernel is an AND ingredient only within the selected map realization. Direct construction of the same probability law by parameter integration remains an unselected alternative.',
 'G85-07 retains the same two AND ingredients; route and scope make that conjunction local to the selected sufficient realization, not a logical necessity across all constructions.',
 'A.7 is the actual n-jump path expansion; A.8 reverses trajectory and ordered times. p4.4 justifies a measure-preserving Borel change of variables despite bounce discontinuity; p5.1 introduces the survival-weight calculation from A.4 and momentum reflection. These support the existing future path-reversal bundle without completing it.',
 'The revised route boundary explicitly preserves the optional direct parameter-integral alternative and rejects either representation as a proof ingredient for invariance. The excluded-association edges E85-27/28/29 remain byte-equivalent as JSON objects.',
 'All three added anchor digests match independent stdlib parsing of the pinned primary (math alttext once, whitespace collapsed). Existing pins remain exact and ordered; p4.4 was already pinned. No new hypothesis or conclusion is introduced.'
]
operation_reviews=[]
for k,op in enumerate(proposal['operations']):
    target=effective[op['file']]; sel=op['selector']
    if 'field' in sel:
        assert target[sel['field']]==op['before']
        target[sel['field']]=copy.deepcopy(op['after'])
    else:
        coll=target[sel['collection']]; identity='id' if 'id' in sel else 'target'
        matches=[i for i,v in enumerate(coll) if v.get(identity)==sel[identity]]
        assert len(matches)==1 and coll[matches[0]]==op['before']
        coll[matches[0]]=copy.deepcopy(op['after'])
    operation_reviews.append({'operation':k+1,'file':op['file'],'selector':sel,'before_exact_match':True,'decision':'ACCEPT','blocking':False,'reason':reasons[k],'before_value_sha256':sha(json.dumps(op['before'],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()),'after_value_sha256':sha(json.dumps(op['after'],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())})
eg=effective['source-proof-graph85.json']; ei=effective['source-inventory85.json']
counts={'inventory':len(ei['items']),'nodes':len(eg['nodes']),'relations':len(eg['edges']),'dependencies':sum(e['dependency_edge'] for e in eg['edges']),'excluded_associations':sum(not e['dependency_edge'] for e in eg['edges'])}
assert counts==proposal['counts_unchanged']=={'inventory':16,'nodes':21,'relations':29,'dependencies':26,'excluded_associations':3}
assert ei['items']==inventory['items'] and ei['anchors']==inventory['anchors']
for a in ei['additional_anchor_pins']: assert sha(h.normalized(a['source_id']).encode())==a['normalized_anchor_sha256']
assert len(ei['additional_anchor_pins'])==6
for old,new in zip(graph['edges'],eg['edges']):
    if old['id'] not in ['E85-05','E85-06','E85-07']: assert old==new
    else:
        assert set(k for k in old if old[k]!=new[k])=={'route','reason'}
for old,new in zip(graph['nodes'],eg['nodes']):
    if old['id']!='G85-15': assert old==new
    else:
        assert old['status']==new['status']=='FUTURE_OPEN'
        assert new['source_ids']==old['source_ids']+['A1.E7','A1.E8','A1.SS1.SSS0.Px1.p4.4','A1.SS1.SSS0.Px1.p5.1']
adj={n['id']:[] for n in eg['nodes']}; indeg={n:0 for n in adj}
for e in eg['edges']:
    if e['dependency_edge']: adj[e['from']].append(e['to']); indeg[e['to']]+=1
queue=[n for n,v in indeg.items() if v==0]; visited=[]
while queue:
    n=queue.pop(); visited.append(n)
    for v in adj[n]:
        indeg[v]-=1
        if indeg[v]==0: queue.append(v)
assert len(visited)==len(adj)
raw_inputs=[pin(primary),pin(notes),pin(parser_source),pin(BASE/'source-proof-graph85.json'),pin(BASE/'source-inventory85.json'),pin(BASE/'candidate-recommendation85.json'),pin(BASE/'api-retrieval85.json'),pin(BASE/'source-first-seal85.json'),pin(proposal_path)]
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
evidence={'schema':'astis.exact-overlay-review85.evidence.v1','status':'closed','closed_utc':now,'reviewer':'/root/fresh_source78','overlay_proposer':'/root/exact_verify77','proposal_raw':pin(proposal_path),'raw_inputs':raw_inputs,'operation_reviews':operation_reviews,'counts_before_and_after':counts,'all_before_values_match_exactly':True,'all_source_anchor_pins_verified':True,'only_proposed_operations_applied_in_memory':True,'dependency_graph_acyclic':True,'no_effective_graph_materialized_or_shared_edits':True,'original_extraction_authored_by_reviewer':True,'original_extraction_independently_approved_by_this_run':False,'prior_topology_decision_or_review_verdicts_read':False,'source_originals_unchanged':True,'source_first_context':'Primary-only notes85 preceded any proposed overlay. This bounded audit reparses the same pinned primary and compares the seven exact operations; it is not a new theorem/header/full-original-topology review.'}
evidence_pin=put('run-evidence85.json',evidence)
decision={'schema':'astis.exact-overlay-review85.decision.v1','status':'closed','verdict':'ACCEPT_EXACT_PROPOSED_OVERLAY','review_run_sha256':evidence_pin['raw_sha256'],'proposal_raw_sha256':pin(proposal_path)['raw_sha256'],'reviewer':'/root/fresh_source78','proposer':'/root/exact_verify77','independence':{'original_source_extractor':True,'overlay_proposer':False,'distinct_exact_proposal_review_only':True,'self_approval_of_original_graph':False,'other_reviewer_verdicts_read':False},'operation_reviews':operation_reviews,'counts':counts,'blocking_deltas':[],'required_additional_repairs':[],'truth_boundary':[
 'Accept only the seven exact JSON before/after operations in the pinned proposal. Original inventory/graph/candidate/source-first notes remain byte-identical. This decision grants no theorem/header/implementation acceptance or proof credit.',
 'Source actual transition law is packaged as a jointly indexed probability kernel by an explicitly selected sufficient generic route. Exact actual-clock fiber law, Dirac0 and bounded-Borel expectation transfer remain required candidate outputs; a supplied-measurable arbitrary process wrapper is insufficient.',
 'Source terminal-pi failed-limit0 convention remains distinct from the actual all-finite-time uncovered-initial-phase fallback. Existing fixed-parameter AE semantics justify their law compatibility; no all-sample equality, uniform-parameter AE event or arbitrary correlated-clock substitution is inferred.',
 'Probability fibers do not establish process Markov/restart or Chapman-Kolmogorov. K is only an optional typed representation for future invariance; actual path-law expansion/reversal and nu invariance remain OPEN. Full L2 additionally requires AE-safe Jensen contraction AND independent compact-continuous density.'
 ],'source_license':'Pinned arXiv nonexclusive source; no full source text copied to these artifacts.','run_evidence':evidence_pin}
decision_pin=put('decision85.json',decision)
raw_outputs=[pin(Path(__file__)),evidence_pin,decision_pin]
manifest={'schema':'astis.exact-overlay-review85.manifest.v1','status':'closed','m':{'status':'closed'},'raw_inputs':raw_inputs,'raw_outputs':raw_outputs,'selfhash':'omitted; run evidence does not include result and result binds exact evidence RAW, avoiding cycles','owned_scope':'pbps-transition-kernel-preread85/overlay-review85 only','no_production_or_shared_state_writes':True}
manifest_pin=put('run-manifest85.json',manifest)
for p in raw_inputs+raw_outputs: assert pin(p['path'])==p
print(json.dumps({'verdict':decision['verdict'],'decision':decision_pin,'evidence':evidence_pin,'manifest':manifest_pin,'counts':counts},indent=2))
