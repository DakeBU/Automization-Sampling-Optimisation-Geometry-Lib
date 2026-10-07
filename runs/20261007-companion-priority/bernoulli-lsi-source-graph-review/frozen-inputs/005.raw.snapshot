import pathlib,json,hashlib,datetime,re
D=pathlib.Path(__file__).parent
R=pathlib.Path('.')
def sha(b):return hashlib.sha256(b).hexdigest()
def lf(b):return b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
def dump(n,x):
 b=(json.dumps(x,ensure_ascii=False,indent=2,sort_keys=True)+'\n').encode();(D/n).open('xb').write(b);return sha(b)
def strip(s):
 out=[];i=0;dep=0
 while i<len(s):
  if dep:
   if s[i:i+2]=='/-':dep+=1;out+=[' ',' '];i+=2
   elif s[i:i+2]=='-/':dep-=1;out+=[' ',' '];i+=2
   else:out.append('\n' if s[i]=='\n' else ' ');i+=1
  elif s[i:i+2]=='/-':dep=1;out+=[' ',' '];i+=2
  elif s[i:i+2]=='--':
   j=s.find('\n',i);j=len(s) if j<0 else j;out+=[' ']*(j-i);i=j
  elif s[i]=='"':
   j=i+1
   while j<len(s):
    if s[j]=='\\':j+=2;continue
    if s[j]=='"':j+=1;break
    j+=1
   out+=['\n' if c=='\n' else ' ' for c in s[i:j]];i=j
  else:out.append(s[i]);i+=1
 return ''.join(out)
closed=json.loads((R/'runs/20261007-companion-priority/bernoulli-lsi-source-preread/inputs.closed.json').read_text())['inputs']
pinned={x['path'].replace('\\','/'):x for x in closed}
paths=['runs/20261007-companion-priority/gaussian-transport-preread/source-primary.raw.snapshot.html']
paths+=['runs/20261007-companion-priority/gaussian-one-dimensional-preread/primary.'+n+'.raw.snapshot.html' for n in ['S4.Ex8','S4.SS1.p4.2','S4.E6','S4.SS1.p4.3']]
paths+=['runs/20261007-companion-priority/gaussian-functional-availability/SLT__GaussianLSI__'+n+'.lean.raw.snapshot' for n in ['TwoPoint','Entropy','BernoulliLSI','OneDimGLSICompSmo']]
paths+=['runs/20261007-companion-priority/gaussian-functional-availability/'+n+'.raw.snapshot' for n in ['LICENSE','lean-toolchain','lake-manifest.json']]
paths+=['runs/20261007-companion-priority/gaussian-lsi-t2-readiness/upstream-reference.receipt.json','runs/20261007-companion-priority/bernoulli-lsi-source-preread/primary.contract.json','runs/20261007-companion-priority/bernoulli-lsi-source-preread/authored-induction-route.audit.json','runs/20261007-companion-priority/bernoulli-lsi-source-preread/bounded-synthesis.json','runs/20261007-companion-priority/bernoulli-lsi-source-preread/inputs.closed.json']
inputs=[]
for i,path in enumerate(paths):
 raw=(R/path).read_bytes();norm=lf(raw)
 if path in pinned:
  assert sha(raw)==pinned[path]['raw_sha256'] and sha(norm)==pinned[path]['lf_sha256'],path
 for typ,b in [('raw',raw),('lf',norm)]: (D/('input.%03d.%s.snapshot'%(i,typ))).open('xb').write(b)
 inputs.append(dict(path=path,raw_sha256=sha(raw),lf_sha256=sha(norm),bytes=len(raw),raw_snapshot=(D/('input.%03d.raw.snapshot'%i)).as_posix(),lf_snapshot=(D/('input.%03d.lf.snapshot'%i)).as_posix(),pin_basis='closed47 manifest' if path in pinned else 'fresh observed receipt'))
full=(R/paths[0]).read_bytes();spans=[]
for path,(a,b) in zip(paths[1:5],[(277149,278916),(278917,281134),(281135,283519),(283520,285390)]):
 raw=(R/path).read_bytes();assert full[a:b]==raw;spans.append(dict(path=path,original_utf8_half_open=[a,b],raw_sha256=sha(raw)))
