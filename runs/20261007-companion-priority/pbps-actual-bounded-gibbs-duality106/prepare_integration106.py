"""Admit independently verified bounded Gibbs duality through the existing sole lane."""
from pathlib import Path
import hashlib, json, re, subprocess, sys
root = Path.cwd()
r = Path(__file__).parent
sys.path.insert(0, str(root / 'tools'))
import astis_advance as adv
load = lambda p: json.loads(Path(p).read_bytes())
c = load(r / 'claim.json')
state = adv.current_advances()[c['advance_id']]
assert state['state'] == 'VERIFIED'
science = state['latest_evidence']['verified_commit']
assert subprocess.run(['git','merge-base','--is-ancestor',science,'HEAD']).returncode==0
assert subprocess.run(['git','merge-base','--is-ancestor','origin/main','HEAD']).returncode==0
assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only']).strip()
lanes = [s for s in adv.current_advances().values() if s['state'] == 'STABILIZING']
assert len(lanes) == 1 and lanes[0]['advance_id'] == 'ASTIS-SA-20261011-PBPSActualPrescribedPathDensity'
assert lanes[0]['latest_evidence']['integration_owner'] == 'companion_root_20261005'
out = r / 'integration106'
out.mkdir(exist_ok=False)
owned = ['AutoSamplingTheory/ExampleCases.lean', 'AutoSamplingTheory/TechnicalLemmas/Registry.lean', 'Tests/Basic.lean', 'docs/companion-papers-handoff.md', 'website/content/samplewiki_companion_frontiers.json', 'conversion-windows/ASTIS-SW-PBPS-2026.md', 'research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl']
rows = []
for i, name in enumerate(owned):
    raw = Path(name).read_bytes()
    p = out / f'{i}.before.exactraw.snapshot'
    p.write_bytes(raw)
    rows.append(dict(path=name, raw_sha256=hashlib.sha256(raw).hexdigest(), snapshot=p.as_posix()))
(out / 'owned-before.json').write_text(json.dumps(rows, indent=2) + '\n', encoding='utf8', newline='\n')
def after(name, anchor, text):
    p = Path(name)
    b = p.read_bytes()
    hits = list(re.finditer(rb'(?m)^' + re.escape(anchor.encode()) + rb'(\r?\n|$)', b))
    assert len(hits) == 1 and text.encode() not in b
    h = hits[0]
    p.write_bytes(b[:h.end()] + text.encode().replace(b'\n', h.group(1) or b'\n') + b[h.end():])
module = 'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBoundedGibbsDuality'
decl = c['target_declarations'][0]
for name in owned[:2]:
    after(name, 'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualCountableEndpointLaw', 'import ' + module + '\n')
note = f'Independent science {science}. Under the original six assumptions, one global jointly measurable actual PBPS process retains its exact arc/fallback/zero-time contract. For every y,r,T its endpoint pushes the actual Gibbs phase law times countable exponential clocks to the same Gibbs phase law. For every pair of bounded Borel real F,G, both outer tests are integrable and integral F op(G) equals integral (G composed R) op(F composed R). Actual105, actual normalization103 and UnitExponentialProduct are the three direct producers. Momentum symmetry and signed Fubini are internally discharged. The selected direct-marginal proof and printed F=1 route have separate independently admitted source graph alternatives. L2 operators/domains, restart/Markovness, separate kernel witness identification, hypocoercivity, errors, actual expected costs, full composition and all four full papers remain open.'


