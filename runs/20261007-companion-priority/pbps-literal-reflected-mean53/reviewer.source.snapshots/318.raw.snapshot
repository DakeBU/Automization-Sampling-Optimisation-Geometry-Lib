import json,pathlib,hashlib,re,datetime,sys,copy
sys.stdout.reconfigure(encoding='utf-8')
ROOT=pathlib.Path('E:/Samplinglib');B=ROOT/'runs/20261007-companion-priority/pbps-reflected-density-sourcegraph53';R=ROOT/'runs/20261007-companion-priority/pbps-reflected-density-topology-review53';O=ROOT/'runs/20261007-companion-priority/pbps-reflected-density-topology-overlay53';P=ROOT/'runs/20261007-companion-priority/pbps-reflected-density-preproof53'
def sha(b):return hashlib.sha256(b).hexdigest()
def lf(b):return b.replace(b'\r\n',b'\n')
def js(p):return json.loads(pathlib.Path(p).read_text(encoding='utf-8-sig'))
def enc(o):return (json.dumps(o,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
def dump(n,o):(O/n).write_bytes(enc(o))
def pin(p):
 p=pathlib.Path(p);b=p.read_bytes();return dict(path=str(p),raw_bytes=len(b),lf_bytes=len(lf(b)),raw_sha256=sha(b),lf_sha256=sha(lf(b)))
neg=R/'source-topology-review.json';nl=R/'reviewer.topology.lease.json'
assert pin(neg)['raw_sha256']=='f892e562c4eaafeb49c9c0140a33178b0cbd0ef972702473f6d075b30015ffe0'
assert pin(nl)['raw_sha256']=='7c62ba657e91de6b1200227521405d31fd1ee907ee7928afdcd97dc365ac60d1'
assert js(nl)['status']=='CLOSED' and js(neg)['verdict']=='blocked-source-representation-only'
original_names=['source-proof-graph.json','selected-providers.json','source-coverage.json','caller-inventory.json','lexical-inventory.json','selected-token-inventory.json','counts.json','source-contract.json','hypothesis-contract.json','primary-formula-inventory.json','input-bindings.json','parent-status.json','creation-dependencies.json','run.json','lease.json']
inputs=[]
for n in original_names:
 p=B/n;inputs.append(pin(p));(O/('original.'+n+'.raw.snapshot')).write_bytes(p.read_bytes())
for p in [neg,nl,P/'prospective-statement.txt',P/'statement-seals.accepted.json',P/'root.statement-proposal.json']:
 inputs.append(pin(p));(O/(('negative.' if p.parent==R else 'unchanged.')+p.name+'.raw.snapshot')).write_bytes(p.read_bytes())
# Full successor publishes only the selected old fragments, not new source/library snapshots.
for p in B.iterdir():
 if p.is_file() and (p.suffix in ['.raw','.lf']):
  (O/p.name).write_bytes(p.read_bytes())
for n in ['source-contract.json','hypothesis-contract.json','primary-formula-inventory.json','parent-status.json','creation-dependencies.json']:(O/n).write_bytes((B/n).read_bytes())
g=js(B/'source-proof-graph.json');before=copy.deepcopy(g);pv=js(B/'selected-providers.json');cv=js(B/'source-coverage.json');ci=js(B/'caller-inventory.json');lx=js(B/'lexical-inventory.json')
pidx=next(i for i,p in enumerate(pv) if p['id']=='open-positive-nezero-instance');old=copy.deepcopy(pv[pidx]);src=pathlib.Path(old['path']);raw=src.read_bytes();lines=raw.splitlines(keepends=True)
assert pin(src)['raw_sha256']==old['raw_sha256']
start=sum(map(len,lines[:49]));line=lines[49];assert line.decode().strip()=='instance (priority := 100) [Nonempty X] : NeZero μ :='
# The final assignment on this exact public line is declaration-level; priority option is earlier.
end=start+line.rfind(b':=');frag=raw[start:end]
assert frag.decode().strip()=='instance (priority := 100) [Nonempty X] : NeZero μ'
(O/'original.open-positive-nezero-instance.raw.snapshot').write_bytes((B/'open-positive-nezero-instance.raw').read_bytes())
(O/'open-positive-nezero-instance.raw').write_bytes(frag);(O/'open-positive-nezero-instance.lf').write_bytes(lf(frag))
pv[pidx].update(start_utf8_byte0=start,end_utf8_byte0_exclusive=end,fragment_raw_sha256=sha(frag),fragment_lf_sha256=sha(lf(frag)),inherited_context_provider='open-positive-nezero-context',selection_boundary='Full anonymous public instance header, including priority option; stop before declaration-level :=. Proof unexpanded.')
cstart=sum(map(len,lines[:41]));cend=cstart+len(lines[41]);cfrag=raw[cstart:cend]
assert cfrag.decode().strip()=='variable [IsOpenPosMeasure μ] {s U F : Set X} {x : X}'
context=dict(id='open-positive-nezero-context',node='P53.volNe0',kind='public-typing-context',physical_lines1=[42,42],start_utf8_byte0=cstart,end_utf8_byte0_exclusive=cend,fragment_raw_sha256=sha(cfrag),fragment_lf_sha256=sha(lf(cfrag)),body_selected=False,external_expansion_boundary=False,selection_boundary='Exact inherited public IsOpenPosMeasure context at physical42; bound Set/X variables, no proof body',**pin(src))
pv.append(context);(O/'open-positive-nezero-context.raw').write_bytes(cfrag);(O/'open-positive-nezero-context.lf').write_bytes(lf(cfrag))
covidx=next(i for i,x in enumerate(cv) if x['provider']=='open-positive-nezero-instance');oldcov=copy.deepcopy(cv[covidx]);cv[covidx].update(utf8_byte_start0=start,utf8_byte_end0_exclusive=end,utf8_column_start0=0,utf8_column_end0_exclusive=end-start,reason='Exact full anonymous public instance contract; priority assignment retained, proof assignment excluded')
cv.append(dict(provider=context['id'],path=str(src),physical_line1=42,physical_line0=41,classification='NODE',node='P53.volNe0',reason='Actual inherited IsOpenPosMeasure context supplies the instance prerequisite; no new target binder',fragment_row0=0,utf8_byte_start0=cstart,utf8_byte_end0_exclusive=cend,utf8_column_start0=0,utf8_column_end0_exclusive=cend-cstart))
new_call=[];new_lex=[];ops=[]
resolution={'Nonempty':'D53.Nonempty','NeZero':'D53.NeZero','IsOpenPosMeasure':'D53.OpenPos','Set':'D53.Set'}
existing={(x['utf8_byte_start0'],x['utf8_byte_end0_exclusive']) for x in lx if x['provider']==old['id']}
for provider,base,fragment,line1 in [(old['id'],start,frag,50),(context['id'],cstart,cfrag,42)]:
 for m in re.finditer(r'[A-Za-z_α-ωΑ-Ω𝕜ℝ][A-Za-z0-9_α-ωΑ-Ω𝕜ℝ]*(?:\.[A-Za-z_][A-Za-z0-9_\']*)*',fragment.decode()):
  tok=m.group();s=base+len(fragment.decode()[:m.start()].encode());e=base+len(fragment.decode()[:m.end()].encode())
  if provider==old['id'] and (s,e) in existing:continue
  dest=resolution.get(tok);item=dict(index0=len(lx),provider=provider,consumer='P53.volNe0',physical_line1=line1,physical_line0=line1-1,utf8_byte_start0=s,utf8_byte_end0_exclusive=e,utf8_column_start0=s-base,utf8_column_end0_exclusive=e-base,token=tok,classification='primitive-contract-reference' if dest else 'bound-identifier-or-syntax',resolution=dest)
  lx.append(item);new_lex.append(item)
  if dest:
   caller=dict(index0=len(ci),lexical_index0=item['index0'],provider=provider,consumer='P53.volNe0',physical_line1=line1,physical_line0=line1-1,utf8_byte_start0=s,utf8_byte_end0_exclusive=e,utf8_column_start0=s-base,utf8_column_end0_exclusive=e-base,token=tok,resolution=dest,classification='public-contract-definition-use');ci.append(caller);new_call.append(caller)
   # Preserve existing mathematical edges and add their precise real caller binding, rather than duplicate premises.
   reuse=next((x for x in g['edges'] if x['ingredient']==dest and x['consumer']=='P53.volNe0'),None)
   if reuse:
    assert 'caller_index0' not in reuse;reuse['caller_index0']=caller['index0'];ops.append(dict(op='add',path='/edges/'+str(g['edges'].index(reuse))+'/caller_index0',value=caller['index0'],reason='Attach exact newly selected public token to existing truthful ingredient edge; no extra premise'))
   else:
    edge=dict(id='E53.'+str(len(g['edges'])),ingredient=dest,consumer='P53.volNe0',kind='public-contract-definition-use',reason='Exact repaired header/context token; primitive contract, not an implementation call or target premise',compiled53call=False,caller_index0=caller['index0']);g['edges'].append(edge);ops.append(dict(op='append',path='/edges',value=edge))
assert g['nodes']==before['nodes'];assert len(g['edges'])==256
for i,(a,b) in enumerate(zip(before['edges'],g['edges'])):
 aa=copy.deepcopy(b);aa.pop('caller_index0',None) if 'caller_index0' not in a else None
 assert aa==a,i
assert len(new_call)==4
for x in new_lex+new_call:assert raw[x['utf8_byte_start0']:x['utf8_byte_end0_exclusive']].decode()==x['token']
ops.insert(0,dict(op='replace',path='/selected-providers/'+str(pidx),before=old,after=pv[pidx],reason='T53-1 repair declaration-level assignment boundary only'))
ops.append(dict(op='append',path='/selected-providers',value=context));ops.append(dict(op='replace',path='/source-coverage/'+str(covidx),before=oldcov,after=cv[covidx]));ops.append(dict(op='append',path='/source-coverage',value=cv[-1]));ops.append(dict(op='append',path='/caller-inventory',values=new_call));ops.append(dict(op='append',path='/lexical-inventory-and-selected-token-inventory',values=new_lex))
dump('source-proof-graph.json',g);dump('selected-providers.json',pv);dump('source-coverage.json',cv);dump('caller-inventory.json',ci);dump('lexical-inventory.json',lx);dump('selected-token-inventory.json',lx)
counts=dict(nodes=len(g['nodes']),edges=len(g['edges']),providers=len(pv),coverage_rows=len(cv),NODE=sum(x['classification']=='NODE' for x in cv),EXCLUDED=sum(x['classification']=='EXCLUDED' for x in cv),callers=len(ci),lexemes=len(lx),primary_formulae=len(js(B/'primary-formula-inventory.json')),compiler_invocations=0)
dump('counts.json',counts);dump('overlay-operations.json',dict(schema='minimal-representation-overlay53/v1',repair='T53-1 only',original_counts=js(B/'counts.json'),successor_counts=counts,operations=ops,unchanged='All79 nodes; all254 original edge contents except exact caller_index0 attachments to E53.11 andE53.12. Append only2 primitive-to-instance edges. All unrelated providers/coverage/lexemes/callers/formulas/source hypotheses/conclusions/signature/parents unchanged.',header_scope='Full OpenPos50 instance header and true inherited42 context; proof body excluded',no_mathematical_delta=True,no_target_binder_delta=True,source_topology_admitted=False))
inputs.append(pin(src));dump('input-bindings.json',inputs)
dump('overlay-contract.json',dict(schema='sourcegraph53-representation-overlay-contract/v1',status='CREATED_FOR_DISTINCT_REPAIRED_TOPOLOGY_REVIEW',original_negative=pin(neg),negative_actual_CLOSED_lease=pin(nl),original_creator_actual_CLOSED_lease=pin(B/'lease.json'),actual_overlay_lease='lease.json, separate OPEN before reads/Python/write; CLOSED last',target_lf_sha256=pin(P/'prospective-statement.txt')['lf_sha256'],repair='Option assignment priority:= was falsely treated as proof boundary; full actual header/context now pinned. NeZero output and Nonempty/OpenPos/Set typing caller edges are real selected tokens.',internal_nonempty='NormedAddCommGroup E supplies vector zero and hence Nonempty; no new target premise',exposure='Original graph creator/prior APIs/bodies/accidental metadata known; original negative first read in this lease. Only OpenPos42/50 source syntax read, no proof body/compiler/future53 implementation/new mathematics/source self-admission.',counts=counts,hash_recipe='Physical SHA256 exact raw bytes; LF CRLF->LF only. Native logical run entire object minus run_sha256 sorted compact UTF8 ensure_ascii=False allow_nan=False, no newline. Byte spans0-based rawUTF8 end-exclusive; physical lines1-based.'))
# Structural bookkeeping only; distinct phase must admit source topology.
dump('creator-bookkeeping-checks.json',dict(kind='RAW_BYTE_AND_PREFIX_ARITHMETIC_ONLY_NOT_SELF_TOPOLOGY_ADMISSION',node_prefix_unchanged=True,old_edges_unchanged_except_two_caller_bindings=True,original_inputs_preserved=True,new_token_spans_match=True,proof_or_compiler_run=False))
lease=js(O/'lease.json');lease.update(read='CLOSED',write='CLOSED',python='CLOSED',compiler='NOT_STARTED_CLOSED',closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),last_filesystem_operation='This actual CLOSED lease write follows all artifacts/pins/run/capsule',source_topology_admitted=False);lb=enc(lease);lh=sha(lb)
caps='''Representation-only overlay53 CLOSED for separate independent repair review.

Sole T53-1: OpenPos.lean50 now selects the full `instance (priority := 100) [Nonempty X] : NeZero μ` header, stopping before its declaration-level assignment. Actual inherited `IsOpenPosMeasure μ` context42 is selected separately; proof body remains opaque. Existing Nonempty/OpenPos ingredient edges receive exact caller bindings, while NeZero output and Set context obtain2 new primitive edges. No new target binder: vector zero supplies Nonempty internally.

Original79nodes/254edges and negative remain immutable. Successor counts: '''+json.dumps(counts)+'''. Exact758 signature, mathematics, source formulas,3opaque parents, normalization and residual rough/main/cost boundaries remain unchanged. Minimal operations and full successor inventories are in overlay-operations.json and source-proof-graph.json; raw/LF original/negative/statement pins and native recipes are in input-bindings.json/overlay-contract.json/run.json.

Actual separate CLOSED lease SHA256 '''+lh+'''. No compiler/proof/claim/canonical changes or creator repair admission. Distinct phase reviewer required.
'''
(O/'capsule.md').write_bytes(caps.encode())
outputs=[pin(p) for p in sorted(O.iterdir()) if p.is_file() and p.name not in ['lease.json','run.json']]
run=dict(schema='native-sourcegraph53-overlay-run/v1',result='MINIMAL_T53_1_OVERLAY_CLOSED_FOR_DISTINCT_REVIEW',inputs=inputs,outputs=outputs,counts=counts,compiler_invocations=0,theorem_credit=False,source_topology_admitted=False,actual_lease=dict(path=str(O/'lease.json'),raw_bytes=len(lb),lf_bytes=len(lb),raw_sha256=lh,lf_sha256=lh,status='CLOSED',historical=False),historical_leases='Original creator/negative reviewer immutable CLOSED inputs; distinct from actual overlay lease',hash_recipe='SHA256 UTF8 sorted compact JSON entire object minus run_sha256, ensure_ascii=False allow_nan=False, no newline')
run['run_sha256']=sha(json.dumps(run,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode());dump('run.json',run)
receipt=dict(CLOSED=True,counts=counts,graph=pin(O/'source-proof-graph.json'),operations=pin(O/'overlay-operations.json'),run=pin(O/'run.json'),logical_run_sha256=run['run_sha256'],actual_lease_rawLF_sha256=lh)
# MUST be the final filesystem operation.
(O/'lease.json').write_bytes(lb)
print(json.dumps(receipt,ensure_ascii=False))