inputs_hash=dump('inputs.frozen.json',dict(actor='gaussian_domain_preproof_reviewer_29',inputs=inputs,primary_span_exact_recheck=spans,source_only=True,no_implementation_exposure=True))
mods={}; decls={}; ranges={}
pat=re.compile(r'^[ \t]*(?:@\[[^\n]*?\][ \t]*)?(?:(?:private|noncomputable|protected)\s+)*(def|theorem|lemma|instance)\b(?:[ \t]+([^\s(:{]+))?',re.M)
for module in ['TwoPoint','Entropy','BernoulliLSI']:
 path='runs/20261007-companion-priority/gaussian-functional-availability/SLT__GaussianLSI__'+module+'.lean.raw.snapshot'
 raw=(R/path).read_bytes(); lines=raw.split(b'\n'); last=len(lines)-1 if raw.endswith(b'\n') else len(lines); text=raw.decode().replace('\r','');clean=strip(text)
 offsets=[0]
 for line in lines:offsets.append(offsets[-1]+len(line)+1)
 ms=list(pat.finditer(clean));ds=[]
 for k,m in enumerate(ms):
  name=m.group(2) if m.group(1)!='instance' else 'probability_instance'
  start=clean[:m.start()].count('\n')+1;end=clean[:ms[k+1].start()].count('\n') if k+1<len(ms) else last
  block=clean[m.start():ms[k+1].start() if k+1<len(ms) else len(clean)]
  # Actual statement (comments stripped only in parsing copy), not proof body.
  header=block.split(':=',1)[0].strip()
  ident=module+'.'+name
  ds.append(ident); decls[ident]=dict(id=ident,kind=m.group(1),module=module,name=name,start_line=start,end_line=end,header=header,clean=block)
  region=raw[offsets[start-1]:min(offsets[end],len(raw))]
  ranges[ident]=dict(path=path,start_line=start,end_line=end,raw_byte_half_open=[offsets[start-1],min(offsets[end],len(raw))],raw_sha256=sha(region),file_raw_sha256=sha(raw),file_lf_sha256=sha(lf(raw)))
 mods[module]=dict(path=path,raw=raw,lines=lines,last=last,offsets=offsets,decls=ds,clean=clean)
# Exact named source references (headers and bodies) + actual implicit simp/instance parents.
refs={i:set() for i in decls}
for i,d in decls.items():
 for j,e in decls.items():
  if i==j:continue
  if d['module']==e['module']:
   if re.search(r'(?<![\w])'+re.escape(e['name'])+r'(?![\w])',d['clean']):refs[i].add(j)
  elif re.search(r'(?<![\w])'+re.escape(('LogSobolev' if e['module'] in ['TwoPoint','Entropy'] else 'BernoulliLSI')+'.'+e['name'])+r'(?![\w])',d['clean']):refs[i].add(j)
manual={
 'TwoPoint.phi_zero':['TwoPoint.gPlus_zero','TwoPoint.gMinus_zero'],
 'BernoulliLSI.probability_instance':['BernoulliLSI.card_fin_bool'],
 'BernoulliLSI.han_inequality':['Entropy.entropy_const','BernoulliLSI.probability_instance'],
 'BernoulliLSI.entropy_chain_rule_succ':['Entropy.entropy','BernoulliLSI.probability_instance'],
 'BernoulliLSI.bernoulli_integral_eq_sum':['BernoulliLSI.probability_instance'],
 'BernoulliLSI.avg_twoPointEntropyCoord_le':['BernoulliLSI.probability_instance'],
 'BernoulliLSI.entropy_le_half_gradient':['BernoulliLSI.probability_instance'],
}
for child,parents in manual.items():refs[child].update(parents)
root='BernoulliLSI.bernoulli_logSobolev';selected=set()
def visit(i):
 if i in selected:return
 selected.add(i)
 for p in refs[i]:visit(p)
