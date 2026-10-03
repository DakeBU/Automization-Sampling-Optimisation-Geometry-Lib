(() => {
  "use strict";

  const app = document.querySelector("[data-live-app]");
  if (!app) return;

  const elements = {
    mapping: document.querySelector("[data-live-mapping]"),
    load: document.querySelector("[data-live-load]"),
    formalize: document.querySelector("[data-live-formalize]"),
    compile: document.querySelector("[data-live-compile]"),
    exportJson: document.querySelector("[data-live-export-json]"),
    exportMarkdown: document.querySelector("[data-live-export-markdown]"),
    latex: document.querySelector("[data-live-latex]"),
    context: document.querySelector("[data-live-context]"),
    sourceAnchor: document.querySelector("[data-live-source-anchor]"),
    preferredModule: document.querySelector("[data-live-preferred-module]"),
    preview: document.querySelector("[data-live-preview]"),
    lean: document.querySelector("[data-live-lean]"),
    diagnostics: document.querySelector("[data-live-diagnostics]"),
    local: document.querySelector("[data-live-local]"),
    mathlib: document.querySelector("[data-live-mathlib]"),
    assumptions: document.querySelector("[data-live-assumptions]"),
    obligations: document.querySelector("[data-live-obligations]"),
    semanticNotes: document.querySelector("[data-live-semantic-notes]"),
    mode: document.querySelector("[data-live-mode]"),
    modeTitle: document.querySelector("[data-live-mode-title]"),
    modeDetail: document.querySelector("[data-live-mode-detail]"),
    translation: document.querySelector("[data-status-translation]"),
    leanStatus: document.querySelector("[data-status-lean]"),
    proof: document.querySelector("[data-status-proof]"),
    review: document.querySelector("[data-status-review]"),
    duration: document.querySelector("[data-live-duration]"),
  };

  let mappings = [];
  let currentResult = null;
  let localMode = false;
  let compiledSource = "";
  let compilerAccepted = false;
  let semanticReviewed = false;

  const setStatus = (node, text, kind) => {
    if (!node) return;
    node.textContent = text;
    node.className = `status status-${kind}`;
  };

  const renderList = (node, values, empty) => {
    if (!node) return;
    node.replaceChildren();
    const items = Array.isArray(values) ? values : [];
    if (!items.length) {
      const item = document.createElement("li");
      item.className = "muted";
      item.textContent = empty;
      node.append(item);
      return;
    }
    items.forEach((value) => {
      const item = document.createElement("li");
      item.textContent = String(value);
      node.append(item);
    });
  };

  const typeset = async () => {
    if (!elements.preview) return;
    try {
      if (window.MathJax?.startup?.promise) await window.MathJax.startup.promise;
      window.MathJax?.typesetClear?.([elements.preview]);
      await window.MathJax?.typesetPromise?.([elements.preview]);
    } catch (error) {
      elements.preview.textContent = `MathJax preview error: ${error.message}`;
    }
  };

  const renderLatex = () => {
    const value = elements.latex?.value.trim() || "";
    elements.preview.textContent = value || "Enter a LaTeX statement to render it here.";
    typeset();
  };

  const resetAfterEdit = () => {
    currentResult = null;
    compilerAccepted = false;
    compiledSource = "";
    semanticReviewed = false;
    setStatus(elements.translation, "Unresolved", "gray");
    setStatus(elements.leanStatus, "Not compiled", "gray");
    setStatus(elements.proof, "Unproved", "orange");
    setStatus(elements.review, "Not reviewed", "gray");
  };

  const applyResult = (result, reviewed = false) => {
    currentResult = result;
    semanticReviewed = reviewed;
    if (result.lean_source) elements.lean.value = result.lean_source;
    renderList(elements.assumptions, result.assumptions, "No assumptions extracted.");
    renderList(elements.local, result.local_candidates, "No Samplinglib candidate retrieved.");
    renderList(elements.mathlib, result.mathlib_candidates, "No Mathlib candidate retrieved.");
    renderList(elements.obligations, result.remaining_proof_obligations, "No obligation recorded.");
    renderList(elements.semanticNotes, result.semantic_notes, "No semantic note recorded.");
    setStatus(
      elements.translation,
      reviewed ? "Reviewed mapping" : result.status === "candidate" ? "Candidate" : "Unresolved",
      reviewed ? "blue" : result.status === "candidate" ? "yellow" : "orange",
    );
    setStatus(elements.leanStatus, "Not compiled", "gray");
    setStatus(elements.proof, result.proof_status === "proved" ? "Compiled locally" : "Unproved", result.proof_status === "proved" ? "blue" : "orange");
    setStatus(elements.review, reviewed ? "Semantically reviewed" : "Not reviewed", reviewed ? "blue" : "gray");
    elements.diagnostics.textContent = reviewed
      ? "Reviewed mapping loaded. Local compilation is still a separate check."
      : result.status === "candidate"
        ? "Candidate translation generated. It is not semantically reviewed and its proposition is not proved."
        : "No deterministic translation template matched. Export the unresolved packet for ASTIS decomposition.";
    compilerAccepted = false;
    compiledSource = "";
  };

  const loadMapping = (mapping) => {
    if (!mapping) return;
    elements.latex.value = mapping.latex;
    elements.context.value = mapping.plain_language_interpretation || "";
    elements.sourceAnchor.value = mapping.source_anchor || "";
    elements.preferredModule.value = mapping.imports?.[0] || "";
    renderLatex();
    applyResult(mapping, true);
  };

  const formalize = async () => {
    if (!localMode) return;
    elements.formalize.disabled = true;
    elements.diagnostics.textContent = "ASTIS is extracting a candidate contract and retrieving local interfaces…";
    try {
      const response = await fetch("../api/formalize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          latex: elements.latex.value,
          natural_language_context: elements.context.value,
          source_anchor: elements.sourceAnchor.value,
          preferred_module: elements.preferredModule.value,
        }),
      });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.error || `HTTP ${response.status}`);
      applyResult(payload.result, false);
    } catch (error) {
      elements.diagnostics.textContent = `Formalization request failed: ${error.message}`;
      setStatus(elements.translation, "Unavailable", "red");
    } finally {
      elements.formalize.disabled = !localMode;
    }
  };

  const compile = async () => {
    if (!localMode || !elements.lean.value.trim()) return;
    elements.compile.disabled = true;
    elements.diagnostics.textContent = "Lean is checking a temporary snippet…";
    try {
      const response = await fetch("../api/compile", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code: elements.lean.value }),
      });
      const payload = await response.json();
      elements.diagnostics.textContent = payload.output || payload.error || "No diagnostics returned.";
      elements.duration.textContent = Number.isFinite(payload.duration_ms) ? `${payload.duration_ms} ms` : "";
      compilerAccepted = Boolean(payload.ok);
      compiledSource = compilerAccepted ? elements.lean.value : "";
      setStatus(elements.leanStatus, compilerAccepted ? "Compiles" : "Does not compile", compilerAccepted ? "blue" : "red");
      setStatus(elements.proof, "Unproved", "orange");
      setStatus(elements.review, semanticReviewed ? "Semantically reviewed" : "Not reviewed", semanticReviewed ? "blue" : "gray");
    } catch (error) {
      elements.diagnostics.textContent = `Local Lean service unavailable: ${error.message}`;
      setStatus(elements.leanStatus, "Unavailable", "red");
    } finally {
      elements.compile.disabled = !localMode;
    }
  };

  const packet = () => {
    const result = currentResult || {};
    const sourceCurrent = compilerAccepted && compiledSource === elements.lean.value;
    return {
      schema_version: "1.0",
      project: "Auto-Sampling-Theory-In-Sleep",
      library: "Samplinglib",
      original_latex: elements.latex.value,
      plain_language_interpretation: result.plain_language_interpretation || elements.context.value,
      source_anchor: elements.sourceAnchor.value,
      analytic_contract: {
        artifact: "analytic_contract",
        statement: result.plain_language_interpretation || elements.context.value,
        exact_assumptions: result.assumptions || [],
        measure: "explicit in candidate or unresolved",
        source: elements.sourceAnchor.value || "user submission",
        dependencies: result.remaining_proof_obligations || [],
      },
      formalization_map: {
        artifact: "formalization_map",
        lean_statement: result.lean_statement || "",
        lean_source: elements.lean.value,
        imports: result.imports || [],
        hypothesis_map: result.assumptions || [],
        local_samplinglib_candidates: result.local_candidates || [],
        mathlib_candidates: result.mathlib_candidates || [],
        rejected_candidates: result.rejected_candidates || [],
        statement_hash: result.statement_hash || "",
      },
      proof_attempt: {
        artifact: "proof_attempt",
        compiler_status: sourceCurrent ? "compiles" : "not_run_failed_or_changed",
        compiler_diagnostics: elements.diagnostics.textContent,
        proof_status: "unproved",
        exact_subgoal: (result.remaining_proof_obligations || []).join("; "),
      },
      review: {
        artifact: "review",
        semantic_review_status: semanticReviewed
          ? result.semantic_review_status || "reviewed_mapping"
          : "not_reviewed",
        reviewer_status: "not_reviewed",
        accepted: false,
      },
      created_at: new Date().toISOString(),
    };
  };

  const download = (content, extension, type) => {
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `samplinglib-formalization-packet.${extension}`;
    document.body.append(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
  };

  const exportJson = () => download(`${JSON.stringify(packet(), null, 2)}\n`, "json", "application/json");
  const exportMarkdown = () => {
    const value = packet();
    const text = `# ASTIS Formalization Packet\n\n## Original LaTeX\n\n\`\`\`latex\n${value.original_latex}\n\`\`\`\n\n## Candidate Lean\n\n\`\`\`lean\n${value.formalization_map.lean_source}\n\`\`\`\n\n## Assumptions\n\n${value.analytic_contract.exact_assumptions.map((item) => `- ${item}`).join("\n") || "- unresolved"}\n\n## Remaining obligations\n\n${value.analytic_contract.dependencies.map((item) => `- ${item}`).join("\n") || "- unresolved"}\n\n## Status\n\n- Translation: ${currentResult?.translation_status || "unresolved"}\n- Lean: ${value.proof_attempt.compiler_status}\n- Proof: unproved\n- Review: not reviewed\n`;
    download(text, "md", "text/markdown");
  };

  const checkHealth = async () => {
    try {
      const response = await fetch("../api/health", { headers: { Accept: "application/json" } });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const health = await response.json();
      localMode = true;
      elements.mode.classList.add("local");
      elements.modeTitle.textContent = "Local verified mode";
      elements.modeDetail.textContent = `${health.lean_version}; deterministic ASTIS adapter; repository source is read-only.`;
      elements.formalize.disabled = false;
      elements.compile.disabled = false;
    } catch (_error) {
      localMode = false;
      elements.mode.classList.add("static");
      elements.modeTitle.textContent = "Static mode";
      elements.modeDetail.textContent = "Reviewed mappings, LaTeX preview, navigation, and packet export are available. Candidate generation and Lean execution are disabled.";
      elements.formalize.disabled = true;
      elements.compile.disabled = true;
    }
  };

  fetch(app.dataset.liveData)
    .then((response) => response.json())
    .then((payload) => {
      mappings = payload.reviewed_mappings || [];
      elements.mapping.innerHTML = mappings.map((item, index) => `<option value="${index}">${item.name}</option>`).join("");
      if (mappings.length) loadMapping(mappings[0]);
      else renderLatex();
    })
    .catch((error) => {
      elements.diagnostics.textContent = `Could not load reviewed mappings: ${error.message}`;
    });

  elements.mapping?.addEventListener("change", () => loadMapping(mappings[Number(elements.mapping.value)]));
  elements.load?.addEventListener("click", () => loadMapping(mappings[Number(elements.mapping.value)]));
  elements.formalize?.addEventListener("click", formalize);
  elements.compile?.addEventListener("click", compile);
  elements.exportJson?.addEventListener("click", exportJson);
  elements.exportMarkdown?.addEventListener("click", exportMarkdown);
  elements.latex?.addEventListener("input", () => { renderLatex(); resetAfterEdit(); });
  elements.lean?.addEventListener("input", () => {
    compilerAccepted = false;
    semanticReviewed = false;
    setStatus(elements.leanStatus, "Changed; not compiled", "gray");
    setStatus(elements.proof, "Unproved", "orange");
    setStatus(elements.review, "Not reviewed", "gray");
  });
  checkHealth();
})();
