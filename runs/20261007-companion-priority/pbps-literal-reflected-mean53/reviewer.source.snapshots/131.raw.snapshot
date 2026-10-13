import pathlib,json,hashlib,re,subprocess,datetime,sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT=pathlib.Path('E:/Samplinglib'); OUT=ROOT/'runs/20261007-companion-priority/pbps-reflected-density-sourcegraph53'
PRE=ROOT/'runs/20261007-companion-priority/pbps-reflected-density-preread53'
OLD=ROOT/'runs/20261007-companion-priority/pbps-gaussian-reflected-mean-topology-overlay52'
def sha(b):return hashlib.sha256(b).hexdigest()
def lf(b):return b.replace(b'\r\n',b'\n')
def js(p):return json.loads(pathlib.Path(p).read_text(encoding='utf-8-sig'))
def dump(name,obj):(OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def pin(p):
 p=pathlib.Path(p);b=p.read_bytes();return dict(path=str(p),raw_bytes=len(b),lf_bytes=len(lf(b)),raw_sha256=sha(b),lf_sha256=sha(lf(b)))
nodes=[];edges=[];providers=[];coverage=[];callers=[];lex=[];inputs=[];formulae=[]
def node(n,k,c,q=None):
 if not any(x['id']==n for x in nodes):nodes.append(dict(id=n,kind=k,contract=c,qualified_id=q,compiled53=False,proof_body_expanded=False))
def edge(a,b,k,c,caller=None):
 d=dict(id='E53.'+str(len(edges)),ingredient=a,consumer=b,kind=k,reason=c,compiled53call=False)
 if caller is not None:d['caller_index0']=caller
 edges.append(d)
def select(label,n,p,a,b,kind='public-header',start=None,end=None):
 p=pathlib.Path(p);raw=p.read_bytes();lines=raw.splitlines(keepends=True);lo=sum(map(len,lines[:a-1])) if start is None else start;hi=sum(map(len,lines[:b])) if end is None else end
 frag=raw[lo:hi];(OUT/(label+'.raw')).write_bytes(frag);(OUT/(label+'.lf')).write_bytes(lf(frag));d=dict(id=label,node=n,kind=kind,physical_lines1=[a,b],start_utf8_byte0=lo,end_utf8_byte0_exclusive=hi,fragment_raw_sha256=sha(frag),fragment_lf_sha256=sha(lf(frag)),body_selected=(kind=='definition-body'),external_expansion_boundary=(kind=='primitive-declaration-token-anchor'),**pin(p));providers.append(d)
 return d,frag
def hdr(label,n,p,name,q):
 raw=pathlib.Path(p).read_bytes();m=re.search(rb'(?:theorem|lemma) '+re.escape(name.encode())+rb'(?=\s|[({])',raw);assert m,name
 end=None
 for e in re.finditer(rb':=',raw[m.start():]):
  pos=m.start()+e.start();line=raw[raw.rfind(b'\n',m.start(),pos)+1:pos].strip()
  if not line.startswith(b'let '):end=pos;break
 assert end is not None,name
 a=raw[:m.start()].count(b'\n')+1;b=raw[:end].count(b'\n')+1
 node(n,'opaque-verified-parent' if n.startswith('P53.parent') else 'pinned-public-API','Exact selected public contract; proof opaque',q)
 return select(label,n,p,a,b,start=m.start(),end=end)
primary=ROOT/'runs/20261007-companion-priority/next-ready-preread47/primary-pbps.raw.snapshot.html'
# Historical source-before-candidate records remain unchanged; current reread chronology is explicit.
for p in [PRE/'source-contract.json',PRE/'run.json',PRE/'lease.json',ROOT/'runs/20261007-companion-priority/phase-pbps-primary-preread53/primary.contract.json',ROOT/'runs/20261007-companion-priority/phase-pbps-primary-preread53/source.preread.run.json',ROOT/'runs/20261007-companion-priority/phase-pbps-primary-preread53/reviewer.primary.lease.json']:
 inputs.append(pin(p));(OUT/('historical.'+p.parent.name+'.'+p.name+'.raw.snapshot')).write_bytes(p.read_bytes())
src=[('standing','S53.standing',351,361,'Actual normalized Gibbs mu, source C2 and two-sided alpha/beta Hessian'),('augmentation','S53.joint',614,640,'Source eta cap; actual joint, generator and outer Gaussian marginal'),('pair','S53.pair',3717,3735,'Actual Y+/Y- reflection and literal macroscopic conditional mean B8/B9'),('rough','S53.rough',3777,3786,'Full every-L2 H1 and B13: downstream residual, not current conclusion'),('compact','S53.compact',4573,4576,'Source smooth compact reduction; genuine density and closed-gradient gap retained'),('density','S53.density',4579,4587,'Source all-y proportional reflected conditional density A3.Ex1'),('score','S53.score',4589,4595,'Source score definition: contextual derivative input, not current covariance conclusion'),('derivative','S53.derivative',4596,4604,'Differentiating normalized density C1; omitted analytic prerequisites, current C1 mean adapter'),('energy-consumer','S53.energy',4654,4664,'Formula(C.2) within C.1 and B13 consumer; not subsection C.2')]
for lab,n,a,b,c in src:
 node(n,'source-residual' if n in ['S53.rough','S53.energy'] else 'primary-source',c);select('primary-'+lab,n,primary,a,b,'primary-source')
fullprimary=primary.read_text(encoding='utf-8');plines=fullprimary.splitlines()
for p in providers:
 if p['kind']!='primary-source':continue
 for i in range(p['physical_lines1'][0],p['physical_lines1'][1]+1):
  t=plines[i-1];text=re.sub('<[^>]+>',' ',t).strip();math=bool(re.search(r'<math\b|<p\b|<div\b[^>]*ltx_para|<td\b[^>]*ltx_eqn_cell',t)) or (bool(text) and not re.fullmatch(r'\(?[BC12.0-9]+\)?',text))
  # B13/energy rows are mathematically meaningful residual NODEs; only literal markup/labels EXCLUDED.
  coverage.append(dict(provider=p['id'],path=p['path'],physical_line1=i,classification='NODE' if math else 'EXCLUDED',node=p['node'] if math else None,reason='Mathematical statement/assumption/definition or explicitly residual consumer' if math else 'HTML/table/layout/printed equation label only',raw_line_sha256=sha(primary.read_bytes().splitlines(keepends=True)[i-1])))
  for m in re.finditer(r'href="([^"]+)"',t):
   ref=m.group(1);target=ref.split('#')[-1];dest=next((x['node'] for x in providers if x['kind']=='primary-source' and ('id="'+target+'"') in b''.join(primary.read_bytes().splitlines(keepends=True)[x['physical_lines1'][0]-1:x['physical_lines1'][1]]).decode()),None)
   if dest is None:
    dest='X53.source.'+re.sub(r'[^A-Za-z0-9]+','_',target);node(dest,'external-unexpanded-source-reference','Literal source reference '+ref+'; selected source does not expand its mathematical contents')
   off=sum(len(x) for x in primary.read_bytes().splitlines(keepends=True)[:i-1]);ci=len(callers);callers.append(dict(index0=ci,provider=p['id'],consumer=p['node'],physical_line1=i,utf8_byte_start0=off+len(t[:m.start(1)].encode()),utf8_byte_end0_exclusive=off+len(t[:m.end(1)].encode()),token=ref,resolution=dest,classification='source-direct-reference'));edge(dest,p['node'],'source-reference','Literal primary href',ci)
  for m in re.finditer(r'<annotation encoding="application/x-tex">(.*?)</annotation>',t):formulae.append(dict(provider=p['id'],physical_line1=i,tex=m.group(1),node=p['node']))
gibbs=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/GibbsAugmentation.lean';affine=ROOT/'AutoSamplingTheory/TechnicalLemmas/Measure/AffineGibbs.lean';mean=ROOT/'AutoSamplingTheory/TechnicalLemmas/Measure/GaussianReflectedMean.lean'
hdr('gibbs-public','P53.parentG',gibbs,'normalized_augmentation_density','AutoSamplingTheory.ExampleCases.ProximalBPS.GibbsAugmentation.normalized_augmentation_density');select('gibbs-context','P53.parentG',gibbs,31,32)
hdr('affine-public','P53.parentA',affine,'map_affine_gibbs','AutoSamplingTheory.TechnicalLemmas.Measure.AffineGibbs.map_affine_gibbs');select('affine-context','P53.parentA',affine,16,17)
hdr('mean52-public','P53.parent52',mean,'gaussian_reflected_mean_c1','AutoSamplingTheory.TechnicalLemmas.Measure.GaussianReflectedMean.gaussian_reflected_mean_c1')
mac=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/MacroscopicEnergy.lean';hdr('consumer50-public','P53.consumer50',mac,'actual_macroscopic_gradient_energy_blocks','AutoSamplingTheory.ExampleCases.ProximalBPS.MacroscopicEnergy.actual_macroscopic_gradient_energy_blocks')
providers[-1]['kind']='opaque-consumer-header-context'
providers[-1]['selection_boundary']='Complete public header exposed and pinned as opaque consumer context; only every-y source-density lines45-46 are selected expanded contracts. Other public operator/domain conclusions are excluded downstream context.'
tilt=ROOT/'.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Tilted.lean'
node('D53.tilt','definition','Literal real reciprocal-normalizer totalized tilt; degenerate mass0 must be excluded internally','MeasureTheory.Measure.tilted');select('tilted-definition','D53.tilt',tilt,42,43,'definition-body')
for lab,n,name,q in [('tilt-compose','P53.compose','tilted_tilted','MeasureTheory.tilted_tilted'),('tilt-prob','P53.prob','isProbabilityMeasure_tilted','MeasureTheory.isProbabilityMeasure_tilted'),('tilt-set','P53.set','tilted_apply_eq_ofReal_integral\'',"MeasureTheory.tilted_apply_eq_ofReal_integral'")]:hdr(lab,n,tilt,name,q)
boch=ROOT/'.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Bochner/Basic.lean'
hdr('integral-ne0','P53.ne0',boch,'Integrable.of_integral_ne_zero','MeasureTheory.Integrable.of_integral_ne_zero')
hdr('exp-positive','P53.expPos',boch,'integral_exp_pos','MeasureTheory.integral_exp_pos')
integ=ROOT/'.lake/packages/mathlib/Mathlib/MeasureTheory/Function/L1Space/Integrable.lean'
# one-line term body is omitted at :=; hdr expects by, so select its public header only.
r=integ.read_bytes();m=re.search(rb'theorem integrable_const \[',r);e=r.index(b':=',m.start());node('P53.const','pinned-public-API','Constant bound1 integrable under genuine finite probability','MeasureTheory.integrable_const');select('integrable-constant','P53.const',integ,r[:m.start()].count(b'\n')+1,r[:e].count(b'\n')+1,start=m.start(),end=e)
hdr('norm-scale','P53.scale',ROOT/'.lake/packages/mathlib/Mathlib/Analysis/Normed/Module/RCLike/Real.lean','norm_smul_of_nonneg','norm_smul_of_nonneg')
# Jacobian convention contract, public-only, used as interpretation of opaque affine parent not re-proof.
haar=ROOT/'.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Haar/Unique.lean'
bind=js(PRE/'public-API-bindings.json');h=next(x for x in bind if x['label']=='haar-map-public');node('P53.haar','pinned-public-API','Exact affine Haar scale convention; normalization already implemented by opaque affine parent',h['qualified_id']);select('haar-map','P53.haar',h['path'],*h['physical_lines1'],start=h['start_utf8_byte0'],end=h['end_utf8_byte0_exclusive'])
# Actual primitive declaration-name tokens reused only after fresh byte equality check; no proof bodies selected.
oldproviders=js(OLD/'selected-providers.json');oldnodes={x['id']:x for x in js(OLD/'source-proof-graph.json')['nodes']}
needed=['NAC','IP','FD','MS','Borel','Measure','prob','CD','Integrable','stdG','map','prod','wd','ofReal','volume','integral','Real','Norm','Module','fderiv','finrank','sqrt','pi','exp','compact','SMul','Set','AEStrong','Measurable','FiniteMeasure','CLM','Strong','Continuous','TopologicalSpace']
for suffix in needed:
 old='D52.'+suffix;x=next(z for z in oldproviders if z['node']==old and z['kind']=='primitive-declaration-token-anchor');nid='D53.'+suffix;q=oldnodes[old]['qualified_id'];node(nid,'external-unexpanded-primitive','Exact declaration-name anchor; full primitive contract/proof remains pinned external boundary',q)
 assert pin(x['path'])['raw_sha256']==x['whole_raw_sha256'],x['path']
 select('primitive-'+suffix,nid,x['path'],*x['physical_lines1'],kind='primitive-declaration-token-anchor',start=x['start_utf8_byte0'],end=x['end_utf8_byte0_exclusive'])
ne=pathlib.Path('C:/Users/admin/.elan/toolchains/leanprover--lean4---v4.33.0/src/lean/Init/Data/NeZero.lean');rr=ne.read_bytes();mm=re.search(rb'class (NeZero)\b',rr);node('D53.NeZero','external-unexpanded-primitive','Actual core NeZero class; μ≠0 derived internally, not input certificate','NeZero');select('primitive-NeZero','D53.NeZero',ne,29,29,'primitive-declaration-token-anchor',start=mm.start(1),end=mm.end(1))
ms=ROOT/'.lake/packages/mathlib/Mathlib/MeasureTheory/MeasurableSpace/Defs.lean';rr=ms.read_bytes();mm=re.search(rb'def (MeasurableSet)\b',rr);node('D53.MeasurableSet','external-unexpanded-primitive','Actual measurable-set definition','MeasurableSet');select('primitive-MeasurableSet','D53.MeasurableSet',ms,64,64,'primitive-declaration-token-anchor',start=mm.start(1),end=mm.end(1))
ab=ROOT/'.lake/packages/mathlib/Mathlib/Algebra/Order/Group/Unbundled/Abs.lean';rr=ab.read_bytes();mm=re.search(rb'def (mabs)\b',rr);node('D53.abs','external-unexpanded-generated-primitive','Actual abs generated from mabs by to_additive at source38; no handwritten abs definition alleged','abs');select('primitive-abs-generated','D53.abs',ab,39,39,'primitive-declaration-token-anchor',start=mm.start(1),end=mm.end(1));inputs.append(pin(ab))
for nid,q,p,pat in [('D53.Haar','MeasureTheory.Measure.IsAddHaarMeasure',ROOT/'.lake/packages/mathlib/Mathlib/MeasureTheory/Group/Measure.lean',rb'class (IsAddHaarMeasure)\b'),('D53.OpenPos','MeasureTheory.Measure.IsOpenPosMeasure',ROOT/'.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/OpenPos.lean',rb'class (IsOpenPosMeasure)\b'),('D53.Nonempty','Nonempty',pathlib.Path('C:/Users/admin/.elan/toolchains/leanprover--lean4---v4.33.0/src/lean/Init/Prelude.lean'),rb'class inductive (Nonempty)\b')]:
 rr=p.read_bytes();mm=re.search(pat,rr);assert mm,q;line=rr[:mm.start(1)].count(b'\n')+1;node(nid,'external-unexpanded-primitive','Exact class declaration anchor; inherited class contract external-unexpanded',q);select('primitive-'+nid.split('.')[-1],nid,p,line,line,'primitive-declaration-token-anchor',start=mm.start(1),end=mm.end(1))
ofb=ROOT/'.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Haar/OfBasis.lean';rr=ofb.read_bytes();lines=rr.splitlines(keepends=True);lo=sum(map(len,lines[:313]));hi=rr.index(b':=',lo);node('P53.volHaar','anonymous-pinned-instance-contract','Actual anonymous instance canonical finite inner-product volume is additive Haar; no guessed emitted qualified name');select('volume-Haar-instance','P53.volHaar',ofb,314,315,start=lo,end=hi)
op=ROOT/'.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/OpenPos.lean';rr=op.read_bytes();lines=rr.splitlines(keepends=True);lo=sum(map(len,lines[:49]));hi=rr.index(b':=',lo);node('P53.volNe0','anonymous-pinned-instance-contract','Actual anonymous Nonempty/IsOpenPosMeasure instance gives NeZero μ; class context38/42 remains explicit external contract');select('open-positive-nezero-instance','P53.volNe0',op,50,50,start=lo,end=hi)
pr=ROOT/'.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Typeclasses/Probability.lean';rr=pr.read_bytes();mm=re.search(rb'instance \(priority := 100\) IsProbabilityMeasure.neZero',rr);hi=rr.index(b':=',mm.end());node('P53.probNe0','pinned-instance-contract','Genuine probability implies actual nonzero measure','MeasureTheory.IsProbabilityMeasure.neZero');select('probability-nezero-instance','P53.probNe0',pr,87,88,start=mm.start(),end=hi)
candidate=ROOT/'runs/20261007-companion-priority/pbps-reflected-density-preproof53/prospective-statement.txt';proposal=ROOT/'runs/20261007-companion-priority/pbps-reflected-density-preproof53/root.statement-proposal.json'
node('T53','prospective-target','Source-backed authored every-y law identity and literal compact C1 mean; statement/type admission pending',js(proposal)['declaration']);select('prospective-statement','T53',candidate,1,len(candidate.read_bytes().splitlines()),'prospective-public-statement');inputs.extend([pin(candidate),pin(proposal)]);(OUT/'root.statement-proposal.raw.snapshot.json').write_bytes(proposal.read_bytes())
for nam in ['root.statement-proposal.placement0.raw.snapshot.json','placement.diagnosis.json']:
 p=proposal.parent/nam;inputs.append(pin(p));(OUT/nam).write_bytes(p.read_bytes())
status=[]
for path,commit,n in [(gibbs,'38e1ef64e5851b8ecab7b6a3d2771a55ab5db40e','P53.parentG'),(affine,'36bdaa8404ff4b716dd0bf8e8844f2f02f43f2e4','P53.parentA'),(mean,'a18cd1cf8e8310f228391d4c53a2ac8f1a8900ec','P53.parent52')]:
 old=subprocess.run(['git','show',commit+':'+path.relative_to(ROOT).as_posix()],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 assert old.returncode==0 and lf(path.read_bytes())==lf(old.stdout),(path,commit)
 status.append(dict(node=n,verified_commit=commit,current=pin(path),verified_blob_raw_sha256=sha(old.stdout),verified_blob_lf_sha256=sha(lf(old.stdout)),LF_science_equal=True,body_semantics_inspected=False,status_authority='Root exact52 VERIFIED notification; parentG and parentA exact selected historical VERIFIED ledger fields'))
# Read/retain only named parent status rows, never other reviews/decoder entries.
for idx,line in enumerate((ROOT/'runs/substantive_advances.jsonl').read_text(encoding='utf-8').splitlines(),1):
 j=json.loads(line)
 if j.get('to_state')=='VERIFIED' and j.get('advance_id') in ['ASTIS-ADV-20260910-PBPSGibbsAugmentation','ASTIS-SA-20261006-StandardizedRGOPositionFisher']:
  e=j.get('evidence',{});status.append(dict(ledger_line1=idx,advance_id=j['advance_id'],to_state=j['to_state'],verified_commit=e.get('verified_commit'),raw_row_sha256=sha(line.encode()),classification='Selected administrative verified-parent provenance, not mathematical source'))
dump('parent-status.json',status)
# Fresh source reconstruction: each authored ingredient is an uncompiled obligation, never a certificate premise.
ob=[('ZV','Actual ZV>0 under C2/global positive Hessian; parentG projection internally'),('L1','Actual exp(-V)L1 from nonzero real Gibbs integral, never supplied'),('muProb','True volume nonzero and Gibbs tilt probability; finite positive normalizer'),('postL1','For every y, K_y=exp(-norm(x-y)^2/(2eta)) continuous,0<K<=1; bounded measurable likelihood and finite μ give L1'),('partitions','Every-y Zmu>0 finite; ZR=ZV Zmu and sourceZS positive finite; correct nondegenerate laws'),('compose','Literal posterior (volume.tilted(-V)).tilted(Klog)=volume.tilted(-V+Klog) by actual base L1'),('jacobian','T_y x=2x-y, inverseH_yu=half(u+y); j=abs((2^d)^-1)=2^-d; opaque affine normalization, sourceZS=2^d ZR'),('exponent','H_yu-y=half(u-y); squared norm/2eta becomes norm(y-u)^2/8eta; potential sum/sign exact'),('law','Every-y sourceS=T_y#literalR; no AE conditional-version substitution'),('mean','Everywhere measure identity yields exact literal mean-function identity'),('C1','Actual signedcompact mean globally C1 using parent52 genuine probability; no new differentiation/continuity input'),('same50','Future consumer: actual50 EVERY-y source density equates literal Tf to this sourceS mean; no current graph membership theorem')]
for lab,c in ob:node('A53.'+lab,'authored-internal-obligation',c)
def connects(dest,srcs,reason,kind='mathematical-ingredient'):
 for s in srcs:edge(s,dest,kind,reason)
connects('A53.ZV',['S53.standing','P53.parentG'],'True positive Gibbs partition produced internally')
connects('A53.L1',['A53.ZV','P53.ne0'],'Positive real integral is nonzero, hence true Bochner L1')
connects('P53.volHaar',['D53.Haar','D53.volume'],'Canonical finite real inner-product volume Haar instance; anonymous provider header not invented wrapper')
connects('P53.volNe0',['P53.volHaar','D53.OpenPos','D53.Nonempty'],'Haar extends open positivity; vector-space0 supplies Nonempty, including rank0')
connects('A53.muProb',['A53.L1','P53.prob','D53.volume','D53.NeZero','P53.volNe0'],'Canonical finite-Hilbert volume is nonzero (including rank0); tilt normalization probability')
connects('A53.postL1',['A53.muProb','P53.const','S53.joint'],'Gaussian log likelihood nonpositive, positive exponential≤1, measurable; L1 by actual finite measure bound')
connects('A53.partitions',['A53.postL1','P53.expPos','A53.ZV','A53.jacobian','P53.probNe0'],'Actual positive finite posterior/source partitions, normalized mass1')
connects('A53.compose',['A53.L1','P53.compose','D53.tilt'],'Actual exp(-V)L1 discharges real composition premise')
connects('A53.jacobian',['P53.parentA','P53.haar','D53.finrank','S53.pair'],'True scale2 affine pushforward; Haar reference fixes Jacobian convention without copying proof')
connects('A53.exponent',['S53.density','P53.scale','S53.joint'],'Exact inverse affine algebra and norm scaling; ordinary vector/scalar algebra internal')
connects('A53.law',['A53.compose','A53.jacobian','A53.exponent','S53.density'],'Every-y source normalization identity with same laws')
connects('A53.mean',['A53.law','S53.pair'],'Everywhere law equality permits actual mean function equality')
connects('A53.C1',['A53.mean','A53.muProb','P53.parent52','S53.compact','S53.derivative'],'Opaque verified52 regularity after exact literal law transport')
connects('T53',['A53.law','A53.C1'],'Both proposed conclusions; no wrapper or extra desired-result premise')
connects('A53.same50',['T53','P53.consumer50','S53.energy'],'Actual sameS/Tf downstream compact graph regularity consumer, not completed by source graph')
connects('S53.derivative',['S53.density','S53.score','S53.pair'],'Printed normalized covariance uses exact source density/score/literal mean; covariance route contextual, not compulsory for parent52 join','source-definition-use')
connects('S53.compact',['S53.rough'],'Printed B13 compact reduction has genuine omitted rough density/closedness boundary','source-residual')
connects('S53.energy',['S53.derivative','S53.rough'],'Exact formula(C.2) consumer and rough B13 boundary, not current theorem result','source-residual')
# Exhaustive public selected lexical inventory: identifiers/notation, actual binder names vs callable primitives.
alias={}
for x in nodes:
 if x['qualified_id']:
  q=x['qualified_id'];alias[q]=x['id'];alias[q.split('.')[-1]]=x['id']
alias.update({'ℝ':'D53.Real','exp':'D53.exp','volume':'D53.volume','tilted':'D53.tilt','map':'D53.map','prod':'D53.prod','withDensity':'D53.wd','Module.finrank':'D53.finrank','Real.exp':'D53.exp','Real.sqrt':'D53.sqrt','Real.pi':'D53.pi','ENNReal.ofReal':'D53.ofReal','Measure.map':'D53.map'})
binders={'E','X','α','η','V','f','F','p','s','x','y','u','v','μ','R','S','ZV','joint','hs','hα','hV','hH','hη','hf','hc','hμ','g','G','β','c','t','ht','𝕜','a','A','n','m','h','r','hr','_','priority','instance','fderivWithin','MeasureTheory','Measure','Real','ENNReal','Module'}
keywords={'theorem','lemma','def','let','fun','Type','Prop','where','by','in','public','variable','namespace','open','scoped'}
unresolved=[]
for p in providers:
 if p['kind'] in ['primary-source','primitive-declaration-token-anchor']:continue
 raw=pathlib.Path(p['path']).read_bytes();frag=raw[p['start_utf8_byte0']:p['end_utf8_byte0_exclusive']].decode('utf-8');base=p['start_utf8_byte0']
 for rowno,line in enumerate(frag.splitlines(keepends=True)):
  physical=p['physical_lines1'][0]+rowno
  # Selected row partition for headers/definition body; no parent body selected.
  incidental=p['kind']=='opaque-consumer-header-context' and physical not in [45,46]
  coverage.append(dict(provider=p['id'],path=p['path'],physical_line1=physical,classification='NODE' if line.strip() and not incidental else 'EXCLUDED',node=p['node'] if line.strip() and not incidental else None,reason='Opaque downstream public consumer context; excluded operator/domain expansion' if incidental else ('Exact public contract/typing or true selected definition body' if line.strip() else 'Blank layout'),fragment_row0=rowno))
  if incidental:base+=len(line.encode());continue
  for m in re.finditer(r'[A-Za-z_α-ωΑ-Ω𝕜ℝ][A-Za-z0-9_α-ωΑ-Ω𝕜ℝ]*(?:\.[A-Za-z_][A-Za-z0-9_\']*)*|∫|‖|•',line):
   tok=m.group();start=base+len(line[:m.start()].encode());end=base+len(line[:m.end()].encode());dest=alias.get(tok)
   if dest is None and '.' in tok and tok.split('.')[0] in {'μ','R','S','volume'}:dest=alias.get(tok.split('.')[-1])
   if tok=='∫':dest='D53.integral'
   if tok=='‖':dest='D53.Norm'
   if tok=='•':dest='D53.SMul'
   decl=bool(re.search(r'(theorem|lemma|def)\s+$',line[:m.start()])) or (p['id']=='probability-nezero-instance' and tok=='IsProbabilityMeasure.neZero')
   if decl:cls='declaration-name-binding';dest=p['node']
   elif dest:cls='primitive-contract-reference'
   elif tok in keywords or tok in binders:cls='bound-identifier-or-syntax'
   else:cls='unresolved-lexical-contract';unresolved.append(dict(token=tok,provider=p['id'],line1=physical))
   li=dict(index0=len(lex),provider=p['id'],consumer=p['node'],physical_line1=physical,utf8_byte_start0=start,utf8_byte_end0_exclusive=end,token=tok,classification=cls,resolution=dest);lex.append(li)
   if dest and cls=='primitive-contract-reference':
    ci=len(callers);callers.append(dict(index0=ci,lexical_index0=li['index0'],provider=p['id'],consumer=p['node'],physical_line1=physical,utf8_byte_start0=start,utf8_byte_end0_exclusive=end,token=tok,resolution=dest,classification='public-contract-definition-use'));edge(dest,p['node'],'public-contract-definition-use','Exact public contract token; not a guessed implementation call or self-loop',ci)
    if tok.startswith('Module.'):
     lex.append(dict(index0=len(lex),provider=p['id'],consumer=p['node'],physical_line1=physical,utf8_byte_start0=start,utf8_byte_end0_exclusive=start+6,token='Module',classification='global-class-typing-prefix',resolution='D53.Module'))
     ci=len(callers);callers.append(dict(index0=ci,provider=p['id'],consumer=p['node'],physical_line1=physical,utf8_byte_start0=start,utf8_byte_end0_exclusive=start+6,token='Module',resolution='D53.Module',classification='global-class-typing-prefix'));edge('D53.Module',p['node'],'typing-prefix','Global Module class primitive distinct from Module.finrank',ci)
  base+=len(line.encode())
for p in providers:
 if p['kind']=='primitive-declaration-token-anchor':
  coverage.append(dict(provider=p['id'],path=p['path'],physical_line1=p['physical_lines1'][0],classification='NODE',node=p['node'],reason='Exact primitive declaration-name token only; rest of physical source line OUTSIDE_SELECTED_SCOPE',utf8_byte_start0=p['start_utf8_byte0'],utf8_byte_end0_exclusive=p['end_utf8_byte0_exclusive']))
  lex.append(dict(index0=len(lex),provider=p['id'],consumer=p['node'],physical_line1=p['physical_lines1'][0],utf8_byte_start0=p['start_utf8_byte0'],utf8_byte_end0_exclusive=p['end_utf8_byte0_exclusive'],token=(OUT/(p['id']+'.raw')).read_text(encoding='utf-8'),classification='primitive-provider-name-binding-not-call',resolution=p['node']))
dump('unresolved-lexemes.json',unresolved)
dump('source-proof-graph.json',dict(schema_version='bounded-source-proof-graph53/v1',status='CREATOR_SOURCE_RECONSTRUCTION_NOT_TOPOLOGY_ADMITTED',edge_orientation='ingredient -> consumer',nodes=nodes,edges=edges,scope='Source-derived six-step normalized affine law / opaque C1 integration. Opaque parent internals excluded; selected source physical rows exhaustive. No53proof exists.'))
dump('selected-providers.json',providers);dump('source-coverage.json',coverage);dump('caller-inventory.json',callers);dump('lexical-inventory.json',lex);dump('primary-formula-inventory.json',formulae)
dump('input-bindings.json',inputs+[pin(primary),pin(ROOT/'lake-manifest.json'),pin(ROOT/'lean-toolchain')])
print(json.dumps(dict(nodes=len(nodes),edges=len(edges),providers=len(providers),coverage=len(coverage),callers=len(callers),lexemes=len(lex),unresolved=unresolved),ensure_ascii=False))