visit(root)
# These source helpers are retained solely as ingredients of the authored RMS alternative.
authored_helpers=['BernoulliLSI.gradientNormSq_succ_decomposition','BernoulliLSI.fin_succ_eq_snoc','BernoulliLSI.last_coord_gradient_bound','BernoulliLSI.flipCoord_castSucc_snoc','BernoulliLSI.flipCoord_last_snoc','BernoulliLSI.condMeanLast','BernoulliLSI.condMeanSqrt','BernoulliLSI.condMeanLast_eq_condMeanSqrt_sq','BernoulliLSI.entropy_chain_rule_succ']
orig=set(selected)
for i in authored_helpers:visit(i)
altonly=selected-orig
nodes=[];edges=[]
def node(i,kind,formula,**kw):nodes.append(dict(id=i,kind=kind,formula=formula,**kw))
def edge(p,c,kind='SOURCE_DEPENDENCY',**kw):edges.append(dict(parent=p,consumer=c,kind=kind,**kw))
for i in sorted(selected):
 d=decls[i]
 node(i,'SOURCE_DEFINITION' if d['kind']=='def' else 'SOURCE_TYPECLASS' if d['kind']=='instance' else 'SOURCE_LEMMA',d['header'],source_anchor=ranges[i],truth_contract='external-reference-only; no ASTIS compiled producer asserted',route_role='AUTHORED_ALTERNATIVE_SOURCE_INGREDIENT' if i in altonly else 'UPSTREAM_HAN_ROUTE',binder_policy='exact printed declaration header retained; prerequisites derived at internal callers, never licensed as added final public premises')
 for parent in sorted(refs[i]):edge(parent,i,evidence='implicit simp/instance (documented)' if parent in manual.get(i,[]) else 'exact named source reference',source_anchor=ranges[i])
# Backgrounds explicitly used by source proofs. These are not supplied public concentration/LSI hypotheses.
node('ENTROPY-TYPE-CONTEXT','SOURCE_TYPECLASS_CONTEXT','variable {Omega : Type*} [MeasurableSpace Omega] {mu : Measure Omega}; actual finite consumer instantiates Omega=Fin n -> Bool.',source_anchor=dict(path=mods['Entropy']['path'],start_line=36,end_line=36,file_raw_sha256=sha(mods['Entropy']['raw'])),public_input=False)
for c in ['Entropy.entropy','Entropy.entropy_const']:edge('ENTROPY-TYPE-CONTEXT',c,'SOURCE_TYPECLASS_CONTEXT_DEPENDENCY')
backgrounds={
 'API-SCALAR-CALCULUS':('Real derivative rules/log/sqrt domains and MVT on internal compact subintervals of (-1,1)', ['exists_deriv_eq_slope','DifferentiableAt.continuousAt','DifferentiableAt.differentiableWithinAt','HasDerivAt.log','HasDerivAt.sqrt','Filter.EventuallyEq.deriv_eq'],[i for i in selected if i.startswith('TwoPoint.') and any(x in decls[i]['name'] for x in ['deriv','differentiable','Defect_nonneg'])]),
 'API-SCALAR-ZERO-SIGN':('log 0=0 in Lean, 0*log0=0; sqrt(a^2)=|a|; reverse absolute triangle; log2<=1 from actual upstream exp_one_gt_d9', ['Real.log_zero','Real.sqrt_sq_eq_abs','abs_abs_sub_abs_le_abs_sub','Real.exp_one_gt_d9','Real.log_lt_log','Real.log_exp'], ['TwoPoint.gPlus_zero','TwoPoint.gMinus_zero','TwoPoint.phi_zero','TwoPoint.rothausDefect_zero','TwoPoint.rothaus_lemma','BernoulliLSI.twoPointEntropyCoord_le_gradientTerm']),
 'API-FINITE-COUNT-SNOC':('finite Bool cube cardinal 2^n; actual count scaling; Fin.snoc equivalence with slices; no extra measure certificate', ['Measure.count_apply_finite','Measure.smul_apply','ENNReal.inv_mul_cancel','Fintype.card_fun','Fintype.card_bool','Fin.snoc','Fin.sum_univ_castSucc'], [i for i in selected if i.startswith('BernoulliLSI.') and any(x in decls[i]['name'] for x in ['card_fin','probability_instance','integral_eq_sum','sum_fin_succ','integral_succ_split','flipCoord','fin_succ'])]),
 'API-FINITE-L1':('every real function on actual finite Bool cube is measurable and L1 under its probability measure; internal integral addition/sum/monotonicity legal', ['Integrable.of_finite','integral_finsetSum','integral_add','integral_sub','integral_mono_of_nonneg','integral_const_mul'],[i for i in selected if i.startswith('BernoulliLSI.') and any(x in decls[i]['name'] for x in ['integral','entropy_chain','han_inequality','avg_twoPoint','entropy_le_half'])]),
 'API-CONVEX-ENTROPY':('convex x log x on nonnegative reals; concavity of binary entropy on [0,1]; all zero mass cases separated before division', ['Real.convexOn_mul_log','Real.strictConcave_binEntropy','ConvexOn'],[i for i in selected if i.startswith('BernoulliLSI.') and decls[i]['name'] in ['phi_convex_avg','binaryKLfromUniform_convexOn','binaryKLfromUniform_weighted_le','jensenGap_joint_convex']]),
}
for i,(f,apis,consumers) in backgrounds.items():
 node(i,'IMPORTED_BACKGROUND',f,api_names=apis,truth_contract='API usage/source mathematical prerequisite; no new local compiled/API-availability assertion',public_input=False)
 for c in consumers:edge(i,c,'IMPORTED_BACKGROUND_DEPENDENCY',source_anchor=ranges[c])
