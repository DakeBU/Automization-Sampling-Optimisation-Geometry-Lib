"""Admit independently verified normalization through the existing sole lane."""
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
out = r / 'integration105'
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
module = 'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualCountableEndpointLaw'
decl = c['target_declarations'][0]
for name in owned[:2]:
    after(name, 'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualNormalizedEndpointSector', 'import ' + module + '\n')
note = f'Independent science {science}. Under the original six assumptions, one global jointly measurable actual clock process Z retains the exact arc/fallback/zero-time contract. For every y,r,T, its Gibbs-initialized endpoint law Q is the countable sum of all actual normalized fixed-count endpoint sectors, is a probability, and is preserved by J(z0,zT)=(RzT,Rz0). Actual93, normalization103, UnitExponentialProduct and sector reversal104 are the four direct producers. Fixed-initial measurable count fibers, jointly measurable sector integrals and nonnegative Tonelli close assembly without a joint-count premise or signed uniform domination. Signed bilinear duality, marginal phase invariance, restart/Markovness, hypocoercivity, implementation errors, expected costs, full composition and all four full papers remain open.'

block = '  {\n' + '\n'.join(['    key := "pbps.actualCountableEndpointLaw"', '    localDecl := ' + json.dumps(decl), '    upstreamDecl := "Actual PBPS countable endpoint probability and reversal"', '    upstreamFile := "arXiv2609.06905v1 Appendix A.1 A7 and nonnegative Gibbs averaging before A8"', '    status := LemmaMemoryStatus.formalizedLocal', '    tags := ["PBPS", "Gibbs", "endpoint", "reversal"]', '    saldUse := "Actual countable endpoint law; no SALD claim"', '    note := ' + json.dumps(note)]) + '\n  },\n'
after(owned[1], 'def analysisMemory : List LemmaMemoryEntry := [', block)
p = Path(owned[2])
b = p.read_bytes()
assert b.count(b'formalizedTechnicalLemmaCount = 556') == 1
p.write_bytes(b.replace(b'formalizedTechnicalLemmaCount = 556', b'formalizedTechnicalLemmaCount = 557'))
prefix = f'''## Actual PBPS countable endpoint law (2026-10-12)

Independent science {science}. Under the original six analytic assumptions,
one global jointly measurable actual process Z retains its arc, fallback and
almost-sure zero-time characterization. For every y,r and finite nonnegative T,
let Q be the endpoint-pair pushforward of actual Gibbs phase law times the
countable unit-exponential input. Then Q is exactly the sum of all actual
fixed-count endpoint sectors, Q has mass one, and J(z0,zT)=(RzT,Rz0) preserves Q.

The proof uses actual93 once for the same global witness, normalization103
for the actual initial probability, UnitExponentialProduct for the clock
probability and its sigma-finiteness, and104 for each normalized sector.
Count fibers are partitioned at fixed initial phase. Jointly measurable
prescribed-sector integrals and nonnegative Tonelli justify the subsequent
averaging and countable exchange, with no joint-count assumption or uniform
signed energy bound.

Eight adjacent formula/Lean regions explain this ASTIS completion of the
Appendix A.1 A7 averaging step. The full sealed statement, fresh blind decoder,
whole mathematical proof and independent source/exposition reviews passed.
Signed bilinear duality, marginal phase invariance, restart/Markovness,
hypocoercivity, implementation error, actual expected costs and full
composition remain red. Full paper completion remains0/4.

The sole SAU94 lane serializes integration. Actual browser acceptance, main
merge of this PBPS contribution and postmerge purification remain distinct.

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
anchor = b'#actual-normalized-pbps-endpoint-pair-sector-reversal-2026-10-12'
assert b.count(anchor) == 1
p.write_bytes(b.replace(anchor, b'#actual-pbps-countable-endpoint-law-2026-10-12', 1))
prepend(owned[5], f'## Actual countable endpoint law105 (2026-10-12)\n\n{note}\n\nEight source-reviewed formula/Lean regions. Aggregate/visual acceptance, main merge and purification retain separate evidence.\n\n')
entry = dict(key='pbps.actualCountableEndpointLaw', local_decl=decl, local_file=c['proposed_files'][0], status='formalized-local', verified_commit=science, evidence=state['latest_evidence'], next_action=note)
with Path(owned[6]).open('ab') as f:
    f.write((json.dumps(entry, ensure_ascii=False) + '\n').encode())
(out / 'integration-scope.json').write_text(json.dumps(dict(owned=owned, science_commit=science, single_stabilization_lane=lanes[0]['advance_id'], child_status='VERIFIED', aggregate='pending', visual='pending', Goal_complete=False), indent=2) + '\n', encoding='utf8', newline='\n')
print('Verified countable endpoint child admitted through existing sole lane; Registry557; aggregate gates pending.')
