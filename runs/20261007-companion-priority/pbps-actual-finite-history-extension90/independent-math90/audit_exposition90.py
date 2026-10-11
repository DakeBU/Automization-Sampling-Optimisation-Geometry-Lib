from pathlib import Path
import datetime,hashlib,json
R=Path('E:/Samplinglib');O=Path(__file__).parent
def pin(p):
 p=Path(p);b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteHistoryExtension.lean'
L=O/'lesson90.original.exactraw.json';P=O/'publication90.original.exactraw.json'
u=json.loads(L.read_text('utf8'))['units'][0];p=json.loads(P.read_text('utf8'))['items'][0]
assert u['statement']==p['statement'] and u['assumptions']==p['assumptions']
lines=M.read_bytes().splitlines(keepends=True);checks=[]
for i,s in enumerate(u['steps']):
 q=s['lean_source_region'];a=q['start_line'];b=q['end_line'];exact=b''.join(lines[a-1:b])
 assert q['source_raw_sha256']==pin(M)['raw_sha256']
 assert hashlib.sha256(exact).hexdigest()==q['exact_code_raw_sha256']
 assert exact.decode('utf8')==s['lean']
 checks.append({'step':i+1,'start_line':a,'end_line':b,'exact_BODY_digest':q['exact_code_raw_sha256'],'code_matches_exact_region':True,'title':s['title'],'formula':s['formula']})
assert len(checks)==6 and checks[0]['start_line']==120 and checks[-1]['end_line']==340
assert all(a['end_line']+1==b['start_line'] for a,b in zip(checks,checks[1:]))
assert lines[118].decode().strip().endswith(':= by') and lines[119].decode().strip()=='classical'
assert b''.join(lines[340:]).decode().strip()=='end\nend AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryExtension'
roles=[
 'Definitions and four actual producer applications, all original model assumptions and totalizations. Only formula0 needs exact total-definition display repair.',
 'Borel Hnext, zero-safe Sum update, finite tuple coordinate proof and exact old-prefix preservation match complete BODY.',
 'Literal strict component definitions then89 observable/law/mass/test conclusions, Y Borel. Formula states definitions only, no premature theorem claim.',
 'Live finite upper bound and stopped positive contradiction; Nat.rec final coordinate and unchanged earlier coordinates. Pointwise, not only AE.',
 'Restricted AE congruence and measurable composition, actual joint+marginal pushforward and inherited subprobability mass. No normalization.',
 'Admissible F∘lift, parameter measurability and integrand equality throughout B∩H^-1A, then exact89 identity. Null A/infinite F included.'
]
result={'status':'WHOLE_EXPOSITION_READ_EXACT_SIX_REGIONS_TWO_FIELD_TOTAL_DEFINITION_REPAIR_PENDING',
 'reviewer_id':'/root/exact_verify77','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'module':pin(M),'original_lesson':pin(L),'original_publication':pin(P),'regions':checks,
 'complete_contiguous_public_BODY_coverage':True,'full_BODY_lines':[120,340],
 'whole_statement_and_assumptions_same_lesson_publication':True,'six_original_analytics_all_literal_definitions_and_test_classes_complete':True,
 'all_six_natural_proof_steps_independently_mathematically_checked':roles,
 'correct_attribution':'Printed A1(A1,A2,A7) and A2 Borel construction; explicit ASTIS source-implicit complete-history transport ingredient, no printed standalone source theorem claimed.',
 'full_quantifiers':'All fixed y/ref/z0/deterministic n, all Borel pointwise finite cutoffs d with no global bound, all Borel ENNReal joint F and all Borel old-history A including null events.',
 'boundaries':'Restricted subprobability finite component only; no noatom or closed/open mass equality, finite-wait guarantee, unrestricted next history, random stopping/restart/Markov/fullA7/global invariance/L2/cost/main/wholeGoal.',
 'required_exposition_repairs':[{'lesson_pointer':'/units/0/steps/0/formula','publication_pointer':'/items/0/formulae/0/tex','proposal':pin(O/'proposed-exposition-overlay90.json'),'reason':'Display exact total live branch T+max{s,0} for all real s, not partial live s>0 branch.'}],
 'mathematical_Lean_or_Seal_repairs_required':False,'no_final_source_or_decoder_verdict_read':True,'no_canonical_writes_or_acceptance_of_own_repair':True}
with (O/'original-exposition90.audit.json').open('x',encoding='utf8',newline='\n') as f:json.dump(result,f,ensure_ascii=False,indent=2);f.write('\n')
print('ALL_SIX_BODY_REGIONS_EXACT_120_340; TOTAL_DEFINITION_FORMULA_REPAIR_PENDING')