edge('BernoulliLSI.probability_instance','API-FINITE-L1','DERIVED_INTERNAL_DOMAIN');edge('API-FINITE-COUNT-SNOC','API-FINITE-L1','DERIVED_INTERNAL_DOMAIN')
# Signed and zero scope explicitly separated, with exact proof regions.
branches=[('SIGNED-POSITIVE',446,458,'a=h(epsilon)^2>0 and b=h(flip epsilon)^2>0: positive Rothaus then sqrt squares=abs and reverse abs triangle'),('SIGNED-ZERO-B',459,479,'b=0: expression a/2 log2 <=a/2, with internal a>=0; redundant a=0 branch retained'),('SIGNED-ZERO-A-SETUP',480,482,'a=0 derived from a>=0 and not a>0; no public nonnegativity assumption on h'),('SIGNED-BOTH-ZERO',483,484,'a=b=0: entropy and flip energy both zero'),('SIGNED-ZERO-A-POSITIVE-B',485,500,'a=0 and b!=0: expression b/2 log2<=b/2, h(epsilon)=0 derived from square0')]
for i,a,b,f in branches:
 m=mods['BernoulliLSI'];raw=m['raw'][m['offsets'][a-1]:m['offsets'][b]]
 node(i,'SOURCE_PROOF_CASE',f,source_anchor=dict(path=m['path'],start_line=a,end_line=b,raw_byte_half_open=[m['offsets'][a-1],m['offsets'][b]],raw_sha256=sha(raw),file_raw_sha256=sha(m['raw'])))
 edge(i,'BernoulliLSI.twoPointEntropyCoord_le_gradientTerm','EXHAUSTIVE_CASE_DEPENDENCY')
 edge('API-SCALAR-ZERO-SIGN',i,'IMPORTED_BACKGROUND_DEPENDENCY')
 if i=='SIGNED-POSITIVE':edge('TwoPoint.rothaus_lemma',i)
