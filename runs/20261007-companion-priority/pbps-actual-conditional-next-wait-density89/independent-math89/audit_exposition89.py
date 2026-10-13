import hashlib,json
from pathlib import Path
from datetime import datetime,timezone
R=Path('E:/Samplinglib'); O=Path(__file__).parent
def pin(p):
    b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def put(n,x):
    p=O/n
    with p.open('x',encoding='utf8',newline='\n') as f:json.dump(x,f,ensure_ascii=False,indent=2);f.write('\n')
    return pin(p)
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualConditionalNextWaitDensity.lean'
assert pin(M)['raw_sha256']=='36813b659cbdbb4b31c6300abd1300858d42afe683046b8c06ff9c22806e8e37'
lines=M.read_text('utf8').splitlines()
L=O/'lesson89.original.exactraw.json'; P=O/'publication89.original.exactraw.json'
u=json.loads(L.read_text('utf8'))['units'][0]
pub=json.loads(P.read_text('utf8'))
regions=[]
expected=[(115,258),(259,306),(307,358),(359,366),(367,406),(407,436)]
for i,(s,pair) in enumerate(zip(u['steps'],expected)):
    x=s['lean_source_region']; assert (x['start_line'],x['end_line'])==pair
    assert x['source_raw_sha256']==pin(M)['raw_sha256']
    code='\n'.join(lines[pair[0]-1:pair[1]])+'\n'
    assert s['lean']==code
    sha=hashlib.sha256(code.encode()).hexdigest();assert sha==x['exact_code_raw_sha256']
    regions.append({'step':i+1,'lines':list(pair),'exact_code_raw_sha256':sha,'code_exact':True,'title':s['title'],'formula':s['formula']})
assert len(u['steps'])==6
assert all(expected[i][1]+1==expected[i+1][0] for i in range(5))
assert lines[113].endswith(':= by') and lines[435].strip().endswith('D h s')
result=put('original-exposition89.audit.json',{
 'status':'MATHEMATICS_ACCEPTED_ORIGINAL_EXPOSITION_REQUIRES_ONE_SEQUENCING_FIELD_REPAIR',
 'reviewer_id':'/root/exact_verify77','created_utc':datetime.now(timezone.utc).isoformat(),
 'module':pin(M),'original_lesson_snapshot':pin(L),'original_publication_snapshot':pin(P),
 'coverage':{'public_BODY_lines':[115,436],'six_exact_contiguous_regions':regions,'entire_BODY_covered_without_gaps_or_overlap':True,'initial_classical_and_local_definitions_included':True},
 'full_statement':{'six_original_analytic_conditions':True,'fourteen_model_and_nine_packaging_definitions':True,'full_tagged_history_not_state_only':True,'fixed_depth_parameters':True,'all_abstract_history_fibers':True,'all_Borel_finite_valued_cutoffs_no_global_bound':True,'all_jointly_Borel_ENNReal_tests_no_L1_premise':True,'unnormalized_event_including_null_A':True,'strict_endpoints_top_and_stopped_exclusions':True,'no_closed_open_mass_equivalence':True},
 'stepwise_findings':[
  'Step1 derives all total joint Borel observables and finite density from internally consumed actual parents, retaining six assumptions and literal model.',
  'Step2 text and exact code correctly construct actual histories, guards, density and measurable withDensity kernel. Its formula alone states the later mass bound before its proof; remove that single clause.',
  'Step3 correctly restricts verified86 Ioc law by Iio, with explicit top/finite comparison and dead branch. It makes no no-atom or strict mass equality claim.',
  'Step4 proves every-history kernel mass at most1 from actual restricted probability, including unrealizable histories. It does not claim pointwise density at most1.',
  'Step5 identifies the full joint measure on arbitrary Borel sets through actual87 product law and Tonelli, and establishes subprobability.',
  'Step6 transfers every jointly Borel nonnegative extended test and Borel history event; no conditional normalization, positive mass, signed integration or boundedness requirement.'
 ],
 'publication_conclusions':'The five theorem-level formulas are mathematically correct including global kernel mass bound. No publication conclusion field repair is required.',
 'source_attribution_and_boundary':'Source A1.E7 ordered-event factor with A1.E1/A1.E2 and Appendix A2 is expressly attributed as ASTIS source-implicit completion. Only deterministic-depth conditional finite-density component is supplied; survival88 is adjacent, not an AND dependency. Full I5/A7, ordered-time iteration/final survival/count/path summability and global invariance/Markov/restart/L2/cost/composition/wholepaper/Goal remain OPEN.',
 'readability':'Complete attributed conditions, measures, definitions and formula proofs are adjacent to exact Lean source regions. This audit checks content/code pairing only, not rendered browser layout or live delivery.',
 'required_repairs':[{'json_pointer':'/units/0/steps/1/formula','type':'exposition-only sequencing','proposal':pin(O/'proposed-exposition-overlay89.json'),'independent_acceptance':'pending distinct reviewer'}],
 'no_final_source_or_decoder_verdict_read':True,'no_canonical_changes':True})
print(json.dumps(result))
