"""Render only the admitted normalization node and its exact five public parents."""
from pathlib import Path
import hashlib, html, json
r = Path(__file__).resolve().parent
out = r / 'integration103/static-svg'
out.mkdir(parents=True, exist_ok=True)
claim = json.loads((r / 'claim.json').read_bytes())
graphp = Path('_site/data/underlying-lean-graph.json')
g = json.loads(graphp.read_bytes())
decl, parents = claim['target_declarations'][0], claim['dag_inputs']
ids = {'decl:' + x for x in parents + [decl]}
nodes = [n for n in g['nodes'] if n['id'] in ids]
assert len(nodes) == 6
scanner_edges = [e for e in g['edges'] if e['target'] == 'decl:' + decl and e['source'].startswith('decl:')]
review_path = r / 'independent-whole-math103/whole-math-decision103.native.json'
review = json.loads(review_path.read_bytes())
assert {x['declaration'] for x in review['direct_consumed_public_producers']} == set(parents)
edges = [dict(source='decl:' + p, target='decl:' + decl, relation='independently reviewed exact public producer call', evidence=str(review_path)) for p in parents]
labels = [
    ('Hessian lower bound', 'C2 + lower Hessian ⇒ strong convexity'),
    ('Gibbs integrable tail', 'Positive strong convexity ⇒ exp(-V) in L1'),
    ('Gaussian integral', 'Exact factor C = (sqrt(2 pi))^dimension'),
    ('Standard Gaussian density', 'Variance one ⇒ density C^(-1) exp(-|p|²/2)'),
    ('Gibbs probability normalization', 'Positive finite mass ⇒ normalized law'),
]
parts = []
for i, (label, meaning) in enumerate(labels):
    row, col = divmod(i, 3)
    x, y = 25 + 410 * col, 140 + 150 * row
    if row == 1:
        x += 200
    parts.append(f'<rect x="{x}" y="{y}" width="390" height="112" rx="10" fill="#e9f3f4" stroke="#43858d"/>')
    parts.append(f'<text x="{x+14}" y="{y+32}" class="node">{html.escape(label)}</text>')
    parts.append(f'<text x="{x+14}" y="{y+60}" class="body">{html.escape(meaning)}</text>')
    parts.append(f'<text x="{x+14}" y="{y+88}" class="code">{html.escape(parents[i].split(".")[-2])}</text>')
    # Separate rails for upper and lower rows keep arrows out of boxes.
    rail = 270 if row == 0 else 430
    side = 15 if row == 0 else 1245
    parts.append(f'<path d="M{x+195} {y+112} V{rail} H{side} V460 H635 V480" fill="none" stroke="#43858d" stroke-width="1.5" marker-end="url(#arrow)"/>')
exact = ''.join(f'<text x="35" y="{670+21*i}" class="code">{html.escape(p)}</text>' for i, p in enumerate(parents))
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1270" height="820" viewBox="0 0 1270 820">
<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6" fill="#43858d"/></marker></defs>
<style>text{{font-family:Arial,sans-serif;fill:#163c45}}.title{{font-size:27px;font-weight:bold}}.node{{font-size:18px;font-weight:bold}}.body{{font-size:15px}}.code{{font-family:Consolas,monospace;font-size:11px}}.small{{font-size:13px}}</style>
<rect width="1270" height="820" fill="#fbfcfa"/>
<text x="25" y="45" class="title">Actual PBPS phase Gibbs normalization</text>
<text x="25" y="78" class="body">Original six analytic assumptions · Actual position-momentum energy · Every center y · Dimension zero included</text>
<text x="25" y="107" class="small">ASTIS completion of arXiv:2609.06905v1 Eq3.1 proportionality; canonical shared leaves and fixed Mathlib</text>
{''.join(parts)}
<rect x="190" y="480" width="890" height="130" rx="10" fill="#e4efe2" stroke="#4e8052"/>
<text x="212" y="512" class="node">103 · ActualPhaseNormalization.actual_phase_gibbs_normalization</text>
<text x="212" y="543" class="body">Zphase(y) = ofReal(Zx(y) C) &gt; 0 and finite; nu_y = tilted(-Vy) × stdGaussian(E)</text>
<text x="212" y="570" class="body">Internal proof: proximal domination → product integral → exact density identification</text>
<text x="212" y="593" class="small">No supplied minimizer, normalizer or integrability. No process-invariance or cost claim.</text>
<text x="25" y="641" class="node">Exact independently checked public producer calls</text>
{exact}
<text x="25" y="797" class="small">Exact producer calls from independent proof review; scanner references are incomplete. NORM is independent of sector102; they join only at a future consumer.</text>
</svg>'''
p = out / 'phase-normalization103.svg'
p.write_text(svg, encoding='utf8', newline='\n')
(out / 'branch-slice103.json').write_text(json.dumps(dict(source_graph=graphp.as_posix(), source_graph_RAW_sha256=hashlib.sha256(graphp.read_bytes()).hexdigest(), nodes=nodes, edges=edges, scanner_edges=scanner_edges, scanner_is_not_kernel_dependency_certificate=True, exact_review=str(r / 'independent-whole-math103/whole-math-decision103.native.json'), svg=str(p), svg_RAW_sha256=hashlib.sha256(p.read_bytes()).hexdigest(), viewed=False, interactive_page=False), indent=2) + '\n', encoding='utf8', newline='\n')
print(p)