# Authored OR route, reviewed mathematically in earlier CLOSED preread only; not source attribution.
node('AUTHORED-RMS-CONTRACTION','AUTHORED_BACKGROUND_LEAF','For arbitrary real pairs A,B, g=||(a,b)||_2/sqrt2: (g(A)-g(B))^2 <=((aA-aB)^2+(bA-bB)^2)/2, including zero pairs.',provenance='root suggested after primary freeze; independent mathematical audit in authored-induction-route.audit.json',required_semantics='Euclidean L2 pair norm / WithLp 2, never ordinary product sup norm',truth_contract='mathematically reviewed authored route, no proof/compile credit')
node('AUTHORED-DIRECT-INDUCTION','AUTHORED_ROUTE','Induct n: n=0 single atom entropy0; successor entropy chain + signed last-coordinate two-point bound + IH on RMS g + reverse L2 norm contraction yield exact 1/2 full flip Dirichlet energy.',provenance='root-authored alternative for omitted background; not SPHMC printed proof, not upstream Han proof',public_input=False,truth_contract='authored unimplemented alternative; no proof credit')
for p in ['AUTHORED-RMS-CONTRACTION','Entropy.entropy_const','BernoulliLSI.probability_instance','BernoulliLSI.twoPointEntropyCoord_le_gradientTerm','API-FINITE-L1']+authored_helpers:edge(p,'AUTHORED-DIRECT-INDUCTION','AUTHORED_ALTERNATIVE_DEPENDENCY')
node('FINITE-BOOL-LSI','SOURCE_CONCLUSION','For all n:Nat and h:(Fin n -> Bool)->Real, Ent_mu_n(h^2) <= (1/2) E_mu_n sum_(j:Fin n) (h(epsilon)-h(update epsilon j (!epsilon j)))^2; mu_n=(card(univ))^-1 count =2^-n count.',source_anchor=ranges[root],truth_contract='exact external Bernoulli source conclusion; no ASTIS proof credit')
# Conclusion OR is genuinely separate from the literal upstream declaration's sole Han dependency.
hyperedges=[dict(id='UPSTREAM-HAN-OR-AUTHORED-RMS',consumer='FINITE-BOOL-LSI',operator='OR',alternatives=[dict(id='PRINTED-SLT-HAN',requires=['BernoulliLSI.bernoulli_logSobolev'],provenance='exact upstream source proof'),dict(id='AUTHORED-RMS',requires=['AUTHORED-DIRECT-INDUCTION'],provenance='authored alternative independently mathematically reviewed; unimplemented')],compiled=False)]
node('SPHMC-FIRST-4.6','PRIMARY_CONSUMER','W2(r_y,N(0,I)) <= sqrt(E_(r_y)||grad rho_y||^2); primary explanation invokes Gaussian Talagrand + Gaussian LSI.',source_anchor=spans[2],explanation_anchor=spans[3],truth_contract='actual ultimate paper consumer; no printed Bernoulli theorem attribution')
node('SPHMC-RHO-LAW','PRIMARY_DEFINITION','rho_y(u)=V(p+sqrt(eta)u)-V(p)-sqrt(eta)<gradV(p),u>; r_y proportional exp(-||u||^2/2-rho_y(u)); 0<=Hess rho_y<=eta I.',source_anchor=spans[0],law_anchor=spans[1])
gaps=[
 ('GAP-BOOL-RADEMACHER','Actual Boolean-to-Rademacher pushforward, shifted coordinate energy and entropy transport; upstream Bernoulli1252-1632 beyond finite core.'),
 ('GAP-GAUSSIAN-CLT-ENTROPY','Actual standardized Rademacher law convergence and genuine entropy convergence for compact smooth f; not concentration naming.'),
 ('GAP-FLIP-ENERGY-LIMIT','Actual sum squared flipped differences ->4 integral(deriv f)^2; together half gives Gaussian constant2.'),
 ('GAP-COMPACT-GAUSSIAN-CORE','Compact smooth 1D Gaussian function LSI Ent_gamma(f^2)<=2 integral(fprime)^2 remains an external candidate, not local completion.'),
 ('GAP-FINITE-HILBERT','True finite Gaussian product/tensorization and orthonormal Hilbert/Parseval measure+gradient adapters.'),
 ('GAP-NONCOMPACT-CUTOFF','Actual positive noncompact sqrt-density from packet32 needs cutoff entropy/mass/energy limits, not a compact-only theorem.'),
 ('GAP-KL-FISHER-ADAPTER','Join same true posterior finite KL and f=sqrt(q), Ent_gamma(f^2)=KL, 4 Dirichlet=Fisher; canonical RN only AE, no arbitrary RN pointwise derivative.'),
 ('GAP-T2','Independent Gaussian Talagrand/T2 with exact squared Euclidean metric, finite moments, KL convention and constants W2^2<=2 KL.'),
]
for i,f in gaps:node(i,'SOURCE_GAP',f,truth_contract='outside bounded finite Bernoulli delta; unmet producer/adapter recorded, no completion')
for p,c in [('FINITE-BOOL-LSI','GAP-BOOL-RADEMACHER'),('GAP-BOOL-RADEMACHER','GAP-COMPACT-GAUSSIAN-CORE'),('GAP-GAUSSIAN-CLT-ENTROPY','GAP-COMPACT-GAUSSIAN-CORE'),('GAP-FLIP-ENERGY-LIMIT','GAP-COMPACT-GAUSSIAN-CORE'),('GAP-COMPACT-GAUSSIAN-CORE','GAP-FINITE-HILBERT'),('GAP-FINITE-HILBERT','GAP-NONCOMPACT-CUTOFF'),('GAP-NONCOMPACT-CUTOFF','GAP-KL-FISHER-ADAPTER'),('SPHMC-RHO-LAW','GAP-KL-FISHER-ADAPTER'),('GAP-KL-FISHER-ADAPTER','SPHMC-FIRST-4.6'),('GAP-T2','SPHMC-FIRST-4.6')]:edge(p,c,'OPEN_FUTURE_DEPENDENCY')
# Exhaustive physical-LF line coverage of all three exact source files.
inventory=[];coverage=[]
def coverage_region(module,a,b,nodeid=None,reason=None):
 m=mods[module];raw=m['raw'][m['offsets'][a-1]:min(m['offsets'][b],len(m['raw']))]
 inventory.append(dict(source=module,path=m['path'],start_line=a,end_line=b,raw_byte_half_open=[m['offsets'][a-1],min(m['offsets'][b],len(m['raw']))],raw_sha256=sha(raw),disposition='NODE' if nodeid else 'EXCLUDED',node_id=nodeid,reason=reason))
