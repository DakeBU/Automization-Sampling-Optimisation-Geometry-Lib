# coding: utf-8
import pathlib,json,re,hashlib,copy,sys,html
sys.stdout.reconfigure(encoding='utf-8')
ROOT=pathlib.Path('E:/Samplinglib');BASE=ROOT/'runs/20261007-companion-priority';OUT=BASE/'pbps-macroscopic-energy-sourcegraph50';OLD=BASE/'pbps-outer-gradient-topology-overlay49'
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(name,x):(OUT/name).write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
g=j(OUT/'source-proof-graph.json');N={n['id']:n for n in g['nodes']};ps=j(OUT/'selected-providers.json')['new'];anchors=j(OUT/'primary-balanced-inventory.json')['new_anchors'];oldcov=j(OLD/'source-coverage.after.json');oldcalls=j(OLD/'caller-inventory.after.json');oldtokens=j(OLD/'selected-token-inventory.after.json');newrows={};entries=[];lex=[]
def row(path,line,start,end,classification,reason,provider,node):
 key=(str(path),line);data=path.read_bytes();ls=data.splitlines(keepends=True);offset=sum(map(len,ls[:line-1]));physical=ls[line-1]
 r=newrows.setdefault(key,dict(path=str(path),physical_line1=line,classification=classification,reason=reason,provider_ids=[],node_ids=[],physical_line_raw_sha256=sha(physical),selected_intervals_utf8_byte0=[]))
 r['provider_ids'].append(provider);r['node_ids'].append(node);r['selected_intervals_utf8_byte0'].append([start,end])
 if classification=='NODE':r['classification']='NODE';r['reason']='At least one exact selected fragment contains genuine source/contract/definition/typing content; nonselected trailing bytes are not authorized.'
def cover(p,primary=False):
 path=pathlib.Path(p['path']);data=path.read_bytes();ls=data.splitlines(keepends=True);offset=0
 for n,physical in enumerate(ls,1):
  st=max(offset,p['start_utf8_byte0']);en=min(offset+len(physical),p['end_utf8_byte0_exclusive']);offset+=len(physical)
  if en<=st:continue
  segment=data[st:en].decode().strip();nodeid=p.get('node_id','')
  cl='NODE';reason='Actual selected public statement/real definition or necessary typing contract; no provider proof body selected.'
  if not segment or segment.startswith('--') or segment.startswith('section ') or segment.startswith('namespace '):cl='EXCLUDED';reason='Blank/comment/namespace/section delimiter; not a mathematical call.'
  if p['id']=='typing-condExpL2' and 49<=n<=60:cl='EXCLUDED';reason='Ancillary Eprime/F/G section variables or comments not used by exact condExpL2; incidental typing context, no public premise.'
  if primary:
   if re.fullmatch(r'(?:</?[^>]+>\s*)+',segment):cl='EXCLUDED';reason='Selected balanced HTML structural delimiter only.'
   else:reason='Printed mathematical source definition/identity/domain in exact balanced anchor; parent compilation does not replace this source coverage.'
  row(path,n,st,en,cl,reason,p['id'],nodeid)
for p in ps:cover(p)
amap={'A2.E1':'S50.P','A2.E2':'S50.P','A2.SS1.p1.4':'S50.P','A2.SS1.p1.5':'S50.P','A2.SS1.p2.1':'S50.blocks','A2.E3':'S50.blocks','A2.SS1.p2.2':'S50.blocks','A2.SS1.p3.1':'S50.U','A2.E4':'S50.U','A2.SS1.p3.2':'S50.U','A2.Ex3':'S50.U','A2.SS1.p3.3':'S50.ABD','A2.E5':'S50.ABD'}
for a in anchors:cover(dict(a,node_id=amap[a['id']]),True)
keywords=set('theorem lemma def noncomputable protected class where namespace section variable let fun by haveI Type Prop inferInstance _ L SL ₗᵢ ₘ ₂ ¹ ᵐ that attr fun_prop to_additive to_fun'.split())
local=set('α β γ ε 𝕜 σ₁₂ E E₂ F G Gprime Eprime E\' G\' Ω M K R S J Λ ν μ ρ ρCond η V Tf P A B D U a c f g h hf hg hm hfm hφ hκ hα hαβ hV hH hη hβη m m0 mα mβ p s t u v x y z'.split())
definition_names=set('actual_macroscopic_gradient_energy_blocks reflected_conditional_gradient_energy macroscopic_reflection_smooth_representative actual_reflection_block_identities eq_condKernel_of_measure_eq_compProd ae_of_ae_map map_map ext inner_def real_inner_self_eq_norm_sq integral_congr_ae integral_map condExpL2 lpMeas IsCondKernel MemLp subtypeL toContinuousLinearMap comap congr const_smul mul stronglyMeasurable_one disintegrate'.split())
res={}
def resolve(tokens,node,q):
 for token in tokens.split('|'):res[token]=(node,q)
