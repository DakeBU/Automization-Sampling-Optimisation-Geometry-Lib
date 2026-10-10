from pathlib import Path
import hashlib,json,os
OUT=Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-recursive-path-preread76')
for name in ['build.receipt.json','selected.contract.json']:
 old=OUT/name;dest=OUT/('historical-v1.'+name);assert not dest.exists();dest.write_bytes(old.read_bytes())
p=OUT/'build76.py';b=p.read_bytes()
old=b"Finite-arc interface is exactly zeta_(T_n+t)=Phi_t(z_n) for 0<=t<tau, without claiming a globally stitched all-time path."
new=b"Record-indexed outgoing arc_n(t)=Phi_t(z_n) for 0<=t<tau. Source zeta_(T_n+t) interpretation is deferred to a stitched source-law path; arbitrary zero thresholds may share event times, so this edge asserts no global phase function."
assert b.count(old)==1;b=b.replace(old,new)
old=b"No strict event-time growth is asserted for arbitrary threshold sequences."
new=b"No strict event-time growth or single physical-time phase function is asserted for arbitrary threshold sequences with zero waits."
assert b.count(old)==1;b=b.replace(old,new)
p.write_bytes(b)
r={'schema':'owned-open-planning-clarification-v1','actual_PID':os.getpid(),'actual_EXIT':0,'reason':'Clarify record-indexed arcs versus global physical-time phase when deterministic thresholds may be zero; no candidate/header/source changes. Correct two optional prior source-context locators after filename-only lookup.','historical_receipt':'historical-v1.build.receipt.json','historical_contract':'historical-v1.selected.contract.json','not_a_source_candidate_repair':True,'source_statement_seal':False,'write_scope':'new preread76 only'}
(OUT/'refine.receipt.json').write_bytes((json.dumps(r,indent=2,sort_keys=True)+'\n').encode())
print(json.dumps(r))
