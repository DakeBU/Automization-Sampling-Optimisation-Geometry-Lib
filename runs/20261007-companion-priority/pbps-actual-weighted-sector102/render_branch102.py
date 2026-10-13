from pathlib import Path
import json,html,hashlib
r=Path(__file__).resolve().parent;out=r/'integration102/static-svg';out.mkdir(parents=True,exist_ok=True)
claim=json.loads((r/'claim.json').read_bytes());graphp=Path('_site/data/underlying-lean-graph.json');g=json.loads(graphp.read_bytes())
decl=claim['target_declarations'][0];parents=claim['dag_inputs'];ids={'decl:'+x for x in parents+[decl]};nodes=[n for n in g['nodes'] if n['id'] in ids];assert len(nodes)==4
edges=[e for e in g['edges'] if e['target']=='decl:'+decl and e['source'] in ids];assert {e['source'] for e in edges}=={'decl:'+p for p in parents}
labels={'ActualFiniteCountPath':('93 · Actual finite-count path law','Joint measurability of the original density'), 'ActualEndpointTimeReversal':('97 · Actual endpoint/time reversal','Preserves phase × strict-simplex volume'), 'ActualPrescribedWeightedDensity':('101 · Actual weighted density balance','W(q) = W(Theta(q))')}
texts=[];rects=[];paths=[]
for i,p in enumerate(parents):
 x=35+395*i;m=p.split('.')[-2];label,meaning=labels[m];short=p.split('.')[-1]
 rects.append(f'<rect x="{x}" y="150" width="365" height="150" rx="10" fill="#e9f3f4" stroke="#43858d"/>')
 texts.append(f'<text x="{x+16}" y="180" class="node">{html.escape(label)}</text><text x="{x+16}" y="210" class="body">{html.escape(meaning)}</text><text x="{x+16}" y="245" class="code">{html.escape(m)}</text>')
 paths.append(f'<path d="M{x+182} 300 V335 H610 V374" fill="none" stroke="#43858d" stroke-width="2" marker-end="url(#arrow)"/>')
lines=[]
for i,p in enumerate(parents):lines.append(f'<text x="45" y="{575+22*i}" class="code">{html.escape(p)}</text>')
svg=f"""<svg xmlns="http://www.w3.org/2000/svg" width="1220" height="685" viewBox="0 0 1220 685">
<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6" fill="#43858d"/></marker></defs>
<style>text{{font-family:Arial,sans-serif;fill:#163c45}}.title{{font-size:27px;font-weight:bold}}.node{{font-size:18px;font-weight:bold}}.body{{font-size:16px}}.code{{font-family:Consolas,monospace;font-size:12px}}.small{{font-size:13px}}</style>
<rect width="1220" height="685" fill="#fbfcfa"/>
<text x="35" y="48" class="title">Actual PBPS weighted finite-sector substitution</text>
<text x="35" y="80" class="body">Original six analytic assumptions · Actual path density · Unnormalized measure · Measurable ENNReal tests</text>
<text x="35" y="109" class="small">PBPS arXiv:2609.06905v1, Appendix A.1 A7/A8; ASTIS completion with an explicit nonnegative-test extension</text>
{''.join(rects)}{''.join(texts)}{''.join(paths)}
<rect x="215" y="375" width="790" height="133" rx="10" fill="#e4efe2" stroke="#4e8052"/>
<text x="240" y="405" class="node">102 · ActualWeightedSector.actual_weighted_sector_lintegral</text>
<text x="240" y="435" class="body">integral W(q) F(Theta(q)) dmu = integral W(q) F(q) dmu</text>
<text x="240" y="463" class="body">Internal bridge: measurable Gibbs factor × joint density, then Mathlib lintegral_comp</text>
<text x="240" y="488" class="small">No normalizer or finite-integral premise. Zero cases and infinite nonnegative values remain included.</text>
<text x="35" y="546" class="node">Exact verified parent calls</text>
{''.join(lines)}
<text x="35" y="658" class="small">Slice of generated references, checked against independent proof review; no conceptual edges. Full invariance, costs and paper completion remain open.</text>
</svg>"""
p=out/'weighted-sector102.svg';p.write_text(svg,encoding='utf8',newline='\n')
(out/'branch-slice102.json').write_text(json.dumps(dict(source_graph=str(graphp),source_graph_RAW_sha256=hashlib.sha256(graphp.read_bytes()).hexdigest(),nodes=nodes,edges=edges,exact_review=str(r/'independent-whole-math102/whole-math-decision102.native.json'),svg=str(p),svg_RAW_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),viewed=False,interactive_page=False),indent=2)+'\n',encoding='utf8')
print(p)
