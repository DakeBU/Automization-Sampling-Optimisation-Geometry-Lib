from pathlib import Path
import json
r=Path(__file__).parent;out=r/'integration101';note=json.loads((r/'integration.notes.json').read_bytes())
text=f'''The actual finite PBPS construction now has pointwise weighted-density matching under event-time reversal and momentum reversal of the terminal state. The new result connects the original algorithmic density (prefix density times terminal survival) to the Gibbs-survival, incoming-rate and path-integral reversal results. Both real and ENNReal identities retain the original six assumptions, including zero-rate and zero-event cases.

The declaration has independent mathematical, anonymous-decoder, primary-first source and exact-commit reviews. Six adjacent formula/Lean steps explain the proof; an indexing convention clarification was independently reviewed. All 15 local contributor/publication/semantic/frontier/graph/site gates passed, including `lake build Tests`, `tools/astis.py check`, Python compilation and `git diff --check`. Reviewed science commit: `{note['science_commit']}`.

Weighted-sector integration, normalized Gibbs invariance, Markov properties, hypocoercivity, implementation errors, expected oracle costs and actual-input composition remain open. The four-paper Goal remains incomplete (0/4 full papers). Local generated-reader checks and static SVG inspection passed; actual page/fine-branch visual acceptance, main merge and postmerge purification remain pending. Existing collaborator changes and the sole stabilization lane are preserved.
'''
(out/'pr-body101.md').write_text(text,encoding='utf8',newline='\n')
