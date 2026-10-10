# coding: utf-8
import copy, datetime, hashlib, json, pathlib, re, sys
sys.stdout.reconfigure(encoding='utf-8')
R=pathlib.Path('E:/Samplinglib'); B=R/'runs/20261007-companion-priority'
O=B/'pbps-gaussian-marginal-gradient-topology-overlay51'
G=B/'pbps-gaussian-marginal-gradient-sourcegraph51'
V=B/'pbps-gaussian-marginal-gradient-topology-review51'
def h(b): return hashlib.sha256(b).hexdigest()
def lf(b): return b.replace(b'\r\n',b'\n')
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def write(n,d): (O/n).write_bytes((json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode())
def pin(p):
 b=p.read_bytes(); return dict(path=str(p),bytes=len(b),raw_sha256=h(b),lf_sha256=h(lf(b)))
lease=read(O/'lease.json'); assert lease['status']=='OPEN'
inputs=[]
names=['source-proof-graph.json','caller-inventory.json','lexical-inventory.json','selected-token-inventory.json','selected-providers.json','source-coverage.json','source-contract.json','hypothesis-contract.json','primary-formula-inventory.json','input-bindings.json','run.json','lease.json','candidate.raw','statement-seals.accepted.json.raw']
for n in names:
 p=G/n; inputs.append(pin(p)); (O/('original.'+n+'.raw.snapshot')).write_bytes(p.read_bytes())
for n in ['source-topology-review.json','reviewer.topology.lease.json']:
 p=V/n; inputs.append(pin(p)); (O/('negative.'+n+'.raw.snapshot')).write_bytes(p.read_bytes())
assert inputs[-2]['raw_sha256']=='ad755247f894d631fff643fe47f940067b678a16035a31bbc4f8d880447b704c'
assert read(V/'reviewer.topology.lease.json')['status']=='CLOSED'
assert read(G/'lease.json')['status']=='CLOSED'
oldbindings=read(G/'input-bindings.json')
for x in oldbindings['files']:
 p=pathlib.Path(x['path']); actual=pin(p)
 assert actual['raw_sha256']==x['raw_sha256'] and actual['lf_sha256']==x['lf_sha256'], str(p)
 inputs.append(actual)
graph=read(G/'source-proof-graph.json'); original=copy.deepcopy(graph)
calls=read(G/'caller-inventory.json'); oldcalls=copy.deepcopy(calls)
lex=read(G/'lexical-inventory.json'); oldlex=copy.deepcopy(lex)
providers=read(G/'selected-providers.json'); oldproviders=copy.deepcopy(providers)
coverage=read(G/'source-coverage.json'); oldcoverage=copy.deepcopy(coverage)
tokens=read(G/'selected-token-inventory.json')
operations=[]
def appendcaller(c):
 idx=len(calls['entries']); c.update(index0=idx,caller_index0=idx,compiled51call=False,provider_body_selected=False)
 source=pathlib.Path(c['path']).read_bytes()
 assert source[c['start_utf8_byte0']:c['end_utf8_byte0_exclusive']].decode()==c['token']
 calls['entries'].append(c)
 graph['edges'].append(dict(id='E51.'+str(len(graph['edges'])),ingredient=c['resolved_node'],consumer=c['caller_node'],kind='definition-or-typing-reference',reason='Exact overlay51 direct primitive reference; no implementation call',caller_index0=idx,compiled51call=False))
 return idx
for i in [20,70]:
 c=copy.deepcopy(calls['entries'][i]); c.update(token='D.closure',end_utf8_byte0_exclusive=c['start_utf8_byte0']+9,resolved_node='D51.closure',qualified_id='LinearPMap.closure',classification='composite-subexpression-definition-reference')
 idx=appendcaller(c)
 lex['entries'].append({k:v for k,v in c.items() if k not in ['index0','compiled51call','provider_body_selected']})
 operations.append(dict(repair='T1',operation='append exact nested closure caller and ingredient edge',original_caller_index0=i,new_caller_index0=idx,original_whole_composite_retained=True))
module=R/'.lake/packages/mathlib/Mathlib/Algebra/Module/Defs.lean'
raw=module.read_bytes(); inputs.append(pin(module)); lines=raw.splitlines(keepends=True)
start=sum(map(len,lines[:53])); anchor=b''.join(lines[53:55]); selected=b'class Module'
assert raw[start:start+len(selected)]==selected
assert h(raw)=='e6f12b8aa288c01588b63a78e805212276fc9a554bdd09ffdee7183871e9612e'
assert h(anchor)=='2768087350c22f23e70fa1dc4f271f38912268b2e3a8b85149e8b358da27b833'
(O/'D51.Module.raw').write_bytes(selected); (O/'D51.Module.lf').write_bytes(lf(selected))
(O/'Module-definition-header.context.raw').write_bytes(anchor); (O/'Module-definition-header.context.lf').write_bytes(lf(anchor))
graph['nodes'].append(dict(id='D51.Module',kind='external-unexpanded-typing-primitive',contract='Global Module R M class (scalar module structure), not namespace Module.finrank. Actual class header54-55 pinned as unexpanded context; selected declaration anchor only. No new public premise.',qualified_id='Module',compiled51=False,proof_body_expanded=False))
providers.append(dict(id='D51.Module',node='D51.Module',path=str(module),kind='external-unexpanded-declaration-anchor',whole_raw_sha256=h(raw),whole_lf_sha256=h(lf(raw)),start_utf8_byte0=start,end_utf8_byte0_exclusive=start+len(selected),physical_lines1=[54,54],fragment_raw_sha256=h(selected),fragment_lf_sha256=h(lf(selected)),body_selected=False,external_expansion_boundary=True,selection_boundary='Literal declaration-name prefix only. Remaining signature54-55 pinned separately as unexpanded context, not selected caller/provider expansion. No superclass body selected.',definition_header_context=dict(physical_lines1=[54,55],start_utf8_byte0=start,end_utf8_byte0_exclusive=start+len(anchor),raw_sha256=h(anchor),lf_sha256=h(lf(anchor)))))
coverage['rows'].append(dict(provider='D51.Module',path=str(module),physical_line1=54,start_utf8_byte0=start,end_utf8_byte0_exclusive=start+len(selected),classification='NODE',node='D51.Module',reason='Selected literal class declaration-name prefix; all selected bytes covered. Remainder of header/body is external-unexpanded, not falsely excluded layout.',raw_line_sha256=h(selected),row_fragment_is_partial_physical_line=True))
for tok,a,z in [('class',0,5),('Module',6,12)]:
 lex['entries'].append(dict(provider='D51.Module',caller_node='D51.Module',path=str(module),physical_line1=54,start_utf8_byte0=start+a,end_utf8_byte0_exclusive=start+z,token=tok,classification='declaration-kind-language-symbol' if tok=='class' else 'own-declaration-label-not-call',resolved_node=None))
for i in [614,621,647,802]:
 c=copy.deepcopy(lex['entries'][i]); c.update(classification='external-unexpanded-typing-reference',resolved_node='D51.Module',qualified_id='Module')
 idx=appendcaller(c); lex['entries'][i].update(classification=c['classification'],resolved_node='D51.Module',qualified_id='Module',caller_index0=idx)
 operations.append(dict(repair='T2',operation='resolve existing global Module lexeme; append direct typing caller/edge',lexical_index0=i,new_caller_index0=idx))
r=coverage['rows'][141]; assert r['physical_line1']==49 and r['classification']=='EXCLUDED'
r.update(classification='NODE',node='D51.MS',reason='Actual @[class] structure MeasurableSpace declaration shares this selected line; its body remains external-unexpanded.')
operations.append(dict(repair='T3',operation='reclassify existing exact structure header row',coverage_index0=141,changed_fields=['classification','node','reason'],bytes_and_range_unchanged=True))
tokens['entries']=copy.deepcopy(calls['entries'])
assert graph['nodes'][:104]==original['nodes'] and graph['edges'][:275]==original['edges']
assert calls['entries'][:230]==oldcalls['entries'] and providers[:61]==oldproviders
assert [i for i in range(943) if lex['entries'][i]!=oldlex['entries'][i]]==[614,621,647,802]
assert [i for i in range(169) if coverage['rows'][i]!=oldcoverage['rows'][i]]==[141]
assert len(graph['nodes'])==105 and len(graph['edges'])==281
for c in calls['entries'][230:]:
 assert c['caller_node']!=c['resolved_node']
counts=dict(nodes=105,edges=281,providers=62,selected_rows=170,NODE=sum(r['classification']=='NODE' for r in coverage['rows']),EXCLUDED=sum(r['classification']=='EXCLUDED' for r in coverage['rows']),named_callers=len(calls['entries']),lexemes=len(lex['entries']))
for n,d in [('source-proof-graph.json',graph),('caller-inventory.json',calls),('lexical-inventory.json',lex),('selected-token-inventory.json',tokens),('selected-providers.json',providers),('source-coverage.json',coverage),('counts.json',counts)]: write(n,d)
write('overlay-operations.json',dict(scope='Only authorized representation T1/T2/T3; no mathematical/source/header change',operations=operations,append=dict(nodes=1,edges=6,providers=1,coverage_rows=1,callers=6,lexemes=4),changed_existing=dict(coverage=[141],lexical=[614,621,647,802]),untouched_prefix=dict(nodes=104,edges=275,providers=61,callers=230),external_boundary='Module full literal definition header54-55 context pinned; selected declaration-anchor prefix only. No optional typing expansion. Original61 full selected providers retained unchanged.'))
write('input-bindings.json',dict(schema='overlay51-rawLF-input-bindings-v1',files=inputs,raw_recipe='SHA256 exact physical bytes',lf_recipe='SHA256 bytes replacing CRLF with LF only',historical='Original graph/review CLOSED leases stored as immutable raw snapshots; actual own lease is lease.json and was OPEN during authoring.',unchanged_statement=dict(lf_bytes=697,lf_sha256='d7273526caa94ec518b790626edb6b289bdabfdd1104a196cd2e8eb110211e81')))
write('creator-bookkeeping-checks.json',dict(status='MECHANICAL_CHECKS_ONLY_NOT_TOPOLOGY_ADMISSION',original_graph_prefix_unchanged=True,original_caller_prefix_unchanged=True,only_authorized_existing_fields_changed=True,new_caller_token_offsets_checked=True,all_original_current_input_pins_match=True,negative_receipt_hash_matches=True,original_and_negative_actual_leases_closed=True,no_compiler=True,no_proof_or_canonical_edit=True,counts=counts))
(O/'capsule.md').write_text('Representation-only successor for graph51; independent topology review remains required.\n\nT1 appends two exact D.closure callers and dependency edges while preserving original IsClosed calls. T2 adds one honest external-unexpanded global Module declaration primitive and four exact typing edges; the selected prefix class Module is pinned, and full definition header54-55 is separately pinned unexpanded context. T3 reclassifies the existing MeasurableSpace declaration row without changing its bytes.\n\nCounts: 105 nodes, 281 edges, 62 providers, 170 selected rows (144 NODE/26 EXCLUDED), 236 named callers, 947 lexical entries. Original 104 nodes/275 edges/61 providers/230 callers remain exact prefixes; only original lexical614/621/647/802 and coverage141 fields change. Source/hypothesis contracts, primary formula inventory, negative, exact697 statement and seals remain original byte snapshots.\n\nNo51 implementation or proof exists/read; no compiler, theorem claim or topology self-admission. Prior49/50 body/sourcegraph/parent and historical metadata exposures remain disclosed in unchanged original contracts; preread52 minimal parent local-body exposure is known and unrelated to this repair. Global Module superclass context is explicitly an unexpanded boundary, not an implementation or typing self-call.\n\nSchema stays original51 with one explicit partial-physical-line declaration-anchor row; all offsets are 0-indexed raw UTF8 bytes, ends exclusive, physical line numbers1-based. Raw/LF recipes in input-bindings; native run recipe removes run_sha256 then JSON sorted compact UTF8. Historical CLOSED leases are snapshots; actual closure is lease.json.\n',encoding='utf-8')
footprints=[pin(p) for p in sorted(O.iterdir()) if p.is_file() and p.name not in ['lease.json','run.json']]
run=dict(schema='overlay51-native-run-v1',status='CREATOR_SEALED_REPRESENTATION_ONLY_NOT_ADMITTED',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),counts=counts,inputs_file='input-bindings.json',outputs=footprints,run_recipe='sha256 UTF8 json.dumps(whole object minus run_sha256, sort_keys=True, separators=(comma,colon), ensure_ascii=False)',compiler='NOT_STARTED_CLOSED',proof_started=False,topology_admission=False)
run['run_sha256']=h(json.dumps(run,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()); write('run.json',run)
outpins={n:pin(O/n)['raw_sha256'] for n in ['source-proof-graph.json','caller-inventory.json','lexical-inventory.json','source-coverage.json','selected-providers.json','overlay-operations.json','run.json']}
lease.update(status='CLOSED',read='CLOSED',write='CLOSED',python='CLOSED',closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),compiler='NOT_STARTED_CLOSED',closure_note='Last filesystem operation of authorized overlay51 scope; original and negative leases remain immutable.')
write('lease.json',lease)
# No filesystem operation after actual lease closure.
print(json.dumps(dict(counts=counts,outputs=outpins,run_logical_sha256=run['run_sha256'],actual_closed_lease_sha256=h((json.dumps(lease,ensure_ascii=False,indent=2)+'\n').encode())),indent=2))
