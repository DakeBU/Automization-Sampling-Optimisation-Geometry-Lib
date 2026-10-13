from pathlib import Path
import hashlib,json
r=Path('runs/20261007-companion-priority/pbps-actual-corrector-change71');p=Path('conversion-windows/ASTIS-SW-PBPS-2026.md');b=p.read_bytes();nl='\r\n' if b'\r\n' in b else '\n';text=b.decode().replace('\r\n','\n');anchor='# Proximal BPS · formalization result window\n\n';assert text.startswith(anchor)
assert '## Current verified corrector checkpoint (2026-10-10)' not in text
v=json.loads((r/'verified.json').read_bytes());assert v['status']=='VERIFIED'
(r/'integration71/conversion.before.exactraw.md').write_bytes(b)
entry=f'''## Current verified corrector checkpoint (2026-10-10)

The historical source packets and earlier checkpoint paragraphs below are
preserved. Current status is supplied by the handoff, live Frontier Cells and
Harness capsule. `ASTIS-SW-PBPS-actual-corrector-change` has independent
commit-bound verification at `{v['verified_commit']}` for the discrete B21
corrector change under the actual reflected observable.

The complete attributed statement and eight-step formula proof are authored
once in `website/content/declaration_lessons/pbps-actual-corrector-change.json`.
The matching publication binds exact source obligations and assumption
differences. `ActualCorrectorChange.actual_corrector_change`, its complete
private literal proposition and all proof spans remain adjacent folded Lean
on the original companion page.

| Source ingredient | Exact current Lean meaning |
|---|---|
| Reflected observable and actual coordinates | Same `g = U (P f - (f - P f))`, actual conditional `gP`, and `gV = V0.adjoint (R g)` |
| Corrector B20 | `C u v = (norm(u)^2-norm(v)^2)/2-inner(A0(Inv u),v)` on the SAME `HP0` |
| Discrete corrector change B21 | `C gP gV-C fP fV = -norm(fP)^2+norm(fV)^2` |
| Actual-update comparison B27/B28 | Subsequent obligation: half-turn/refreshment error components and perturbation |

All six original analytic callers, twelve common witnesses and previous
clauses persist. Exact half and signs, legal rank0/alphaeta1 and the same
centered inverse are preserved. The local algebra supplies no extra
regularity, onto-map, mean or sharp-bound premise.

Full B4/H1/B2 dynamics, invariance/nonexplosion, PBPS/SPHMC mains,
implementation errors/caps, initialization and actual-input expected-query
costs/composition remain independent. TV proximity does not transfer
unbounded cost. Aggregate/reader/remote CI, full Exposition/PURIFIED,
main/live and whole-paper/Goal completion are separate admissions.

'''
p.write_bytes((anchor+entry+text[len(anchor):]).replace('\n',nl).encode())
print('PASS original conversion window points to reviewed71 B21; earlier history retained; SHA',hashlib.sha256(p.read_bytes()).hexdigest())
