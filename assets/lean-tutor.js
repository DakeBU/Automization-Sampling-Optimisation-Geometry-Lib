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
    { key: "theorem", re: /\btheorem\b/, zh: "声明一个需要证明的命题。冒号后面是命题，`:= by` 后面给出证明。", en: "Declares a proposition to prove. The proposition follows `:`, and the proof follows `:= by`." },
    { key: "lemma", re: /\blemma\b/, zh: "和 theorem 一样是已证明命题；通常表示被后续定理复用的较小步骤。", en: "A proved proposition, usually a smaller reusable step for later theorems." },
    { key: "def", re: /\bdef\b/, zh: "定义一个新对象或函数；Lean 会记住右侧给出的构造。", en: "Defines a new object or function and records its construction." },
    { key: "structure", re: /\bstructure\b/, zh: "把若干字段和它们必须满足的性质打包成一个数学对象。", en: "Bundles fields and the properties they must satisfy into one mathematical object." },
    { key: "namespace", re: /\bnamespace\b/, zh: "进入命名空间，避免不同数学模块里的名字互相冲突。", en: "Enters a namespace so names from different mathematical modules do not collide." },
    { key: "variable", re: /\bvariable\b/, zh: "预先声明后面若干定理会共同使用的变量和类型假设。", en: "Introduces variables and type assumptions shared by later declarations." },
    { key: "{…}", re: /\{[^}]*\}/, zh: "花括号参数是 implicit parameter：通常可由上下文推断，所以调用定理时常不用手写。", en: "Braces mark implicit parameters, which Lean usually infers from context." },
    { key: "[…]", re: /\[[^\]]*\]/, zh: "方括号通常是 typeclass 假设，例如 measurable space、normed space；Lean 会自动搜索可用实例。", en: "Brackets usually mark typeclass assumptions; Lean searches automatically for suitable instances." },
    { key: "(…)", re: /\([^)]*\)/, zh: "圆括号通常是显式参数：使用这个定理或定义时，需要提供或让 elaborator 明确得到它。", en: "Parentheses usually mark explicit parameters supplied when the declaration is used." },
    { key: ":", re: /(^|\s):($|\s|[^=])/, zh: "冒号读作“具有类型/命题”。在 theorem 中，冒号右边就是要证明的数学命题。", en: "A colon reads as ‘has type’. In a theorem, the right-hand side is the proposition to prove." },
    { key: ":=", re: /:=/, zh: "把左边的名字定义为右边的项。`:= by` 表示右边将用 tactic 构造证明。", en: "Defines the left-hand name by the term on the right. `:= by` starts a tactic proof." },
    { key: "→", re: /→|->/, zh: "函数箭头；在命题里也就是蕴含：“如果左边成立，那么右边成立”。", en: "Function arrow; in propositions it is implication: if the left side holds, the right side follows." },
    { key: "↔", re: /↔|<->/, zh: "当且仅当。证明它通常需要分别证明两个方向。", en: "If and only if. A proof normally establishes both directions." },
    { key: "∀", re: /∀/, zh: "全称量词：“对所有……”。证明时常用 `intro` 把任意对象放进上下文。", en: "Universal quantifier: ‘for every’. `intro` commonly brings the arbitrary object into context." },
    { key: "∃", re: /∃/, zh: "存在量词：“存在……”。证明时需要给出 witness，再证明它满足性质。", en: "Existential quantifier. To prove it, provide a witness and prove the required property." },
    { key: "∧", re: /∧/, zh: "逻辑且。证明目标 `P ∧ Q` 时通常拆成两个子目标。", en: "Logical and. Proving `P ∧ Q` usually splits into two subgoals." },
    { key: "∨", re: /∨/, zh: "逻辑或。证明时选择一个分支；使用假设时通常分类讨论。", en: "Logical or. Prove one branch; when using it as a hypothesis, split into cases." },
    { key: "¬", re: /¬/, zh: "否定。Lean 把 `¬ P` 看成 `P → False`。", en: "Negation. Lean treats `¬ P` as `P → False`." },
    { key: "∈", re: /∈/, zh: "集合成员关系，例如 `x ∈ A`。", en: "Set membership, for example `x ∈ A`." },
    { key: "=", re: /(^|[^:<>])=([^>]|$)/, zh: "等式。可以用 `rfl`、`rw`、`simp`、`calc` 或已有等式来证明/改写。", en: "Equality. Common tools include `rfl`, `rw`, `simp`, `calc`, or an existing equality." },
    { key: "≤/<", re: /≤|≥|<|>/, zh: "序关系。很多分析证明会把它交给已有单调性 lemma、`linarith` 或 `positivity`。", en: "Order relation, often handled by monotonicity lemmas, `linarith`, or `positivity`." },
    { key: "fun", re: /\bfun\b|↦/, zh: "匿名函数；`fun x => ...` 就是数学里的 `x ↦ ...`。", en: "Anonymous function: `fun x => ...` is the Lean form of `x ↦ ...`." },
    { key: "by", re: /\bby\b/, zh: "进入 tactic proof：从当前目标出发，一步步把目标化简或交给已有定理。", en: "Starts a tactic proof, transforming the current goal step by step." },
    { key: "intro", re: /\bintro\b/, zh: "把 `∀ x` 或 `P → Q` 左边的任意对象/假设引入局部上下文。", en: "Introduces a universally quantified object or implication hypothesis into the local context." },
    { key: "exact", re: /\bexact\b/, zh: "直接给出一个类型恰好等于当前目标的证明项，从而关闭目标。", en: "Closes the goal by supplying a proof term whose type is exactly the goal." },
    { key: "apply", re: /\bapply\b/, zh: "反向使用一个定理：先把当前目标匹配到该定理的结论，再把它的前提变成新的子目标。", en: "Uses a theorem backwards: match its conclusion to the goal, then turn its premises into subgoals." },
    { key: "refine", re: /\brefine\b/, zh: "给出证明结构的一部分，并把 `_` 留成接下来要填的子目标。", en: "Provides part of a proof term and leaves `_` holes as new subgoals." },
    { key: "constructor", re: /\bconstructor\b/, zh: "使用当前归纳类型/逻辑连接词的构造器；常见于拆开 `∧` 或构造结构体。", en: "Applies a constructor, often splitting a conjunction or building a structure." },
    { key: "cases/rcases", re: /\b(?:cases|rcases)\b/, zh: "对假设或对象分类讨论，并把其构造结构拆开。", en: "Splits an object or hypothesis into its possible constructors/components." },
    { key: "have", re: /\bhave\b/, zh: "在主证明中先证明一个局部中间结论，之后可以像 lemma 一样复用。", en: "Proves a local intermediate fact that can be reused later in the proof." },
    { key: "show", re: /\bshow\b/, zh: "把当前目标用一个更易读但定义上等价的形式重新展示。", en: "Restates the current goal in a definitionally equal, often clearer, form." },
    { key: "rw", re: /\brw\b/, zh: "按给定等式进行定向重写；相当于把等号一侧替换成另一侧。", en: "Rewrites using an equality in a chosen direction." },
    { key: "simp/simpa", re: /\b(?:simp|simpa)\b/, zh: "调用 Lean 的简化器和 `[simp]` 规则做规范化；`simpa` 还会在简化后直接尝试关闭目标。", en: "Runs the simplifier using `[simp]` rules; `simpa` also tries to close the simplified goal." },
    { key: "rfl", re: /\brfl\b/, zh: "证明两边经过定义展开后完全相同，也就是 reflexivity。", en: "Proves equality by definitional reflexivity: both sides reduce to the same term." },
    { key: "calc", re: /\bcalc\b/, zh: "把一条长等式/不等式链写成纸面数学风格的逐步推导。", en: "Writes a chain of equalities or inequalities in paper-style step-by-step form." },
    { key: "linarith/nlinarith", re: /\b(?:linarith|nlinarith)\b/, zh: "把上下文中的线性/多项式等式不等式组合起来自动完成算术推理。", en: "Automatically combines linear/polynomial equalities and inequalities from the context." },
    { key: "positivity", re: /\bpositivity\b/, zh: "自动证明许多表达式的非负/正性目标。", en: "Automatically proves many nonnegativity or positivity goals." },
    { key: "ext", re: /\bext\b/, zh: "用 extensionality 把函数、集合、测度等对象的相等转化成逐点/逐事件相等。", en: "Uses extensionality to reduce equality of functions, sets, measures, etc. to pointwise/eventwise equality." },
    { key: "⟨…⟩", re: /⟨|⟩/, zh: "构造器记号。常用来同时给出存在量词的 witness 与证明，或构造 pair/structure。", en: "Constructor notation, often used for existential witnesses, pairs, and structures." },
    { key: "_", re: /(^|\W)_(\W|$)/, zh: "占位符：让 Lean 推断该项，或在 `refine` 中把它变成稍后要解决的子目标。", en: "Placeholder: ask Lean to infer the term, or create a later subgoal under `refine`." },
    { key: "@", re: /@\w/, zh: "关闭某个声明的隐式参数机制，让你显式提供原本会自动推断的参数。", en: "Makes implicit arguments explicit for a declaration." },
    { key: "•", re: /•/, zh: "scalar action，例如实数对向量的数乘。", en: "Scalar action, for example real scalar multiplication of a vector." },
    { key: "^", re: /\^/, zh: "幂。`x ^ 2` 是平方；自然数幂由类型类统一处理。", en: "Power. `x ^ 2` is a square; natural powers are handled generically by typeclasses." },
    { key: "∫/∫⁻", re: /∫|∫⁻/, zh: "积分记号；`∫⁻` 是 ENNReal-valued lintegral，特别适合先做非负函数的 Tonelli/可积性论证。", en: "Integral notation; `∫⁻` is the ENNReal-valued lintegral, useful for nonnegative Tonelli/integrability arguments." },
    { key: "=ᵐ", re: /=ᵐ/, zh: "almost-everywhere equality：两个函数只需在给定测度下几乎处处相等。", en: "Almost-everywhere equality under the indicated measure." },
    { key: "∀ᶠ", re: /∀ᶠ/, zh: "filter-eventually：“从某个阶段以后一直成立”或“在该滤子意义下最终成立”。", en: "Filter-eventually: the property holds eventually with respect to the given filter." },
    { key: "Tendsto", re: /\bTendsto\b/, zh: "Lean 的极限表达：一个函数把源 filter 映到目标邻域 filter。", en: "Lean's filter formulation of convergence from a source filter to a target neighborhood filter." },
    { key: "Measurable", re: /\b(?:Measurable|StronglyMeasurable|AEMeasurable)\b/, zh: "可测性接口；随机变量、积分、条件期望等后续操作都依赖这些条件。", en: "Measurability interfaces required by random variables, integration, conditional expectation, and related operations." },
    { key: "Integrable", re: /\b(?:Integrable|MemLp)\b/, zh: "可积性/Lp 条件；Lean 不会因为公式看起来可积就自动假设它。", en: "Integrability/Lp conditions; Lean does not infer them merely because a paper formula looks integrable." },
    { key: "Continuous", re: /\b(?:Continuous|ContinuousOn)\b/, zh: "连续性接口；注意 `ContinuousOn` 只在指定集合上要求连续。", en: "Continuity interface; `ContinuousOn` only requires continuity on the specified set." }
  ];

  const actionRules = [
    [/\bintro\b/, ["引入变量或假设", "introduce a variable or hypothesis"]],
    [/\bapply\b/, ["把目标反推成一个已有定理的前提", "reduce the goal to premises of an existing theorem"]],
    [/\bexact\b/, ["用现成证明项直接关闭目标", "close the goal with an existing proof term"]],
    [/\b(?:rw|simp|simpa)\b/, ["重写或规范化当前目标", "rewrite or normalize the current goal"]],
    [/\b(?:constructor|cases|rcases)\b/, ["拆分或构造逻辑/数据结构", "split or construct a logical/data structure"]],
    [/\b(?:have|show)\b/, ["建立一个中间命题或重述目标", "establish an intermediate fact or restate the goal"]],
    [/\bcalc\b/, ["开始纸面风格的等式/不等式推导链", "start a paper-style equality/inequality chain"]],
    [/\b(?:theorem|lemma)\b/, ["声明本行之后要证明的数学命题", "declare the mathematical proposition to be proved"]],
    [/\bdef\b/, ["定义后续证明会使用的数学对象", "define a mathematical object used later"]],
    [/\bby\b/, ["从命题陈述切换到 tactic proof", "switch from the proposition to tactic proof mode"]]
  ];

  function currentLanguage() {
    const saved = localStorage.getItem("samplinglib-lean-language");
    if (saved === "zh" || saved === "en") return saved;
    return navigator.language?.toLowerCase().startsWith("zh") ? "zh" : "en";
  }

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

  function actionForLine(line, lang) {
    for (const [re, labels] of actionRules) {
      if (re.test(line)) return labels[lang === "zh" ? 0 : 1];
    }
    return lang === "zh"
      ? "继续构造当前证明项；先看最左侧关键字，再检查这一行给目标增加了什么信息。"
      : "Continue constructing the current proof term; read the leftmost keyword first and ask what information this line adds to the goal.";
  }

  function explainLine(line, lang) {
    const trimmed = line.trim();
    if (!trimmed) return lang === "zh" ? "空行：只用于把证明分成更易读的小段。" : "Blank line used only to separate proof steps.";
    if (trimmed.startsWith("--") || trimmed.startsWith("/-")) {
      return lang === "zh" ? "注释：给人看的说明，不参与 Lean 的逻辑证明项。" : "Comment for human readers; it is not part of the proof term.";
    }
    const action = actionForLine(trimmed, lang);
    if (/\b(theorem|lemma)\b/.test(trimmed)) {
      const match = trimmed.match(/\b(?:theorem|lemma)\s+([^\s({:]+)/);
      const name = match ? match[1] : "this result";
      return lang === "zh"
        ? `这里开始声明 \`${name}\`。先读名字，再读参数，最后把冒号右侧当成“本定理最终必须证明的命题”。`
        : `This starts the declaration \`${name}\`. Read the name, then the parameters, and treat the expression after the colon as the final proposition to prove.`;
    }
    if (/\bdef\b/.test(trimmed)) {
      return lang === "zh" ? "这一行定义一个对象。数学上先问：它对应纸面证明里的哪个量、集合、过程或算子？" : "This line defines an object. Ask which paper-level quantity, set, process, or operator it represents.";
    }
    return lang === "zh" ? `本行的证明动作：${action}。` : `Proof action on this line: ${action}.`;
  }

  function renderTutor(studio, lang) {
    const code = document.querySelector(".theorem-layout article code.language-lean");
    const host = studio.querySelector("[data-lean-line-tutor]");
    const glossary = studio.querySelector("[data-lean-glossary]");
    if (!host || !glossary) return;
    if (!code) {
      host.innerHTML = `<p class="lean-tutor-empty">${lang === "zh" ? "这个页面没有可解析的 Lean source block；可以从 declaration catalog 打开精确声明。" : "This page has no parseable Lean source block; open the exact declaration from the catalog."}</p>`;
      glossary.innerHTML = "";
      return;
    }

    const lines = code.textContent.split("\n");
    const visibleLimit = 18;
    host.innerHTML = lines.map((line, index) => {
      const syntax = syntaxForLine(line);
      const chips = syntax.map((rule) => `<button type="button" class="syntax-chip" data-syntax-key="${esc(rule.key)}" title="${esc(lang === "zh" ? rule.zh : rule.en)}">${esc(rule.key)}</button>`).join("");
      return `<article class="lean-line-explanation${index >= visibleLimit ? " lean-line-extra" : ""}" ${index >= visibleLimit ? "hidden" : ""}>
        <div class="lean-line-number">${index + 1}</div>
        <pre><code>${esc(line || " ")}</code></pre>
        <div class="lean-line-natural"><p>${esc(explainLine(line, lang))}</p><div class="syntax-chips">${chips}</div></div>
      </article>`;
    }).join("");

    if (lines.length > visibleLimit) {
      const more = document.createElement("button");
      more.type = "button";
      more.className = "button lean-show-all";
      more.textContent = lang === "zh" ? `展开全部 ${lines.length} 行解释` : `Show explanations for all ${lines.length} lines`;
      more.addEventListener("click", () => {
        host.querySelectorAll(".lean-line-extra").forEach((node) => { node.hidden = false; });
        more.remove();
      });
      host.appendChild(more);
    }

    const present = syntaxRules.filter((rule) => lines.some((line) => rule.re.test(line)));
    glossary.innerHTML = present.map((rule) => `<details class="lean-syntax-entry"><summary><code>${esc(rule.key)}</code></summary><p>${esc(lang === "zh" ? rule.zh : rule.en)}</p></details>`).join("");
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

  function renderGraph(studio, entries, entry, mode, lang) {
    const host = studio.querySelector("[data-lean-graph-canvas]");
    if (!host) return;
    if (!entry) {
      host.innerHTML = `<div class="note">${lang === "zh" ? "这个 declaration 目前不是 Registry theorem leaf，因此这里不伪造依赖边。你仍可在 declaration catalog 查看精确源码和模块位置。" : "This declaration is not currently a Registry theorem leaf, so no dependency edges are invented here. Its exact source remains available in the declaration catalog."}</div>`;
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
      host.innerHTML = `<svg class="lean-proof-graph tree" viewBox="0 0 ${width} 440" role="img" aria-label="${esc(lang === "zh" ? "Lean 证明依赖树" : "Lean proof dependency tree")}"><g class="graph-edges">${lines.join("")}</g>${nodes.join("")}</svg>`;
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
      host.innerHTML = `<svg class="lean-proof-graph network" viewBox="0 0 ${width} 500" role="img" aria-label="${esc(lang === "zh" ? "Lean 局部证明网络" : "Lean local proof network")}"><g class="graph-edges">${lines.join("")}</g>${nodes.join("")}</svg>`;
    }

    const stats = studio.querySelector("[data-lean-graph-stats]");
    if (stats) {
      stats.textContent = lang === "zh"
        ? `${deps.length} 个直接前置 lemma · ${consumers.length} 个直接下游 consumer。边来自 ASTIS 源码中的保守依赖扫描，不补造隐含依赖。`
        : `${deps.length} direct prerequisites · ${consumers.length} direct consumers. Edges come from ASTIS's conservative source dependency scan; hidden dependencies are not invented.`;
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
    const langButton = studio.querySelector("[data-lean-language-toggle]");
    let lang = currentLanguage();
    const mode = localStorage.getItem("samplinglib-reading-mode") || "beginner";
    setReadingMode(mode);

    studio.querySelectorAll("[data-reading-mode]").forEach((button) => {
      button.addEventListener("click", () => setReadingMode(button.dataset.readingMode));
    });

    const setLanguage = (next) => {
      lang = next;
      localStorage.setItem("samplinglib-lean-language", lang);
      if (langButton) langButton.textContent = lang === "zh" ? "English explanation" : "中文讲解";
      renderTutor(studio, lang);
    };
    langButton?.addEventListener("click", () => setLanguage(lang === "zh" ? "en" : "zh"));
    setLanguage(lang);

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
    const render = () => renderGraph(studio, unique, entry, graphMode, lang);
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
    langButton?.addEventListener("click", () => window.setTimeout(render, 0));
  }

  studios.forEach((studio) => bootStudio(studio));
})();
