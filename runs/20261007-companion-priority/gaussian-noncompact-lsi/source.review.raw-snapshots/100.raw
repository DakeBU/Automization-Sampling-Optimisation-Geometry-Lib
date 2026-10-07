from pathlib import Path
import json, hashlib, re, datetime

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
OLD = ROOT / 'runs/20261007-companion-priority/gaussian-noncompact-lsi-preread42'
def dump(name, obj):
    (OUT/name).write_text(json.dumps(obj, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
def sha(b): return hashlib.sha256(b).hexdigest()
manifest = json.loads((OLD/'inputs.json').read_text(encoding='utf-8'))
# Physical partitions cover ALL frozen selected ranges, with explicit exclusions.
# Only listed relevant provider declarations are source-body expanded.
selected_names = {
 'Cutoff': ['smoothUnitCutoff','smoothUnitCutoff_eq_smoothTransition','smoothUnitCutoff_contDiff',
 'smoothUnitCutoff_eq_one_of_abs_le_one','smoothUnitCutoff_eq_zero_of_two_le_abs','smoothUnitCutoff_mem_Icc',
 'smoothUnitCutoff_hasCompactSupport','smoothUnitCutoff_deriv_bounded','radialSmoothCutoff',
 'radialSmoothCutoff_eq_one_of_norm_le','radialSmoothCutoff_eq_zero_of_two_mul_le_norm',
 'radialSmoothCutoff_mem_Icc','fderiv_norm_div_bound','radialSmoothCutoff_contDiff',
 'radialSmoothCutoff_fderiv_bound','radialSmoothCutoff_fderiv_eq_zero_of_two_mul_le_norm',
 'radialSmoothCutoff_support_subset_closedBall','radialSmoothCutoff_tsupport_subset_closedBall',
 'radialSmoothCutoff_hasCompactSupport','radialSmoothCutoff_tendsto_one'],
 'Gradient':['continuous_gradient_of_contDiff_one'],
 'SLTdefs':['GaussianSobolevNormSq','GaussianSobolevNorm','MemW12Gaussian','memW12Gaussian_iff_sobolevNormSq_lt_top'],
 'SLTcutoff':['cutoff_product_rule','cutoff_gradient_error_bound','cutoff_gradient_extra_term','tendsto_cutoff_W12'],
 'SLToneDim':['phi_continuous','mul_log_ge_neg_inv_exp','gaussian_logSobolev_W12_real'],
 'SLTtensor':['partialDeriv','gradNormSq','MemW12GaussianPi','gaussian_logSobolev_W12_pi'],
 'MathlibDCT':['tendsto_integral_of_dominated_convergence','tendsto_integral_filter_of_dominated_convergence'],
 'MathlibL2':['MemLp.integrable_sq','memLp_two_iff_integrable_sq_norm','memLp_two_iff_integrable_sq'],
 'MathlibGradient':['HasGradientAtFilter','HasGradientWithinAt','HasGradientAt','gradientWithin','gradient',
 'toDual_gradientWithin','toDual_gradient','toDual_comp_gradientWithin','toDual_comp_gradient',
 'HasGradientAt.unique','DifferentiableAt.hasGradientAt','HasGradientAt.differentiableAt',
 'DifferentiableWithinAt.hasGradientWithinAt','HasGradientWithinAt.differentiableWithinAt',
 'HasGradientAt.gradient','gradient_eq','Filter.EventuallyEq.gradient_eq','Filter.EventuallyEq.gradient'],
 'MathlibRiesz':['toDualMap','toContinuousLinearMap_toDualMap','toDualMap_apply_apply','toDual','toDual_apply_apply','toDual_symm_apply'],
 'MathlibProduct':['HasFDerivAt.mul','fderiv_fun_mul','fderiv_mul'],
 'MathlibPhi':['self_sub_one_lt_mul_log','self_sub_one_le_mul_log','continuous_mul_log','Continuous.mul_log',
 'negMulLog','negMulLog_def','negMulLog_eq_neg','negMulLog_zero','negMulLog_one','negMulLog_nonneg',
 'negMulLog_mul','continuous_negMulLog','negMulLog_lt_one_sub_self','negMulLog_le_one_sub_self'],
 'MathlibOrder':['le_of_tendsto_of_tendsto_of_frequently','le_of_tendsto_of_tendsto','le_of_tendsto_of_tendsto\''],
}
prefix = {'Cutoff':'AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.',
 'Gradient':'AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient.',
 'SLTdefs':'GaussianSobolev.','SLTcutoff':'GaussianSobolev.','SLToneDim':'GaussianSobolevReal.','SLTtensor':'GaussianLSI.',
 'MathlibDCT':'MeasureTheory.','MathlibL2':'MeasureTheory.','MathlibRiesz':'InnerProductSpace.',
 'MathlibPhi':'Real.','MathlibGradient':'','MathlibProduct':'','MathlibOrder':''}
decre = re.compile(r'^\s*(?:@\[[^\]]+\]\s*)*(?:(?:noncomputable|private|protected|public|unsafe)\s+)*(?:def|abbrev|lemma|theorem|alias)\s+([\w.\']+)')
nodes, edges, providers, coverage = [], [], [], []
data = {}

def node(nid, **kw):
    nodes.append(dict(id=nid, **kw)); return nid
def edge(a,b,span,**kw):
    edges.append(dict(id='edge:'+str(len(edges)+1), prerequisite=a,consumer=b,consumer_use_site=span,
                      truth='source-dependency-only-no-compiled-edge',**kw))

# New exact order-limit source, plus missing Phi sign primitive, are API retrieval, not proof search.
orderpath='.lake/packages/mathlib/Mathlib/Topology/Order/OrderClosed.lean'
bp=(ROOT/orderpath).read_bytes();lf=bp.decode().replace('\r\n','\n').replace('\r','\n')
(OUT/'MathlibOrder.raw.snapshot').write_bytes(bp);(OUT/'MathlibOrder.lf.snapshot').write_bytes(lf.encode())
manifest.append(dict(key='MathlibOrder',path=orderpath,raw_sha256=sha(bp),lf_sha256=sha(lf.encode()),ranges=[[467,482]]))
for item in manifest:
 key=item['key']; lines=(OUT/(key+'.lf.snapshot')).read_text(encoding='utf-8').splitlines();data[key]=lines
 item['ranges']=[[a,min(b,len(lines))] for a,b in item['ranges']]
 if key=='MathlibPhi':item['ranges'].append([151,158])
 decls=[(i+1,match.group(1)) for i,line in enumerate(lines) if (match:=decre.match(line))]
 relevant=[]
 for j,(a,name) in enumerate(decls):
  z=decls[j+1][0]-1 if j+1<len(decls) else len(lines)
  # End before next doc comment / namespace terminator, preserving only mathematical declaration body.
  for k in range(a,z):
   if lines[k].startswith(('/--','/-!','namespace ','section ','end ')):
    z=k;break
  if name not in selected_names.get(key,[]):continue
  segs=[]
  for lo,hi in item['ranges']:
   if max(a,lo)<=min(z,hi):segs.append([max(a,lo),min(z,hi)])
  if not segs:continue
  nid='source:'+key+':'+name
  qname=prefix.get(key,'')+name
  relevant.append((a,z,nid))
  providers.append(dict(id=nid,key=key,name=name,qname_claim=qname,full_provider_span=[a,z],selected_provider_spans=segs,
                        body_expansion='selected-physical-spans-only; omitted remainder external-unexpanded',
                        source_kind='external-reference' if key.startswith('SLT') else 'canonical-source-api'))
  node(nid,kind='SOURCE_PROVIDER',source=key,source_ranges=segs,qualified_identifier=qname,
       identifier_check='exact spelling plus source namespace checked; no elaboration claim',
       formal_truth='not-admitted-by-this-sourcegraph',external_reference=key.startswith('SLT'))
 # Non-provider public contracts and primary displays are explicit anchor nodes.
 extra=[]
 if key=='primary':
  extra=[(1210,1295,'primary:surrounding-setup'),(1296,1300,'primary:standardized-law'),
         (1301,1309,'primary:FIRST4.6'),(1310,1314,'primary:LSI-T2-invocation'),(1315,1320,'primary:following-estimate')]
 elif key=='041signature':extra=[(1,len(lines),'parent:compact41-public')]
 elif key=='032shared':extra=[(211,235,'interface:shared32')]
 elif key=='032consumer':extra=[(21,53,'interface:actual32')]
 elif key=='033consumer':extra=[(24,52,'interface:actual33')]
 for a,z,nid in extra:
  relevant.append((a,z,nid));node(nid,kind='SOURCE_ANCHOR' if key=='primary' else 'PUBLIC_INTERFACE',source=key,source_ranges=[[a,z]],
   body_read=False,formal_truth='source/public contract only, no proof inspected')
 # Partition each selected physical line exactly once, including all trivia and out-of-route declarations.
 for lo,hi in item['ranges']:
  for n in range(lo,hi+1):
   owners=[nid for a,z,nid in relevant if a<=n<=z]
   assert len(owners)<=1,(key,n,owners)
   if owners:coverage.append(dict(source=key,line=n,disposition='NODE',node=owners[0]))
   else:
    reason=('policy/provenance evidence, not mathematical proof source' if key in ['SLTbackgroundRegistry','SLTreusePolicy','TechnicalPolicy']
            else 'header/import/comment/namespace/trivia or declaration outside first-gradient noncompact-LSI route; retained, no closure credit')
    coverage.append(dict(source=key,line=n,disposition='EXCLUDED',reason=reason))

# Source-name reference index: exact tokens and explicit source locations. No compiler or theorem search.
# Namespaces/sections are parsed solely to avoid invented qualified API identities.
index={}
for path in (ROOT/'.lake/packages/mathlib/Mathlib').rglob('*.lean'):
 stack=[]
 for n,line in enumerate(path.read_text(encoding='utf-8').splitlines(),1):
  ns=re.match(r'^\s*namespace\s+([\w.]+)',line)
  se=re.match(r'^\s*(?:noncomputable\s+)?section(?:\s+([\w.]+))?',line)
  en=re.match(r'^\s*end(?:\s+([\w.]+))?\s*$',line)
  if ns:stack.append(('namespace',ns.group(1)))
  elif se:stack.append(('section',se.group(1)))
  elif en and stack:stack.pop()
  mt=decre.match(line)
  if mt:
   name=mt.group(1);nsname='.'.join(x for typ,x in stack if typ=='namespace')
   q=(name[7:] if name.startswith('_root_.') else '.'.join(x for x in [nsname,name] if x))
   rec=dict(qname=q,declared_name=name,path=str(path.relative_to(ROOT)).replace('\\','/'),line=n)
   index.setdefault(name.split('.')[-1],[]).append(rec)
# Unselected same-source declarations are external-unexpanded, never silently dropped.
for key,lines in data.items():
 if key.startswith('Mathlib') or key not in prefix:continue
 for n,line in enumerate(lines,1):
  mt=decre.match(line)
  if not mt:continue
  name=mt.group(1);q=prefix[key]+name
  p=next((p for p in providers if p['key']==key and p['name']==name),None)
  rec=dict(qname=q,declared_name=name,source=key,line=n)
  if p:rec['provider_node']=p['id']
  index.setdefault(name.split('.')[-1],[]).append(rec)

uses=[];primitive_ids={};ident_checks=[]
keywords=set('by have let show fun forall forall_eq_exists_imp_forall intro intros obtain rcases rintro exact apply refine constructor left right cases casesm by_cases by_contra classical simp simpa simp_rw simp_all simp_arith only rw rfl change unfold dsimp norm_num positivity linarith nlinarith ring ring_nf gcongr aesop tauto trivial assumption ext funext congr congrArg convert convert! filter_upwards calc at with using from in if then else match return do Type Prop where false true change unfold push Not simp_all aesop all_goals next case repeat first rename_i guard_hyp choose dsimp simp? rfl? abel field_simp fun_prop infer_instance inherit_doc lemma local notation nth_rewrite noncomputable protected reorder rwa scoped theorem variable def'.split())
keywords.update(['Gradient',"d'",'i₀','μs','ₗᵢ'])
types=set('E F n R x y C L f a b u v z h K rho gamma gamma_r Type Prop Nat Real MeasureTheory Filter Set ENNReal NNReal Topology ProbabilityTheory InnerProductSpace ContinuousLinearMap Function Metric WithTop ContDiff MemLp Integrable DifferentiableAt Differentiable HasCompactSupport Continuous Tendsto Fin Measure'.split())
# Every lexical identifier occurrence in selected provider bodies receives a disposition.
# Named uses resolved only when declaration suffix + explicit namespace agree; ambiguity stays external.
for p in providers:
 key=p['key'];lines=data[key];start=p['full_provider_span'][0]
 body_started=False;locals_=set()
 for n in range(start,p['full_provider_span'][1]+1):
  line=lines[n-1]
  # Collect local binders before checking tokens; names h..., proof-local terms are not dependency vertices.
  for mt in re.finditer(r'\b(?:have|let|intro|by_cases|by_contra)\s+([\w\']+)',line):locals_.add(mt.group(1))
  if not body_started:
   for mt in re.finditer(r'[({]\s*([\w\s\']+)\s*:',line):locals_.update(mt.group(1).split())
  first_body_line=not body_started and ':=' in line
  if ':=' in line:body_started=True
  if not body_started or not any(a<=n<=b for a,b in p['selected_provider_spans']):continue
  code=line.split('--',1)[0]
  if first_body_line:code=' '* (code.index(':=')+2)+code.split(':=',1)[1]
  for mt in re.finditer(r'(?<![\w])[\w][\w\'.]*',code):
   token=mt.group(0);parts=token.split('.');last=parts[-1]
   if token[0].isdigit() or token in keywords or token in types or last in keywords:disposition='syntax/tactic-or-carrier'
   elif token in locals_ or ((parts[0] in locals_ or re.match(r'^h[\w\']*$',parts[0])) and (len(parts)==1 or last.isdigit())):disposition='local-binder-or-local-proof-field'
   elif len(token)==1:disposition='local-scalar-or-identifier'
   else:
    candidates=index.get(last,[])
    exacts=[c for c in candidates if c['qname']==token or c['qname'].endswith('.'+token)]
    if not exacts and len(parts)==1:exacts=candidates
    # Same-source named provider wins only for a genuine unqualified direct call.
    same=[c for c in exacts if c.get('source')==key and c.get('provider_node')!=p['id']]
    if len(parts)==1 and len(same)==1:exacts=same
    if len(exacts)==1:
     c=exacts[0];nid=c.get('provider_node')
     if nid is None:
      nid='primitive:'+c['qname']+':'+sha((c.get('path',c.get('source'))+str(c['line'])).encode())[:8]
      if nid not in primitive_ids:
       primitive_ids[nid]=True;node(nid,kind='EXTERNAL_UNEXPANDED_PRIMITIVE',qualified_identifier=c['qname'],declaration_locator=c,formal_truth='pinned API source only; not a new compiled edge')
     edge(nid,p['id'],dict(source=key,line_start=n,line_end=n,column_start=mt.start()+1,column_end=mt.end()),
          use_kind='direct-named-source-use',source_token=token)
     ident_checks.append(dict(token=token,resolved_qname=c['qname'],declaration_locator=c,source=key,line=n))
     disposition='named-use-edge'
    elif candidates:
     # Method notation cannot be elaborated by source-text search. Retain the dependency token, not a guessed QName.
     nid='primitive-token:'+token
     if nid not in primitive_ids:
      primitive_ids[nid]=True;node(nid,kind='EXTERNAL_UNEXPANDED_PRIMITIVE',source_token=token,
       resolution='source-token only; method/namespace ambiguity, not asserted qualified API identity',
       candidate_locators=exacts[:12] if exacts else candidates[:12])
     edge(nid,p['id'],dict(source=key,line_start=n,line_end=n,column_start=mt.start()+1,column_end=mt.end()),use_kind='direct-named-source-use-unelaborated',source_token=token)
     disposition='named-use-edge-unelaborated-token'
    else:
     # Retain every opaque named-use token as an unexpanded primitive edge, never invent a QName.
     nid='primitive-token:'+token
     if nid not in primitive_ids:
      primitive_ids[nid]=True;node(nid,kind='EXTERNAL_UNEXPANDED_PRIMITIVE',source_token=token,
       resolution='opaque source symbol/API or local syntax; not asserted qualified identifier; manual inventory below')
     edge(nid,p['id'],dict(source=key,line_start=n,line_end=n,column_start=mt.start()+1,column_end=mt.end()),use_kind='opaque-source-token-use',source_token=token)
     disposition='opaque-source-token-edge'
   uses.append(dict(provider=p['id'],source=key,line=n,columns=[mt.start()+1,mt.end()],token=token,disposition=disposition))

dump('source-inputs.json',manifest)
dump('source-coverage.json',dict(schema='ASTIS-42-physical-source-partition-v1',entries=coverage,
 invariant='exactly one NODE or EXCLUDED for every selected physical line; no unselected proof coverage claim'))
dump('named-use-inventory.json',dict(schema='ASTIS-42-provider-token-disposition-v1',providers=providers,entries=uses,
 invariant='source named use edges contain exact physical caller span; unresolved tokens not falsely QNamed'))
dump('qualified-api-resolution.json',dict(schema='source-static-declaration-locator-v1',entries=ident_checks,
 boundary='Static source declaration/namespace resolution, not Lean elaboration or compiled proof-dependency evidence'))
dump('sourcegraph.base.json',dict(nodes=nodes,edges=edges,providers=providers))
print(json.dumps({'provider_nodes':len(providers),'nodes':len(nodes),'edges':len(edges),'coverage_lines':len(coverage),'tokens':len(uses),'opaque_tokens':sorted(set(u['token'] for u in uses if u['disposition']=='opaque-source-token-edge'))},ensure_ascii=False))
