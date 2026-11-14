import json,os
from run import ROOT,run,sha
m=json.loads((ROOT/'input-manifest.json').read_text());env=dict(os.environ);env['LEAN_PATH']=os.pathsep.join(m['lean_path']);env.pop('LEAN_SRC_PATH',None)
for label,src in [('independent-literal-kernel-v3','IndependentLiteralCheckV3.lean')]:
    r=run(label,[m['lean_binary']['path'],'-R',str(ROOT/'scratch'),str(ROOT/'scratch'/src)],cwd=ROOT/'scratch',env=env)
    assert r.returncode==0,label
data=(ROOT/'native-all-bodies-v2.json').read_bytes();rows=json.loads(data)
new=[r for r in rows if r['module'] in ['AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowLaw','Tests.GaussianComplexityFixedSpectrumSourceRowLaw']]
assert len(new)==4,len(new)
producer=next(r for r in new if r['name'].endswith('.actual_source_row_marginal_law'))
consumer=next(r for r in new if r['name'].endswith('.actual_original_all_good_cutoff_probability'))
reachable=set(producer['transitive_owned']+consumer['transitive_owned'])
def ps(root):
    todo=list(root['direct']);seen=set();parents=set()
    own={r['name']:r for r in new}
    while todo:
        n=todo.pop()
        if n in seen:continue
        seen.add(n)
        if n==producer['name']:parents.add(n)
        elif n in own:todo.extend(own[n]['direct'])
        elif n.startswith('AutoSamplingTheory.'):parents.add(n)
    return sorted(parents)
prodparents=ps(producer);conparents=ps(consumer)
expected='AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianRadialExponential.integrable_exp_norm_sq_div_three_and_integral_stdGaussian'
assert prodparents==[] and conparents==sorted([producer['name'],expected]),(prodparents,conparents)
assert all(r['name'] in reachable for r in new)
assert any('MeasureTheory.integral_map' in r['direct'] for r in new)
summary=[]
for r in rows:
    summary.append({k:v for k,v in r.items() if k not in ['body','type','direct']}|{'type_sha256':sha(r['type'].encode()),'body_sha256':sha(r['body'].encode()),'type_chars':len(r['type']),'body_chars':len(r['body']),'reachable_from_new_roots':r['name'] in reachable})
unreachable=[r for r in summary if not r['reachable_from_new_roots']]
result={'candidate_commit':m['candidate_commit'],'module_owned_total':len(rows),'new_owned_total':len(new),'new_owned_names':[r['name'] for r in new],'producer_ASTIS_parents':prodparents,'consumer_ASTIS_parents':conparents,'all_new_owned_reachable':True,'all_types_bodies_closed':True,'only_standard_axioms':['propext','Classical.choice','Quot.sound'],'large_full_dump':{'path':'native-all-bodies-v2.json','bytes':len(data),'sha256':sha(data),'portable_inclusion':False},'all_declarations':summary,'older_unreachable_preserved':[r['name'] for r in unreachable]}
(ROOT/'native-summary.json').write_text(json.dumps(result,indent=2)+'\n')
(ROOT/'native-authored-types.txt').write_text('\n\n'.join(r['name']+'\n'+r['type'] for r in rows if not any(x in r['name'] for x in ['proof_','_aux','match_']))+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='all_declarations'},indent=2))
