from pathlib import Path
import hashlib,json
r=Path(__file__).parent;p=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhaseTransitionKernel.lean')
q=json.loads((r/'focused85-attempt1/receipt.json').read_bytes());assert q['exit_code']==1
raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()==q['source_RAW_sha256']
s=raw.decode('utf8')
doc='''/-- Actual full-phase law with joint finite-time index, Dirac initialization and
bounded Borel expectation transfer. Probability fibers do not assert process
Markovness, restart, invariance or Chapman-Kolmogorov. -/
set_option maxHeartbeats 1600000 in
'''
replacement='''set_option maxHeartbeats 1600000 in
/-- Actual full-phase law with joint finite-time index, Dirac initialization and
bounded Borel expectation transfer. Probability fibers do not assert process
Markovness, restart, invariance or Chapman-Kolmogorov. -/
'''
old='''      Measurable (Z y xRef z₀ t) := hZM.comp
    ((measurable_const.prodMk measurable_const).prodMk
      (measurable_const.prodMk measurable_id))'''
new='''      Measurable (Z y xRef z₀ t) := hZM.comp
    (show Measurable (fun sample : ℕ → ℝ => (((y, xRef), z₀), t, sample)) from
      measurable_const.prodMk (measurable_const.prodMk measurable_id))'''
assert s.count(doc)==s.count(old)==1
s=s.replace(doc,replacement,1).replace(old,new,1)
prop=lambda x:x.split('private def ',1)[1].split('\n\n/--',1)[0].split('\n\nset_option maxHeartbeats',1)[0].rstrip()
assert prop(s)==prop(raw.decode('utf8'))
diagnosis=dict(classification='PARSER_AND_PRODUCT_ASSOCIATION_ELABORATION',route_fingerprint='actual80-Z/actual-Exp1/id-const-map/Dirac0/bounded-Borel-transfer',same_mathematical_route=True,attempt=1,errors=['Declaration doc comment precedes scoped set_option, an invalid Lean command ordering already diagnosed in84; move scoped option before the doc comment.','Clock-section map omitted the initial-phase factor in Param=((y,xRef),z0); explicitly type the constant Param and (t,sample) product.'],statement_or_source_assumptions_changed=False,private_Prop_unchanged=True,no_tactic_loop=True,prior_module_RAW_sha256=hashlib.sha256(raw).hexdigest(),repaired_module_RAW_sha256=hashlib.sha256(s.encode()).hexdigest(),negative_receipt=(r/'focused85-attempt1/receipt.json').as_posix())
d=r/'compiler-route-diagnosis85.json';assert not d.exists();d.write_text(json.dumps(diagnosis,indent=2)+'\n',encoding='utf8',newline='\n')
p.write_text(s,encoding='utf8',newline='\n')
print('Parser/BODY association repaired; private sealed Prop unchanged; negative retained')
