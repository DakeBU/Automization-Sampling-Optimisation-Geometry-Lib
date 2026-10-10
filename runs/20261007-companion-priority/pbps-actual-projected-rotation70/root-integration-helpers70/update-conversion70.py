from pathlib import Path
import hashlib,json
r=Path('runs/20261007-companion-priority/pbps-actual-projected-rotation70');p=Path('conversion-windows/ASTIS-SW-PBPS-2026.md');b=p.read_bytes();nl='\r\n' if b'\r\n' in b else '\n';text=b.decode().replace('\r\n','\n');anchor='# Proximal BPS · formalization result window\n\n';assert text.startswith(anchor)
assert '## Current verified companion checkpoint (2026-10-10)' not in text
v=json.loads((r/'verified.json').read_bytes());assert v['status']=='VERIFIED'
(r/'integration70/conversion.before.exactraw.md').write_bytes(b)
entry=f'''## Current verified companion checkpoint (2026-10-10)

The historical source packets below are preserved. Current theorem status and
remaining dependencies come from `docs/companion-papers-handoff.md`, the live
Frontier Cells and the Harness capsule, rather than the older dated paragraphs.

`ASTIS-SW-PBPS-actual-projected-rotation` now has independent commit-bound
verification at `{v['verified_commit']}`. Its source anchor is Appendix B.3,
the actual projected rotation used by (B.21) and Lemma B.4. The complete source
conditions, notation and eight-step formula proof are authored once in
`website/content/declaration_lessons/pbps-actual-projected-rotation.json`, with
exact obligations and assumption differences in the matching publication file.
The production declaration is
`ActualProjectedRotation.actual_projected_rotation`; its full literal statement
and exact proof remain adjacent folded Lean in the original companion page.

| Source object or ingredient | Exact current Lean meaning |
|---|---|
| Actual reflected observable | `g = U (P f - (f - P f))` on the same joint law |
| Global centering of the output | Proved internally from the actual reflection law and conditional expectation |
| Output macroscopic coordinate | `gP` is the same conditional expectation in `HP0` |
| Output polar coordinate | `gV = V0.adjoint (R g)` |
| Rotation and energy | Exact formulas and pair-energy identity in the linked declaration lesson |
| Printed corrector change (B.21) | Next sealed source target; not proved by pair-energy conservation |

All six original analytic callers and twelve common witnesses persist. No new
mean, regularity, onto-map or sharp-energy premise is added. Dimension zero and
the endpoint alpha*eta=1 remain admitted. Shared aggregate/reader checks and
remote CI are separate from this science verification. Full B4 dynamics,
invariance/nonexplosion, PBPS/SPHMC main results, errors/caps, initialization and
actual-input expected-query costs/composition remain separate obligations.
TV proximity does not transfer unbounded costs. This is not a whole-paper,
Exposition Seal, PURIFIED, main or live-deployment completion claim.

'''
p.write_bytes((anchor+entry+text[len(anchor):]).replace('\n',nl).encode())
print('PASS original conversion window refreshed by pointers to reviewed70 mathematics; older history retained; SHA',hashlib.sha256(p.read_bytes()).hexdigest())
