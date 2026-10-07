# -*- coding: utf-8 -*-
import pathlib,json,hashlib,re,sys
sys.stdout.reconfigure(encoding='utf-8');r=pathlib.Path('E:/Samplinglib');d=r/'runs/20261007-companion-priority/pbps-outer-gradient-sourcegraph49';H=lambda b:hashlib.sha256(b).hexdigest();graph=json.loads((d/'source-proof-graph.json').read_text(encoding='utf-8'));nm={n['id']:n for n in graph['nodes']};providers=json.loads((d/'selected-providers.json').read_text(encoding='utf-8'));anchors=json.loads((d/'primary-balanced-inventory.json').read_text())['anchors'];coverage={};callers=[];tokens=[]
# Add explicitly unexpanded named semantics encountered in contracts.
for i,q,c in [('P.prob','MeasureTheory.IsProbabilityMeasure','Probability/finite-law typing predicate; actual target outputs internally produced'),('P.sqrt','Real.sqrt','Actual generative sqrtη scale'),('P.norm','norm','Norm squared energy and Hessian forms'),('P.volume','MeasureTheory.volume','Canonical Euclidean additive Haar volume; rank0 included'),('P.mathlib-variance','ProbabilityTheory.variance','Mathlib evariance.toReal, bridged to local integral variance on actual domains'),('P.AE','ae','AE representative equality/AE-measurability vocabulary, not an assumed law version')]:
 graph['nodes'].append(dict(id=i,kind='external-unexpanded-primitive',qualified_id=q,contract=c));nm[i]=graph['nodes'][-1]
# Exhaustive physical primary line union of balanced selected anchors.
raw=pathlib.Path(anchors[0]['path']).read_bytes();lines=raw.splitlines(keepends=True)
anchor_nodes={}
for n in graph['nodes']:
 for a in n.get('primary_anchors',[]):anchor_nodes.setdefault(a,[]).append(n['id'])
for a in anchors:
 first,last=a['physical_lines1']
 for line in range(first,last+1):
  key=(a['path'],line);part=lines[line-1].decode('utf-8');rec=coverage.setdefault(key,dict(path=a['path'],physical_line1=line,classification='EXCLUDED',reason='HTML layout, labels, blank lines or wrappers; not an independent mathematical ingredient',anchor_ids=[],node_ids=[],physical_line_raw_sha256=H(lines[line-1])))
  rec['anchor_ids'].append(a['id'])
  # Physical paragraph continuation text plus all math annotation rows are substantive.
  plain=re.sub(r'<[^>]+>','',part).strip()
  if '<math ' in part or '<p ' in part or (plain and not plain.startswith('(C.2)') and not plain.startswith('(B.13)') and not part.lstrip().startswith('<')):
   rec.update(classification='NODE',reason='Printed mathematical definition/hypothesis/formula/proof sentence or explicitly typed outside-target residual')
   rec['node_ids']=sorted(set(rec['node_ids']+anchor_nodes.get(a['id'],[])))
  if line==358:rec['inline_excluded']=['kappa=beta/alpha: conditioning notation unused by49']
  if line in [637,638]:rec['inline_excluded']=['Marginal potential U_eta naming: no curvature/PI/spectral claim is imported']
  if a['id']=='A2.E13':rec['residual_boundary']='AllL2 weightedH1 and literal Gamma/operator identity are source residuals, not established49outputs.'