resolve('Measure.map|J.map|μ.map|map','P.map','MeasureTheory.Measure.map')
resolve('μ.prod','P.prod','MeasureTheory.Measure.prod');resolve('J.snd','P.snd','MeasureTheory.Measure.snd');resolve('ρ.fst|Λ.fst','P.fst','MeasureTheory.Measure.fst')
resolve('μ.tilted|tilted','D.tilt','MeasureTheory.Measure.tilted');resolve('gradient','D.gradient','gradient');resolve('fderiv','P.fderiv','fderiv');resolve('innerSL','P.Riesz','innerSL')
resolve('Real.sqrt','P.sqrt','Real.sqrt');resolve('volume','P.volume','MeasureTheory.Measure.volume');resolve('stdGaussian','P.stdGauss','ProbabilityTheory.stdGaussian')
resolve('AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance','D.variance','AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance')
resolve('Lp|Submodule|LinearIsometry|ContinuousLinearMap|star|IsSelfAdjoint','P50.operator-types','standard typed operator primitive; exact public parent/typecheck identity, unexpanded')
resolve('Function.Involutive','P50.operator-types','Function.Involutive');resolve('U.toContinuousLinearMap|toContinuousLinearMap','D50.isometryCLM','LinearIsometry.toContinuousLinearMap')
resolve('condExpL2','D50.condExpL2','MeasureTheory.condExpL2');resolve('lpMeas','D50.lpMeas','MeasureTheory.lpMeas');resolve('MemLp','D50.MemLp','MeasureTheory.MemLp')
resolve('MeasurableSpace.comap|comap','D50.comap','MeasurableSpace.comap');resolve('subtypeL','D50.subtypeL','Submodule.subtypeL')
resolve('IsCondKernel|Λ.IsCondKernel','D50.IsCondKernel','MeasureTheory.Measure.IsCondKernel');resolve('IsCondKernel.disintegrate','D50.IsCondKernel','MeasureTheory.Measure.IsCondKernel.disintegrate')
resolve('ρ.condKernel','P50.condunique','MeasureTheory.Measure.condKernel');resolve('orthogonalProjectionOnto','P50.orthProj','Submodule.orthogonalProjectionOnto')
resolve('measurable_snd.comap_le|Measurable|AEMeasurable|MeasurableSet','P50.measurable','actual measurability primitive in selected public contract, unexpanded')
resolve('AEStronglyMeasurable','P50.AE','MeasureTheory.AEStronglyMeasurable');resolve('eLpNorm','D50.MemLp','MeasureTheory.eLpNorm');resolve('Integrable','P.integral','MeasureTheory.Integrable')
resolve('IsProbabilityMeasure','P.prob','MeasureTheory.IsProbabilityMeasure');resolve('IsMarkovKernel','P.markov','ProbabilityTheory.IsMarkovKernel');resolve('Kernel','P.markov','ProbabilityTheory.Kernel')
resolve('IsFiniteMeasure|IsFiniteKernel','P50.condunique-context','MeasureTheory.IsFiniteMeasure / ProbabilityTheory.IsFiniteKernel')
resolve('hf.add','P50.AEadd','MeasureTheory.AEStronglyMeasurable.add');resolve('hf.const_smul','P50.AEsmul','MeasureTheory.AEStronglyMeasurable.const_smul');resolve('hf.congr|congr','P50.AEcongr','MeasureTheory.AEStronglyMeasurable.congr')
resolve('stronglyMeasurable_zero','P50.measzero','MeasureTheory.stronglyMeasurable_zero');resolve('Lp.coeFn_zero','P50.Lpzero','MeasureTheory.Lp.coeFn_zero');resolve('Lp.coeFn_add','P50.Lpadd','MeasureTheory.Lp.coeFn_add');resolve('Lp.coeFn_smul','P50.Lpsmul','MeasureTheory.Lp.coeFn_smul')
resolve('Prod.snd','P50.measurable','Prod.snd');resolve('Prod.swap','P50.measurable','Prod.swap');resolve('symm','P50.AE','Filter.EventuallyEq.symm (AE equality context)')
resolve('∫','P.integral','MeasureTheory.integral')
resolve('NormedAddCommGroup|InnerProductSpace|FiniteDimensional|MeasurableSpace|BorelSpace|ContDiff|Differentiable|HasCompactSupport|HasFDerivAt|TopologicalSpace|NormedSpace|CompleteSpace|RCLike|Nonempty|StandardBorelSpace|Semiring|AddCommMonoid|Module|Fact|Set|NNReal|ℝ|Measure|ContinuousConstSMul|ContinuousMul|Mul|One|SMul|StronglyMeasurable','P50.domain-types','standard typed class/domain/scalar primitive; retained unexpanded under actual parent and statement typechecks')
resolve('K.HasOrthogonalProjection','P50.orthProj-context','Submodule.HasOrthogonalProjection')
generated={'carrier','zero_mem\'','add_mem\'','smul_mem\'','toLinearMap','p.subtype','f.toLinearMap','f.continuous','MeasurableSet\'','IsCondKernel.disintegrate','disintegrate'}
namespace={'ProbabilityTheory','MeasureTheory.Measure','LpMeas'}
unresolved=set()
for p in ps:
 data=pathlib.Path(p['path']).read_bytes();st=p['start_utf8_byte0'];fragment=data[st:p['end_utf8_byte0_exclusive']].decode()
 def mask(m):return ''.join('\n' if c=='\n' else ' ' for c in m.group())
 masked=re.sub(r'/\-.*?\-/',mask,fragment,flags=re.S);masked=re.sub(r'--[^\r\n]*',mask,masked)
 spans=list(re.finditer(r"[^\W\d][\w']*(?:\.[^\W\d][\w']*)*",masked))
 # Real integral notation is a mathematical named reference, unlike syntax arrows/subscripts.
 spans+=list(re.finditer('∫',masked));spans.sort(key=lambda m:m.start())
 for m in spans:
  tok=m.group();start=st+len(fragment[:m.start()].encode());end=start+len(tok.encode());line=data[:start].count(b'\n')+1;linest=data.rfind(b'\n',0,start)+1
  r=dict(caller_selected_provider=p['id'],caller_node=p['node_id'],caller_path=p['path'],caller_physical_line1=line,caller_column0_utf8=start-linest,caller_column0_unicode=len(data[linest:start].decode()),caller_start_utf8_byte0=start,caller_end_utf8_byte0_exclusive=end,token=tok,compiled50caller=False,provider_mathematical_proof_body_selected=False)
  before=masked[:m.start()];decl=bool(re.search(r'(?:theorem|lemma|def|class)\s+$',before))
  if newrows[(p['path'],line)]['classification']=='EXCLUDED':r.update(classification='EXCLUDED/incidental selected context',resolved_node=None)
  elif decl:r.update(classification='declaration-name (not self-call)',resolved_node=p['node_id'])
  elif tok in keywords or tok in namespace:r.update(classification='syntax/namespace/generated-attribute (not mathematical call)',resolved_node=None)
  elif tok in generated:r.update(classification='generated structure field/projection (not mathematical call)',resolved_node=res.get(tok,(p['node_id'],None))[0],qualified_id=res.get(tok,(None,None))[1])
  elif tok in res:
   dest,q=res[tok];r.update(classification='named selected-contract/definition/typing-reference',resolved_node=dest,qualified_id=q)
   if dest!=p['node_id']:
    g['edges'].append(dict(from_node=dest,to_node=p['node_id'],relation='selected-public-or-real-definition-reference',component='50-new-source-only',compiled50caller=False,caller=dict(path=p['path'],line1=line,column0_utf8=start-linest,byte_interval0=[start,end],token=tok),classification=r['classification']))
   else:r['classification']='same-definition typing/name occurrence (no self-loop)'
   entries.append(r)
  elif tok in local or tok.rstrip("'") in local or len(tok)==1 or tok.endswith("prime") or tok in {'volume_tac','ₘ','ₗᵢ','₁₂','_ℝ',"¹'"}:r.update(classification='local bound variable / type syntax / default elaboration tactic (not theorem call)',resolved_node=None)
  else:unresolved.add(tok);r.update(classification='UNRESOLVED requires creator diagnosis',resolved_node=None)
  lex.append(r)
