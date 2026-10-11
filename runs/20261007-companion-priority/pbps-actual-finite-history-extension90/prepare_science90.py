from pathlib import Path
r=Path(__file__).parent;o=r.parent/'pbps-actual-conditional-next-wait-density89'
s=(o/'commit_science89.py').read_text(encoding='utf8').replace('89','90').replace('pbps-conditional-next-wait-density-preread90','pbps-next-history-extension-preread90').replace('ActualConditionalNextWaitDensity','ActualFiniteHistoryExtension').replace('actual-conditional-next-wait-density','actual-finite-history-extension')
s=s.replace("'semantic','frontier','contributor'","'accepted-semantic','frontier','accepted-contributor'").replace('36813b659cbdbb4b31c6300abd1300858d42afe683046b8c06ff9c22806e8e37','6cdc14328be5ec3ece3f028e6e1dd0185ee4031a8e651956ee0f55d4beebf029')
s=s.replace("ledger.write_bytes(prefix+tail.replace", "(r/'science-ledger-tail90.exactraw.snapshot').write_bytes(tail)\nledger.write_bytes(prefix+tail.replace")
s=s.replace("p.suffix not in {'.log','.diff','.html','.lean','.snapshot'}:continue","not (p.suffix in {'.log','.diff','.html','.lean','.snapshot'} or '.snapshot.' in p.name):continue")
s=s.replace("and p.suffix not in {'.log','.diff','.html','.lean','.snapshot'}]","and p.suffix not in {'.log','.diff','.html','.lean','.snapshot'} and '.snapshot.' not in p.name]")
s=s.replace('Prove actual PBPS conditional finite next-wait density','Prove actual PBPS complete finite-history extension')
p=r/'commit_science90.py';assert not p.exists();p.write_text(s,encoding='utf8',newline='\n')
s=(o/'push_science89.py').read_text(encoding='utf8').replace('89','90').replace('Prove actual PBPS conditional finite next-wait density','Prove actual PBPS complete finite-history extension')
p=r/'push_science90.py';assert not p.exists();p.write_text(s,encoding='utf8',newline='\n')
print('Prepared scoped90 science commit/push; snapshots losslessly archived.')