# Whole selected provider fragments, exact byte selection including partial terminal line before proof.
for p in providers:
 b=pathlib.Path(p['path']).read_bytes();part=(d/(p['snapshot']+'.raw')).read_bytes();lo=sum(len(v) for v in b.splitlines(keepends=True)[:p['physical_lines1'][0]-1]);start=b.find(part,lo);assert start>=0
 end=start+len(part);p['start_utf8_byte0']=start;p['end_utf8_byte0_exclusive']=end
 first=b[:start].count(b'\n')+1;last=b[:end-1].count(b'\n')+1;p['selected_physical_lines1']=[first,last]
 p['end_column0_utf8']=len(b[:end].split(b'\n')[-1]);p['selection_scope']='Exact selected fragment; trailing proof text on terminal physical line excluded.'
 if p['id'].startswith('parent-'):owner={'parent-ConditionalGradientVariance':'A.48','parent-GibbsAugmentation':'A.Gibbs','parent-GaussianReflection':'A.reflection'}[p['id']]
 elif p['id'].startswith('api-'):owner=p['id'][4:]
 else:owner=p['id'][9:]
 plines=b.splitlines(keepends=True)
 for line in range(first,last+1):
  key=(p['path'],line);rec=coverage.setdefault(key,dict(path=p['path'],physical_line1=line,classification='NODE',reason='Selected public contract/definition/typing context; not provider proof coverage',provider_ids=[],node_ids=[],physical_line_raw_sha256=H(plines[line-1])))
  rec.setdefault('provider_ids',[]).append(p['id']);rec['node_ids']=sorted(set(rec['node_ids']+[owner]));rec['selected_fragment_byte_interval0']=[start,end]
  if not plines[line-1].strip():rec.update(classification='EXCLUDED',reason='Blank selected provider line')
 # Explicit named and notation vocabulary, not falsely labelled compiled calls.
 patterns=[(r'\bMeasure\.map\b','P.map','mathematical-reference'),(r'\.prod\b','P.prod','mathematical-reference'),(r'\bstdGaussian\b','P.stdGauss','mathematical-reference'),(r'\bgradient\b','D.gradient','mathematical-reference'),(r'Poincare\.variance\b','D.variance','mathematical-reference'),(r'\bfderiv\b','P.fderiv','mathematical-reference'),(r'\btoDual\b','P.Riesz','mathematical-reference'),(r'\.tilted\b','D.tilt','mathematical-reference'),(r'\.withDensity\b','P.withDensity','mathematical-reference'),(r'\bReal\.exp\b|\bexp\b','P.exp','mathematical-reference'),(r'\bENNReal\.ofReal\b','P.ofReal','mathematical-reference'),(r'\bReal\.sqrt\b','P.sqrt','mathematical-reference'),(r'\bvolume\b','P.volume','mathematical-reference'),(r'∫','P.integral','integral-notation-reference'),(r'\bVar\[','P.mathlib-variance','variance-notation-reference'),(r'\bIsCondKernel\b','P.disintegration','typing-reference'),(r'\bIsMarkovKernel\b','P.markov','typing-reference'),(r'\bIsProbabilityMeasure\b','P.prob','typing-reference'),(r'\b(MemLp|Integrable|AEStronglyMeasurable|StronglyMeasurable|SFinite|IsSFiniteKernel|ContDiff|HasCompactSupport|Differentiable|DifferentiableAt|FiniteDimensional|BorelSpace|MeasurableSpace|InnerProductSpace|NormedAddCommGroup|NormedSpace|Kernel)\b','P.typing','typing-reference')]
 t=part.decode('utf-8');linebase=first
 for patt,node,kind in patterns:
  for m in re.finditer(patt,t):
   before=t[:m.start()];line=linebase+before.count('\n');column_chars=len(before.split('\n')[-1]);charoffset=len(b[:start].decode('utf-8'))+m.start();byte0=start+len(before.encode());byte1=byte0+len(m.group().encode());rec=dict(caller_selected_provider=p['id'],caller_node=owner,caller_path=p['path'],caller_physical_line1=line,caller_column0_unicode=column_chars,caller_start_utf8_byte0=byte0,caller_end_utf8_byte0_exclusive=byte1,token=m.group(),resolved_node=node,qualified_id=nm[node].get('qualified_id'),classification=kind,compiled49caller=False,provider_body_selected=owner.startswith('D.'))
   tokens.append(rec)
   if node!=owner:
    callers.append(rec)
    edge=dict(from_node=node,to_node=owner,relation='selected-public-or-definition-reference',caller=dict(path=p['path'],line1=line,byte_interval0=[byte0,byte1]),classification=kind)
    if edge not in graph['edges']:graph['edges'].append(edge)
 # Generated class/instance projections are observed, not advertised as mathematical calls.
 if owner in ['P.markov','P.markov-instance','P.disintegration']:
  callers.append(dict(caller_selected_provider=p['id'],caller_node=owner,caller_path=p['path'],caller_span_lines1=[first,last],classification='generated-structure-field-or-instance-projection',compiled49caller=False,mathematical_call=False))
# Exact source href references observed in selected balanced bodies, internal or explicit out-of-scope.
for a in anchors:
 fragment=(d/(a['snapshot']+'.raw.html')).read_text(encoding='utf-8');base=a['physical_lines1'][0]
 for m in re.finditer(r'href="#([^"]+)"',fragment):
  target=m.group(1);rec=dict(caller_primary_anchor=a['id'],caller_path=a['path'],caller_physical_line1=base+fragment[:m.start()].count('\n'),source_reference=target,classification='printed-primary-reference',resolved_source_nodes=anchor_nodes.get(target,[]),compiled49caller=False)
  if not rec['resolved_source_nodes']:rec['resolution_boundary']='External unexpanded source context: retained reference, no new theorem claim.'
  callers.append(rec)
rows=[v for k,v in sorted(coverage.items())];assert all(v['node_ids'] for v in rows if v['classification']=='NODE');assert len(rows)==len(set((v['path'],v['physical_line1']) for v in rows))
(d/'selected-providers.json').write_text(json.dumps(providers,indent=2),encoding='utf-8');(d/'source-coverage.json').write_text(json.dumps(dict(scope='Union of exact selected physical source/provider rows, not whole file/library/paper',line_convention='One based physical LF lines; fragment intervals zero based UTF8 bytes, end exclusive; partial terminal lines explicitly limited to fragment interval',rows=rows),indent=2,ensure_ascii=False),encoding='utf-8');(d/'caller-inventory.json').write_text(json.dumps(dict(scope='Exact selected public/definition/source references and generated projections, not fabricated49implementation callers',provider_proof_bodies_selected=0,entries=callers),indent=2,ensure_ascii=False),encoding='utf-8');(d/'selected-token-inventory.json').write_text(json.dumps(dict(scope='Exhaustive configured named mathematical vocabulary and typing tokens WITHIN selected Lean fragments; not all Lean identifiers; integral/variance notation included',entries=tokens),indent=2,ensure_ascii=False),encoding='utf-8');(d/'source-proof-graph.json').write_text(json.dumps(graph,indent=2,ensure_ascii=False),encoding='utf-8');print(json.dumps(dict(nodes=len(graph['nodes']),edges=len(graph['edges']),rows=len(rows),NODE=sum(v['classification']=='NODE' for v in rows),EXCLUDED=sum(v['classification']=='EXCLUDED' for v in rows),callers=len(callers),tokens=len(tokens))))