block = '  {\n' + '\n'.join(['    key := "pbps.actualBoundedGibbsDuality"', '    localDecl := ' + json.dumps(decl), '    upstreamDecl := "Actual PBPS bounded signed Gibbs duality and fixed-time invariance"', '    upstreamFile := "arXiv2609.06905v1 Appendix A.1 final bounded signed bilinear identity and Gibbs stationarity"', '    status := LemmaMemoryStatus.formalizedLocal', '    tags := ["PBPS", "Gibbs", "endpoint", "reversal"]', '    saldUse := "Actual bounded duality and fixed-time invariance; no SALD claim"', '    note := ' + json.dumps(note)]) + '\n  },\n'
after(owned[1], 'def analysisMemory : List LemmaMemoryEntry := [', block)
p = Path(owned[2])
b = p.read_bytes()
matches = re.findall(rb'formalizedTechnicalLemmaCount = (\d+)', b)
assert len(matches) == 1
before_count = int(matches[0]); after_count = before_count + 1
p.write_bytes(b.replace(b'formalizedTechnicalLemmaCount = ' + matches[0], b'formalizedTechnicalLemmaCount = ' + str(after_count).encode(), 1))
prefix = f'''## Actual PBPS bounded Gibbs duality and fixed-time invariance (2026-10-12)

Independent science {science}. Under the original six analytic assumptions,
one global jointly measurable actual process Z retains its exact live-arc,
raw fallback and parameterwise almost-sure zero-time contract. For every y,r
and finite nonnegative T, endpoint(z,w)=Z(y,r,z,T,w) is measurable and sends
the actual Gibbs phase law nu_y times the countable exponential law P to nu_y.
For all bounded Borel real F,G with finite nonnegative bounds, both outer tests
are integrable and integral F op_T(G) dnu_y equals
integral (G composed R) op_T(F composed R) dnu_y, with R(x,p)=(x,-p).

Actual105 supplies the same global process and endpoint-pair reversal.
Actual normalization103 and UnitExponentialProduct provide the exact input
probabilities. Gaussian negation gives R_*nu_y=nu_y. The direct-marginal route
identifies the endpoint law; finite test bounds justify signed Fubini and
both outer L1 conclusions. The original printed F=1 source route is retained
as an alternative, with the selected extra source edge independently reviewed.
The effective source graph has 62 nodes and 123 edges, without a new source premise.

Eight adjacent formula/Lean regions explain the ASTIS completion. Header,
whole mathematics, fresh blind decoding and primary-first source/exposition
reviews have passed. L2 operator/domain identity, restart/Markovness,
identification with a separate existential kernel witness, hypocoercivity,
implementation errors, actual expected costs and full composition remain red.
Full paper completion remains 0/4. The original sole SAU94 lane handles public
integration; actual browser acceptance, main merge and purification retain
separate evidence.

'''


def prepend(name, text):
    p = Path(name)
    b = p.read_bytes()
    nl = b'\r\n' if b'\r\n' in b else b'\n'
    first, rest = b.split(nl, 1)
    assert text.splitlines()[0].encode() not in b
    p.write_bytes(first + nl + nl + text.encode().replace(b'\n', nl) + rest)
prepend(owned[3], prefix)
p = Path(owned[4])
b = p.read_bytes()
anchor = b'#actual-pbps-countable-endpoint-law-2026-10-12'
assert b.count(anchor) == 1
p.write_bytes(b.replace(anchor, b'#actual-pbps-bounded-gibbs-duality-and-fixed-time-invariance-2026-10-12', 1))
prepend(owned[5], f'## Actual bounded Gibbs duality106 (2026-10-12)\n\n{note}\n\nEight source-reviewed formula/Lean regions. Aggregate/visual acceptance, main merge and purification retain separate evidence.\n\n')
entry = dict(key='pbps.actualBoundedGibbsDuality', local_decl=decl, local_file=c['proposed_files'][0], status='formalized-local', verified_commit=science, evidence=state['latest_evidence'], next_action=note)
with Path(owned[6]).open('ab') as f:
    f.write((json.dumps(entry, ensure_ascii=False) + '\n').encode())
(out / 'integration-scope.json').write_text(json.dumps(dict(owned=owned, science_commit=science, single_stabilization_lane=lanes[0]['advance_id'], child_status='VERIFIED', aggregate='pending', visual='pending', Goal_complete=False), indent=2) + '\n', encoding='utf8', newline='\n')
print(f'Verified bounded duality child admitted through existing sole lane; Registry{after_count}; aggregate gates pending.')
