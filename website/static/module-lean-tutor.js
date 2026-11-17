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
    ["theorem/lemma", /\b(?:theorem|lemma)\b/, "Declares a proposition. Read the hypotheses, then the conclusion after the colon."],
    ["def", /\bdef\b/, "Defines a mathematical object or function."],
    ["{…}", /\{[^}]*\}/, "Braces mark implicit parameters that Lean usually infers."],
    ["[…]", /\[[^\]]*\]/, "Brackets mark typeclass assumptions, such as a measurable or normed space."],
    ["(…)", /\([^)]*\)/, "Parentheses usually mark explicit parameters."],
    ["→", /→|->/, "Function arrow; in a proposition, read it as implication."],
    ["↔", /↔|<->/, "If and only if. Prove both directions."],
    ["∀", /∀/, "Universal quantifier: for every object in the indicated type."],
    ["∃", /∃/, "Existential quantifier: give a witness and prove its property."],
    ["by", /\bby\b/, "Starts a tactic proof."],
    ["intro", /\bintro\b/, "Introduces an arbitrary object or an implication hypothesis."],
    ["apply", /\bapply\b/, "Applies an existing result backwards, turning its premises into subgoals."],
    ["exact", /\bexact\b/, "Supplies a term that proves the current goal."],
    ["have", /\bhave\b/, "Proves a local intermediate fact for later use."],
    ["rw", /\brw\b/, "Rewrites the goal or a hypothesis using an equality."],
    ["simp/simpa", /\b(?:simp|simpa)\b/, "Applies simplification rules. `simpa` also tries to close the simplified goal."],
    ["calc", /\bcalc\b/, "Writes a chain of equalities or inequalities."],
    ["rfl", /\brfl\b/, "Proves equality when both sides reduce to the same term."],
    ["∫ / ∫⁻", /∫|∫⁻/, "`∫⁻` is the nonnegative extended-real integral, used in Tonelli arguments."],
    ["=ᵐ", /=ᵐ/, "Equality almost everywhere with respect to the indicated measure."],
    ["Tendsto", /\bTendsto\b/, "Expresses convergence via filters."],
    ["Measurable", /\b(?:Measurable|StronglyMeasurable|AEMeasurable)\b/, "Measurability is a hypothesis, not a consequence of writing an integral."],
    ["Integrable / MemLp", /\b(?:Integrable|MemLp)\b/, "These express integrability or an Lp condition; check the measure and exponent."],
    ["Continuous", /\b(?:Continuous|ContinuousOn)\b/, "`ContinuousOn` requires continuity on the specified set."]
  ];

  function lineAction(line) {
    const t = line.trim();
    if (!t) return "Blank line between proof steps.";
    if (/^--|^\/-/.test(t)) return "Comment for the reader; it is not part of the proof term.";
    if (/\b(?:theorem|lemma)\b/.test(t)) return "Read the declaration as a mathematical sentence: identify its name, objects, assumptions, and conclusion.";
    if (/\bdef\b/.test(t)) return "Identifies an object that will be used in the argument.";
    if (/\bintro\b/.test(t)) return "Introduce an arbitrary object or an implication hypothesis.";
    if (/\bapply\b/.test(t)) return "Use a known result backwards: prove the remaining premises.";
    if (/\bexact\b/.test(t)) return "Supply an existing proof term that matches the goal.";
    if (/\b(?:rw|simp|simpa)\b/.test(t)) return "Rewrite the goal, or simplify it using known rules.";
    if (/\b(?:constructor|cases|rcases)\b/.test(t)) return "Split into cases or build the result using a constructor.";
    if (/\bhave\b/.test(t)) return "Prove an intermediate fact before returning to the main goal.";
    if (/\bcalc\b/.test(t)) return "Start a chain of equalities or inequalities.";
    if (/\bby\b/.test(t)) return "Start the tactic proof after the statement.";
    return "Ask whether this line introduces information, rewrites the goal, applies a result, or constructs a witness.";
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
      <summary>Read this declaration line by line</summary>
      <div class="module-tutor-body">
        <div class="note"><strong>Read the mathematics first.</strong> <code>${esc(name)}</code> is the exact Lean declaration in this module. The guide explains the syntax used here without changing what the declaration says.</div>
        <div class="module-tutor-route">
          <div><strong>1. Name</strong><span>${esc(name.split(".").pop())}</span></div>
          <div><strong>2. Parameters and structures</strong><span>Parentheses mark explicit objects. Lean usually infers parameters in braces and uses typeclass search for brackets.</span></div>
          <div><strong>3. Statement</strong><span>For a theorem or lemma, read the proposition after the colon. For a definition, read the construction on the right.</span></div>
          <div><strong>4. Proof</strong><span>After <code>by</code>, identify which mathematical step each tactic implements.</span></div>
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
