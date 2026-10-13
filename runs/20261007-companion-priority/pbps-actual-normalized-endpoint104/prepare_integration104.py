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
assert subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip() == science
assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only']).strip()
lanes = [s for s in adv.current_advances().values() if s['state'] == 'STABILIZING']
assert len(lanes) == 1 and lanes[0]['advance_id'] == 'ASTIS-SA-20261011-PBPSActualPrescribedPathDensity'
assert lanes[0]['latest_evidence']['integration_owner'] == 'companion_root_20261005'
out = r / 'integration104'
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
module = 'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualNormalizedEndpointSector'
decl = c['target_declarations'][0]
for name in owned[:2]:
    after(name, 'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseNormalization', 'import ' + module + '\n')
note = f'Independent science {science}. Under the original six assumptions and every y,r,n,T, the actual density q_n times terminal survival weights the product of the normalized phase law and strict-simplex measure. Its pushforward through B(z,t)=(z,Gamma(z,t)(T)) is preserved by J(z0,zT)=(RzT,Rz0). Four actual public parents supply finite-count density measurability, endpoint reversal, unnormalized weighted substitution and phase normalization. Same reversal witness, simplex sigma-finiteness and normalized-sector preservation are derived internally. No additional premise or claim that a fixed-count sector is a probability measure. Countable assembly, signed bilinear identity, process invariance, Markovness, hypocoercivity, errors, expected costs and whole-paper/composition remain open.'

block = '  {\n' + '\n'.join(['    key := "pbps.actualNormalizedEndpointSector"', '    localDecl := ' + json.dumps(decl), '    upstreamDecl := "Actual normalized PBPS endpoint-pair sector reversal"', '    upstreamFile := "arXiv2609.06905v1 Appendix A.1 fixed-count reversal and Eq3.1 averaging"', '    status := LemmaMemoryStatus.formalizedLocal', '    tags := ["PBPS", "Gibbs", "endpoint", "reversal"]', '    saldUse := "Actual normalized endpoint-pair sector; no SALD claim"', '    note := ' + json.dumps(note)]) + '\n  },\n'
after(owned[1], 'def analysisMemory : List LemmaMemoryEntry := [', block)
p = Path(owned[2])
b = p.read_bytes()
assert b.count(b'formalizedTechnicalLemmaCount = 554') == 1
p.write_bytes(b.replace(b'formalizedTechnicalLemmaCount = 554', b'formalizedTechnicalLemmaCount = 555'))
prefix = f'''## Actual normalized PBPS endpoint-pair sector reversal (2026-10-12)

Independent science {science}. For every y,r,n and finite nonnegative T,
let sigma be the product of the actual conditional Gibbs phase probability
and strict-simplex measure, weighted by the actual event-density times terminal
survival. Let B(z,t)=(z,Gamma(z,t)(T)) and L=B_*sigma. The original six analytic
assumptions imply that J(z0,zT)=(RzT,Rz0) is measurable and J_*L=L.

The proof identifies the same reversal witness in the endpoint and weighted
substitution parents, proves simplex sigma-finiteness, normalizes the full
sector measure using phase normalization103, then pushes the identity through B.
All four dependencies are actual public producers93/97/102/103. No proof
ingredient becomes a public assumption. Initial phase is normalized; no
fixed-count sector mass-one or finite-mass conclusion is asserted.

This is ASTIS completion of the Appendix A.1 fixed-count calculation and Eq3.1
Gibbs averaging, with eight adjacent formula/Lean steps. Whole mathematics,
exact sealed kernel, fresh blind reconstruction and independent primary-first
source/exposition review passed. Countable sector assembly and signed bilinear
averaging toward the actual process law remain red, as do restart/Markovness,
hypocoercivity, implementation error, actual costs and full composition.
Full papers completed remains 0/4. Existing four-paper priorities persist.

The sole SAU94 stabilization lane serializes aggregate publication. Browser
acceptance, main merge and postmerge purification retain separate evidence.

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
anchor = b'#actual-pbps-phase-gibbs-normalization-2026-10-12'
assert b.count(anchor) == 1
p.write_bytes(b.replace(anchor, b'#actual-normalized-pbps-endpoint-pair-sector-reversal-2026-10-12', 1))
prepend(owned[5], f'## Actual normalized endpoint-pair sector104 (2026-10-12)\n\n{note}\n\nEight source-reviewed formula/Lean regions. Aggregate/visual acceptance, main merge and purification retain separate evidence.\n\n')
entry = dict(key='pbps.actualNormalizedEndpointSector', local_decl=decl, local_file=c['proposed_files'][0], status='formalized-local', verified_commit=science, evidence=state['latest_evidence'], next_action=note)
with Path(owned[6]).open('ab') as f:
    f.write((json.dumps(entry, ensure_ascii=False) + '\n').encode())
(out / 'integration-scope.json').write_text(json.dumps(dict(owned=owned, science_commit=science, single_stabilization_lane=lanes[0]['advance_id'], child_status='VERIFIED', aggregate='pending', visual='pending', Goal_complete=False), indent=2) + '\n', encoding='utf8', newline='\n')
print('Verified endpoint-pair child admitted through existing sole lane; Registry555; aggregate gates pending.')
