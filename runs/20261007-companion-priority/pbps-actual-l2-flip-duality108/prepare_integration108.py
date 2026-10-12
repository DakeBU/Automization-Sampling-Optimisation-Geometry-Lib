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
out = r / 'integration108'
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
module = 'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualL2FlipDuality'
decl = c['target_declarations'][0]
for name in owned[:2]:
    after(name, 'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualL2Expectation', 'import ' + module + '\n')
note = f'Independent science {science}. Under the original six assumptions, the same global actual PBPS process and the same real L2 expectation family from107 retain all path, Borel, Gibbs, bounded-duality, integrability, contraction and initialization conclusions. The canonical momentum-flip pullback J is an involutive L2 isometry and A_T.adjoint = J A_T J for every nonnegative T, on all real L2 classes. Gaussian reflection and product maps prove phase preservation. Bounded simple representatives give the signed pairing; continuity and two-variable density extend it to all L2, then adjoint uniqueness closes Eq A.3. No new source premise. Restart/Markov/semigroup, strong continuity, separate kernel witnesses, actual position averaging, hypocoercivity, errors, actual expected costs, composition and four complete papers remain open.'




block = '  {\n' + '\n'.join(['    key := "pbps.actualL2FlipDuality"', '    localDecl := ' + json.dumps(decl), '    upstreamDecl := "Actual PBPS full real-L2 momentum-flip adjoint identity"', '    upstreamFile := "arXiv2609.06905v1 Appendix A.1 Eq A.3 and density extension"', '    status := LemmaMemoryStatus.formalizedLocal', '    tags := ["PBPS", "L2", "adjoint", "momentum-flip"]', '    saldUse := "Actual same-process full real-L2 flip duality; no SALD claim"', '    note := ' + json.dumps(note)]) + '\n  },\n'
after(owned[1], 'def analysisMemory : List LemmaMemoryEntry := [', block)
p = Path(owned[2])
b = p.read_bytes()
matches = re.findall(rb'formalizedTechnicalLemmaCount = (\d+)', b)
assert len(matches) == 1
before_count = int(matches[0]); after_count = before_count + 1
p.write_bytes(b.replace(b'formalizedTechnicalLemmaCount = ' + matches[0], b'formalizedTechnicalLemmaCount = ' + str(after_count).encode(), 1))
prefix = f'''## Actual PBPS full real-L2 flip duality (2026-10-12)

Independent science {science}. The original six analytic assumptions and
one global actual process Z are unchanged. All107 conclusions remain on
that same witness and the same family A_T: actual expectations, joint
Borel dependence for Borel tests, AE section integrability for MemLp inputs,
Gibbs preservation, bounded duality, contraction and A_0=id.

For the literal momentum reflection R(x,p)=(x,-p), prove R preserves nu_y
and define the canonical L2 pullback J. It is an isometry, J^2=id, and
A_T.adjoint = J A_T J for every finite nonnegative T and all real L2 classes.
The proof consumes actual107 once. Gaussian symmetry and product maps
establish reflection preservation; simple representatives and inherited
bounded duality give the pairing on a dense subset; two-variable continuity
extends it to all L2 before adjoint uniqueness. Rank0 and T0 are included.

The independently admitted source graph has107 nodes and196 edges.
Implementation uses AE composition and Lp.ext for involution and class
conversion, and ext_inner_right for adjoint uniqueness. These are faithful
implementations of the same reviewed semantic dependencies, not route changes.
Eight adjacent formula/Lean regions explain the proof. The region-only
step2/3 adjacency repair has separate independent admission.

Independent header, whole mathematics, fresh source-blind reconstruction,
primary-first source/exposition review and exact-commit admission passed.
Restart/Markov/semigroup, strong continuity, separate kernel identification,
actual momentum-averaged position operator, hypocoercivity, implementation
errors, actual expected costs and complete composition remain red.
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
anchor = b'#actual-pbps-l2-expectation-contraction-2026-10-12'
assert b.count(anchor) == 1
p.write_bytes(b.replace(anchor, b'#actual-pbps-full-real-l2-flip-duality-2026-10-12', 1))
prepend(owned[5], f'## Actual full real-L2 flip duality108 (2026-10-12)\n\n{note}\n\nEight source-reviewed formula/Lean regions. Aggregate/visual acceptance, main merge and purification retain separate evidence.\n\n')
entry = dict(key='pbps.actualL2FlipDuality', local_decl=decl, local_file=c['proposed_files'][0], status='formalized-local', verified_commit=science, evidence=state['latest_evidence'], next_action=note)
with Path(owned[6]).open('ab') as f:
    f.write((json.dumps(entry, ensure_ascii=False) + '\n').encode())
(out / 'integration-scope.json').write_text(json.dumps(dict(owned=owned, science_commit=science, single_stabilization_lane=lanes[0]['advance_id'], child_status='VERIFIED', aggregate='pending', visual='pending', Goal_complete=False), indent=2) + '\n', encoding='utf8', newline='\n')
print(f'Verified full real-L2 flip child admitted through existing sole lane; Registry{after_count}; aggregate gates pending.')
