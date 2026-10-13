from pathlib import Path
r=Path(__file__).parent;o=r.parent/'pbps-actual-conditional-next-wait-density89'
for name in ['refresh_graph89.py','inspect_generated_reader89.py','inspect_generated_bindings89.py','record_integration89.py','commit_integration89.py','normalize_verified_tail89.py']:
 s=(o/name).read_text(encoding='utf8').replace('89','90').replace('ActualConditionalNextWaitDensity','ActualFiniteHistoryExtension').replace('actual-conditional-next-wait-density','actual-finite-history-extension')
 s=s.replace('pbps-conditional-next-wait-density-preread90','pbps-next-history-extension-preread90')
 s=s.replace('source-review90.decision.v2.native.json','source-review90.decision.native.json')
 s=s.replace('36813b659cbdbb4b31c6300abd1300858d42afe683046b8c06ff9c22806e8e37','6cdc14328be5ec3ece3f028e6e1dd0185ee4031a8e651956ee0f55d4beebf029')
 s=s.replace('registry_count=538','registry_count=539').replace("'integration-site-regressions'","'site-regressions'")
 s=s.replace('One actual conditional strict finite next-wait density and genuine subprobability kernel theorem. Exact kernel audit certifies six immediate public ASTIS parents: actual87 history/tail, actual86 deterministic density, actual75 hazard, actual flow/rate and actual77 iid product; actual88 is not a dependency.','One actual complete-history Borel append and pointwise finite-recursion identity, restricted next-history joint/marginal laws and all joint ENNReal tests. Exact kernel audit certifies four immediate public ASTIS parents: density89, history87, actual flow and bounce rate; survival88 is not a dependency.')
 # Blind string replacement of round number must not change the actual89 parent phrase.
 s=s.replace('actual90 is not a dependency','actual88 is not a dependency')
 p=r/name.replace('89','90');assert not p.exists();p.write_text(s,encoding='utf8',newline='\n')
print('Prepared sole-lane90 generator/check/commit helpers; no shared writes.')