for module,m in mods.items():
 if module=='Entropy':
  coverage_region(module,1,35,reason='license/imports/namespaces/overview; generic context separately retained')
  coverage_region(module,36,36,'ENTROPY-TYPE-CONTEXT')
  coverage_region(module,37,47,reason='entropy definition documentation and separators; exact definition retained below')
 else:coverage_region(module,1,decls[m['decls'][0]]['start_line']-1,reason='license/imports/namespaces/overview prose; imports retained provenance, not mathematical theorem ingredient; implementation source is controlling over informal summaries')
 for i in m['decls']:
  d=decls[i];a=d['start_line'];b=d['end_line']
  if i=='BernoulliLSI.twoPointEntropyCoord_le_gradientTerm':
   coverage_region(module,a,445,i)
   for z,x,y,_ in branches:coverage_region(module,x,y,z)
   coverage_region(module,501,b,reason='separator and documentation of next declaration')
  elif i in selected:coverage_region(module,a,b,i)
  else:
   reason='not reachable in selected upstream upper Rothaus/Han/finite-LSI route and not an ingredient of authored RMS alternative; no inferred dependency from co-location'
   if module=='TwoPoint' and d['name'] in ['phi_nonneg','two_point_inequality','two_point_entropy_lower_bound','deriv2_phi_ge_two']:reason='neighboring LOWER/positivity entropy bound, not positive upper Rothaus prerequisite; excluded from upper-bound cut'
   if module=='BernoulliLSI' and a>=1252:reason='downstream actual Rademacher/compact application beyond finite Boolean delta; future GAP-BOOL-RADEMACHER records this boundary'
   if module=='BernoulliLSI' and d['name'].startswith('signValue'):reason='Bool-to-real sign representation used downstream only; finite target remains actual Bool count law'
   if i=='BernoulliLSI.two_point_rothaus_bound':reason='older separate nonnegative-h wrapper; final signed source consumer uses twoPointEntropyCoord_le_gradientTerm; no hh_nn convenience binder authorized'
   if module=='Entropy':reason='generic Jensen/nonnegativity/normalized-square/absolute-log identities not consumed by selected finite entropy chain/Han proof; entropy definition and entropy_const retained'
   coverage_region(module,a,b,reason=reason)
 rs=[x for x in inventory if x['source']==module];seen=[]
 for x in rs:seen+=list(range(x['start_line'],x['end_line']+1))
 assert seen==list(range(1,m['last']+1)),module
 coverage.append(dict(source=module,path=m['path'],raw_sha256=sha(m['raw']),lf_sha256=sha(lf(m['raw'])),physical_lf_lines=m['last'],regions=len(rs),node_regions=sum(x['disposition']=='NODE' for x in rs),excluded_regions=sum(x['disposition']=='EXCLUDED' for x in rs),mechanical_partition_no_holes_or_overlap=True))
