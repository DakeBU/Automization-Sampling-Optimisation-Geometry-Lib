from run import ROOT
import json
s=(ROOT/'scratch/IndependentLiteralCheck.lean').read_text()
(ROOT/'scratch/IndependentLiteralCheck.v1.original.lean').write_text(s)
# Seal strings are theorem signatures. A standalone forall uses a comma after
# its final binder, unlike the colon separating theorem binders and conclusion.
s=s.replace('(hq : 2 * q + 1 < d) :\n','(hq : 2 * q + 1 < d),\n')
(ROOT/'scratch/IndependentLiteralCheckV3.lean').write_text(s)
t=(ROOT/'check_native_v2.py').read_text().replace("[('inspect-all-v2','InspectAllV2.lean'),('independent-literal-kernel-v2','IndependentLiteralCheck.lean')]", "[('independent-literal-kernel-v3','IndependentLiteralCheckV3.lean')]")
(ROOT/'check_native_v3.py').write_text(t)
p=ROOT/'verifier-failures.json';data=json.loads(p.read_text());data.append({'original':'receipts/independent-literal-kernel-v2.json','class':'IMPLEMENTATION_FAILED','scope':'Independent literal verifier generator, no candidate theorem failure','diagnosis':'Generated standalone forall retained the theorem-signature colon after hq instead of a comma. Lean parser recovery introduced sorry and kernel mismatch; exit1 is rejected in full despite intermediate logInfo text. V3 changes only the separator in the independently generated literal. Prior exact author probe already passed. Successful inspect-all-v2 is retained without rerunning unchanged.'});p.write_text(json.dumps(data,indent=2)+'\n')
print('Preserved malformed literal original and rejected exit1 in full. V3 uses valid forall separator; reuses exact successful native inspect-all-v2 run.')
