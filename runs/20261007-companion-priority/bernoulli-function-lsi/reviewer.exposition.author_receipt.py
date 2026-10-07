import datetime, hashlib, html, json, re, subprocess
from pathlib import Path
from html.parser import HTMLParser

root=Path('E:/Samplinglib');base=root/'runs/20261007-companion-priority/bernoulli-function-lsi'
commit='d0b872541758537a4f42d9d3e6e8deb12b5bb028'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=str(root)).decode().strip()==commit
def sha(b):return hashlib.sha256(b).hexdigest()
def lf(b):return b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
def rel(p):return str(p.relative_to(root)).replace('\\','/')
def dump(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def immutable_bytes(p,b):
    if p.exists():assert p.read_bytes()==b,p
    else:
        with p.open('xb') as f:f.write(b)
def write(name,x):
    b=dump(x);p=base/name
    with p.open('xb') as f:f.write(b)
    return {'path':rel(p),'raw_sha256':sha(b),'lf_sha256':sha(lf(b)),'bytes':len(b)}
inputs=[]
def bind(path,canonical=False):
    p=root/path;b=p.read_bytes();x={'path':path,'bytes':len(b),'raw_sha256':sha(b),'lf_sha256':sha(lf(b))}
    if canonical:
        gb=subprocess.check_output(['git','show',commit+':'+path],cwd=str(root))
        assert lf(gb)==lf(b),path
        x.update(checked_commit=commit,git_blob_raw_sha256=sha(gb),git_blob_lf_sha256=sha(lf(gb)),working_LF_equals_checked_commit=True)
        gp=base/('reviewer.exposition.input.%03d.git.raw.snapshot'%len(inputs))
        immutable_bytes(gp,gb)
        x['git_snapshot']=rel(gp)
    for kind,val in [('raw',b),('lf',lf(b))]:
        sp=base/('reviewer.exposition.input.%03d.%s.snapshot'%(len(inputs),kind))
        immutable_bytes(sp,val)
        x[kind+'_snapshot']=rel(sp)
    inputs.append(x)
    return x

slugs=['two-point-squared-entropy','bernoulli-function-log-sobolev','balanced-rademacher-count-clt']
modules=['AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/TwoPointEntropy.lean','AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/BernoulliLogSobolev.lean','AutoSamplingTheory/TechnicalLemmas/Probability/BalancedRademacherCLT.lean']
tests=['Tests/BernoulliLogSobolev.lean','Tests/BalancedRademacherCLT.lean']
modpages=['_site/modules/autosamplingtheory-technicallemmas-functionalinequalities-twopointentropy.html','_site/modules/autosamplingtheory-technicallemmas-functionalinequalities-bernoullilogsobolev.html','_site/modules/autosamplingtheory-technicallemmas-probability-balancedrademacherclt.html','_site/modules/tests-bernoullilogsobolev.html','_site/modules/tests-balancedrademacherclt.html']
cells=['research-wiki/frontier-cells/ASTIS-SW-SPHMC-two-point-squared-entropy.json','research-wiki/frontier-cells/ASTIS-SW-SPHMC-bernoulli-function-lsi.json','research-wiki/frontier-cells/ASTIS-SW-SPHMC-balanced-rademacher-clt.json']
lessons=['website/content/declaration_lessons/'+s+'.json' for s in slugs]
pubs=['website/content/publications/'+s+'.json' for s in slugs]
for p in modules+tests+lessons+pubs+cells+['website/content/functor_hypergraph.json','website/content/graph_memory_index.json','website/static/underlying-lean-graph.css']:bind(p,True)
for p in ['_site/example-cases/samplewiki/companions/smoothed-picard-hmc.html']+modpages:bind(p)
run34='runs/20261007-companion-priority/bernoulli-function-lsi/'
run35='runs/20261007-companion-priority/balanced-rademacher-clt/'
evidence=[run34+p for p in ['math-freeze.json','verified.json','integration.json','publication-plan.json','graph.0.json','graph.1.json','graph.2.json','preproof/statement-seals.accepted.json','preproof/two-point.signature.txt','preproof/bernoulli.signature.txt','preproof/reviewer.statement.review.json','whole-proof-review/reviewer.math.review.json','source.0.review.overlay1.json','source.1.review.overlay1.json','source.0.reviewer-packet.overlay1.json','source.1.reviewer-packet.overlay1.json']]
evidence += [run35+p for p in ['math-freeze.json','verified.json','integration.json','publication-plan.json','preproof/statement-seals.accepted.json','preproof/signature.prospective.txt','whole-proof-review/math.review.json','source.0.review.json','source.0.reviewer-packet.json']]
evidence += ['runs/20261007-companion-priority/bernoulli-lsi-source-graph-review/source-topology-review.json','runs/20261007-companion-priority/rademacher-law-source-graph-review/source-topology-review.repaired.json','runs/20261007-companion-priority/bernoulli-lsi-source-graph-review/conceptual-mirror-review.json','runs/20261007-companion-priority/bernoulli-lsi-source-graph-review/discovery-validation.receipt.json']
evidence += ['docs/evidence-routed-memory-protocol.md','docs/proof-digestion-protocol.md','docs/theorem-publication-protocol.md','.agents/skills/astis-semantic-roundtrip/SKILL.md','.lake/packages/mathlib/Mathlib/Probability/CentralLimitTheorem.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/LevyConvergence.lean']
for p in evidence:bind(p)

def readj(p):return json.loads((root/p).read_text(encoding='utf-8'))
for path,selection in [(run34+'math-freeze.json',modules[:2]+tests[:1]),(run35+'math-freeze.json',modules[2:]+tests[1:])]:
    fz=readj(path)
    for p in selection:
        x=next(x for x in fz['inputs'] if x['path']==p);b=(root/p).read_bytes()
        assert sha(b)==x['raw_sha256'] and sha(lf(b))==x['lf_sha256']
for path,p in zip([run34+'source.0.review.overlay1.json',run34+'source.1.review.overlay1.json',run35+'source.0.review.json'],modules):
    x=readj(path);b=(root/p).read_bytes();assert x['verdict']=='equivalent-after-elaboration' and x['blocking']==False
    assert x['whole_module_lf_sha256']==sha(lf(b))
for r,c in [(run34,'6d5df34cdb124e28022f16f566ff549145eb7e65'),(run35,'4d9e71a6b835b54453a5cfd2d132f9a51f66f69c')]:
    x=readj(r+'verified.json');assert x['verified_commit']==c and x['verification_status']=='passed-scoped'
    for p in ([modules[0],modules[1],tests[0]] if r==run34 else [modules[2],tests[1]]):
        gb=subprocess.check_output(['git','show',c+':'+p],cwd=str(root));assert lf(gb)==lf((root/p).read_bytes())

class Reader(HTMLParser):
    def __init__(self):super().__init__();self.code=None;self.codes=[];self.details=[];self.links=[];self.text=[];self.ids=[]
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag=='code':self.code=[]
        if tag=='details':self.details.append(d)
        if tag=='a' and 'href' in d:self.links.append(d['href'])
        if 'id' in d:self.ids.append(d['id'])
    def handle_data(self,data):
        self.text.append(data)
        if self.code is not None:self.code.append(data)
    def handle_endtag(self,tag):
        if tag=='code' and self.code is not None:self.codes.append(''.join(self.code));self.code=None
def outer_section(t,slug):
    start=t.index('<section id="'+slug+'"');depth=0
    for m in re.finditer(r'<section\b[^>]*>|</section>',t[start:]):
        depth+= -1 if m.group().startswith('</') else 1
        if depth==0:return t[start:start+m.end()]
    raise RuntimeError('Missing balanced publication section '+slug)
companion='_site/example-cases/samplewiki/companions/smoothed-picard-hmc.html'
ht=(root/companion).read_text(encoding='utf-8');section_checks=[];module_checks=[]
signatures=[run34+'preproof/two-point.signature.txt',run34+'preproof/bernoulli.signature.txt',run35+'preproof/signature.prospective.txt']
for slug,mp,lp,pp,sp in zip(slugs,modules,lessons,pubs,signatures):
    unit=readj(lp)['units'][0];pub=readj(pp)['items'][0];sec=outer_section(ht,slug);r=Reader();r.feed(sec)
    src=lf((root/mp).read_bytes()).decode();short=unit['declaration'].split('.')[-1]
    a=src.index('theorem '+short);b=src.index(':= by',a);end=src.index('\nend ',b)
    header=src[a:b].strip();body=src[a:end].strip()
    assert header==(root/sp).read_text(encoding='utf-8').strip()
    assert any(x.strip()==header for x in r.codes)
    # The renderer retains the trailing namespace closure on the last public declaration.
    # This is an exact source excerpt, not a different proof or standalone copy claim.
    actualtail=src[a:].strip()
    matched=[x for x in r.codes if x.strip()==body or x.strip()==actualtail]
    assert matched
    assert unit['statement'] in ''.join(r.text)
    assert unit['assumptions']==pub['assumptions'] and unit['statement']==pub['statement']
    normtex=lambda x:x.replace('\\\\','\\')
    assert normtex(unit['formula']) in html.unescape(sec)
    for step in unit['steps']:assert step['title'] in html.unescape(sec) and normtex(step['formula']) in html.unescape(sec)
    dl=[d for d in r.details if d.get('data-inline-lean')==unit['declaration']]
    assert len(dl)==2 and all('open' not in d for d in dl)
    links=[l for l in r.links if 'complete-module-source' in l]
    assert len(links)==2
    resolved=[]
    for link in links:
        pathpart,anchor=link.split('#');actual=(root/companion).parent/pathpart;actual=actual.resolve();q=Reader();q.feed(actual.read_text(encoding='utf-8'));assert anchor in q.ids
        resolved.append({'href':link,'resolved_path':rel(actual),'actual_anchor_exists':True})
    test_links=[l for l in r.links if 'tests-bernoullilogsobolev' in l or 'tests-balancedrademacherclt' in l]
    tails=any(k in sec for k in ['theorem normalized_two_coordinate_entropy','theorem actual_first_moments_and_limit','theorem actual_zero_second_moment'])
    assert not tails
    secpath=base/('reviewer.exposition.'+slug+'.section.raw.snapshot.html')
    with secpath.open('xb') as f:f.write(sec.encode())
    section_checks.append({'slug':slug,'declaration':unit['declaration'],'section_snapshot':rel(secpath),'section_raw_sha256':sha(sec.encode()),
      'source_adjacent_statement_assumptions_formula_present':True,'all_authored_formula_steps_present':len(unit['steps']),
      'actual_inline_statement_equals_seal':True,'actual_inline_public_proof_equals_production':True,'statement_and_proof_initially_closed_in_HTML':True,
      'inline_proof_includes_exact_trailing_namespace_closure':any(x.strip()==actualtail for x in matched),
      'complete_module_context_links':resolved,'test_tails_inline':tails,'actual_test_page_links_from_this_section':test_links,
      'scope':'Static HTML/bytes only; no browser rendering or interaction test.'})
for sp,hp in zip(modules+tests,modpages):
    r=Reader();r.feed((root/hp).read_text(encoding='utf-8'));src=lf((root/sp).read_bytes()).decode()
    assert any(c==src for c in r.codes)
    assert 'complete-module-source' in r.ids
    priv=re.findall(r'\bprivate\s+(?:def|theorem|instance)\s+([^\s({:]+)',src)
    module_checks.append({'source':sp,'module_page':hp,'complete_code_block_LF_equals_source':True,'decoded_source_sha256':sha(src.encode()),
       'private_provider_count':len(priv),'private_providers':priv,'all_imports_namespace_body_Test_tail_retained':True,
       'per_declaration_excerpt_may_be_truncated':'TwoPoint individual helper excerpt contains an explicit truncation notice; the complete-module-source block is exact and untruncated.' if 'TwoPoint' in sp else None})

cellsj=[readj(p) for p in cells];units=[readj(p)['units'][0] for p in lessons]
assert cellsj[0]['parents']==[] and cellsj[1]['parents']==['ASTIS-SW-SPHMC-two-point-squared-entropy'] and cellsj[2]['parents']==[]
assert units[0]['astis_dependencies']==[] and units[1]['astis_dependencies']==[units[0]['declaration']] and units[2]['astis_dependencies']==[]
assert 'import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.TwoPointEntropy' in (root/modules[1]).read_text()
assert 'BernoulliLogSobolev' not in (root/modules[2]).read_text()
graph_checks=[readj(run34+'graph.%d.json'%i) for i in range(3)]
f=readj('website/content/functor_hypergraph.json')
def find_id(x,id):
    if isinstance(x,dict):
        if x.get('id')==id:return x
        for y in x.values():
            z=find_id(y,id)
            if z:return z
    if isinstance(x,list):
        for y in x:
            z=find_id(y,id)
            if z:return z
bridge=find_id(f,'transport:bernoulli-gaussian-entropy-energy-limit')
assert bridge['formal_refs']==[] and bridge['status']=='not-Lean-certified'
mr=readj('runs/20261007-companion-priority/bernoulli-lsi-source-graph-review/conceptual-mirror-review.json')
assert mr['verdict']=='accepted-scoped-conceptual-only' and mr['independent_from_creator']
assert bridge['review']['review_raw_sha256']==sha((root/'runs/20261007-companion-priority/bernoulli-lsi-source-graph-review/conceptual-mirror-review.json').read_bytes())
css=(root/'website/static/underlying-lean-graph.css').read_text();assert '.ulg-edge.overlay-edge{stroke-dasharray:7 5;' in css

checks=write('reviewer.exposition.checks.json',{'checked_commit':commit,'scope':'Independently inspected root-authored explanation against exact current code and generated HTML; current source-fidelity/graph truth comes from named distinct phase receipts, not from my sourcegraph authorship.',
 'sections':section_checks,'module_source_pages':module_checks,
 'actual_formal_parents':{'TwoPoint':[],'Bernoulli':[units[0]['declaration']],'CLT':'Only actual Mathlib imports; no fabricated Bernoulli -> CLT formal edge.'},
 'mathlib_CLT_exact_local_header':{'path':'.lake/packages/mathlib/Mathlib/Probability/CentralLimitTheorem.lean','lines':[55,57],'name':'ProbabilityTheory.tendsto_charFun_inv_sqrt_mul_pow','hypotheses':'Actual measurable coordinate, internally derived mean0 and second moment1 under true probability P.'},
 'mirror':{'bridge_id':bridge['id'],'source_ids':bridge['source_ids'],'formal_refs':[],'status':'not-Lean-certified','distinct_validation_receipt':bridge['review']['evidence'],'overlay_dashed_stylesheet_rule_present':True,'browser_dashed_rendering_checked':False},
 'inputs':inputs,'no_compiler_no_rerender_no_canonical_write':True,
 'comparison_reconciliation':'Initial helper demanded body-only equality and stopped before any verdict. Actual renderer preserves exact trailing namespace closure for the last declaration. Reconciled comparison against the literal canonical source tail; all original frozen snapshots reused byte-exact. No input, reader or production change.'})

mapping=[
 {'declaration':units[0]['declaration'],'source_nodes':['SLT d0f506f0 TwoPoint.rothaus_lemma positive upper direction','authored signed-square/zero extension','SPHMC S4.E6 omitted background context only'],
  'conceptual_moves':[{'reader_step':'Positive squares','lean_nodes':['phi','rothausDefect','deriv2_rothausDefect_nonneg','rothausDefect_nonneg','rothaus_lemma'],
  'expansion':'phi(t)=(1+t)log(1+t)+(1-t)log(1-t); |t|<1. Defect D=2-2sqrt(1-t²)-phi has D0=Dprime0=0 and Dsecond>=0; two MVTs on each sign interval give D>=0. Rescale m=(A+B)/2 and t=(A-B)/(A+B). Named private phi is compactly referenced in the roadmap and defined in exact complete module context.'},
  {'reader_step':'Signed inputs','lean_nodes':['two_point_squared_entropy_le_half_sq_sub','Real.sqrt_sq_eq_abs','abs_abs_sub_abs_le_abs_sub'],'expansion':'Positive squares A=a²,B=b² when nonzero; reverse absolute-value inequality gives (|a|-|b|)² <= (a-b)².'},
  {'reader_step':'Zero inputs','lean_nodes':['two_point_squared_entropy_le_half_sq_sub','Real.log_div','Real.log_le_sub_one_of_pos'],'expansion':'One zero gives A log2/2 <= A/2; bothzero0. No caller positivity.'}],
  'preserved_interface':'All signed real a,b; exact homogeneous entropy and 1/2 bound.'},
 {'declaration':units[1]['declaration'],'source_nodes':['SLT d0f506f0 BernoulliLSI finite uniform law/entropy statement','upstream Han route distinctly disclosed; actual entropy/RMS induction authored','SPHMC FIRST4.6 future GaussianLSI context only'],
  'conceptual_moves':[{'reader_step':'Actual finite law','lean_nodes':['bernoulliUniform','card_fin_bool','probability','bernoulli_integral_eq_sum','bernoulli_integral_succ_split'],'expansion':'card=2^n, actual normalized count probability; genuine finite Bochner domains; snoc balanced-coordinate decomposition.'},
  {'reader_step':'Entropy chain','lean_nodes':['rms','rms_sq','localEntropy','entropy_chain'],'expansion':'g=sqrt((hplus²+hminus²)/2); exact entropy = mean local two-point entropy + entropy(g²), all same law.'},
  {'reader_step':'RMS contraction','lean_nodes':['rms_contraction','rms_energy'],'expansion':'Reverse Euclidean norm bound, internal square-root domains and Cauchy-Schwarz derived from (ad-bc)²>=0.'},
  {'reader_step':'Half constant and n0','lean_nodes':[units[0]['declaration'],'energy_chain','flipCoord_last_snoc','flipCoord_castSucc_snoc','entropy_bound','bernoulli_function_logSobolev'],'expansion':'Signed two-point controls last-coordinate energy; IH and RMS control prefix. Sum exact energy decomposition with coefficient1/2. n0 singleton entropy and energyzero; threeL1+probability returned internally.'}],
  'preserved_interface':'Every n>=0 and arbitrary signed h on all Fin n->Bool; actual full update flip, unnormalized coordinate sum, three L1/probability outputs.'},
 {'declaration':units[2]['declaration'],'source_nodes':['Mathlib db584cd6 scalar characteristic-function CLT','Mathlib Levy weak probability convergence','authored exact Bool count/CF/zero/successor adapter','SPHMC S4.E6 omitted GaussianLSI future context only'],
  'conceptual_moves':[{'reader_step':'Actual laws','lean_nodes':['countLaw','countLaw_probability','countLaw_integral','normalizedSum','actualLaw','actualLaw_zero'],'expansion':'True all-N normalized count maps; N0 empty sum iszero and lawdirac0.'},
  {'reader_step':'Actual coordinate moments','lean_nodes':['sign','sign_mean','sign_second_moment','coordinateLaw'],'expansion':'true sign+1/false-1 under actual balanced law, internally mean0 secondmoment1.'},
  {'reader_step':'Finite CF product','lean_nodes':['coordinate_charFun','unscaled_charFun','normalized_charFun','Complex.exp_sum','Fintype.sum_pow'],'expansion':'Finite configuration sum/product yields actual Nth CFpower at inverse sqrt(N)t; no independence/CLT certificate or Bernoulli parent.'},
  {'reader_step':'Pinned CLT','lean_nodes':['ProbabilityTheory.tendsto_charFun_inv_sqrt_mul_pow','ProbabilityTheory.charFun_gaussianReal'],'expansion':'Same internally derived moments -> exp(-t²/2), exact mean0 varianceNNReal1 Gaussian.'},
  {'reader_step':'Weak successor family','lean_nodes':['MeasureTheory.ProbabilityMeasure.tendsto_iff_tendsto_charFun','actualLaw_tendsto','Filter.tendsto_add_atTop_nat','balanced_count_sum_tendsto_gaussian'],'expansion':'Actual family weakly converges, then cofinal successor composition supplies exact sealed conclusion alongside all maps and N0.'}],
  'preserved_interface':'Closed exists-family/all-N exact map, lambda0dirac0, successor weak probability-law Gaussian0 variance1; no entropy/energy/W2 or unbounded-cost conclusion.'}
]
delivery_gap={'status':'FULL_READER_DELIVERY_GAP','blocking_for_scoped_static_mathematical_exposition':False,'blocking_for_PURIFIED_or_full_reader_delivery':True,
 'observed':'Production module and complete Test module pages contain exact full source. Actual Test theorem tails are not inline in companion sections; no linked or interactive Test flow is certified.',
 'remaining':['Actual Test-tail companion placement/link delivery','Copy Lean/copy-download behavior and source/Test download acceptance','Paper/book chapter-pack/link/download completeness','Rendered/browser/mobile/device/interaction evidence','Public live/published-head delivery evidence','Postmerge purification and PURIFIED admission'],
 'not_inferred_from':['existing module Test pages','HTML details markup','repository/static gates','proof compilation','previous phase fidelity verdicts']}
seal=write('ExpositionSeal.json',{'schema_version':1,'artifact_kind':'JOINT_SCOPED_STATIC_EXPOSITION_SEAL','verdict':'ACCEPTED_SCOPED_EXPOSITION_SEAL','status':'accepted-scoped-static-mathematical-exposition','blocking':False,'blockers':[],
 'reviewer':'gaussian_domain_preproof_reviewer_29','author':'companion_root_20261005','independent_from_authored_prose':True,'checked_commit':commit,
 'joint_packets':['ASTIS-SA-20261007-BernoulliFunctionLogSobolev','ASTIS-SA-20261007-BalancedRademacherCLT'],
 'source_expansion_nodes':[z for x in mapping for z in x['source_nodes']],
 'lean_expansion_nodes':[x['declaration'] for x in mapping],
 'compressed_reader_to_source_Lean_expansion':mapping,'assumptions_preserved':True,'quantifiers_constants_signed_zero_domains_preserved':True,'boundary_preserved':True,
 'independent_basis':'Read actual current root-authored lessons/publications, all3 complete modules and2 Tests, generated source-adjacent formulas/closed actual public proofs and exact full module code. Read distinct phase source/mirror receipts for their separate provenance. No prior verdict used as proof of readability and no own sourcegraph validated.',
 'proof_provenance':{'34_verified_commit':'6d5df34cdb124e28022f16f566ff549145eb7e65','35_verified_commit':'4d9e71a6b835b54453a5cfd2d132f9a51f66f69c','production_Test_LF_identical_to_verified_commits':True,'shared_commit_current_LF_binding':commit,'new_compiler_run':False,'repository_gate_owner':'Separate picard verifier; not this exposition reviewer.'},
 'actual_dependency_semantics':'TwoPoint -> Bernoulli is genuine compiled parent. CLT actual proof imports/calls pinned Mathlib and has no Bernoulli parent. Conceptual mirror is independently phase-validated, formal_refs=[], not-Lean-certified with dashed overlay stylesheet semantics only; no rendered certificate.',
 'static_readability_checks':checks,'input_artifacts':inputs,'reader_delivery':delivery_gap,
 'truth_boundary':['Gaussian entropy convergence','full flip-energy4 limit','compact Gaussian LSI','finite-Hilbert/tensorization','actual noncompact sqrt-density/cutoff/W12','Gaussian T2','FIRST4.6/W2/bias','paper main/work/cost/composition','remote live/postmerge PURIFIED'],
 'nonblocking_context_notes':['The compressed Rothaus roadmap names phi; exact definition and all26 private providers are retained through complete module context, and the expansion is explicit in this receipt.','Mathlib source link L59 points inside the named CLT primitive proof; exact current local declaration header is55-57 and is bound here.','Historical graph-family reading order still calls the weak-law stage open; the actual35 lesson/cell/source/proof provenance and genuine module are explicit. This conservative family-stage description supplies no false completion credit.'],
 'no_canonical_production_site_graph_or_ledger_mutation':True,'no_source_topology_selfvalidation':True})
for x in inputs:
    b=(root/x['path']).read_bytes();assert sha(b)==x['raw_sha256'] and sha(lf(b))==x['lf_sha256'],x['path']
runid=sha(json.dumps({'checked_commit':commit,'input_hashes':[{k:x[k] for k in ['path','raw_sha256','lf_sha256']} for x in inputs],'outputs':[checks,seal]},sort_keys=True,separators=(',',':')).encode())
run=write('reviewer.exposition.run.json',{'status':'CLOSED','deterministic_run_sha256':runid,'checked_commit':commit,'outputs':[checks,seal],'all_inputs_unchanged_at_close':True,'input_count':len(inputs),'scope':'Static mathematical exposition only; FULL_READER_DELIVERY_GAP remains open.','compiler_started':False})
lp=base/'reviewer.exposition.lease.json';lease=json.loads(lp.read_text(encoding='utf-8'));lease.update(status='CLOSED',read_lease='CLOSED',write_lease='CLOSED',compiler_lease='CLOSED',compiler_started=False,closed_utc=datetime.datetime.utcnow().isoformat()+'Z',run=run,deterministic_run_sha256=runid)
lp.write_bytes(dump(lease))
print(json.dumps({'seal':seal,'checks':checks,'run':run,'run_id':runid,'inputs':len(inputs),'leases':'CLOSED','verdict':'ACCEPTED_SCOPED_EXPOSITION_SEAL','delivery':'FULL_READER_DELIVERY_GAP'},indent=2))