sourcecalls=[]
for a in anchors:
 b=pathlib.Path(a['path']).read_bytes();frag=b[a['start_utf8_byte0']:a['end_utf8_byte0_exclusive']].decode()
 for m in re.finditer(r'href="(#.*?)"',frag):
  start=a['start_utf8_byte0']+len(frag[:m.start(1)].encode());token=m.group(1);end=start+len(token.encode());line=b[:start].count(b'\n')+1;sourcecalls.append(dict(kind='literal-primary-cross-reference',caller_anchor=a['id'],caller_node=amap[a['id']],path=a['path'],physical_line1=line,column0_utf8=start-(b.rfind(b'\n',0,start)+1),byte_interval0=[start,end],token=token,classification='EXCLUDED background terminology citation (no mathematical use)' if token.startswith('#bib') else 'primary-source-reference',compiled50caller=False))
  if not token.startswith('#bib'):
   # Exact source reflection cross-reference is part of the inherited law branch.
   target={'#S2.I1.i3':'S.reflection','#S2.E14':'S.reflection'}.get(token)
   if target:g['edges'].append(dict(from_node=target,to_node=amap[a['id']],relation='literal-primary-cross-reference',component='50-new-source-only',compiled50caller=False,caller=dict(path=a['path'],line1=line,column0_utf8=start-(b.rfind(b'\n',0,start)+1),byte_interval0=[start,end],token=token)))
 for m in re.finditer(r'alttext="(.*?)"',frag,re.S):
  start=a['start_utf8_byte0']+len(frag[:m.start(1)].encode());end=a['start_utf8_byte0']+len(frag[:m.end(1)].encode());sourcecalls.append(dict(kind='printed-formula-reference-region',caller_anchor=a['id'],caller_node=amap[a['id']],path=a['path'],physical_line1=b[:start].count(b'\n')+1,column0_utf8=start-(b.rfind(b'\n',0,start)+1),byte_interval0=[start,end],formula=html.unescape(m.group(1)),classification='source mathematical formula, not an implementation call',compiled50caller=False))
