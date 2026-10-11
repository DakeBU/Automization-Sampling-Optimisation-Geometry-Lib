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
out = r / 'integration103'
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
module = 'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseNormalization'
decl = c['target_declarations'][0]
for name in owned[:2]:
    after(name, 'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualWeightedSector', 'import ' + module + '\n')
note = f'Independent science {science}. Under the original six analytic assumptions, for every y the actual position Gibbs factor is integrable with positive Zx, and the phase partition is Zphase=ofReal(Zx*(sqrt(2*pi))^dim), positive and finite. The normalized phase withDensity is a probability measure exactly equal to the canonical tilted position law times stdGaussian momentum. Includes rank zero; no minimizer, critical point, normalizer or integrability premise. Existing shared Hessian, Gibbs tail, Gaussian integral/density and Gibbs normalization producers are consumed. Analytically independent of weighted sector102; both are parents only of later normalized averaging. No process invariance, countable assembly, Markovness, hypocoercivity, error, expected cost, main result or composition.'
block = '  {\n' + '\n'.join(['    key := "pbps.actualPhaseNormalization"', '    localDecl := ' + json.dumps(decl), '    upstreamDecl := "Actual PBPS phase Gibbs normalization"', '    upstreamFile := "arXiv2609.06905v1 conditional energy and Eq3.1"', '    status := LemmaMemoryStatus.formalizedLocal', '    tags := ["PBPS", "Gibbs", "normalization", "Gaussian"]', '    saldUse := "Actual conditional position-momentum phase law; no SALD claim"', '    note := ' + json.dumps(note)]) + '\n  },\n'
after(owned[1], 'def analysisMemory : List LemmaMemoryEntry := [', block)
p = Path(owned[2])
b = p.read_bytes()
assert b.count(b'formalizedTechnicalLemmaCount = 552') == 1
p.write_bytes(b.replace(b'formalizedTechnicalLemmaCount = 552', b'formalizedTechnicalLemmaCount = 553'))
prefix = f'''## Actual PBPS phase Gibbs normalization (2026-10-12)

Independent science {science}. For every y, define
Vy(x)=V(x)+||x-y||^2/(2 eta), U_y(x,p)=Vy(x)+||p||^2/2,
Zx(y)=integral exp(-Vy(x)) dx and C_E=(sqrt(2*pi))^dim(E).
Under the original six analytic assumptions, exp(-Vy) is integrable,
Zx(y)>0 and the actual phase partition satisfies

Zphase(y)=ofReal(Zx(y)*C_E), with 0<Zphase(y)<infinity.

Consequently the phase measure with density Zphase(y)^(-1)*exp(-U_y)
is a probability measure, exactly the canonical tilted position law times
standard Gaussian momentum, in position-first order. Rank zero is included.
No normalizer, minimizer, critical point or regularity ingredient is a new
public assumption. Five shared public producers and fixed Mathlib supply
the analytic tail, Gaussian factor, product integral and density identification.

This is ASTIS completion of the proportionality in PBPS Eq3.1, with seven
adjacent formula/Lean steps. Whole mathematics, exact sealed kernel witness,
blind reconstruction and primary-first source/exposition review passed.
NORM is analytically independent of sector102; their next joint consumer
is normalized finite-sector averaging and later countable assembly.
Process invariance, restart/Markovness, hypocoercivity, implementation errors,
actual expected costs, main results and actual-input composition remain open.
Full papers completed remains 0/4. Existing four-paper priorities persist.

The same sole SAU94 lane owns aggregate publication, graph and site integration.
Actual browser acceptance, main merge and postmerge purification retain
separate evidence and are not inferred from compilation or source review.

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
anchor = b'#actual-pbps-weighted-finite-sector-substitution-2026-10-12'
assert b.count(anchor) == 1
p.write_bytes(b.replace(anchor, b'#actual-pbps-phase-gibbs-normalization-2026-10-12', 1))
prepend(owned[5], f'## Actual phase normalization103 (2026-10-12)\n\n{note}\n\nSeven source-reviewed formula/Lean regions. Aggregate/visual acceptance, main merge and purification retain separate evidence.\n\n')
entry = dict(key='pbps.actualPhaseNormalization', local_decl=decl, local_file=c['proposed_files'][0], status='formalized-local', verified_commit=science, evidence=state['latest_evidence'], next_action=note)
with Path(owned[6]).open('ab') as f:
    f.write((json.dumps(entry, ensure_ascii=False) + '\n').encode())
(out / 'integration-scope.json').write_text(json.dumps(dict(owned=owned, science_commit=science, single_stabilization_lane=lanes[0]['advance_id'], child_status='VERIFIED', aggregate='pending', visual='pending', Goal_complete=False), indent=2) + '\n', encoding='utf8', newline='\n')
print('Verified normalization child admitted through existing sole lane; Registry553; aggregate gates pending.')
