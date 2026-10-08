(() => {
  "use strict";
  const host = document.querySelector("[data-underlying-lean-graph]");
  if (!host) return;
  const canvas = document.querySelector("[data-graph-canvas]");
  const svg = document.querySelector("[data-graph-svg]");
  const detail = document.querySelector("[data-graph-detail]");
  const search = document.querySelector("[data-graph-search]");
  const count = document.querySelector("[data-graph-count]");
  const empty = document.querySelector("[data-graph-empty]");
  const buttons = [...document.querySelectorAll("[data-view]")];
  const NS = "http://www.w3.org/2000/svg";
  const state = {view: "overview", color: "status", query: "", focus: "", expanded: new Set(), scale: 0.82, x: 32, y: 36, drag: null};
  const kindOrder = {"library-extension":2, "perspective-family":0,"perspective-method":1,"perspective-target":2,"concept-domain": 0, "concept-bridge": 1, "library-chapter": 2, library: 0, "proof-root": 1, chapter: 2, setting: 2, phase: 2, "semantic-stage": 2, "source-claim": 3, "frontier-case": 3, module: 3, "semantic-audit": 4, "proof-leaf": 4, declaration: 4, "repair-proposal": 5};
  const kindLabel = {"library-extension":"extended source outline","perspective-family":"method family","perspective-method":"method instance","perspective-target":"target class","concept-domain": "domain", "concept-bridge": "transport contract", "library-chapter": "peer book chapter", library: "library", "proof-root": "shared root", chapter: "book chapter", setting: "SampleWiki setting", phase: "formalization phase", "source-claim": "source theorem", "frontier-case": "frontier theorem", module: "Lean module", "proof-leaf": "proof leaf", declaration: "Lean declaration", "semantic-stage": "semantic protocol", "semantic-audit": "fidelity audit", "repair-proposal": "theorem repair proposal"};
  const viewKinds = {
    functor: new Set(["concept-domain", "concept-bridge"]),
    perspectives: new Set(["perspective-family","perspective-method","perspective-target","library"]),
    overview: new Set(["library-extension","library-chapter","library", "proof-root", "chapter", "setting", "phase", "frontier-case", "semantic-stage"]),
    textbook: new Set(["library", "proof-root", "chapter", "source-claim", "proof-leaf"]),
    frontier: new Set(["library", "proof-root", "chapter", "setting", "phase", "frontier-case"]),
    lean: new Set(["library", "proof-root", "module", "declaration", "proof-leaf", "source-claim"]),
    semantic: new Set(["library", "semantic-stage", "semantic-audit", "repair-proposal"]),
  };
  // Solid edges record source module structure, not theorem implication.
  // Name scans and curated proof-leaf links are dashed: neither is an
  // elaborated Lean dependency certificate.
  const FORMAL_RELATIONS = new Set(["imports", "declares"]);
  const colorSelect=document.querySelector('[data-graph-color]');
  const scopeLegend=document.querySelector('[data-scope-legend]');
  let graph, nodes, incident, degree;
  function updateScopeLegend() {
    if (!graph || !scopeLegend) return;
    scopeLegend.hidden=state.color!=='library';
    scopeLegend.innerHTML=Object.entries(graph.library_scope_metadata?.palette||{}).map(([k,v])=>`<span><i style="background:${esc(v.color)}"></i>${esc(v.label)}</span>`).join('');
    if(colorSelect)colorSelect.value=state.color;
  }

  const esc = value => String(value ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  const svgEl = (name, attrs = {}) => { const el = document.createElementNS(NS, name); Object.entries(attrs).forEach(([k,v]) => el.setAttribute(k, v)); return el; };
  const neighbors = id => [...(incident.get(id) || [])].map(e => e.source === id ? e.target : e.source);
  const edgeSetFor = ids => graph.edges.filter(e => ids.has(e.source) && ids.has(e.target));
  const relationEvidence = relation => FORMAL_RELATIONS.has(String(relation || "")) ? "formal" : "overlay";
  const wrap = (value, width = 24, lines = 2) => {
    const text=String(value || ""); const out=[]; let rest=text;
    while (rest && out.length < lines) {
      if (rest.length <= width) { out.push(rest); rest=""; break; }
      let at=rest.lastIndexOf(" ",width); if (at<width/2) at=width;
      out.push(rest.slice(0,at)); rest=rest.slice(at).trimStart();
    }
    if (rest && out.length) out[out.length-1]=out[out.length-1].slice(0,width-1)+"…";
    return out;
  };
  const atlasLabels = {
    "concept:optimization":"Optimisation", "concept:riemannian":"Riemannian optimisation",
    "concept:transport":"Optimal transport", "concept:sampling":"Sampling / MFLD", "concept:lower":"Lower bounds / SampleWiki",
    "transport:metric-lift":"Change the metric", "transport:gibbs-prox":"Minimizer / Gibbs law",
    "transport:dirac":"Maps to Markov kernels", "transport:wasserstein-flow":"Energy to Wasserstein flow",
    "transport:metric-pl":"Metric PL / dissipation", "transport:curvature-growth":"Curvature → coercivity",
    "transport:pl-lsi":"PL ↔ LSI / KL", "transport:pi-chi2":"Poincaré ↔ χ²",
    "transport:entropy-sandwich":"KL gap / PL / growth", "transport:duality":"Convex duality",
    "transport:high-order":"Smoothness to accuracy?", "transport:oracle-reduction":"Oracle reduction",
    "transport:statistical-loss":"Data, loss and risk",
    "concept:discrete-sampling":"Discrete Sampling",
    "transport:discrete-pi":"Finite Poincaré / χ²",
    "transport:discrete-mlsi":"Modified LSI / KL",
    "transport:discrete-transport":"Chain-dependent transport",
    "transport:discrete-influence":"Conditional influence"
  };

  function viewIds(all) {
    const selected = new Set(all.filter(n => viewKinds[state.view].has(n.kind)).map(n => n.id));
    if (state.view === "overview") [...selected].forEach(id => { const n = nodes.get(id); if (n?.kind === "frontier-case" && !["audited","literature-open"].includes(n.status)) selected.delete(id); if (n?.kind === "semantic-stage" && !["semantic:fidelity-checker","semantic:theorem-denoiser"].includes(id)) selected.delete(id); });
    if (state.view === "textbook") [...selected].forEach(id => { const n = nodes.get(id); if (n?.kind === "library" && n.id === "library:samplewiki") selected.delete(id); });
    if (state.view === "frontier") [...selected].forEach(id => { const n = nodes.get(id); if (n?.kind === "library" && n.id === "library:chewi") selected.delete(id); });
    if (state.view === "semantic") [...selected].forEach(id => { const n = nodes.get(id); if (n?.kind === "library" && n.id !== "library:samplinglib") selected.delete(id); });
    if (state.view === "perspectives") [...selected].forEach(id=>{if(!nodes.get(id)?.perspective_position)selected.delete(id);});
    return selected;
  }

  function visibleIds() {
    const all = [...nodes.values()]; let selected;
    if (state.query) {
      const terms = state.query.toLowerCase().split(/\s+/).filter(Boolean);
      const hits = all.filter(n => terms.every(t => n.search.includes(t))).sort((a,b) => (degree.get(b.id)-degree.get(a.id)) || a.label.localeCompare(b.label)).slice(0, 36);
      selected = new Set(hits.map(n => n.id)); hits.forEach(n => neighbors(n.id).forEach(id => selected.add(id)));
    } else {
      selected = viewIds(all);
    }

    // Focus is a visual overlay, not a graph filter. Keep the current textbook /
    // frontier / Lean / semantic context visible, then force the selected branch
    // and its immediate neighborhood into the canvas. This mirrors the
    // QuantumComputinglib interaction and makes highlighted versus muted edges
    // visually meaningful.
    const priority = new Set();
    if (state.focus) {
      priority.add(state.focus); selected.add(state.focus);
      neighbors(state.focus).forEach(id => { if(state.view !== "functor" || viewKinds.functor.has(nodes.get(id)?.kind)) { priority.add(id); selected.add(id); } });
    }
    state.expanded.forEach(id => {
      selected.add(id); priority.add(id);
      neighbors(id).forEach(n => { if(state.view !== "functor" || viewKinds.functor.has(nodes.get(n)?.kind)) selected.add(n); });
    });

    if(state.view === "perspectives") [...selected].forEach(id=>{if(!nodes.get(id)?.perspective_position)selected.delete(id);});
    if (selected.size > 190) {
      const forced = [...priority].filter(id => selected.has(id));
      const forcedSet = new Set(forced);
      const rest = [...selected].filter(id => !forcedSet.has(id)).sort((a,b) => {
        const A=nodes.get(a), B=nodes.get(b); const pa = A.kind === "library" || A.kind === "proof-root" ? 10000 : 0; const pb = B.kind === "library" || B.kind === "proof-root" ? 10000 : 0;
        return (pb + degree.get(b)) - (pa + degree.get(a));
      });
      selected = new Set([...forced.slice(0, 190), ...rest.slice(0, Math.max(0, 190 - forced.length))]);
    }
    return selected;
  }

  function layout(ids) {
    if(state.view === "perspectives") {
      const positions=new Map([...ids].map(id=>{const xy=nodes.get(id).perspective_position;return [id,{x:xy[0]+22,y:xy[1]+52}];}));
      return {positions,width:1470,height:870};
    }
    if (state.view === "functor" && !state.query) {
      // Optimization-centered conceptual atlas, not a topological proof layout.
      // The stable placement groups the new coercivity/dissipation mirrors near
      // the center without turning visual proximity into a theorem implication.
      const anchors = {
        "concept:lower":[0,0], "transport:oracle-reduction":[340,0], "concept:riemannian":[680,0],
        "transport:curvature-growth":[340,170], "transport:metric-lift":[680,170],
        "transport:dirac":[0,340], "concept:optimization":[340,340], "transport:duality":[680,340],
        "transport:gibbs-prox":[0,510], "transport:metric-pl":[340,510], "transport:wasserstein-flow":[680,510],
        "transport:pi-chi2":[0,680], "transport:pl-lsi":[340,680],
        "concept:sampling":[0,850], "transport:entropy-sandwich":[340,850], "concept:transport":[680,850],
        "transport:high-order":[0,1020], "transport:statistical-loss":[680,1020],
        "transport:discrete-influence":[1020,170], "concept:discrete-sampling":[1020,510],
        "transport:discrete-mlsi":[1020,680], "transport:discrete-pi":[1020,850],
        "transport:discrete-transport":[1020,1020],
        "concept:mcmc":[1360,340], "transport:mcmc-metropolis":[1360,0],
        "transport:mcmc-scaling":[1360,170], "transport:mcmc-lifting":[1360,510],
        "transport:mcmc-perturbation":[1360,680], "transport:mcmc-gibbs-coordinate":[1360,850]
      };
      const positions = new Map(); let extra = 0;
      [...ids].forEach(id => { const a=anchors[id] || [340,1190+extra++*140]; positions.set(id,{x:a[0]+20,y:a[1]+20}); });
      return {positions,width:1700,height:1180+extra*140};
    }
    const columns = new Map(); let maxColumn = 0;
    [...ids].forEach(id => { const n=nodes.get(id); const explicit=Number(n.column); const key=Number.isFinite(explicit) ? explicit : (kindOrder[n.kind] ?? 3); maxColumn=Math.max(maxColumn,key); if (!columns.has(key)) columns.set(key, []); columns.get(key).push(n); });
    const positions = new Map(); let maxRows = 1;
    [...columns.entries()].sort((a,b)=>a[0]-b[0]).forEach(([column, list], localColumn) => {
      list.sort((a,b) => (a.kind.localeCompare(b.kind)) || a.label.localeCompare(b.label)); maxRows = Math.max(maxRows, list.length);
      const gap = list.length > 38 ? 64 : 82; list.forEach((n,i) => positions.set(n.id, {x: 62 + (state.query ? localColumn : column) * 310, y: 58 + i * gap}));
    });
    return {positions, width: state.query ? 360 + Math.max(0, columns.size - 1) * 310 : Math.max(1560, 360 + maxColumn * 310), height: Math.max(state.query ? 300 : 700, 130 + maxRows * (maxRows > 38 ? 64 : 82))};
  }

  function applyTransform() { const viewport = svg.querySelector(".ulg-viewport"); if (viewport) viewport.setAttribute("transform", `translate(${state.x} ${state.y}) scale(${state.scale})`); }
  function fit() { const box = svg.getBoundingClientRect(); const width = Number(svg.dataset.worldWidth || 1500), height = Number(svg.dataset.worldHeight || 700); state.scale = Math.max(.2, Math.min(1.05, Math.min((box.width-40)/width, (box.height-40)/height))); state.x = Math.max(18, (box.width-width*state.scale)/2); state.y = 22; applyTransform(); }

  function render() {
    canvas.dataset.view=state.view; canvas.dataset.color=state.color; canvas.dataset.local=state.query?'true':'false'; updateScopeLegend();
    const ids = visibleIds(); const edges = edgeSetFor(ids); const {positions,width,height} = layout(ids);
    const focusNeighbors = new Set(state.focus ? neighbors(state.focus) : []);
    const directEdges = state.focus ? (incident.get(state.focus) || []).filter(e => ids.has(e.source) && ids.has(e.target)) : [];
    svg.replaceChildren(); svg.dataset.worldWidth=width; svg.dataset.worldHeight=height; svg.setAttribute("viewBox", `0 0 ${Math.max(1, svg.clientWidth || 900)} ${Math.max(1, svg.clientHeight || 650)}`);
    const defs = svgEl("defs");
    const marker=svgEl("marker", {id:"ulg-arrow", class:"ulg-arrow-marker", viewBox:"0 0 10 10", refX:"9", refY:"5", markerWidth:"6", markerHeight:"6", orient:"auto-start-reverse"}); marker.append(svgEl("path", {d:"M 0 0 L 10 5 L 0 10 z"})); defs.append(marker);
    const focusMarker=svgEl("marker", {id:"ulg-arrow-focus", class:"ulg-arrow-marker focus", viewBox:"0 0 10 10", refX:"9", refY:"5", markerWidth:"6", markerHeight:"6", orient:"auto-start-reverse"}); focusMarker.append(svgEl("path", {d:"M 0 0 L 10 5 L 0 10 z"})); defs.append(focusMarker);
    svg.append(defs);
    const viewport=svgEl("g", {class:"ulg-viewport"}); const edgeLayer=svgEl("g", {class:"ulg-edges"}); const nodeLayer=svgEl("g", {class:"ulg-nodes"}); viewport.append(edgeLayer,nodeLayer); svg.append(viewport);
    if(state.view === "perspectives") {
      [[20,"METHOD FAMILIES"],[580,"ALGORITHM INSTANCES"],[900,"TARGET CLASSES"],[1220,"TEXTBOOK / ANALYTIC LENSES"]].forEach(([px,title])=>{const t=svgEl("text",{x:px,y:23,class:"ulg-column-title"});t.textContent=title;nodeLayer.append(t);});
    }
    edges.forEach(e => {
      const a=positions.get(e.source), b=positions.get(e.target); if(!a||!b)return;
      const related = Boolean(state.focus && (e.source === state.focus || e.target === state.focus));
      const classes = ["ulg-edge", `${relationEvidence(e.relation)}-edge`];
      if (state.focus) classes.push(related ? "related" : "muted");
      if (related) classes.push(e.target === state.focus ? "incoming" : "outgoing");
      const w=state.view === "functor" ? 300 : 220, cy=state.view === "functor" ? 50 : 31;
      const forward=b.x >= a.x;
      const startX=a.x+(forward?w:0), endX=b.x+(forward?0:w), bend=forward?50:-50;
      const path=svgEl("path", {
        d:`M ${startX} ${a.y+cy} C ${startX+bend} ${a.y+cy}, ${endX-bend} ${b.y+cy}, ${endX} ${b.y+cy}`,
        class: classes.join(" "),
        "data-relation":e.relation,
        "data-evidence":relationEvidence(e.relation),
        "marker-end":related ? "url(#ulg-arrow-focus)" : "url(#ulg-arrow)"
      });
      const title=svgEl("title"); title.textContent=`${e.relation} · ${relationEvidence(e.relation) === "formal" ? "Lean structural edge" : "curated evidence overlay"}`; path.append(title); edgeLayer.append(path);
    });
    [...ids].map(id=>nodes.get(id)).sort((a,b)=>((Number(a.column)||kindOrder[a.kind])-(Number(b.column)||kindOrder[b.kind]))||a.label.localeCompare(b.label)).forEach(n => {
      const p=positions.get(n.id); const classes=["ulg-node"];
      if (state.focus === n.id) classes.push("selected");
      else if (state.focus && focusNeighbors.has(n.id)) classes.push("related");
      else if (state.focus) classes.push("muted");
      const group=svgEl("g", {class:classes.join(" "), transform:`translate(${p.x} ${p.y})`, tabindex:"0", role:"button", "data-id":n.id});
      const conceptual=state.view === "functor";
      group.append(svgEl("rect", {width:conceptual?"300":"220",height:conceptual?"100":"62",rx:"12"}), svgEl("circle", {cx:"17",cy:"17",r:"5",class:`status ${n.status||"planned"}`}));
      if(state.color === "library") {
        const key=n.scope_key||"unassigned", palette=graph.library_scope_metadata?.palette||{}, colour=palette[key]?.color||"#747D89";
        group.setAttribute("data-scope",key);
        const box=group.querySelector("rect"); box.style.stroke=colour;box.style.strokeWidth="3";
        group.append(svgEl("rect",{x:conceptual?"288":"208",y:"9",width:"5",height:conceptual?"82":"44",rx:"2",style:`fill:${colour};stroke:none`}));
      }
      const kind=svgEl("text", {x:"30",y:"20",class:"kind"}); kind.textContent=kindLabel[n.kind]||n.kind; group.append(kind);
      const displayLabel=state.query && ["module","declaration"].includes(n.kind) ? n.label.split('.').slice(n.kind==="module"?-2:-1).join('.') : n.label;
      const label=svgEl("text", {x:"14",y:conceptual?"52":"40",class:"label"}); wrap(conceptual?(atlasLabels[n.id]||n.label):displayLabel,state.query&&!conceptual?20:24).forEach((line,i)=>{ const t=svgEl("tspan",{x:"14",dy:i?(conceptual?"26":"15"):"0"}); t.textContent=line; label.append(t); }); group.append(label);
      const title=svgEl("title"); title.textContent=`${n.label}\n${n.subtitle||""}\nScope: ${(n.library_scope||[]).join(", ")||"not audited"}\n${n.scope_basis||""}`; group.append(title);
      const choose=()=>selectNode(n.id,true); group.addEventListener("pointerdown",ev=>ev.stopPropagation()); group.addEventListener("click",choose); group.addEventListener("keydown",ev=>{if(ev.key==="Enter"||ev.key===" "){ev.preventDefault();choose();}}); nodeLayer.append(group);
    });
    count.textContent=`${ids.size} nodes · ${edges.length} edges${state.focus ? ` · ${directEdges.length} direct relations highlighted` : ""}`; empty.hidden=ids.size>0; applyTransform();
  }

  function linkButton(url,label,primary=false) { return url ? `<a class="${primary?"primary":""}" href="${esc(url)}">${esc(label)} <span>↗</span></a>` : ""; }
  function clearFocus() {
    state.focus="";
    state.expanded.clear();
    try { const url=new URL(location.href); url.searchParams.delete("focus"); url.searchParams.set("view",state.view); history.replaceState(null,"",url); } catch (_) {}
    detail.innerHTML='<div class="ulg-placeholder"><span>Branch inspector</span><h2>Select a node.</h2><p>Source statement, blind reconstruction, semantic deltas, repair proposals, exact Lean leaves, prerequisites, consumers, and reader links appear here.</p></div>';
    render();
  }

  function semanticSections(n) {
    const verdict=n.fidelity_verdict?`<section class="ulg-semantic-verdict"><h3>Fidelity verdict</h3><div class="ulg-verdict"><strong>${esc(n.fidelity_verdict)}</strong><span>${esc(n.blindness||"")}</span></div></section>`:"";
    const original=n.original_theorem?`<section><h3>Original theorem contract</h3><blockquote class="ulg-theorem-text">${esc(n.original_theorem)}</blockquote></section>`:"";
    const reconstructed=n.reconstructed_theorem?`<section><h3>Blind reconstructed theorem</h3><div class="ulg-blind-badge">Source text hidden from decoder</div><blockquote class="ulg-theorem-text">${esc(n.reconstructed_theorem)}</blockquote></section>`:"";
    const repaired=n.repaired_theorem?`<section><h3>Proposed reconstructed theorem</h3><blockquote class="ulg-theorem-text repair">${esc(n.repaired_theorem)}</blockquote><p class="ulg-warning">This proposal remains separate from the pinned source theorem until independent source review accepts it.</p></section>`:"";
    const slots=(n.semantic_slots||[]).length?`<section><h3>Seven-slot semantic diff</h3><div class="ulg-semantic-table-wrap"><table class="ulg-semantic-table"><thead><tr><th>Slot</th><th>Original</th><th>Reconstructed</th><th>Relation</th></tr></thead><tbody>${n.semantic_slots.map(row=>`<tr><th>${esc(row.slot)}</th><td>${esc(row.original)}</td><td>${esc(row.reconstructed)}</td><td><b data-relation="${esc(row.relation)}">${esc(row.relation)}</b>${row.evidence?`<small>${esc(row.evidence)}</small>`:""}</td></tr>`).join("")}</tbody></table></div></section>`:"";
    const deltas=(n.semantic_deltas||[]).length?`<section><h3>Semantic deltas</h3><ol class="ulg-deltas">${n.semantic_deltas.map(row=>`<li data-severity="${esc(row.severity||"review")}"><span>${esc(row.slot||"semantic contract")} · ${esc(row.severity||"review")}</span><strong>${esc(row.description||"")}</strong><p>${esc(row.evidence||"")}</p></li>`).join("")}</ol></section>`:"";
    const repairs=(n.repair_proposals||[]).length?`<section><h3>Lean theorem denoising proposals</h3><div class="ulg-repairs">${n.repair_proposals.map(row=>`<article><header><span>${esc(row.class||"repair")}</span><b>${esc(row.status||"proposed")}</b></header><strong>${esc(row.proposed_change||"")}</strong><p>${esc(row.justification||"")}</p><dl><div><dt>Necessity</dt><dd>${esc(row.necessity||"uncertain")}</dd></div><div><dt>Minimality</dt><dd>${esc(row.minimality_evidence||"not established")}</dd></div></dl><small>Never mutates the source theorem automatically.</small></article>`).join("")}</div></section>`:"";
    return verdict+original+reconstructed+repaired+slots+deltas+repairs;
  }

  function functorSections(n) {
    if (!n.hyperedge) return "";
    const h=n.hyperedge;
    const names=ids=>ids.map(id=>nodes.get(id)?.label||id).join(" + ");
    const sources=(n.sources||[]).map(s=>`<p>${linkButton(s.url,s.title)}<small>${esc(s.anchor)}</small></p>`).join("");
    const families=(h.family_ids||[]).length?`<p><strong>Conceptual families:</strong> ${esc(h.family_ids.join(" · "))}</p>`:"";
    return `<section class="ulg-hyperedge"><h3>Joint-input hyperedge</h3>${families}<p><strong>ALL inputs:</strong> ${esc(names(h.tails))}</p><p><strong>Conditional outputs:</strong> ${esc(names(h.heads))}</p><p><strong>Type:</strong> ${esc(h.relation_kind)}</p><p class="ulg-warning">${esc(h.status)}. These incidence lines are not separate logical implications; candidate Lean substrates are search locations, not transport certificates.</p><h3>Primary source evidence</h3>${sources}</section>`;
  }

  function selectNode(id, expand=false) {
    if (!nodes.has(id)) return; if(state.view === "functor" && !viewKinds.functor.has(nodes.get(id).kind)) setView("lean"); state.focus=id; if(expand) state.expanded.add(id); const n=nodes.get(id);
    try { const url=new URL(location.href); url.searchParams.set("focus",id); url.searchParams.set("view",state.view); history.replaceState(null,"",url); } catch (_) {}
    const incoming=(incident.get(id)||[]).filter(e=>e.target===id).map(e=>nodes.get(e.source)).filter(Boolean); const outgoing=(incident.get(id)||[]).filter(e=>e.source===id).map(e=>nodes.get(e.target)).filter(Boolean);
    const scope=(n.library_scope||[]).length?`<section class="ulg-scope-note"><h3>Library scope · not proof status</h3><p>${n.library_scope.map(k=>`<span>${esc(graph.library_scope_metadata?.palette[k]?.label||k)}</span>`).join(' · ')}</p><small>${esc(n.scope_basis||'Curated source affiliation or planned reuse.')}</small></section>`:'';
    const formula=n.formula?`<div class="ulg-formula">\\[${esc(n.formula)}\\]</div>`:"";
    const equations=(n.proof_equations||[]).length?`<section><h3>Key proof equations</h3><ol class="ulg-equations">${n.proof_equations.map(row=>`<li><div>\\[${esc(row.formula)}\\]</div><p>${esc(row.meaning)}</p></li>`).join("")}</ol></section>`:"";
    const rows=(n.details||[]).filter(row=>row.value).map(row=>`<div><dt>${esc(row.label)}</dt><dd>${esc(row.value)}</dd></div>`).join("");
    const branch=(title,list)=>list.length?`<section><h3>${title}</h3><div class="ulg-neighbors">${list.slice(0,24).map(item=>`<button data-jump="${esc(item.id)}"><span>${esc(kindLabel[item.kind]||item.kind)}</span>${esc(item.label)}</button>`).join("")}</div></section>`:"";
    detail.innerHTML=`<header><span>${esc(kindLabel[n.kind]||n.kind)}</span><i class="${esc(n.status||"planned")}">${esc(n.status||"planned")}</i><h2>${esc(n.label)}</h2><p>${esc(n.subtitle||n.summary||"")}</p></header>${n.theorem?`<section><h3>Primary source theorem</h3><strong>${esc(n.theorem)}</strong>${formula}<p>${esc(n.source_proof||"")}</p></section>`:formula}${scope}${semanticSections(n)}${functorSections(n)}${equations}${rows?`<dl class="ulg-details">${rows}</dl>`:""}<div class="ulg-links">${linkButton(n.url,"Open reader / evidence card",true)}${linkButton(n.source_url,"Open primary source")}</div>${branch(n.hyperedge?"Joint inputs / candidate substrates":state.view==="perspectives"?"Incoming taxonomy / scope relations":"Immediate prerequisites",incoming)}${branch(n.hyperedge?"Conditional outputs":state.view==="perspectives"?"Conditional applicability / reader lenses":"Immediate consumers",outgoing)}`;
    detail.querySelectorAll("[data-jump]").forEach(button=>button.addEventListener("click",()=>selectNode(button.dataset.jump,true)));
    if (window.MathJax?.typesetPromise) window.MathJax.typesetPromise([detail]).catch(()=>{}); render();
  }

  function setView(view) { try { const url=new URL(location.href); url.searchParams.set("view",view); url.searchParams.delete("focus"); if(!state.query)url.searchParams.delete("q"); history.replaceState(null,"",url); } catch (_) {} state.view=view; if(view==="perspectives")state.color="library"; state.focus=""; state.expanded.clear(); buttons.forEach(b=>b.classList.toggle("active",b.dataset.view===view)); render(); requestAnimationFrame(fit); }
  if(colorSelect)colorSelect.addEventListener('change',()=>{state.color=colorSelect.value==='library'?'library':'status';try{const u=new URL(location.href);u.searchParams.set('color',state.color);history.replaceState(null,'',u);}catch(_){}render();});
  buttons.forEach(button=>button.addEventListener("click",()=>setView(button.dataset.view)));
  document.querySelectorAll("[data-functor-jump]").forEach(button=>button.addEventListener("click",()=>{if(!nodes)return; setView("functor"); selectNode(button.dataset.functorJump,true); requestAnimationFrame(fit);}));
  search.addEventListener("input",()=>{state.query=search.value.trim(); state.focus=""; state.expanded.clear(); try{const u=new URL(location.href);u.searchParams.delete("focus");if(state.query)u.searchParams.set("q",state.query);else u.searchParams.delete("q");history.replaceState(null,"",u);}catch(_){} render(); requestAnimationFrame(fit);});
  document.querySelector("[data-graph-fit]").addEventListener("click",fit);
  document.querySelector("[data-graph-reset]").addEventListener("click",()=>{search.value="";state.query="";state.focus="";state.expanded.clear();setView("overview");});
  canvas.addEventListener("keydown",ev=>{if(ev.key==="Escape"&&state.focus){ev.preventDefault();clearFocus();}});
  svg.addEventListener("wheel",ev=>{ev.preventDefault(); const rect=svg.getBoundingClientRect(), px=ev.clientX-rect.left, py=ev.clientY-rect.top, old=state.scale, next=Math.max(.18,Math.min(2.4,old*Math.exp(-ev.deltaY*.001))); state.x=px-(px-state.x)*(next/old);state.y=py-(py-state.y)*(next/old);state.scale=next;applyTransform();},{passive:false});
  svg.addEventListener("pointerdown",ev=>{state.drag={x:ev.clientX,y:ev.clientY,tx:state.x,ty:state.y};svg.setPointerCapture(ev.pointerId);canvas.classList.add("dragging");});
  svg.addEventListener("pointermove",ev=>{if(!state.drag)return;state.x=state.drag.tx+ev.clientX-state.drag.x;state.y=state.drag.ty+ev.clientY-state.drag.y;applyTransform();});
  const stop=()=>{state.drag=null;canvas.classList.remove("dragging");}; svg.addEventListener("pointerup",stop);svg.addEventListener("pointercancel",stop);

  fetch(host.dataset.graphSource).then(r=>{if(!r.ok)throw new Error(`graph data ${r.status}`);return r.json();}).then(data=>{
    graph=data; nodes=new Map(data.nodes.map(n=>[n.id,n])); incident=new Map(data.nodes.map(n=>[n.id,[]])); data.edges.forEach(e=>{if(incident.has(e.source))incident.get(e.source).push(e);if(incident.has(e.target))incident.get(e.target).push(e);}); degree=new Map([...incident].map(([id,list])=>[id,list.length]));
    const params=new URLSearchParams(location.search); const requested=params.get("view"); if(viewKinds[requested])state.view=requested; state.color=params.get("color")==="library"||state.view==="perspectives"?"library":"status";
    state.query=(params.get("q")||"").trim(); search.value=state.query;
    const focus=params.get("focus"); buttons.forEach(b=>b.classList.toggle("active",b.dataset.view===state.view)); render(); requestAnimationFrame(()=>{if(focus&&nodes.has(focus))selectNode(focus,true);fit();});
  }).catch(error=>{empty.hidden=false;empty.textContent=`The formal graph could not be loaded: ${error.message}`;console.error(error);});
})();