for e in g['edges'][296:]:
 if e['relation']=='printed-source-ingredient':
  dest=N[e['to_node']];aa=dest.get('primary_anchors',[]);selected=[a for a in anchors if a['id'] in aa]
  if selected:e['source_caller_regions']=[dict(path=a['path'],anchor=a['id'],physical_lines1=a['physical_lines1'],byte_interval0=[a['start_utf8_byte0'],a['end_utf8_byte0_exclusive']]) for a in selected];e['caller_semantics']='Printed source formula/paragraph dependency, not a Lean declaration call.'
  else:e['source_caller_regions']='Exact inherited49 balanced B8/B9/C2 anchors, bound separately unchanged.'
g['components']['new50']['edges']=len(g['edges'])-296
dump('source-proof-graph.json',g)
dump('source-coverage.json',dict(scope='Exhaustive physical selected-fragment rows; immutable229-row repaired49 prefix retained verbatim; new coverage rows may overlap inherited rows in distinct provider selection contexts.',line_convention='1-based physical raw file lines; UTF8 byte intervals absolute0-based halfopen. Every selected byte interval, including partial terminal header line, recorded. A NODE row does not authorize nonselected proof suffix.',rows=oldcov['rows']+list(newrows.values()),inherited_rows=229,new_rows=len(newrows)))
dump('caller-inventory.json',dict(scope='Historical167-call repaired49 prefix retained verbatim; new named references only from selected public headers/actual definitions, no compiled50 calls. All new lexemes classified separately; source formula regions not API calls.',entries=oldcalls['entries']+entries,inherited_entries=167,new_entries=len(entries),source_references=sourcecalls,provider_mathematical_proof_bodies_selected=0,prior_inherited_raw_incidental_proof_contexts_excluded=1))
dump('selected-token-inventory.json',dict(scope='Historical160 selected semantic tokens plus new configured named references; exhaustive new lexical identifier/integral inventory in lexical-inventory.json.',entries=oldtokens['entries']+entries,inherited_entries=160,new_entries=len(entries)))
dump('lexical-inventory.json',dict(entries=lex,unresolved=sorted(unresolved),comment_mask='Comments/attributes are not mathematical calls; exact raw fragments retained. Structure fields and declaration/type binders explicitly distinguished.'))
print(json.dumps(dict(nodes=len(g['nodes']),edges=len(g['edges']),coverage=len(oldcov['rows'])+len(newrows),new_coverage=len(newrows),new_callers=len(entries),lexemes=len(lex),unresolved=sorted(unresolved),source_refs=len(sourcecalls))))