# Region snapshots preserve raw bytes independently; not just claims from parsing.
for i,x in enumerate(inventory):
 raw=(R/x['path']).read_bytes()[x['raw_byte_half_open'][0]:x['raw_byte_half_open'][1]]
 (D/('region.%03d.raw.snapshot'%i)).open('xb').write(raw);x['raw_snapshot']=(D/('region.%03d.raw.snapshot'%i)).as_posix()
inv_hash=dump('source.inventory.json',dict(status='AUTHOR_INVENTORY_NOT_INDEPENDENT_VALIDATION',line_convention='1-based physical raw LF-separated lines; trailing CR belongs to exact raw bytes; final empty record after terminal LF is not an extra line',coverage=coverage,regions=inventory,primary_balanced_spans=spans,not_claimed='entire primary paper/external project coverage; only exact declared bounded source footprint'))
# No fake closure attribution based on comments; scan actual source code token copy only.
scans=[]
for module,m in mods.items():
 bad=[dict(token=x.group(),line=m['clean'][:x.start()].count('\n')+1) for x in re.finditer(r'\b(?:sorry|admit|axiom)\b|Prop[ \t]*:=[ \t]*True|:=[ \t]*trivial\b',m['clean'])]
 scans.append(dict(source=module,file_raw_sha256=sha(m['raw']),scope='bounded three pinned SLT files; comments/strings removed for token scan only',hits=bad))
scan_hash=dump('static-source-scan.json',dict(scans=scans,compiler_started=False,truth_boundary='static source hygiene only; not transitive Mathlib closure or Lean build/axiom verification'))
contract=dict(status='PRIMARY_AND_SLT_SOURCE_CONTRACT_FROZEN_UNREVIEWED',author='gaussian_domain_preproof_reviewer_29',source_order='exact pinned primary fragments and CLOSED primary contract first; exact SLT source second; no root proposed signature/body exposure',history='prior primary author and independent mathematical route reviewer; author cannot validate this Source Proof Graph',target=dict(quantifiers='n : Nat arbitrary including0; h:(Fin n -> Bool)->Real arbitrary signed, including identically0',measure='literal normalized finite count mu_n=(card Finset.univ)^-1 • Measure.count, cardinal2^n; snoc split weights1/2, n0 singleton',entropy='integral h^2 log(h^2) -mass logmass; x logx at zero defined by 0 multiplication; actual finite L1 internally',energy='actual coordinate Function.update with Bool.not; sum squared flips',constant='1/2; unoriented repeated edges under uniform expectation, no silent reweight',forbidden_extra_public_inputs=['h>=0','n>0','measurability','L1 certificates','given entropy-chain','given Han','given RMS contraction','given desired LSI','given Gaussian concentration']),source_scope='SLT printed finite Bernoulli theorem; SPHMC invokes GaussianLSI/T2 but does not print Bernoulli theorem',positive_core='a,b>0 only internally after h squares; t=(a-b)/(a+b) in(-1,1), m=(a+b)/2>0; defect0=derivative0=0 and second derivative nonnegative; two MVTs on true subintervals for signed t',zero_sign_extension='all square-zero branches explicit; sqrt h²=|h| and reverse triangle removes h sign; no endpoint t=+-1 MVT',source_route='actual Han/joint Jensen-gap convexity induction then signed coordinate upper bound',authored_or='direct entropy chain/RMS reverse Euclidean norm induction; provenance separate and unimplemented',truth_boundary=['no ASTIS Bernoulli proof/compile admission','no Gaussian LSI or T2/W2/bias/main/work/composition result','no source topology selfvalidation'],pins=dict(SLT_revision='d0f506f0a695018265dccb33bcb05e2f5ca1c876',SLT_toolchain='leanprover/lean4:v4.32.0',SLT_Mathlib='81a5d257c8e410db227a6665ed08f64fea08e997',ASTIS_toolchain='leanprover/lean4:v4.33.0',ASTIS_Mathlib='db584cd6d46c92f209a44c0f1c829460d327499d',license='Apache-2.0 exact frozen LICENSE',status='external-reference-only; minimal source cut, no whole external project import; no ML use'),input_manifest_raw_sha256=inputs_hash,source_inventory_raw_sha256=inv_hash)
contract_hash=dump('source.contract.json',contract)
graph=dict(schema=1,status='AUTHORED_UNREVIEWED_SOURCE_PROOF_GRAPH',author='gaussian_domain_preproof_reviewer_29',root=root,bounded_conclusion='FINITE-BOOL-LSI',nodes=nodes,edges=edges,or_hyperedges=hyperedges,compiled_edges=[],source_inventory_raw_sha256=inv_hash,source_contract_raw_sha256=contract_hash,input_manifest_raw_sha256=inputs_hash,coverage=coverage,manual_implicit_dependency_annotations=manual,source_route_nodes=len(orig),authored_alternative_only_source_nodes=len(altonly),mechanical_named_reference_scope='all exact selected source declaration references plus documented simp/probability-instance/domain imports; not inferred from root Lean',self_validation=False,remaining_boundary=contract['truth_boundary'])
graph_hash=dump('source-proof-graph.independent.json',graph)
summary=dict(status='SOURCE_GRAPH_AUTHORED_AWAITING_DISTINCT_REVIEW',graph_raw_sha256=graph_hash,inventory_raw_sha256=inv_hash,contract_raw_sha256=contract_hash,input_manifest_raw_sha256=inputs_hash,nodes=len(nodes),edges=len(edges),or_hyperedges=len(hyperedges),compiled_edges=0,source_coverage=coverage,source_gap_ids=[i for i,_ in gaps],source_hygiene_scan_raw_sha256=scan_hash,at_most_seven_route_steps=['Positive Rothaus upper core: exact log/sqrt/derivative domains, zero anchors and both-sign internal MVT intervals.','Signed actual two-point square entropy: positive squares, one-zero and both-zero branches; abs reverse triangle.','Actual normalized Bool count probability, cardinal2^n and exact last-bit snoc integral split; all finite L1 internally.','Exact finite entropy chain and RMS square identity for conditional means.','SOURCE route: joint Jensen gap convexity via binary entropy then genuine all-n Han; AUTHOR alternative: reverse Euclidean pair norm contraction then direct all-n induction.','Integrate signed coordinate bound and sum all actual flip energies; exact1/2 and n0/allzero.','Only future candidate: actual Rademacher transfer plus entropy/flip-energy limits would feed compact Gaussian constant2; finite-Hilbert/cutoff/KL/T2 remain open.'],independent_validation=False,no_implementation_read=True,no_compiler=True,truth_boundary=contract['truth_boundary'])
sum_hash=dump('bounded-synthesis.json',summary)
# Freeze produced artifacts and exact source reread; lease lifecycle is kept outside immutable run digest.
for x in inputs:assert sha((R/x['path']).read_bytes())==x['raw_sha256'],x['path']
artifacts=[]
for p in sorted(D.iterdir()):
 if p.is_file() and p.name not in ['lease.json','run.json']:
  b=p.read_bytes();artifacts.append(dict(path=p.as_posix(),raw_sha256=sha(b),lf_sha256=sha(lf(b)),bytes=len(b)))
