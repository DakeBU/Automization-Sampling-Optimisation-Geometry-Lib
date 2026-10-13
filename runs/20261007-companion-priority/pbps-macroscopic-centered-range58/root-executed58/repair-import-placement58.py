from pathlib import Path
import json,subprocess
r=Path('runs/20261007-companion-priority/pbps-macroscopic-centered-range58')
assert json.loads((r/'root.integration.0.lease.json').read_text(encoding='utf-8'))['exit_code']==1
p=Path('AutoSamplingTheory/TechnicalLemmas/Measure.lean');s=p.read_text(encoding='utf-8');addition='import AutoSamplingTheory.TechnicalLemmas.Measure.L2PullbackRange\n';assert s.count(addition)==1
(r/'integration.0.measure-aggregate.raw.snapshot.lean').write_bytes(p.read_bytes());before=subprocess.check_output(['git','show','HEAD:AutoSamplingTheory/TechnicalLemmas/Measure.lean']);assert s.replace(addition,'').encode()==before.replace(b'\r\n',b'\n')
p.write_text(s.replace(addition,''),encoding='utf-8')
p=Path('AutoSamplingTheory/TechnicalLemmas.lean');s=p.read_text(encoding='utf-8');anchor='import AutoSamplingTheory.TechnicalLemmas.Measure\n';assert s.count(anchor)==1 and addition not in s;p.write_text(s.replace(anchor,anchor+addition),encoding='utf-8')
d=dict(blocker_class='conservative-changed-module-publication',actual_exit_code=1,actual_tool_chunk='cee010',residual='Old integrable_of_measure_eq has no publication packet; whole-module gate intentionally includes every declaration in touched Measure.lean even if import-only diff.',strict_reduction='Exact old helper statement/proof/module after removing only added import equals HEAD bytes modulo CRLF. New leaf imported from pure imports TechnicalLemmas.lean root and actual paper module; no gate exemption/new helper wrapper/publication.',next_delta='Rerun complete required aggregate/publication/site graph on actual import placement. Prior Tests9452 and mandatory0 PASS retained without current-layout equivalence claim.')
(r/'integration.0.route-diagnosis.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
p=Path('.astis/pbps-marginal-gradient51/check-integration58.py');s=p.read_text(encoding='utf-8');(r/'integration.0.runner.raw.snapshot.py').write_bytes(p.read_bytes());p=Path('.astis/pbps-marginal-gradient51/check-integration58-stage1.py');p.write_text(s.replace('integration.0','integration.1'),encoding='utf-8')
print('Exact unchanged Measure restored; new import placed in pure root aggregator; no old theorem/gate edits.')
