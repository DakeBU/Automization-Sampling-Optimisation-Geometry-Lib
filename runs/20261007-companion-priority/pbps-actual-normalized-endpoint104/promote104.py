from pathlib import Path
import json,hashlib
r=Path('runs/20261007-companion-priority/pbps-actual-normalized-endpoint104')
pre=r.parent/'pbps-normalized-endpoint-preread104'
receipt=r/'focused104/assembly8-explicit-set-conjunction/receipt.json'
if not receipt.exists(): raise SystemExit('Compile still pending; no production write.')
q=json.loads(receipt.read_bytes());assert q['exit_code']==0,q
raw=(r/'Assembly104.lean').read_bytes();assert hashlib.sha256(raw).hexdigest()==q['input_raw_sha256']
s=raw.decode()
ns='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualNormalizedEndpointSector'
s=s.replace('/- Prospective type-only header. No proof, Statement Seal or SAU claim. -/', '''/-!
# Actual normalized endpoint-pair sector reversal

The fixed-count reversal and Gibbs averaging in arXiv:2609.06905v1,
Appendix A.1, with phase normalization from Eq. (3.1) made explicit.
The actual event density and deterministic endpoint map define a sector measure;
the flipped endpoint swap preserves its pushforward. This proves one fixed-count
measure identity, not countable assembly or process invariance.
-/''').replace('PBPSNormalizedEndpointCandidate104',ns)
s=s.replace('def candidate','set_option linter.unusedVariables false in\nprivate def actual_normalized_endpoint_sector_statement')
s=s.replace('theorem assembly','/-- Momentum-flipped reversal preserves every actual normalized fixed-count endpoint-pair measure. -/\ntheorem actual_normalized_endpoint_sector_reversal')
s=s.replace(': candidate hα hαβ hV hH hη hβη',': actual_normalized_endpoint_sector_statement hα hαβ hV hH hη hβη')
s=s.replace('unfold candidate','unfold actual_normalized_endpoint_sector_statement').replace('#print axioms assembly','#print axioms actual_normalized_endpoint_sector_reversal')
literal=s.split('private def actual_normalized_endpoint_sector_statement',1)[1].split('set_option maxHeartbeats',1)[0].strip()
seal=json.loads((pre/'root.statement-seal104.json').read_bytes())
assert literal==seal['expanded_literal_Prop'].strip()
p=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualNormalizedEndpointSector.lean');assert not p.exists()
p.write_text(s,encoding='utf8',newline='\n');(r/'Production104.lean').write_bytes(p.read_bytes())
(r/'production-promotion104.json').write_text(json.dumps(dict(production_path=p.as_posix(),raw_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),assembly_receipt=receipt.as_posix(),statement_seal_unchanged=True,explicit_internal_source_graph_node='SECTOR100: MeasurePreserving Theta sigma sigma',independently_verified=False),indent=2)+'\n',encoding='utf8')
print(p)
