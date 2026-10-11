from pathlib import Path
import json,hashlib,datetime
R=Path('E:/Samplinglib');D=R/'runs/20261007-companion-priority/pbps-actual-prescribed-path-density94/independent-whole-math94/exposition94';W=D.parent
def sha(b):return hashlib.sha256(b).hexdigest()
def info(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=sha(b),bytes=len(b))
def write(n,b):
 p=D/n;assert not p.exists(),p;p.write_bytes(b);return p
def js(n,j):return info(write(n,(json.dumps(j,ensure_ascii=False,indent=2)+'\n').encode()))
pub=R/'website/content/publications/pbps-actual-prescribed-path-density.json';lesson=R/'website/content/declaration_lessons/pbps-actual-prescribed-path-density.json';prod=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPrescribedPathDensity.lean'
oldpub=json.loads((D/'publication.initial.exactraw.json').read_bytes());oldlesson=json.loads((D/'lesson.initial.exactraw.json').read_bytes());p=json.loads(pub.read_bytes());l=json.loads(lesson.read_bytes());u=l['units'][0]
assert sha(prod.read_bytes())=='5065f542feea7024214159903ad3e7b81f6df9a6fcbf46afecace49397d786a0'
assert p==oldpub,'Publication changed; manually inspect before accepting'
assert u['statement']==u['lean_statement']==p['items'][0]['statement']
assert u['assumptions']==p['items'][0]['assumptions']
assert 'a<=b' in u['steps'][1]['text'] and 'a\\le b' in u['steps'][1]['formula']
assert 'continuous' in u['steps'][2]['text'] and 'f=g_j' in u['steps'][2]['text']
assert 'ofReal(exp(-h_n))' in u['steps'][6]['text']
assert "ENNReal.ofReal_mul'" in u['mathlib_dependencies']
def diffs(a,b,path=''):
 if type(a)!=type(b):return [dict(path=path,before=a,after=b)]
 if isinstance(a,dict):
  assert a.keys()==b.keys(),path
  return sum((diffs(a[k],b[k],path+'/'+k) for k in a),[])
 if isinstance(a,list):
  assert len(a)==len(b),path
  return sum((diffs(x,y,path+'/'+str(i)) for i,(x,y) in enumerate(zip(a,b))),[])
 return [] if a==b else [dict(path=path,before=a,after=b)]
delta=diffs(oldlesson,l)
allowed={'/units/0/steps/1/text','/units/0/steps/1/formula','/units/0/steps/2/text','/units/0/steps/2/formula','/units/0/steps/6/text','/units/0/mathlib_dependencies/7'}
assert all(x['path'] in allowed for x in delta),delta
inputs=[info(p) for p in [pub,lesson,prod,W/'whole-math-decision94.native.json',W/'closed-RAW-whole94.native.json',R/'runs/20261007-companion-priority/pbps-prescribed-path-density-preread94/Header94.lean',R/'runs/20261007-companion-priority/pbps-prescribed-path-density-preread94/root.statement-seal94.json']]
write('publication.accepted.exactraw.json',pub.read_bytes());write('lesson.accepted.exactraw.json',lesson.read_bytes())
lines=prod.read_bytes().splitlines(keepends=True);regions=[]
for i,s in enumerate(u['steps'],1):
 r=s['lean_source_region'];raw=b''.join(lines[r['start_line']-1:r['end_line']]);code=s['lean'].encode()
 assert r['source_raw_sha256']==sha(prod.read_bytes()) and r['exact_code_raw_sha256']==sha(code)
 assert raw.decode().replace('\r\n','\n')==s['lean']
 assert s['lean']==oldlesson['units'][0]['steps'][i-1]['lean']
 regions.append(dict(step=i,title=s['title'],start_line=r['start_line'],end_line=r['end_line'],physical_source_region_raw_sha256=sha(raw),embedded_code_utf8_sha256=sha(code),exact_code_metadata_valid=True,equal_after_CRLF_to_LF=True))
