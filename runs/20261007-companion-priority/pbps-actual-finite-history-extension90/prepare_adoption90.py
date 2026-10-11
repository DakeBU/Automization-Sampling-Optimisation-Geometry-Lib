from pathlib import Path
r=Path(__file__).parent
s=(r.parent/'pbps-actual-conditional-next-wait-density89/adopt_source_and_prove89.py').read_text(encoding='utf8')
s=s.replace('89','90').replace('ActualConditionalNextWaitDensity','ActualFiniteHistoryExtension').replace('actual-conditional-next-wait-density','actual-finite-history-extension')
s=s.replace('source-review90.decision.v2.native.json','source-review90.decision.native.json').replace('closed-raw-manifest.source-review90.v2.native.json','closed-raw-manifest.source-review90.native.json').replace('source-review90.run.v2.native.json','source-review90.run.native.json')
start=s.index("original_manifest=load(");end=s.index("runhash=",start)
s=s[:start]+s[end:]
s=s.replace("==23 and","==28 and").replace("assert 'density' in str(n['accepted_truth_boundary']).lower()","assert 'history' in str(n['accepted_truth_boundary']).lower()").replace("assert 'full A.7' in str(n['accepted_truth_boundary']['open'])","assert any('A7' in str(v) or 'A.7' in str(v) for v in n['accepted_truth_boundary']['open'])")
s=s.replace('twenty-three definitions','twenty-eight definitions').replace('7slots/23defs','7slots/28defs')
s=s.replace("c['evidence'].update", "c['conceptual_mirror_audit']=load(r/'conceptual-mirror-audit90.json')\nc['evidence'].update")
s=s.replace("Only density component of S87-I5/G86-11 closed; ordered-time iteration/final factor/fullA7", "Only one actual full-history extension edge of S87-I5/G86-11 closed; ordered-time iteration/final factor/fullA7")
s=s.replace('focused/production6-explicit-order-comparisons/receipt.json','focused/production2-explicit-tuple-API/receipt.json')
s=s.replace('Actual jointly Borel strict finite next-wait density, genuine all-history subprobability kernel, joint measure identity and all nonnegative extended joint tests on all history events. Only density component', 'Actual jointly Borel full-history append/lift, pointwise guarded actual recursion identity, restricted actual next-history joint/marginal measure identities and all nonnegative extended joint tests on all old-history events. Only one actual next-history extension edge')
p=r/'adopt_source_and_prove90.py';assert not p.exists();p.write_text(s,encoding='utf8',newline='\n')
print('Prepared exact inspected native-schema90 adoption.')
