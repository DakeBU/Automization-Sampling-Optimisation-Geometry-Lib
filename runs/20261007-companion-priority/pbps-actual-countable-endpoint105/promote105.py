from pathlib import Path
import json,hashlib
r=Path('runs/20261007-companion-priority/pbps-actual-countable-endpoint105')
pre=r.parent/'pbps-countable-endpoint-preread105'
receipt=r/'focused105/assembly3-function-multiplication/receipt.json'
if not receipt.exists(): raise SystemExit('Compile still pending; no production write.')
q=json.loads(receipt.read_bytes());assert q['exit_code']==0,q
raw=(r/'Assembly105.lean').read_bytes();assert hashlib.sha256(raw).hexdigest()==q['input_raw_sha256']
s=raw.decode()
ns='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualCountableEndpointLaw'
s=s.replace('/- Prospective type-only statement. No proof, seal or claim yet. -/', '/-!\n# Actual PBPS countable endpoint-pair law\n\nThe nonnegative count expansion and Gibbs averaging of arXiv:2609.06905v1,\nAppendix A.1, are identified with the endpoint law of the actual clock process.\nThe same law is a probability, is the sum of all fixed-count endpoint sectors,\nand is preserved by the momentum-flipped endpoint swap. This is the measure\nassembly needed before signed duality and marginal invariance.\n-/').replace('PBPSCountableEndpointCandidate105',ns)
s=s.replace('def candidate','set_option linter.unusedVariables false in\nprivate def actual_countable_endpoint_statement')
s=s.replace('theorem assembly','/-- The actual Gibbs-initialized endpoint law is the countable sector sum, a probability, and preserved by the flipped swap. -/\ntheorem actual_countable_endpoint_law')
s=s.replace(': candidate hα hαβ hV hH hη hβη',': actual_countable_endpoint_statement hα hαβ hV hH hη hβη')
s=s.replace('unfold candidate','unfold actual_countable_endpoint_statement').replace('#print axioms assembly','#print axioms actual_countable_endpoint_law')
literal=s.split('private def actual_countable_endpoint_statement',1)[1].split('set_option maxHeartbeats',1)[0].strip()
seal=json.loads((pre/'root.statement-seal105.json').read_bytes())
assert literal==seal['expanded_literal_Prop'].strip()
p=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCountableEndpointLaw.lean');assert not p.exists()
p.write_text(s,encoding='utf8',newline='\n');(r/'Production105.lean').write_bytes(p.read_bytes())
(r/'production-promotion105.json').write_text(json.dumps(dict(production_path=p.as_posix(),raw_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),assembly_receipt=receipt.as_posix(),statement_seal_unchanged=True,explicit_internal_source_graph_node='ASSEMBLY105: Q = Measure.sum L; ENDPOINT-LAW105: probability and J preservation',independently_verified=False),indent=2)+'\n',encoding='utf8')
print(p)
