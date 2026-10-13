from pathlib import Path
import json
r=Path(__file__).parent;out=r/'integration102';note=json.loads((r/'integration.notes.json').read_bytes())
text=f'''The actual finite PBPS construction now has an unnormalized weighted change-of-variables identity on phase space times the strict event-time simplex. For the actual endpoint/time reversal Theta and actual Gibbs-weighted density W, integral W(q)F(Theta(q)) equals integral W(q)F(q) for every measurable nonnegative extended-real F. The result consumes actual joint density measurability, measure preservation and pointwise weight balance, retaining the six original sampler assumptions. Infinite integrals and all zero cases are allowed; the extension beyond the source bounded tests is explicit.

Independent mathematics, source-blind decoding, primary-first source/exposition and exact-commit reviews passed. Six adjacent formula/Lean steps explain the proof. All15 local contributor/publication/semantic/frontier/graph/site gates passed, including `lake build Tests`, `tools/astis.py check`, Python compilation and `git diff --check`. Reviewed science commit: `{note['science_commit']}`. Original reviewer RAW evidence remains losslessly recoverable alongside normalized public mirrors.

Normalized Gibbs averaging, countable sector assembly, invariance, Markov properties, hypocoercivity, simulation errors, expected oracle costs and actual-input composition remain open. The four-paper Goal remains incomplete (0/4 full papers). Local generated-reader checks and static SVG inspection passed; actual page/fine-branch visual acceptance, main merge and postmerge purification remain pending. Existing collaborator changes and the sole stabilization lane are preserved.
'''
(out/'pr-body102.md').write_text(text,encoding='utf8',newline='\n')
