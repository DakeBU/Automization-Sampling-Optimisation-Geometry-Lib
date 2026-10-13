"""Render only the admitted endpoint node and its exact four public parents."""
from pathlib import Path
import hashlib, html, json
r = Path(__file__).resolve().parent
out = r / 'integration104/static-svg'
out.mkdir(parents=True, exist_ok=True)
claim = json.loads((r / 'claim.json').read_bytes())
graphp = Path('_site/data/underlying-lean-graph.json')
g = json.loads(graphp.read_bytes())
decl, parents = claim['target_declarations'][0], claim['dag_inputs']
ids = {'decl:' + x for x in parents + [decl]}
nodes = [n for n in g['nodes'] if n['id'] in ids]
assert len(nodes) == 5
scanner_edges = [e for e in g['edges'] if e['target'] == 'decl:' + decl and e['source'].startswith('decl:')]
review_path = r / 'independent-whole-math104/whole-math-decision104.native.json'
review = json.loads(review_path.read_bytes())
assert {'AutoSamplingTheory.ExampleCases.ProximalBPS.' + x['declaration'] for x in review['genuine_direct_parents']} == set(parents)
edges = [dict(source='decl:' + p, target='decl:' + decl, relation='independently reviewed exact public producer call', evidence=str(review_path)) for p in parents]
labels = [
    ('Actual finite-count density', 'Jointly measurable actual rho(z,t)'),
    ('Actual endpoint/time reversal', 'Measurable maps and B after Theta = J after B'),
    ('Actual weighted substitution', 'All nonnegative measurable sector tests'),
    ('Actual phase normalization', 'Positive finite Gibbs partition and product law'),
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
<text x="25" y="45" class="title">Actual normalized PBPS endpoint-pair reversal</text>
<text x="25" y="78" class="body">Original six analytic assumptions · Actual position-momentum energy · Every y,r,n,T · Dimension zero included</text>
<text x="25" y="107" class="small">ASTIS completion of arXiv:2609.06905v1 Appendix A.1; four already-reviewed actual producer parents</text>
{''.join(parts)}
<rect x="190" y="480" width="890" height="130" rx="10" fill="#e4efe2" stroke="#4e8052"/>
<text x="212" y="512" class="node">104 · ActualNormalizedEndpointSector</text>
<text x="212" y="543" class="body">Actual normalized sector sigma; endpoint measure L = B_*sigma; flipped swap J_*L = L</text>
<text x="212" y="570" class="body">Internal proof: align witnesses → rewrite density → Theta_*sigma = sigma → endpoint pushforward</text>
<text x="212" y="593" class="small">Original six assumptions. Initial phase normalized; no fixed-sector mass-one or process-invariance claim.</text>
<text x="25" y="641" class="node">Exact independently checked public producer calls</text>
{exact}
<text x="25" y="797" class="small">Exact producer calls independently reviewed; scanner references are not a kernel certificate. Phase normalization103 and weighted sector102 now join in actual104.</text>
</svg>'''
p = out / 'normalized-endpoint104.svg'
p.write_text(svg, encoding='utf8', newline='\n')
(out / 'branch-slice104.json').write_text(json.dumps(dict(source_graph=graphp.as_posix(), source_graph_RAW_sha256=hashlib.sha256(graphp.read_bytes()).hexdigest(), nodes=nodes, edges=edges, scanner_edges=scanner_edges, scanner_is_not_kernel_dependency_certificate=True, exact_review=str(r / 'independent-whole-math104/whole-math-decision104.native.json'), svg=str(p), svg_RAW_sha256=hashlib.sha256(p.read_bytes()).hexdigest(), viewed=False, interactive_page=False), indent=2) + '\n', encoding='utf8', newline='\n')
print(p)
