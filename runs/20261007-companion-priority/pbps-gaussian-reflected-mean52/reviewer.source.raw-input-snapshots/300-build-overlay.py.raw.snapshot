# coding:utf-8
import pathlib,json,hashlib,copy,datetime,sys
sys.stdout.reconfigure(encoding='utf-8')
R=pathlib.Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority';G=B/'pbps-gaussian-reflected-mean-sourcegraph52';V=B/'pbps-gaussian-reflected-mean-topology-review52';O=B/'pbps-gaussian-reflected-mean-topology-overlay52'
def h(b):return hashlib.sha256(b).hexdigest()
def lf(b):return b.replace(b'\r\n',b'\n')
def jr(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(d):return (json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode()
def jw(n,d):(O/n).write_bytes(enc(d))
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),raw_sha256=h(b),lf_sha256=h(lf(b)))
lease=jr(O/'lease.json');assert lease['status']=='OPEN'
negative=pin(V/'source-topology-review.json');assert negative['raw_sha256']=='a23cd0875a1ec946383987a6dc7a9e962b967d8cb4099c2167c533f0907e958d'
assert all(jr(V/'reviewer.topology.lease.json')[x]=='CLOSED' for x in ['read','write','Python'])
assert jr(G/'lease.json')['status']=='CLOSED'
inputs=[]
names=['source-proof-graph.json','source-contract.json','hypothesis-contract.json','selected-providers.json','source-coverage.json','caller-inventory.json','lexical-inventory.json','selected-token-inventory.json','primary-formula-inventory.json','input-bindings.json','counts.json','run.json','lease.json']
for n in names:
 p=G/n;inputs.append(pin(p));(O/('original.'+n+'.raw.snapshot')).write_bytes(p.read_bytes())
for n in ['source-topology-review.json','reviewer.topology.lease.json','reviewer.topology.run.json']:
 p=V/n;inputs.append(pin(p));(O/('negative.'+n+'.raw.snapshot')).write_bytes(p.read_bytes())
for n in ['prospective-statement.txt','statement-seals.accepted.json']:
 p=B/'pbps-gaussian-reflected-mean-preproof52'/n;inputs.append(pin(p));(O/('unchanged.'+n+'.raw.snapshot')).write_bytes(p.read_bytes())
assert inputs[-2]['lf_sha256']=='50ca5c7e0b5aed0f892d2e686fd276b11a586b30745d8edd2d5c1256d7e09d11'
# Byte hashes only, no new parent or implementation-body inspection.
for x in jr(G/'input-bindings.json')['files']:
 p=pathlib.Path(x['path']);d=pin(p);assert d['raw_sha256']==x['raw_sha256'] and d['lf_sha256']==x['lf_sha256'];inputs.append(d)
graph=jr(G/'source-proof-graph.json');original=copy.deepcopy(graph)
target=next(n for n in graph['nodes'] if n['id']=='P52.diff');assert target['qualified_id']=='MeasureTheory.hasFDerivAt_integral_of_dominated_of_fderiv_le'
target['qualified_id']='hasFDerivAt_integral_of_dominated_of_fderiv_le'
pp=R/'.lake/packages/mathlib/Mathlib/Analysis/Calculus/ParametricIntegral.lean';pb=pp.read_bytes();lines=pb.decode('utf-8').splitlines();assert not any(s.lstrip().startswith('namespace ') for s in lines)
assert lines[209].startswith('theorem '+target['qualified_id']+' ')
prim=next(p for p in jr(G/'selected-providers.json') if p['id']=='primary-covariance');source=pathlib.Path(prim['path']);raw=source.read_bytes();ss=raw.splitlines(keepends=True)
def span(line,token,provider):
 b=ss[line-1];start=sum(map(len,ss[:line-1]))+b.index(token.encode());end=start+len(token.encode());assert raw[start:end].decode()==token
 return dict(provider=provider,path=str(source),physical_line1=line,start_utf8_byte0=start,end_utf8_byte0_exclusive=end,token=token)
def definition(a,z,provider,label):
 start=sum(map(len,ss[:a-1]));frag=b''.join(ss[a-1:z]);return dict(provider=provider,anchor=label,path=str(source),physical_lines1=[a,z],start_utf8_byte0=start,end_utf8_byte0_exclusive=start+len(frag),raw_sha256=h(frag),lf_sha256=h(lf(frag)))
new=[]
for ingredient,use,definition_span,reason in [
 ('S52.density',span(4596,'normalized conditional density','primary-covariance'),definition(4581,4587,'primary-density','A3.Ex1'),'The printed normalized-density differentiation/covariance identity uses the genuine reflected conditional density defined earlier by A3.Ex1. This source-definition use is separate from authored numerator/quotient route.'),
 ('S52.score',span(4601,'s_{y}(Y_{-})','primary-covariance'),definition(4589,4595,'primary-score','A3.Ex2'),'The printed A3.E1 covariance uses the specific unnormalized parameter-y score s_y defined in A3.Ex2. Not an arbitrary score and not a mandatory covariance/IBP proof route for T52.')]:
 d=dict(id='E52.'+str(len(graph['edges'])),ingredient=ingredient,consumer='S52.covariance',kind='source-definition-use',reason=reason,compiled52call=False,source_span=use,definition_span=definition_span,mandatory_for_authored_numerator_quotient=False)
 graph['edges'].append(d);new.append(d)
