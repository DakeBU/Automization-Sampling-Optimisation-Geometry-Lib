from pathlib import Path
old=Path('runs/20261007-companion-priority/pbps-actual-physical-time-measurability80')
new=Path('runs/20261007-companion-priority/pbps-actual-physical-time-law81')
for name in ['final_admin80.py','record_final80.py','inspect_reader_html80.py','commit_integration80.py']:
 s=(old/name).read_text(encoding='utf8')
 s=s.replace('pbps-actual-physical-time-measurability80','pbps-actual-physical-time-law81').replace('integration80','integration81').replace('final-admin80','final-admin81').replace('verification80','verification81')
 s=s.replace('ASTIS-SW-PBPS-actual-physical-time-measurability','ASTIS-SW-PBPS-ideal-half-turn-kernel').replace('pbps-actual-physical-time-measurability.json','pbps-ideal-half-turn-kernel.json').replace("'pbps-actual-physical-time-measurability'","'pbps-ideal-half-turn-kernel'")
 s=s.replace('Registry529','Registry530').replace('registry_count=529','registry_count=530')
 s=s.replace('actual jointly measurable physical-time phase declaration with AE interpolation and initialization, consuming actual harmonic flow, finite recursion, positive input support and interval coverage','ideal exact-reference half-turn returned-position probability kernel and product initialization consumer, joining actual joint phase, normalized Gibbs and canonical Gaussian conditional-reference kernel')
 s=s.replace('Actual total joint phase measurability and fixed-parameter common-AE interpolation/initialization independently verified','Ideal exact-reference returned-position probability kernel, actual independent product initialization and terminal live-arc agreement independently verified')
 s=s.replace('Path regularity/adaptedness/Markov/kernel/invariance/main/error/cost/composition','Random-input all-time/version uniqueness, process Markov/semigroup/invariance/mixing/implementation/main/error/cost/composition')
 s=s.replace('Path regularity/adaptedness/Markov/transition kernel/invariance/hypocoercivity/main/errors/query costs and PBPS-SPHMC actual-input composition','Random-input all-time/version uniqueness, phase Markov/semigroup/invariance/hypocoercivity/main/implemented-reference errors/query costs and PBPS-SPHMC actual-input composition')
 s=s.replace('precise actual phase dependency graph','precise ideal initialized-kernel dependency graph')
 if name=='final_admin80.py':
  begin=s.index("old='carries this VERIFIED child.")
  end=s.index("p.write_bytes(raw.replace(old,new,1))",begin)
  s=s[:begin]+'''old='child; serialized aggregate/site/graph and reader visual acceptance are pending\\nfor this snapshot.'.encode().replace(b'\\n',nl);assert raw.count(old)==1
new=(f'child. Local aggregate81 passed (root{jobs[0]}, Tests{jobs[1]}, Registry530),\\nincluding canonical tools/astis.py check, ATLAS and fake-closure scans; py_compile\\npassed. Publication/site/graph checks are bound in81 integration.notes.json.\\nStatic SVG was actually viewed and generated HTML content/folding checked. Actual\\npage/interactive branch visual acceptance remains pending because the bound\\nbrowser surface has no inspectable tab.').encode().replace(b'\\n',nl)
'''+s[end:]
 if name=='inspect_reader_html80.py':
  s=s.replace('== 9','== 10').replace("regions': 9","regions': 10").replace('nine exact adjacent','ten exact adjacent')
 if name=='commit_integration80.py':
  s=s.replace('actual jointly measurable PBPS physical-time phase','ideal PBPS initialized half-turn probability kernel').replace('actual PBPS physical-time phase','ideal PBPS half-turn kernel')
 target=new/name.replace('80','81');assert not target.exists();target.write_text(s,encoding='utf8',newline='\n')
 print(target)
