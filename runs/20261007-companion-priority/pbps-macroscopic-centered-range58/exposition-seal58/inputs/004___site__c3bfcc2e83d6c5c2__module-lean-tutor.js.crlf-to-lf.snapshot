(function () {
  "use strict";

  const scriptUrl = document.currentScript?.src || "";
  if (scriptUrl && !document.querySelector('link[data-module-lean-tutor-style]')) {
    const style = document.createElement("link");
    style.rel = "stylesheet";
    style.href = new URL("module-lean-tutor.css", scriptUrl).href;
    style.dataset.moduleLeanTutorStyle = "true";
    document.head.appendChild(style);
  }

  const declarations = [...document.querySelectorAll("details.declaration")];
  if (!declarations.length) return;

  const esc = (value) => String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");

  const syntax = [
    ["theorem/lemma", /\b(?:theorem|lemma)\b/, "这里声明一个要被 Lean 检查的命题；冒号右侧是命题，证明通常从 `:= by` 开始。"],
    ["def", /\bdef\b/, "这里定义一个数学对象或函数，而不是证明一个命题。"],
    ["{…}", /\{[^}]*\}/, "隐式参数：通常由上下文推断，调用时往往不用显式填写。"],
    ["[…]", /\[[^\]]*\]/, "typeclass 假设：例如测度空间、拓扑、范数空间；Lean 会自动搜索实例。"],
    ["(…)", /\([^)]*\)/, "显式参数：对应纸面数学里明确给出的对象或假设。"],
    ["→", /→|->/, "蕴含或函数箭头。在命题里读作“如果左边成立，那么右边成立”。"],
    ["↔", /↔|<->/, "当且仅当，证明时通常要给两个方向。"],
    ["∀", /∀/, "全称量词“对任意”。证明时常用 `intro` 把任意对象放进上下文。"],
    ["∃", /∃/, "存在量词。证明时必须给 witness，并证明 witness 满足性质。"],
    ["by", /\bby\b/, "进入 tactic proof；从当前目标出发逐步构造证明项。"],
    ["intro", /\bintro\b/, "把任意变量或蕴含前提引入当前上下文。"],
    ["apply", /\bapply\b/, "反向使用已有定理：把当前目标化成该定理需要的前提。"],
    ["exact", /\bexact\b/, "直接给出类型恰好等于当前目标的证明项。"],
    ["have", /\bhave\b/, "先证明一个局部中间结论，之后重复使用。"],
    ["rw", /\brw\b/, "利用等式重写当前目标或假设。"],
    ["simp/simpa", /\b(?:simp|simpa)\b/, "使用简化规则把表达式规范化；`simpa` 还尝试直接关闭目标。"],
    ["calc", /\bcalc\b/, "按纸面数学风格写连续的等式或不等式推导。"],
    ["rfl", /\brfl\b/, "两边定义展开后相同，用自反性关闭等式。"],
    ["∫ / ∫⁻", /∫|∫⁻/, "积分；`∫⁻` 是非负扩展实值 lintegral，常用于 Tonelli 和可积性论证。"],
    ["=ᵐ", /=ᵐ/, "几乎处处相等；具体是相对于命题里写出的那个测度。"],
    ["Tendsto", /\bTendsto\b/, "用 filter 表达极限，是 Lean/Mathlib 分析里最常见的收敛接口。"],
    ["Measurable", /\b(?:Measurable|StronglyMeasurable|AEMeasurable)\b/, "可测性条件。Lean 会强迫纸面证明中常被省略的可测性前提显式出现。"],
    ["Integrable / MemLp", /\b(?:Integrable|MemLp)\b/, "可积性或 Lp 条件；公式写得出来不代表积分自动存在。"],
    ["Continuous", /\b(?:Continuous|ContinuousOn)\b/, "连续性条件；`ContinuousOn` 只要求在指定集合上连续。"]
  ];

  function lineAction(line) {
    const t = line.trim();
    if (!t) return "空行，只用于把证明分段。";
    if (/^--|^\/-/.test(t)) return "注释：只给读者看，不进入证明项。";
    if (/\b(?:theorem|lemma)\b/.test(t)) return "先把这一行读成一个完整数学句子：名字、任意对象、结构假设、显式假设、最后的结论。";
    if (/\bdef\b/.test(t)) return "这一行在定义纸面证明里会反复使用的对象。";
    if (/\bintro\b/.test(t)) return "证明动作：把“任意对象/若 P 则 Q”的左侧内容放进上下文。";
    if (/\bapply\b/.test(t)) return "证明动作：选择一个已有定理作为路线，把它的前提变成接下来要证明的子目标。";
    if (/\bexact\b/.test(t)) return "证明动作：当前目标已经和一个现成证明项完全匹配，因此直接关闭。";
    if (/\b(?:rw|simp|simpa)\b/.test(t)) return "证明动作：用等式或标准化规则把目标改写成更简单的等价形式。";
    if (/\b(?:constructor|cases|rcases)\b/.test(t)) return "证明动作：拆开逻辑结构/数据构造器，或选择相应构造器来组装目标。";
    if (/\bhave\b/.test(t)) return "证明动作：先建立一个局部中间 lemma，让主证明的逻辑更接近纸面推导。";
    if (/\bcalc\b/.test(t)) return "证明动作：开始一条逐步等式/不等式链。";
    if (/\bby\b/.test(t)) return "从 theorem statement 切换到 tactic proof。";
    return "继续构造当前证明项。先问：这行是在引入信息、重写目标、应用已有 lemma，还是构造最终 witness？";
  }

  function makeTutor(details) {
    if (details.querySelector("[data-module-lean-tutor]")) return;
    const name = details.querySelector("summary code")?.textContent?.trim() || "Lean declaration";
    const code = details.querySelector(".declaration-content pre code");
    if (!code) return;
    const source = code.textContent || "";
    const lines = source.split("\n");
    const usedSyntax = syntax.filter(([, re]) => re.test(source));
    const theoremLink = [...details.querySelectorAll("a")].find((a) => /(?:^|\/)theorems\//.test(a.getAttribute("href") || ""));

    const panel = document.createElement("details");
    panel.className = "module-lean-tutor-panel";
    panel.dataset.moduleLeanTutor = "true";
    panel.innerHTML = `
      <summary>Learn this declaration · Lean 逐行讲解</summary>
      <div class="module-tutor-body">
        <div class="note"><strong>先读数学，不背语法。</strong> <code>${esc(name)}</code> 是这个 module 里的精确 Lean 声明。下面只解释这段源码实际出现的语法；不会因为教学需要改变定理的正式含义。</div>
        <div class="module-tutor-route">
          <div><strong>① 名字</strong><span>${esc(name.split(".").pop())}</span></div>
          <div><strong>② 参数与结构</strong><span>圆括号是显式对象，花括号通常可推断，方括号通常由 typeclass search 提供。</span></div>
          <div><strong>③ 命题</strong><span>对 theorem/lemma，从冒号开始翻译成纸面数学；对 def，则读右侧构造。</span></div>
          <div><strong>④ 证明</strong><span><code>by</code> 之后每一行都应能翻译成一个数学证明动作。</span></div>
        </div>
        ${theoremLink
          ? `<p class="module-tutor-graph-link"><a class="button" href="${esc(theoremLink.getAttribute("href"))}">Open full proof tree / dependency network →</a></p>`
          : `<p class="muted"><strong>Dependency graph boundary.</strong> This helper does not currently have Registry-level theorem graph evidence, so Samplinglib shows its exact source and syntax but does not invent proof edges.</p>`}
        <h4>Line-by-line reading</h4>
        <div class="lean-line-tutor module-line-tutor">
          ${lines.slice(0, 16).map((line, i) => `
            <article class="lean-line-explanation">
              <div class="lean-line-number">${i + 1}</div>
              <pre><code>${esc(line || " ")}</code></pre>
              <div class="lean-line-natural"><p>${esc(lineAction(line))}</p></div>
            </article>`).join("")}
        </div>
        ${lines.length > 16 ? `<p class="muted">This compact module tutor explains the first 16 lines. Open a dedicated theorem card when available for the complete proof-learning view.</p>` : ""}
        <h4>Syntax actually used here</h4>
        <div class="lean-syntax-glossary">
          ${usedSyntax.map(([label, , explanation]) => `<details class="lean-syntax-entry"><summary><code>${esc(label)}</code></summary><p>${esc(explanation)}</p></details>`).join("") || '<p class="muted">No special syntax token from the beginner glossary was detected.</p>'}
        </div>
      </div>`;
    details.querySelector(".declaration-content")?.appendChild(panel);
  }

  declarations.forEach((details) => {
    details.addEventListener("toggle", () => {
      if (details.open) makeTutor(details);
    }, { once: true });
  });
})();
