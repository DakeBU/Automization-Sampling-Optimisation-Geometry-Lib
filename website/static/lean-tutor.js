(function () {
  "use strict";

  const studios = [...document.querySelectorAll("[data-lean-studio]")];
  if (!studios.length) return;

  const scriptUrl = document.currentScript?.src || "";
  const siteRoot = scriptUrl ? new URL("../", scriptUrl) : new URL("../", window.location.href);
  const dataUrl = new URL("data/site-data.json", siteRoot);

  const esc = (value) => String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");

  const syntaxRules = [
    { key: "theorem", re: /\btheorem\b/, explanation: "Declares a proposition to prove. The proposition follows `:`, and the proof follows `:= by`." },
    { key: "lemma", re: /\blemma\b/, explanation: "A proved proposition, usually a smaller reusable step for later theorems." },
    { key: "def", re: /\bdef\b/, explanation: "Defines a new object or function and records its construction." },
    { key: "structure", re: /\bstructure\b/, explanation: "Bundles fields and the properties they must satisfy into one mathematical object." },
    { key: "namespace", re: /\bnamespace\b/, explanation: "Enters a namespace so names from different mathematical modules do not collide." },
    { key: "variable", re: /\bvariable\b/, explanation: "Introduces variables and type assumptions shared by later declarations." },
    { key: "{…}", re: /\{[^}]*\}/, explanation: "Braces mark implicit parameters, which Lean usually infers from context." },
    { key: "[…]", re: /\[[^\]]*\]/, explanation: "Brackets usually mark typeclass assumptions; Lean searches automatically for suitable instances." },
    { key: "(…)", re: /\([^)]*\)/, explanation: "Parentheses usually mark explicit parameters supplied when the declaration is used." },
    { key: ":", re: /(^|\s):($|\s|[^=])/, explanation: "A colon reads as ‘has type’. In a theorem, the right-hand side is the proposition to prove." },
    { key: ":=", re: /:=/, explanation: "Defines the left-hand name by the term on the right. `:= by` starts a tactic proof." },
    { key: "→", re: /→|->/, explanation: "Function arrow; in propositions it is implication: if the left side holds, the right side follows." },
    { key: "↔", re: /↔|<->/, explanation: "If and only if. A proof normally establishes both directions." },
    { key: "∀", re: /∀/, explanation: "Universal quantifier: ‘for every’. `intro` commonly brings the arbitrary object into context." },
    { key: "∃", re: /∃/, explanation: "Existential quantifier. To prove it, provide a witness and prove the required property." },
    { key: "∧", re: /∧/, explanation: "Logical and. Proving `P ∧ Q` usually splits into two subgoals." },
    { key: "∨", re: /∨/, explanation: "Logical or. Prove one branch; when using it as a hypothesis, split into cases." },
    { key: "¬", re: /¬/, explanation: "Negation. Lean treats `¬ P` as `P → False`." },
    { key: "∈", re: /∈/, explanation: "Set membership, for example `x ∈ A`." },
    { key: "=", re: /(^|[^:<>])=([^>]|$)/, explanation: "Equality. Common tools include `rfl`, `rw`, `simp`, `calc`, or an existing equality." },
    { key: "≤/<", re: /≤|≥|<|>/, explanation: "Order relation, often handled by monotonicity lemmas, `linarith`, or `positivity`." },
    { key: "fun", re: /\bfun\b|↦/, explanation: "Anonymous function: `fun x => ...` is the Lean form of `x ↦ ...`." },
    { key: "by", re: /\bby\b/, explanation: "Starts a tactic proof, transforming the current goal step by step." },
    { key: "intro", re: /\bintro\b/, explanation: "Introduces a universally quantified object or implication hypothesis into the local context." },
    { key: "exact", re: /\bexact\b/, explanation: "Closes the goal by supplying a proof term whose type is exactly the goal." },
    { key: "apply", re: /\bapply\b/, explanation: "Uses a theorem backwards: match its conclusion to the goal, then turn its premises into subgoals." },
    { key: "refine", re: /\brefine\b/, explanation: "Provides part of a proof term and leaves `_` holes as new subgoals." },
    { key: "constructor", re: /\bconstructor\b/, explanation: "Applies a constructor, often splitting a conjunction or building a structure." },
    { key: "cases/rcases", re: /\b(?:cases|rcases)\b/, explanation: "Splits an object or hypothesis into its possible constructors/components." },
    { key: "have", re: /\bhave\b/, explanation: "Proves a local intermediate fact that can be reused later in the proof." },
    { key: "show", re: /\bshow\b/, explanation: "Restates the current goal in a definitionally equal, often clearer, form." },
    { key: "rw", re: /\brw\b/, explanation: "Rewrites using an equality in a chosen direction." },
    { key: "simp/simpa", re: /\b(?:simp|simpa)\b/, explanation: "Runs the simplifier using `[simp]` rules; `simpa` also tries to close the simplified goal." },
    { key: "rfl", re: /\brfl\b/, explanation: "Proves equality by definitional reflexivity: both sides reduce to the same term." },
    { key: "calc", re: /\bcalc\b/, explanation: "Writes a chain of equalities or inequalities in paper-style step-by-step form." },
    { key: "linarith/nlinarith", re: /\b(?:linarith|nlinarith)\b/, explanation: "Automatically combines linear/polynomial equalities and inequalities from the context." },
    { key: "positivity", re: /\bpositivity\b/, explanation: "Automatically proves many nonnegativity or positivity goals." },
    { key: "ext", re: /\bext\b/, explanation: "Uses extensionality to reduce equality of functions, sets, measures, etc. to pointwise/eventwise equality." },
    { key: "⟨…⟩", re: /⟨|⟩/, explanation: "Constructor notation, often used for existential witnesses, pairs, and structures." },
    { key: "_", re: /(^|\W)_(\W|$)/, explanation: "Placeholder: ask Lean to infer the term, or create a later subgoal under `refine`." },
    { key: "@", re: /@\w/, explanation: "Makes implicit arguments explicit for a declaration." },
    { key: "•", re: /•/, explanation: "Scalar action, for example real scalar multiplication of a vector." },
    { key: "^", re: /\^/, explanation: "Power. `x ^ 2` is a square; natural powers are handled generically by typeclasses." },
    { key: "∫/∫⁻", re: /∫|∫⁻/, explanation: "Integral notation; `∫⁻` is the ENNReal-valued lintegral, useful for nonnegative Tonelli/integrability arguments." },
    { key: "=ᵐ", re: /=ᵐ/, explanation: "Almost-everywhere equality under the indicated measure." },
    { key: "∀ᶠ", re: /∀ᶠ/, explanation: "Filter-eventually: the property holds eventually with respect to the given filter." },
    { key: "Tendsto", re: /\bTendsto\b/, explanation: "Lean's filter formulation of convergence from a source filter to a target neighborhood filter." },
    { key: "Measurable", re: /\b(?:Measurable|StronglyMeasurable|AEMeasurable)\b/, explanation: "Measurability interfaces required by random variables, integration, conditional expectation, and related operations." },
    { key: "Integrable", re: /\b(?:Integrable|MemLp)\b/, explanation: "Integrability/Lp conditions; Lean does not infer them merely because a paper formula looks integrable." },
    { key: "Continuous", re: /\b(?:Continuous|ContinuousOn)\b/, explanation: "Continuity interface; `ContinuousOn` only requires continuity on the specified set." }
  ];

  const actionRules = [
    [/\bintro\b/, "introduce a variable or hypothesis"],
    [/\bapply\b/, "reduce the goal to premises of an existing theorem"],
    [/\bexact\b/, "close the goal with an existing proof term"],
    [/\b(?:rw|simp|simpa)\b/, "rewrite or normalize the current goal"],
    [/\b(?:constructor|cases|rcases)\b/, "split or construct a logical/data structure"],
    [/\b(?:have|show)\b/, "establish an intermediate fact or restate the goal"],
    [/\bcalc\b/, "start a paper-style equality/inequality chain"],
    [/\b(?:theorem|lemma)\b/, "declare the mathematical proposition to be proved"],
    [/\bdef\b/, "define a mathematical object used later"],
    [/\bby\b/, "switch from the proposition to tactic proof mode"]
  ];

  function shortName(name) {
    return String(name || "").split(".").pop() || name;
  }

  function collectRegistryEntries(value, sink = []) {
    if (!value || typeof value !== "object") return sink;
    if (Array.isArray(value)) {
      value.forEach((item) => collectRegistryEntries(item, sink));
      return sink;
    }
    if (typeof value.local_decl === "string" && typeof value.card === "string") {
      sink.push(value);
    }
    Object.values(value).forEach((item) => collectRegistryEntries(item, sink));
    return sink;
  }

  function currentEntry(entries) {
    const path = decodeURIComponent(window.location.pathname).replace(/^\/+/, "");
    return entries.find((entry) => path.endsWith(String(entry.card || ""))) || null;
  }

  function syntaxForLine(line) {
    return syntaxRules.filter((rule) => rule.re.test(line));
  }

  function actionForLine(line) {
    for (const [re, label] of actionRules) {
      if (re.test(line)) return label;
    }
    return "Continue constructing the current proof term; read the leftmost keyword first and ask what information this line adds to the goal.";
  }

  function explainLine(line) {
    const trimmed = line.trim();
    if (!trimmed) return "Blank line used only to separate proof steps.";
    if (trimmed.startsWith("--") || trimmed.startsWith("/-")) {
      return "Comment for human readers; it is not part of the proof term.";
    }
    const action = actionForLine(trimmed);
    if (/\b(theorem|lemma)\b/.test(trimmed)) {
      const match = trimmed.match(/\b(?:theorem|lemma)\s+([^\s({:]+)/);
      const name = match ? match[1] : "this result";
      return `This starts the declaration \`${name}\`. Read the name, then the parameters, and treat the expression after the colon as the final proposition to prove.`;
    }
    if (/\bdef\b/.test(trimmed)) {
      return "This line defines an object. Ask which paper-level quantity, set, process, or operator it represents.";
    }
    return `Proof action on this line: ${action}.`;
  }

  function renderTutor(studio) {
    const code = document.querySelector(".theorem-layout article code.language-lean");
    const host = studio.querySelector("[data-lean-line-tutor]");
    const glossary = studio.querySelector("[data-lean-glossary]");
    if (!host || !glossary) return;
    if (!code) {
      host.innerHTML = `<p class="lean-tutor-empty">This page has no parseable Lean source block; open the exact declaration from the catalog.</p>`;
      glossary.innerHTML = "";
      return;
    }

    const lines = code.textContent.split("\n");
    const visibleLimit = 18;
    host.innerHTML = lines.map((line, index) => {
      const syntax = syntaxForLine(line);
      const chips = syntax.map((rule) => `<button type="button" class="syntax-chip" data-syntax-key="${esc(rule.key)}" title="${esc(rule.explanation)}">${esc(rule.key)}</button>`).join("");
      return `<article class="lean-line-explanation${index >= visibleLimit ? " lean-line-extra" : ""}" ${index >= visibleLimit ? "hidden" : ""}>
        <div class="lean-line-number">${index + 1}</div>
        <pre><code>${esc(line || " ")}</code></pre>
        <div class="lean-line-natural"><p>${esc(explainLine(line))}</p><div class="syntax-chips">${chips}</div></div>
      </article>`;
    }).join("");

    if (lines.length > visibleLimit) {
      const more = document.createElement("button");
      more.type = "button";
      more.className = "button lean-show-all";
      more.textContent = `Show explanations for all ${lines.length} lines`;
      more.addEventListener("click", () => {
        host.querySelectorAll(".lean-line-extra").forEach((node) => { node.hidden = false; });
        more.remove();
      });
      host.appendChild(more);
    }

    const present = syntaxRules.filter((rule) => lines.some((line) => rule.re.test(line)));
    glossary.innerHTML = present.map((rule) => `<details class="lean-syntax-entry"><summary><code>${esc(rule.key)}</code></summary><p>${esc(rule.explanation)}</p></details>`).join("");
  }

  function graphHref(entry) {
    return entry?.card ? new URL(String(entry.card), siteRoot).href : "#";
  }

  function svgNode(x, y, width, height, entry, kind, current) {
    const label = shortName(entry?.local_decl || entry?.name || "unmapped");
    const href = graphHref(entry);
    const cls = current ? "graph-node current" : `graph-node ${kind}`;
    const safeLabel = label.length > 28 ? `${label.slice(0, 25)}…` : label;
    return `<a href="${esc(href)}" class="${cls}">
      <rect x="${x}" y="${y}" width="${width}" height="${height}" rx="12" ry="12"></rect>
      <text x="${x + width / 2}" y="${y + height / 2 - 4}" text-anchor="middle">${esc(safeLabel)}</text>
      <text class="graph-node-kind" x="${x + width / 2}" y="${y + height / 2 + 16}" text-anchor="middle">${esc(current ? "current theorem" : kind)}</text>
    </a>`;
  }

  function renderGraph(studio, entries, entry, mode) {
    const host = studio.querySelector("[data-lean-graph-canvas]");
    if (!host) return;
    if (!entry) {
      host.innerHTML = `<div class="note">This declaration is not currently a Registry theorem leaf, so no dependency edges are invented here. Its exact source remains available in the declaration catalog.</div>`;
      return;
    }
    const byName = new Map(entries.map((item) => [String(item.local_decl || ""), item]));
    const deps = (entry.dependencies || []).map((name) => byName.get(String(name))).filter(Boolean).slice(0, 8);
    const consumers = (entry.consumers || []).map((name) => byName.get(String(name))).filter(Boolean).slice(0, 8);
    const width = 960;
    const nodeW = 210;
    const nodeH = 60;
    const lines = [];
    const nodes = [];

    if (mode === "tree") {
      const levels = [deps, [entry], consumers];
      const ys = [30, 190, 350];
      levels.forEach((level, levelIndex) => {
        const count = Math.max(level.length, 1);
        const gap = (width - 40 - count * nodeW) / Math.max(count - 1, 1);
        level.forEach((item, i) => {
          const x = level.length === 1 ? (width - nodeW) / 2 : 20 + i * (nodeW + gap);
          nodes.push(svgNode(x, ys[levelIndex], nodeW, nodeH, item, levelIndex === 0 ? "prerequisite" : "consumer", levelIndex === 1));
          if (levelIndex === 0) lines.push(`<line x1="${x + nodeW / 2}" y1="${ys[0] + nodeH}" x2="${width / 2}" y2="${ys[1]}" />`);
          if (levelIndex === 2) lines.push(`<line x1="${width / 2}" y1="${ys[1] + nodeH}" x2="${x + nodeW / 2}" y2="${ys[2]}" />`);
        });
      });
      host.innerHTML = `<svg class="lean-proof-graph tree" viewBox="0 0 ${width} 440" role="img" aria-label="Lean proof dependency tree"><g class="graph-edges">${lines.join("")}</g>${nodes.join("")}</svg>`;
    } else {
      const centerX = (width - nodeW) / 2;
      const centerY = 200;
      const sideX = [35, width - 35 - nodeW];
      const sideGroups = [deps, consumers];
      sideGroups.forEach((group, side) => {
        const span = 340;
        const start = centerY + nodeH / 2 - ((Math.max(group.length, 1) - 1) * span / Math.max(group.length - 1, 1)) / 2;
        group.forEach((item, i) => {
          const yCenter = group.length === 1 ? centerY + nodeH / 2 : start + i * span / Math.max(group.length - 1, 1);
          const y = Math.max(15, Math.min(425 - nodeH, yCenter - nodeH / 2));
          nodes.push(svgNode(sideX[side], y, nodeW, nodeH, item, side === 0 ? "prerequisite" : "consumer", false));
          if (side === 0) lines.push(`<line x1="${sideX[0] + nodeW}" y1="${y + nodeH / 2}" x2="${centerX}" y2="${centerY + nodeH / 2}" />`);
          else lines.push(`<line x1="${centerX + nodeW}" y1="${centerY + nodeH / 2}" x2="${sideX[1]}" y2="${y + nodeH / 2}" />`);
        });
      });
      nodes.push(svgNode(centerX, centerY, nodeW, nodeH, entry, "current", true));
      host.innerHTML = `<svg class="lean-proof-graph network" viewBox="0 0 ${width} 500" role="img" aria-label="Lean local proof network"><g class="graph-edges">${lines.join("")}</g>${nodes.join("")}</svg>`;
    }

    const stats = studio.querySelector("[data-lean-graph-stats]");
    if (stats) {
      stats.textContent = `${deps.length} direct prerequisites · ${consumers.length} direct consumers. Edges come from ASTIS's conservative source dependency scan; hidden dependencies are not invented.`;
    }
  }

  function setReadingMode(mode) {
    const allowed = new Set(["beginner", "rigorous", "lean"]);
    const selected = allowed.has(mode) ? mode : "beginner";
    document.body.dataset.readingMode = selected;
    localStorage.setItem("samplinglib-reading-mode", selected);
    document.querySelectorAll("[data-reading-mode]").forEach((button) => {
      const active = button.dataset.readingMode === selected;
      button.classList.toggle("active", active);
      button.setAttribute("aria-pressed", String(active));
    });
    if (selected === "lean") {
      document.querySelectorAll("details.formalization-lens").forEach((details) => { details.open = true; });
    } else {
      document.querySelectorAll("details.formalization-lens").forEach((details) => { details.open = false; });
    }
  }

  async function bootStudio(studio) {
    const mode = localStorage.getItem("samplinglib-reading-mode") || "beginner";
    setReadingMode(mode);

    studio.querySelectorAll("[data-reading-mode]").forEach((button) => {
      button.addEventListener("click", () => setReadingMode(button.dataset.readingMode));
    });

    renderTutor(studio);

    let data;
    try {
      const response = await fetch(dataUrl);
      if (!response.ok) throw new Error(`site-data ${response.status}`);
      data = await response.json();
    } catch (error) {
      const host = studio.querySelector("[data-lean-graph-canvas]");
      if (host) host.innerHTML = `<div class="note">${esc(error.message)}</div>`;
      return;
    }

    const entries = collectRegistryEntries(data, []);
    const unique = [...new Map(entries.map((entry) => [String(entry.local_decl), entry])).values()];
    const entry = currentEntry(unique);
    let graphMode = "tree";
    const render = () => renderGraph(studio, unique, entry, graphMode);
    studio.querySelectorAll("[data-graph-mode]").forEach((button) => {
      button.addEventListener("click", () => {
        graphMode = button.dataset.graphMode === "network" ? "network" : "tree";
        studio.querySelectorAll("[data-graph-mode]").forEach((peer) => {
          const active = peer.dataset.graphMode === graphMode;
          peer.classList.toggle("active", active);
          peer.setAttribute("aria-pressed", String(active));
        });
        render();
      });
    });
    render();
  }

  studios.forEach((studio) => bootStudio(studio));
})();
