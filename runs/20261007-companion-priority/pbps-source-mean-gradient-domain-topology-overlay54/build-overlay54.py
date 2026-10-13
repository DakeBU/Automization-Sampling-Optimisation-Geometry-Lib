import pathlib, json, hashlib, re, copy, datetime

R=pathlib.Path('E:/Samplinglib')
O=R/'runs/20261007-companion-priority/pbps-source-mean-gradient-domain-topology-overlay54'
B=R/'runs/20261007-companion-priority/pbps-source-mean-gradient-domain-sourcegraph54'
N=R/'runs/20261007-companion-priority/pbps-source-mean-gradient-domain-topology-review54'
P=R/'runs/20261007-companion-priority/pbps-source-mean-gradient-domain-preproof54'
def sha(b): return hashlib.sha256(b).hexdigest()
def lf(b): return b.replace(b'\r\n',b'\n')
def readj(p): return json.loads(p.read_text(encoding='utf-8'))
def writej(name,d): (O/name).write_bytes((json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
inputs=[]
def pin(p,role,expected=None):
    p=pathlib.Path(p); b=p.read_bytes()
    if expected: assert sha(b)==expected,(p,sha(b))
    assert b'\r' not in lf(b), ('lone CR',p)
    x={'path':str(p),'role':role,'raw_bytes':len(b),'lf_bytes':len(lf(b)),'raw_sha256':sha(b),'lf_sha256':sha(lf(b))}
    if not any(v['path']==str(p) for v in inputs): inputs.append(x)
    return b
pin(N/'source-topology-review.json','original independent CLOSED negative','94a67e263ea984782b2ad9effb77e3ec2bc36be5968bacd53359a3569b8f52e2')
pin(N/'reviewer.topology.lease.json','actual historical reviewer lease','724e82a21debd356ae891a97d164b1d476ad306b984150de59f00917053eb667')
assert all(readj(N/'reviewer.topology.lease.json').get(k)!='OPEN' for k in ['read','write','python'])
names=['source-proof-graph.json','selected-providers.json','source-coverage.json','caller-inventory.json','lexical-inventory.json','selected-token-inventory.json','source-contract.json','hypothesis-contract.json','primary-formula-inventory.json','run.json','lease.json']
for name in names: pin(B/name,'immutable original creator artifact')
pin(P/'prospective-statement.txt','unchanged exact statement')
assert sha(lf((P/'prospective-statement.txt').read_bytes()))=='19de42336148aa900917e6c77753325145d6010dfd1718c1625b2b9a8f7ce595'
pin(P/'statement-seals.accepted.json','adopted exact StatementSeal')
g=readj(B/'source-proof-graph.json'); providers=readj(B/'selected-providers.json'); coverage=readj(B/'source-coverage.json'); callers=readj(B/'caller-inventory.json'); lex=readj(B/'lexical-inventory.json')
original=copy.deepcopy({'graph':g,'providers':providers,'coverage':coverage,'callers':callers,'lexical':lex})
(O/'fragments').mkdir(exist_ok=True)
fragmentpins=[]; operations=[]
def provider(pid,node,rel,lo,hi,kind='external-public-header',**extra):
    p=R/'.lake/packages/mathlib/Mathlib'/rel; data=pin(p,'affected pinned public source; body unexpanded'); lines=data.splitlines(keepends=True)
    start=sum(map(len,lines[:lo-1])); end=sum(map(len,lines[:hi]))-len(lines[hi-1])+len(lines[hi-1].rstrip(b'\r\n'))
    frag=data[start:end]; (O/'fragments'/ (pid+'.raw.txt')).write_bytes(frag); (O/'fragments'/(pid+'.lf.txt')).write_bytes(lf(frag))
    x={'id':pid,'node':node,'kind':kind,'path':str(p),'physical_lines1':[lo,hi],'start_utf8_byte0':start,'end_utf8_byte0_exclusive':end,'fragment_raw_sha256':sha(frag),'fragment_lf_sha256':sha(lf(frag)),'whole_raw_sha256':sha(data),'whole_lf_sha256':sha(lf(data)),'body_selected':False,'external_expansion_boundary':True,'header_complete':True}
    x.update(extra); fragmentpins.append(x); return x
def replace_provider(pid,new):
    i=next(i for i,x in enumerate(providers) if x['id']==pid); old=copy.deepcopy(providers[i]); providers[i]=new; operations.append({'operation':'replace-provider','id':pid,'before':old,'after':new}); return old
def edge(ingredient,consumer,kind,reason,**kw):
    x={'id':'E54.overlay.'+str(sum(e['id'].startswith('E54.overlay.') for e in g['edges'])),'ingredient':ingredient,'consumer':consumer,'kind':kind,'reason':reason,'compiled54call':False}; x.update(kw);g['edges'].append(x)
def node(nid,qname,contract):
    x={'id':nid,'kind':'external-unexpanded-primitive','contract':contract,'qualified_id':qname,'compiled54':False,'proof_body_expanded':False};g['nodes'].append(x)
def mutate_node(nid,**kw):
    x=next(x for x in g['nodes'] if x['id']==nid); old=copy.deepcopy(x);x.update(kw);operations.append({'operation':'update-node','id':nid,'before':old,'after':copy.deepcopy(x)})
def rows(prov,excluded=None):
    excluded=excluded or {}; data=pathlib.Path(prov['path']).read_bytes(); lines=data.splitlines(keepends=True); lo,hi=prov['physical_lines1']
    for line in range(lo,hi+1):
        if any(x['provider']==prov['id'] and x['physical_line1']==line for x in coverage):continue
        b=lines[line-1].rstrip(b'\r\n');start=sum(map(len,lines[:line-1])); cls,reason=excluded.get(line,('NODE','Exact added public declaration/generation/context; external implementation boundary'))
        coverage.append({'provider':prov['id'],'path':prov['path'],'physical_line1':line,'physical_line0':line-1,'utf8_byte_start0':start,'utf8_byte_end0_exclusive':start+len(b),'utf8_column_start0':0,'utf8_column_end0_exclusive':len(b),'classification':cls,'node':prov['node'] if cls=='NODE' else None,'reason':reason,'raw_line_sha256':sha(b)})
rx=re.compile(r'[^\W\d]\w*(?:\.[^\W\d]\w*)*', re.UNICODE)
def lexical(prov,resolutions=None,decl=None,excludedlines=None):
    resolutions=resolutions or {};excludedlines=excludedlines or {}; data=pathlib.Path(prov['path']).read_bytes(); lines=data.splitlines(keepends=True)
    for line in range(prov['physical_lines1'][0],prov['physical_lines1'][1]+1):
        text=lines[line-1].rstrip(b'\r\n').decode('utf-8');start=sum(map(len,lines[:line-1]))
        for m in rx.finditer(text):
            a=start+len(text[:m.start()].encode('utf8'));b=start+len(text[:m.end()].encode('utf8'));t=m.group()
            if any(x['provider']==prov['id'] and x['utf8_byte_start0']==a and x['utf8_byte_end0_exclusive']==b for x in lex):continue
            resolution=resolutions.get(t); cls='primitive-public-reference' if resolution else 'bound-identifier-or-syntax'
            if t==decl:cls='declaration-name-binding';resolution=None
            if t in ['Add','SMul','One']:cls='explicit-external-unexpanded-type-hierarchy-boundary';resolution=None
            if line in excludedlines:cls=excludedlines[line];resolution=None
            if prov['id']=='primitive-compact' and line in [213,214,215]:
                cls='generation-attribute-syntax' if t=='to_additive' else 'EXCLUDED-generation-doc-comment';resolution=None
            x={'index0':len(lex),'provider':prov['id'],'consumer':prov['node'],'physical_line1':line,'physical_line0':line-1,'utf8_byte_start0':a,'utf8_byte_end0_exclusive':b,'utf8_column_start0':a-start,'utf8_column_end0_exclusive':b-start,'token':t,'classification':cls,'resolution':resolution,'composite_projections':[]};lex.append(x)
            if resolution:
                c=dict(x);c['index0']=len(callers);callers.append(c);edge(resolution,prov['node'],'public-header-or-context-reference','Exact selected public header/context token; not compiled54 call',caller_index0=c['index0'],provider=prov['id'])

# T54-1: retain wrong Core exposure as excluded, and select actual class header.
uniform=provider('type-leaf-UniformSpace','X54.type.UniformSpace','Topology/UniformSpace/Defs.lean',193,193,kind='external-unexpanded-type-boundary',inherited_context='extends TopologicalSpace alpha; remaining class fields external-unexpanded')
old=replace_provider('type-leaf-UniformSpace',uniform)
old['id']='incidental-UniformSpace-Core';old['node']=None;old['kind']='incidental-excluded';old['header_complete']=False;old['reason']='Original wrong identity retained as incidental exposure, not UniformSpace provider'
providers.append(old)
data=pathlib.Path(old['path']).read_bytes(); f=data[old['start_utf8_byte0']:old['end_utf8_byte0_exclusive']];(O/'fragments'/'incidental-UniformSpace-Core.raw.txt').write_bytes(f);(O/'fragments'/'incidental-UniformSpace-Core.lf.txt').write_bytes(lf(f))
for a in [coverage,lex]:
    for x in a:
        if x['provider']=='type-leaf-UniformSpace':
            x['provider']=old['id'];x['classification']='EXCLUDED' if a is coverage else 'EXCLUDED-incidental-wrong-identity'
            if a is coverage:x['node']=None;x['reason']='Core129 is unrelated to selected actual UniformSpace193 identity; original exposure retained'
            else:x['resolution']=None
mutate_node('X54.type.UniformSpace',contract='Actual class UniformSpace at Defs.lean193 extends TopologicalSpace; full class fields and deeper hierarchy explicitly external-unexpanded')
rows(uniform);lexical(uniform,{'TopologicalSpace':'D54.TopologicalSpace'},decl='UniformSpace')

# T54-2: generation carrier and inherited variables; output is additive generated definition.
compact=provider('primitive-compact','D54.compact','Topology/Algebra/Support.lean',213,217,kind='generated-additive-definition-carrier',carrier_qualified_id='HasCompactMulSupport',generated_output_qualified_id='HasCompactSupport',generation_attribute='to_additive',body_selected=True,body_expansion_boundary='Carrier definition RHS217 pinned only; lexical body excluded. Generated additive output has IsCompact(tSupport f); no proof copy.')
replace_provider('primitive-compact',compact)
mutate_node('D54.compact',kind='generated-additive-primitive',contract='HasCompactSupport is generated by to_additive213-215 from HasCompactMulSupport216-217. Additive contract: compact closure of support; Zero codomain replaces One. Generated definition body and deeper primitive hierarchy remain external-unexpanded.')
edge('X54.type.HasCompactMulSupport','D54.compact','generated-additive-definition','Actual to_additive carrier213-217; generation provenance, not theorem implication')
rows(compact,{217:('EXCLUDED','Pinned carrier RHS as generation provenance; implementation body outside selected public-header expansion')})
lexical(compact,excludedlines={217:'EXCLUDED-unexpanded-definition-body'})
ctx=provider('compact-generation-context','X54.type.HasCompactMulSupport','Topology/Algebra/Support.lean',207,208,kind='context-public',generated_context='Used carrier slots TopologicalSpace alpha and One beta translate to TopologicalSpace alpha and Zero beta; unused ambient alpha-prime/gamma/delta variables are not new output premises')
providers.append(ctx);rows(ctx);lexical(ctx,{'TopologicalSpace':'D54.TopologicalSpace'})

# T54-3: ambient topological vector-space slots for all closure consumers.
node('X54.type.ContinuousAdd','ContinuousAdd','Actual class ContinuousAdd: ambient addition jointly continuous; deeper Add hierarchy and fields external-unexpanded')
node('X54.type.ContinuousSMul','ContinuousSMul','Actual class ContinuousSMul: ambient scalar action jointly continuous; deeper SMul hierarchy and fields external-unexpanded')
node('A54.closureAmbientInstances',None,'Internal standard real/Lp normed-space topology supplies ContinuousAdd on both Lp spaces and ContinuousSMul real on both. Existing51 full closability and actual C1 adapter public contracts already elaborate these ambient types. Instance elaboration is an explicit external-unexpanded boundary, not a new caller certificate; finite position E does not make Lp finite-dimensional.')
for pid,nid,rel,lo,hi,decl in [('type-leaf-ContinuousAdd','X54.type.ContinuousAdd','Topology/Algebra/Monoid/Defs.lean',42,42,'ContinuousAdd'),('type-leaf-ContinuousSMul','X54.type.ContinuousSMul','Topology/Algebra/MulAction.lean',46,47,'ContinuousSMul')]:
    q=provider(pid,nid,rel,lo,hi,kind='external-unexpanded-type-boundary');providers.append(q);rows(q);lexical(q,{'TopologicalSpace':'D54.TopologicalSpace'},decl=decl)
ctx=provider('closure-continuity-context','D54.closable','Topology/Algebra/Module/LinearPMap.lean',66,67,kind='context-public',consumers=['D54.closable','D54.closure','P54.closureGraph'],instance_supply_boundary='Internal standard real/Lp topology, external-unexpanded; no additional public binder')
providers.append(ctx);rows(ctx);lexical(ctx,{'ContinuousAdd':'X54.type.ContinuousAdd','ContinuousSMul':'X54.type.ContinuousSMul','TopologicalSpace':'D54.TopologicalSpace'})
for target in ['D54.closable','D54.closure','P54.closureGraph']:
    for source in ['X54.type.ContinuousAdd','X54.type.ContinuousSMul','D54.TopologicalSpace','A54.closureAmbientInstances']:
        edge(source,target,'inherited-ambient-class-slot','Actual inherited66-67 applies to graph closure/closability and subsequent closure; supplied inside real/Lp types')
for source in ['D54.Lp','X54.type.NormedSpace','D54.TopologicalSpace']:
    assert any(n['id']==source for n in g['nodes']),source
    edge(source,'A54.closureAmbientInstances','external-unexpanded-instance-supply','Standard existing real/Lp normed topology; no guessed generated instance name or parent proof expanded')

g['representation_overlay']={'schema':'minimal-topology-overlay54/v1','repairs':['T54-1','T54-2','T54-3'],'topology_admitted':False,'mathematical_statement_changed':False,'original_graph_sha256':sha((B/'source-proof-graph.json').read_bytes()),'negative_receipt_sha256':sha((N/'source-topology-review.json').read_bytes())}
operations.extend([{'operation':'append-nodes','nodes':g['nodes'][len(original['graph']['nodes']):]},{'operation':'append-edges','edges':g['edges'][len(original['graph']['edges']):]},{'operation':'append-providers','providers':providers[len(original['providers']):]}])
for key,now in [('coverage',coverage),('lexical',lex),('callers',callers)]:
    before=original[key]; changed=[{'index0':i,'before':before[i],'after':now[i]} for i in range(len(before)) if before[i]!=now[i]]
    operations.append({'operation':'inventory-delta','inventory':key,'changed_original_rows':changed,'appended_rows':now[len(before):]})
writej('overlay-operations.json',{'scope':'Only T54-1/T54-2/T54-3 representation repairs; original bytes and exact statement/math assumptions unchanged','operations':operations})
for name,data in [('source-proof-graph.json',g),('selected-providers.json',providers),('source-coverage.json',coverage),('caller-inventory.json',callers),('lexical-inventory.json',lex),('selected-token-inventory.json',lex)]:writej(name,data)
writej('added-public-fragment-bindings.json',fragmentpins)
writej('input-bindings.json',inputs)
writej('exposure-and-boundaries.json',{'prior':'Original54 sourcegraph, historical49/50 wholeproof and parent source/API exposure remain disclosed; not source-blind','new':'Only original negative/affected inventories and selected actual public headers/generation/context. No primary reread, proof54, parent proof copy, compiler or verdict admission. Full source files byte-hashed only; semantics decoded only selected displayed lines.','failed_retrievals':[{'attempt':0,'error':'Inventory inspector mistakenly used dict.get on provider list; AttributeError; read only, no artifact changed'},{'attempt':1,'error':'Missing Analysis/Normed/Module/Defs.lean and GBK stdout on comment print; retained diagnosis; corrected UTF8 print and explicitly external-unexpanded normed-instance supply, no guessed instance'}],'instance_boundary':'ContinuousAdd E/F, TopologicalSpace R, ContinuousSMul R E/F are inherited primitive ambient contracts, not public theorem54 premises. Standard actual Lp/real normed topology supplies them internally; no finite-dimensional Lp claim.','unchanged_residuals':'Paper weak-H1 equivalence, all-rough B13, Gamma/main/cost remain unchanged residuals','compiler':'NOT_STARTED_CLOSED','self_topology_admission':False})
counts={'nodes':len(g['nodes']),'edges':len(g['edges']),'providers':len(providers),'coverage':len(coverage),'callers':len(callers),'lexemes':len(lex),'original':{'nodes':126,'edges':547,'providers':120,'coverage':442,'callers':494,'lexemes':2315}}
writej('counts.json',counts)
# Bookkeeping validation is only byte/inventory consistency, not topology review/admission.
nodeids={x['id'] for x in g['nodes']};assert len(nodeids)==len(g['nodes'])
assert all(e['ingredient'] in nodeids and e['consumer'] in nodeids for e in g['edges'])
for pr in providers:
    b=pathlib.Path(pr['path']).read_bytes();f=b[pr['start_utf8_byte0']:pr['end_utf8_byte0_exclusive']];assert sha(f)==pr['fragment_raw_sha256'];assert sha(lf(f))==pr['fragment_lf_sha256']
    selected={x['physical_line1'] for x in coverage if x['provider']==pr['id']};assert selected==set(range(pr['physical_lines1'][0],pr['physical_lines1'][1]+1)),pr['id']
for c in callers:
    assert any(e.get('caller_index0')==c['index0'] and e['ingredient']==c['resolution'] and e['consumer']==c['consumer'] for e in g['edges']),c
for c in lex:
    if c['resolution'] and c['classification']=='primitive-public-reference':
        assert any(x['provider']==c['provider'] and x['utf8_byte_start0']==c['utf8_byte_start0'] and x['resolution']==c['resolution'] for x in callers),c
writej('creator-byte-bookkeeping.json',{'exact_original_prefix_except_explicit_operations':True,'all_successor_provider_fragments_match_actual_bytes':True,'selected_provider_line_coverage_exhaustive':True,'all_callers_have_ingredient_edges':True,'all_resolved_lexemes_have_callers':True,'topology_admission':False,'note':'Mechanical consistency only; creator cannot independently admit representation repairs'})
print(json.dumps(counts))
