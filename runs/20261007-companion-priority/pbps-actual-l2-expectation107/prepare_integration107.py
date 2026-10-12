"""Admit independently verified L2 expectation contraction through the existing sole lane."""
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
out = r / 'integration107'
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
module = 'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualL2Expectation'
decl = c['target_declarations'][0]
for name in owned[:2]:
    after(name, 'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBoundedGibbsDuality', 'import ' + module + '\n')
note = f'Independent science {science}. Under the original six assumptions, the same global jointly measurable actual PBPS Z retains live arcs, fallback, parameterwise initialization, Gibbs preservation and bounded flip duality. Every Borel test has a joint Borel total clock expectation; a uniform finite bound proves every section L1. For each y,r an internally constructed real L2 contraction family A_T realizes the literal clock expectation of every MemLp representative, with almost-everywhere section L1, output L2 membership, exact quotient identity, square-integral contraction and A_0=id. Actual106, normalization103 and UnitExponentialProduct are the three producers. Adjoint pullbacks, product L1, signed Fubini and indicator uniqueness are internal dependencies. Representative independence is a consequence of universal quotient identification; the planned direct-AE route remains an unselected alternative. Full L2 flip identity A.3, restart/Markov/semigroup, separate kernel witness identification, strong continuity, hypocoercivity, errors, actual expected costs, composition and all four papers remain open.'



block = '  {\n' + '\n'.join(['    key := "pbps.actualL2Expectation"', '    localDecl := ' + json.dumps(decl), '    upstreamDecl := "Actual PBPS L2 expectation contraction and zero-time identity"', '    upstreamFile := "arXiv2609.06905v1 Appendix A.1 expectation operator and L2 domain toward Eq A.3"', '    status := LemmaMemoryStatus.formalizedLocal', '    tags := ["PBPS", "L2", "expectation", "contraction"]', '    saldUse := "Actual same-process L2 expectation contraction; no SALD claim"', '    note := ' + json.dumps(note)]) + '\n  },\n'
after(owned[1], 'def analysisMemory : List LemmaMemoryEntry := [', block)
p = Path(owned[2])
b = p.read_bytes()
matches = re.findall(rb'formalizedTechnicalLemmaCount = (\d+)', b)
assert len(matches) == 1
before_count = int(matches[0]); after_count = before_count + 1
p.write_bytes(b.replace(b'formalizedTechnicalLemmaCount = ' + matches[0], b'formalizedTechnicalLemmaCount = ' + str(after_count).encode(), 1))
prefix = f'''## Actual PBPS L2 expectation contraction (2026-10-12)

Independent science {science}. Under the original six analytic assumptions,
the same global actual process Z retains joint measurability, exact live arcs,
raw fallback, parameterwise zero-time initialization, fixed-time Gibbs
preservation and bounded signed momentum-flip duality.

Every Borel real observable has a jointly Borel total clock expectation.
A finite pointwise bound proves every clock section integrable. For each y,r,
there exists a family of continuous real linear operators A_T on L2(nu_y)
with norm at most1 and A_0=id. Every arbitrary MemLp representative G has
integrable clock sections for nu_y-almost every phase point, its actual
expectation belongs to L2, A_T[G]=[op_T G], and
integral |op_T G|^2 dnu_y <= integral |G|^2 dnu_y.

The proof consumes actual106, actual normalization103 and UnitExponentialProduct.
First-coordinate and endpoint pullbacks are L2 isometries; their adjoint
composition constructs the contraction. Product L1 and signed Fubini precede
indicator-test uniqueness, which identifies the operator with the literal
expectation. Universal quotient identification supplies representative
independence. The retained direct-AE route is an unselected source-graph
alternative, not an asserted invocation of ae_ae_of_ae_prod. The effective
source graph has85 nodes and161 edges, with no new source premise.

Ten adjacent formula/Lean regions explain this ASTIS completion. Header,
whole mathematics, fresh blind reconstruction and final primary-first
source/exposition reviews passed. Full L2 momentum-flip identity Eq A.3,
restart/Markov/semigroup, strong continuity, separate kernel-witness equality,
hypocoercivity, implementation errors, actual expected costs and complete
composition remain red. No time-index regularity of A_T is asserted.
Full paper completion remains0/4. Public integration uses the sole SAU94 lane;
actual browser acceptance, main merge and purification remain separate.

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
anchor = b'#actual-pbps-bounded-gibbs-duality-and-fixed-time-invariance-2026-10-12'
assert b.count(anchor) == 1
p.write_bytes(b.replace(anchor, b'#actual-pbps-l2-expectation-contraction-2026-10-12', 1))
prepend(owned[5], f'## Actual L2 expectation contraction107 (2026-10-12)\n\n{note}\n\nTen source-reviewed formula/Lean regions. Aggregate/visual acceptance, main merge and purification retain separate evidence.\n\n')
entry = dict(key='pbps.actualL2Expectation', local_decl=decl, local_file=c['proposed_files'][0], status='formalized-local', verified_commit=science, evidence=state['latest_evidence'], next_action=note)
with Path(owned[6]).open('ab') as f:
    f.write((json.dumps(entry, ensure_ascii=False) + '\n').encode())
(out / 'integration-scope.json').write_text(json.dumps(dict(owned=owned, science_commit=science, single_stabilization_lane=lanes[0]['advance_id'], child_status='VERIFIED', aggregate='pending', visual='pending', Goal_complete=False), indent=2) + '\n', encoding='utf8', newline='\n')
print(f'Verified L2 contraction child admitted through existing sole lane; Registry{after_count}; aggregate gates pending.')