assert len(graph['nodes'])==97 and len(graph['edges'])==287
assert graph['edges'][:285]==original['edges']
changed=[i for i in range(97) if graph['nodes'][i]!=original['nodes'][i]];assert changed==[8]
check=copy.deepcopy(graph['nodes'][8]);check['qualified_id']=original['nodes'][8]['qualified_id'];assert check==original['nodes'][8]
# Source graph route into target remains byte-for-byte same original edges; new edges have only source covariance consumer.
assert all(e['consumer']=='S52.covariance' and e['ingredient'] in ['S52.density','S52.score'] for e in new)
jw('source-proof-graph.json',graph)
# Exact unchanged successor inventories/contracts copied without reserialization.
unchanged=['source-contract.json','hypothesis-contract.json','selected-providers.json','source-coverage.json','caller-inventory.json','lexical-inventory.json','selected-token-inventory.json','primary-formula-inventory.json']
for n in unchanged:(O/n).write_bytes((G/n).read_bytes())
counts=jr(G/'counts.json');counts['edges']=287;jw('counts.json',counts)
jw('overlay-operations.json',dict(schema='topology52-minimal-overlay-v1',scope='Exactly one qualified-name field and two source-definition/use edges; no mathematical or public binder change',operations=[dict(id='T52-1',path='/nodes/8/qualified_id',before='MeasureTheory.hasFDerivAt_integral_of_dominated_of_fderiv_le',after=target['qualified_id'],evidence='Pinned ParametricIntegral.lean has open MeasureTheory but no enclosing namespace; exact declaration210-216 remains unchanged'),dict(id='T52-2',operation='append',edge=new[0]),dict(id='T52-3',operation='append',edge=new[1])],unchanged_inventory_files=unchanged,immutable_prefix=dict(nodes_except_one_field=97,edges=285,providers=81,rows=165,callers=191,lexemes=747),math_route_change=False,source_coverage_change=False,typing_expansion=False,covariance_mandatory_for_authored_route=False))
jw('input-bindings.json',dict(schema='topology52-overlay-native-rawLF-v1',files=inputs,raw_recipe='SHA256 exact bytes',lf_recipe='SHA256 bytes replacing CRLF with LF only',historical_actual_closed_leases='Original creator and independent negative reviewer leases preserved as raw snapshots, distinct from own actual overlay lease.json',original_negative_unchanged=True,statement_lf_bytes=497,statement_lf_sha256='50ca5c7e0b5aed0f892d2e686fd276b11a586b30745d8edd2d5c1256d7e09d11'))
jw('creator-bookkeeping-checks.json',dict(status='MECHANICAL_MINIMAL_DELTA_ONLY_NOT_TOPOLOGY_ADMISSION',original285edge_prefix_unchanged=True,only_node8_qualified_id_changed=True,all_inventories_byte_identical=True,source_definition_use_offsets_match=True,all_original_rawLF_input_pins_match=True,original_and_negative_leases_closed=True,no_covariance_dependency_added_to_authored_math_route=True,counts=counts,compiler='NOT_STARTED_CLOSED'))
(O/'capsule.md').write_text('Representation-only topology52 successor is ready for distinct independent review. Exactly one node qualified_id correction and two appended source-definition/use edges. P52.diff is the global hasFDerivAt_integral_of_dominated_of_fderiv_le; open MeasureTheory does not create a namespace. E52.285: source density -> printed covariance; E52.286: source score -> printed covariance. Both have exact raw UTF8 caller-use and balanced definition anchors in primary A3.Ex1/A3.Ex2/A3.E1.\n\n97 nodes, 287 edges; original285 edge prefix preserved. Original81 providers/165 selected rows/191 callers/747 lexemes and all source formulas/public contracts are exact byte-identical successor copies. Only node8 qualified_id changes. Exact497 LF statement and seals unchanged. The authored N/Z C1 proof-obligation route has no new covariance/IBP dependency.\n\nSee overlay-operations.json for exact field paths and source offsets, input-bindings.json for current/historical rawLF pins, run.json for native output hashes, lease.json for actual closure. Raw/LF: physical SHA256 / CRLF->LF only. Run logical recipe: sorted compact UTF8 JSON whole object minus run_sha256. Historical creator/negative CLOSED leases remain snapshots; own actual lease is separate. No compiler, proof, claim, canonical edit or self-topology admission. Original negative retained despite transport interruption after its disk closure. Prior own source/parent/body exposure disclosed in unchanged original source contract; no52 implementation read.\n',encoding='utf-8')
outputs=[pin(p) for p in sorted(O.iterdir()) if p.is_file() and p.name not in ['run.json','lease.json']]
run=dict(schema='topology52-overlay-native-run-v1',status='CREATOR_CLOSED_REPRESENTATION_ONLY_PENDING_INDEPENDENT_REVIEW',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),counts=counts,outputs=outputs,input_bindings='input-bindings.json',native_run_recipe='SHA256 UTF8 JSON whole object minus run_sha256; sort_keys=True,separators=(comma,colon),ensure_ascii=False',compiler='NOT_STARTED_CLOSED',proof=False,self_topology_admission=False)
run['run_sha256']=h(json.dumps(run,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode());jw('run.json',run)
pins={n:pin(O/n)['raw_sha256'] for n in ['source-proof-graph.json','overlay-operations.json','run.json']}
lease.update(status='CLOSED',read='CLOSED',write='CLOSED',python='CLOSED',compiler='NOT_STARTED_CLOSED',closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),final_filesystem_operation=True,result='Authorized T52-1/T52-2/T52-3 representation-only overlay, distinct topology admission pending')
jw('lease.json',lease)
# No filesystem operation follows actual own lease closure.
print(json.dumps(dict(counts=counts,pins=pins,run_logical_sha256=run['run_sha256'],actual_closed_lease_sha256=h(enc(lease))),indent=2))