runbasis=dict(actor='gaussian_domain_preproof_reviewer_29',input_manifest_raw_sha256=inputs_hash,graph_raw_sha256=graph_hash,artifacts=artifacts,all_input_raw_hashes_rechecked=True,read_lease='CLOSED',write_lease='CLOSED',compiler_lease='CLOSED',compiler_started=False)
runhash=sha(json.dumps(runbasis,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
dump('run.json',dict(runbasis,deterministic_run_sha256=runhash,hash_recipe='SHA256 of UTF8 canonical JSON runbasis sort_keys compact separators, no trailing newline'))
lease=json.loads((D/'lease.json').read_text());lease.update(status='CLOSED',read_lease='CLOSED',write_lease='CLOSED',compiler_lease='CLOSED',compiler_started=False,closed_utc=datetime.datetime.utcnow().isoformat()+'Z',run_sha256=runhash,graph_raw_sha256=graph_hash,implementation_exposure=False,self_validation=False)
(D/'lease.json').write_bytes((json.dumps(lease,indent=2,sort_keys=True)+'\n').encode())
print(json.dumps(dict(run_sha256=runhash,graph_raw_sha256=graph_hash,nodes=len(nodes),edges=len(edges),or_hyperedges=len(hyperedges),coverage=coverage,source_named_nodes=len(orig),authored_only_source_nodes=sorted(altonly),leases='CLOSED')))
