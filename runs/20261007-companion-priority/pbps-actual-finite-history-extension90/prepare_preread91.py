"""Prepare, do not execute, the next fresh capsule/safe-fetch boundary."""
from pathlib import Path
r=Path(__file__).parent
s=(r.parent/'pbps-actual-conditional-next-wait-density89/preread90.py').read_text(encoding='utf8')
s=s.replace('after89','after90').replace('preread90','preread91').replace('fetch90','fetch91').replace('scheduling90','scheduling91').replace('pbps-next-history-extension-preread90','pbps-ordered-history-iteration-preread91')
s=s.replace('Integrate verified actual PBPS conditional finite next-wait density','Integrate verified actual PBPS complete finite-history extension')
s=s.replace("candidate_source_node='Remaining S87-I5/G86-11: actual next-history extension and restricted joint law',source_graph='independent-source-first90/source-proof-graph90.native.json',reason='Fresh capsule/updated handoff plus independently reconstructed source identify the missing actual append/recursion transport consumer of89 conditional density. Derive constructor Borelness and actual H_(n+1) equality internally; old88 survival and a noatom lemma are not AND parents.'","candidate_source_node='Remaining S87-I5/G86-11 ordered absolute-time iteration/final survival/path/count assembly',source_graph_status='Await new independent source-first reconstruction; no next SAU selected yet.',reason='Fresh capsule and latest90 handoff first; actual full-history extension90 is accepted only within its restricted one-step scope. Reconstruct exact remaining source graph before selecting a substantive dependency-ready delta; retain OR alternatives and no provider premises.'")
s=s.replace("next_source_node='Actual next-history extension'","next_source_node='Source-first remaining ordered-history assembly; no claim yet'")
p=r/'preread91.py';assert not p.exists();p.write_text(s,encoding='utf8',newline='\n')
print('Prepared next capsule/fetch preread only; requires90 integration committed and pushed before execution.')