js('initial-required-corrections94.native.json',dict(status='INITIAL_EXPOSITION_PRECISION_CHECK_NOT_ACCEPTED',initial_publication=info(D/'publication.initial.exactraw.json'),initial_lesson=info(D/'lesson.initial.exactraw.json'),findings=[dict(location='steps[1].text/formula',severity='required mathematical hypothesis',finding='Readable generic arc integral implication omitted a<=b.',counterexample='a=1,b=0,f identically1,g identically0: agreement on empty Ioo(1,0) holds and g is continuous, but integral1..0 f=-1 while integral1..0 g=0.'),dict(location='steps[2].text',severity='required complete readable hypotheses',finding='The generic finite-sum step needs continuous g_j and f=g_j on each open arc, in addition to a nondecreasing grid.',counterexample='One interval[0,1], f identically1 and g0 identically0 gives1!=0 if comparison agreement is omitted.'),dict(location='steps[6].text',severity='type precision',finding='Tagged weight is ofReal(exp(-h_n)), not literally the real exponential.'),dict(location='mathlib_dependencies',severity='API precision',finding="The directly used multiplication lemma is ENNReal.ofReal_mul'.")],production_defects=[]))
js('accepted-revision-diff94.native.json',dict(status='PASS',publication_semantically_unchanged=True,lesson_changes=delta,all_embedded_lean_unchanged=True,regions=regions,normalization_recipe='Embedded code strings encode the exact cited source lines with CRLF decoded to LF. Metadata exact_code_raw_sha256 is SHA256 of that embedded UTF8 code; physical CRLF slice RAW is recorded separately. Entire physical production RAW remains independently pinned.'))
review={
 'schema_version':1,'kind':'INDEPENDENT_AUTHORED_EXPOSITION_MATHEMATICAL_CONSISTENCY_REVIEW','reviewer':'/root/independent_whole_math93','author':'companion_root_20261005','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'decision':'ACCEPT_REVISED_AUTHORED_EXPOSITION','inputs':inputs,
 'scope':'Complete statement, definitions, quantifiers, degenerate cases, displayed formulae, seven stepwise mathematical explanations and exact Lean-region associations against accepted production. No source fidelity verdict, visual acceptance, publication-state transition or ledger change.',
 'kernel_reuse':'Unchanged exact production RAW5065f542feea7024214159903ad3e7b81f6df9a6fcbf46afecace49397d786a0 matches the accepted whole-math/kernel review. No repeat kernel compilation needed for prose-only corrections.',
 'statement_review':['Publication and lesson statement/lean_statement agree. All six analytic conditions, finite-dimensional real Hilbert Borel typing and rank-zero inclusion match the sealed theorem.','Flow c/Phi, totalized reflection S, nonnegative rate, Lebesgue arc hazard, strict simplex, recursively reflected states, live/stopped histories, qReal/q, truncated terminal duration, W/rho, total ordered-record interpolation, Gamma and real clamp agree with the20 literal definitions. readTime in prose is a disclosed mathematical name for production liveTime with identical live/stopped values.','The theorem is universally quantified in parameters, finite count/horizon and every strict tuple. Integrability and incoming limits are conclusions; no actual stochastic provider or positive-rate premise is added.','All four conjunctions are stated. Incoming rate factors use pre-bounce limits; endpoint post-bounce values are not substituted. The n+1 hazard sum includes the final survival interval.','n=0 has one survival arc and empty product1; T=0 has only the zero-event simplex; rank zero and zero rates remain included. No claim that n=0 density is always1.','The clamp agrees on[0,T] and is locally inactive at interior events. No full path-space topology or uncountable joint-evaluation measurability assumption is introduced.','Statements explicitly leave actual finite-count composition, all-count summation/full A7, signed convergence and broader paper results outside this theorem.'],
 'steps_review':[
  {'step':1,'result':'PASS','reason':'Nondecreasing grid, clamp removal on open arcs and last-eligible-record formula match actual_arc, including n=0,T=0.'},
  {'step':2,'result':'PASS_AFTER_CORRECTION','reason':'Now explicitly assumes a<=b in prose and formula. Continuous comparison plus open-interval agreement transfers Lebesgue interval integrability and integral through null endpoints, including a=b.'},
  {'step':3,'result':'PASS_AFTER_CORRECTION','reason':'Now states nondecreasing grid, continuous comparisons and open-arc agreement. Prefix/last induction and finite sum splitting match finite_arc_integral, allowing zero lengths.'},
  {'step':4,'result':'PASS','reason':'Strict preceding gap supplies a left neighborhood; continuity and eventual equality give incoming limit without using endpoint value.'},
  {'step':5,'result':'PASS','reason':'Actual flow/rate continuity, fixed-arc composition, finite integration, translation and incoming-limit composition match actual_analysis. Formula includes n+1 hazards and phase/rate limits.'},
  {'step':6,'result':'PASS','reason':'Real product/exponential algebra is valid for arbitrary real arrays and empty products; no positivity, cancellation or rate division needed.'},
  {'step':7,'result':'PASS_AFTER_TYPE_PRECISION','reason':'Terminal duration comparison uses0<=a_n<=T, weight is explicitly ofReal(exp(-h_n)), and the nonnegative terminal exponential justifies ofReal multiplication. Product survival and the proved hazard sum yield original rho.'}
 ],
 'regions_review':{'count':7,'status':'PASS','all_line_ranges_valid':True,'whole_source_hash_valid':True,'all_embedded_hashes_valid':True,'newline_convention_disclosed':True,'compiled_regions_not_standalone_proofs':'Embedded regions are exact source excerpts in their production environment, with unchanged previously checked dependencies; no separate standalone-compilation claim.'},
 'dependency_review':'Three ASTIS producer declarations agree with actual code dependencies. Mathlib directly used ofReal_mul\u0027 name corrected; finite integration/left-neighborhood/exponential APIs align with the proof.',
 'initial_findings_retained':True,'unresolved_required_corrections':[],'production_or_public_files_edited_by_reviewer':False,'source_review_verdict':False,'visual_acceptance':False,'SAU_verified_transition':False,'whole_A7_completed':False
}
a=js('exposition-decision94.native.json',review)
manifest={'schema_version':1,'kind':'CLOSED_RAW_EXPOSITION_REVIEW','hash_recipe':'SHA256 exact bytes; no canonical JSON or newline-normalized substitute for file RAW. Manifest excludes itself. Region newline semantics explicitly recorded.','inputs':inputs,'outputs':[info(p) for p in sorted(D.iterdir()) if p.is_file()],'closure':'All owned files prior to manifest creation enumerated; initial failed precision review and corrected exact inputs retained. Earlier closed whole-math manifest untouched.'}
m=js('closed-RAW-exposition94.native.json',manifest)
for row in manifest['inputs']+manifest['outputs']:assert info(R/row['path'])==row
assert {p.name for p in D.iterdir() if p.is_file()}=={Path(x['path']).name for x in manifest['outputs']}|{'closed-RAW-exposition94.native.json'}
print(json.dumps(dict(status='PASS',accepted_publication=inputs[0],accepted_lesson=inputs[1],decision=a,manifest=m),indent=2))
