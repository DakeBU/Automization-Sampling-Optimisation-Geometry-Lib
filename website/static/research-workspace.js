(() => {
  "use strict";

  const app = document.querySelector("[data-research-workspace]");
  if (!app) return;

  const elements = {
    workspace: app.querySelector("[data-rw-workspace]"),
    theorem: app.querySelector("[data-rw-theorem]"),
    source: app.querySelector("[data-rw-source]"),
    copy: app.querySelector("[data-rw-copy]"),
    json: app.querySelector("[data-rw-json]"),
    bundle: app.querySelector("[data-rw-bundle]"),
    title: app.querySelector("[data-rw-title]"),
    role: app.querySelector("[data-rw-role]"),
    steps: app.querySelector("[data-rw-steps]"),
    stepTitle: app.querySelector("[data-rw-step-title]"),
    stepStatus: app.querySelector("[data-rw-step-status]"),
    formula: app.querySelector("[data-rw-formula]"),
    explanation: app.querySelector("[data-rw-explanation]"),
    anchor: app.querySelector("[data-rw-anchor]"),
    boundary: app.querySelector("[data-rw-boundary]"),
    assumptions: app.querySelector("[data-rw-assumptions]"),
    leanSupport: app.querySelector("[data-rw-lean-support]"),
    ledger: app.querySelector("[data-rw-ledger]"),
    ledgerIntro: app.querySelector("[data-rw-ledger-intro]"),
    quantities: app.querySelector("[data-rw-quantities]"),
    errorFlow: app.querySelector("[data-rw-error-flow]"),
    apiMode: app.querySelector("[data-rw-api-mode]"),
    aiStatus: app.querySelector("[data-rw-ai-status]"),
    leanStatus: app.querySelector("[data-rw-lean-status]"),
    reviewStatus: app.querySelector("[data-rw-review-status]"),
    question: app.querySelector("[data-rw-question]"),
    answer: app.querySelector("[data-rw-answer]"),
    actions: [...app.querySelectorAll("[data-rw-action]")],
  };

  let workspaces = [];
  let selectedWorkspace = null;
  let selectedTheorem = null;
  let selectedStep = null;
  let assistantAvailable = false;

  const setList = (node, values, emptyText) => {
    node.replaceChildren();
    const rows = Array.isArray(values) ? values : [];
    if (!rows.length) {
      const item = document.createElement("li");
      item.className = "muted";
      item.textContent = emptyText;
      node.append(item);
      return;
    }
    rows.forEach((value) => {
      const item = document.createElement("li");
      item.textContent = String(value);
      node.append(item);
    });
  };

  const typeset = async (nodes) => {
    try {
      if (window.MathJax?.startup?.promise) await window.MathJax.startup.promise;
      window.MathJax?.typesetClear?.(nodes);
      await window.MathJax?.typesetPromise?.(nodes);
    } catch (error) {
      console.warn("Research workspace MathJax error", error);
    }
  };

  const updateUrl = () => {
    if (!selectedWorkspace || !selectedTheorem || !selectedStep) return;
    const url = new URL(window.location.href);
    url.searchParams.set("workspace", selectedWorkspace.id);
    url.searchParams.set("theorem", selectedTheorem.id);
    url.searchParams.set("step", selectedStep.id);
    window.history.replaceState(null, "", url);
  };

  const evidenceLabel = (step) => {
    if (step.compiled_support?.length) return "Open step · reusable support compiles";
    return "Open Lean obligation";
  };

  const renderStep = (step) => {
    selectedStep = step;
    elements.stepTitle.textContent = step.title;
    elements.stepStatus.textContent = evidenceLabel(step);
    elements.stepStatus.className = `status ${step.compiled_support?.length ? "status-yellow" : "status-red"}`;
    elements.formula.textContent = `\\[${step.formula}\\]`;
    elements.explanation.textContent = step.explanation;
    elements.anchor.textContent = step.source_anchor;
    elements.boundary.textContent = selectedTheorem.boundary;
    setList(elements.assumptions, selectedTheorem.assumptions, "No assumption record.");
    elements.leanSupport.replaceChildren();
    if (step.compiled_support?.length) {
      const note = document.createElement("p");
      note.textContent = step.support_note;
      const list = document.createElement("ul");
      step.compiled_support.forEach((name) => {
        const item = document.createElement("li");
        const code = document.createElement("code");
        code.textContent = name;
        item.append(code);
        list.append(item);
      });
      elements.leanSupport.append(note, list);
      elements.leanStatus.textContent = "Support only";
    } else {
      elements.leanSupport.textContent = "No ASTIS declaration is attached to this step. The mathematical statement remains an explicit red obligation.";
      elements.leanStatus.textContent = "Not formalized";
    }
    elements.aiStatus.textContent = "Not requested";
    elements.reviewStatus.textContent = "Not implied";
    elements.answer.textContent = "Choose an action. In static mode the site creates a bounded prompt that can be copied into ChatGPT or Codex; local API mode can answer here.";
    [...elements.steps.querySelectorAll("button")].forEach((button) => {
      button.setAttribute("aria-current", button.dataset.stepId === step.id ? "step" : "false");
    });
    typeset([elements.formula]);
    updateUrl();
  };

  const renderRoute = () => {
    elements.steps.replaceChildren();
    selectedTheorem.steps.forEach((step, index) => {
      const item = document.createElement("li");
      const button = document.createElement("button");
      button.type = "button";
      button.dataset.stepId = step.id;
      const count = document.createElement("span");
      count.textContent = String(index + 1).padStart(2, "0");
      const label = document.createElement("strong");
      label.textContent = step.title;
      const status = document.createElement("small");
      status.textContent = evidenceLabel(step);
      button.append(count, label, status);
      button.addEventListener("click", () => renderStep(step));
      item.append(button);
      elements.steps.append(item);
    });
  };

  const appendFormulaCell = (row, value) => {
    const cell = document.createElement("td");
    cell.textContent = `\\(${value}\\)`;
    row.append(cell);
    return cell;
  };

  const renderLedger = () => {
    const ledger = selectedWorkspace.ledger;
    elements.ledger.hidden = !ledger;
    if (!ledger) return;
    elements.ledgerIntro.textContent = ledger.intro;
    elements.quantities.replaceChildren();
    const mathNodes = [];
    ledger.quantities.forEach((quantity) => {
      const row = document.createElement("tr");
      mathNodes.push(appendFormulaCell(row, quantity.symbol));
      [quantity.meaning].forEach((value) => {
        const cell = document.createElement("td");
        cell.textContent = value;
        row.append(cell);
      });
      mathNodes.push(appendFormulaCell(row, quantity.update));
      const role = document.createElement("td");
      role.textContent = quantity.role;
      row.append(role);
      elements.quantities.append(row);
    });
    elements.errorFlow.replaceChildren();
    ledger.error_flow.forEach((entry) => {
      const item = document.createElement("li");
      const title = document.createElement("h4");
      title.textContent = entry.stage;
      const text = document.createElement("p");
      text.textContent = `Input: ${entry.input} Output: ${entry.output}`;
      const charge = document.createElement("p");
      charge.className = "ledger-charge";
      charge.textContent = `Ledger charge: ${entry.charge}`;
      item.append(title, text, charge);
      elements.errorFlow.append(item);
    });
    typeset(mathNodes);
  };

  const renderTheorem = (theorem, preferredStepId = "") => {
    selectedTheorem = theorem;
    elements.theorem.value = theorem.id;
    renderRoute();
    const step = theorem.steps.find((row) => row.id === preferredStepId) || theorem.steps[0];
    renderStep(step);
  };

  const renderWorkspace = (workspace, preferredTheoremId = "", preferredStepId = "") => {
    selectedWorkspace = workspace;
    elements.workspace.value = workspace.id;
    elements.title.textContent = workspace.title;
    elements.role.textContent = workspace.role;
    elements.source.href = workspace.source_reader;
    elements.json.href = workspace.downloads.json;
    elements.bundle.href = workspace.downloads.bundle;
    elements.theorem.replaceChildren();
    workspace.theorems.forEach((theorem) => {
      const option = document.createElement("option");
      option.value = theorem.id;
      option.textContent = theorem.title;
      elements.theorem.append(option);
    });
    renderLedger();
    const theorem = workspace.theorems.find((row) => row.id === preferredTheoremId) || workspace.theorems[0];
    renderTheorem(theorem, preferredStepId);
  };

  const buildPrompt = (action = "explain") => {
    const source = selectedWorkspace.source_records.map((row) => `${row.title} (${row.version}): ${row.url}`).join("\n");
    const support = selectedStep.compiled_support.length
      ? selectedStep.compiled_support.map((name) => `- ${name}`).join("\n")
      : "- none attached; this step remains open";
    const question = elements.question.value.trim();
    return `# Samplinglib bounded research request\n\nAction: ${action}\nWorkspace: ${selectedWorkspace.title} (${selectedWorkspace.id})\nSources:\n${source}\n\nTheorem: ${selectedTheorem.title}\nStatement: ${selectedTheorem.statement}\nFormula: $${selectedTheorem.formula}$\nAssumptions:\n${selectedTheorem.assumptions.map((item) => `- ${item}`).join("\n")}\n\nSelected step: ${selectedStep.title} (${selectedStep.id})\nSource anchor: ${selectedStep.source_anchor}\nFormula: $${selectedStep.formula}$\nExplanation: ${selectedStep.explanation}\nCompiled reusable support:\n${support}\n\nStrict theorem boundary: ${selectedTheorem.boundary}\n${question ? `\nResearcher question: ${question}\n` : ""}\nEvidence rule: distinguish paper/source facts, ASTIS-authored expansion, ASTIS-owned compiled declarations, Mathlib/external facts, and your own unverified inference. Do not claim that this source theorem is formalized. If proposing Lean, state the exact remaining obligation and keep compilation plus independent source-fidelity review separate.`;
  };

  const copyText = async (value) => {
    try {
      await navigator.clipboard.writeText(value);
      return true;
    } catch (_error) {
      const area = document.createElement("textarea");
      area.value = value;
      area.style.position = "fixed";
      area.style.opacity = "0";
      document.body.append(area);
      area.select();
      const ok = document.execCommand("copy");
      area.remove();
      return ok;
    }
  };

  const runAction = async (action) => {
    const prompt = buildPrompt(action);
    elements.actions.forEach((button) => { button.disabled = true; });
    elements.aiStatus.textContent = assistantAvailable ? "Generating" : "Prompt ready";
    if (!assistantAvailable) {
      const copied = await copyText(prompt);
      elements.answer.textContent = `${copied ? "Copied" : "Prepared"} a bounded ${action} request for ChatGPT/Codex. No AI response or Lean verification occurred on this static page.`;
      elements.actions.forEach((button) => { button.disabled = false; });
      return;
    }
    elements.answer.textContent = "The source-grounded assistant is working on the selected step…";
    try {
      const response = await fetch("../api/assist", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          workspace_id: selectedWorkspace.id,
          theorem_id: selectedTheorem.id,
          step_id: selectedStep.id,
          action,
          question: elements.question.value.trim(),
        }),
      });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.error || `HTTP ${response.status}`);
      elements.answer.textContent = `AI explanation — unverified\n\n${payload.answer}`;
      elements.aiStatus.textContent = "Unverified answer";
      elements.reviewStatus.textContent = "Still required";
    } catch (error) {
      elements.answer.textContent = `Assistant unavailable: ${error.message}\n\nThe bounded prompt has been copied so it can be used in ChatGPT or Codex.`;
      await copyText(prompt);
      elements.aiStatus.textContent = "Unavailable";
    } finally {
      elements.actions.forEach((button) => { button.disabled = false; });
    }
  };

  const checkAssistant = async () => {
    try {
      const response = await fetch("../api/health", { headers: { Accept: "application/json" } });
      if (!response.ok) throw new Error();
      const health = await response.json();
      assistantAvailable = Boolean(health.ai_assistant_configured);
      elements.apiMode.textContent = assistantAvailable ? "Local API ready" : "Prompt export mode";
      elements.apiMode.className = `status ${assistantAvailable ? "status-yellow" : "status-gray"}`;
    } catch (_error) {
      assistantAvailable = false;
      elements.apiMode.textContent = "Static prompt mode";
      elements.apiMode.className = "status status-gray";
    }
  };

  fetch(app.dataset.workspaceData)
    .then((response) => {
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return response.json();
    })
    .then((payload) => {
      workspaces = payload.workspaces || [];
      elements.workspace.replaceChildren();
      workspaces.forEach((workspace) => {
        const option = document.createElement("option");
        option.value = workspace.id;
        option.textContent = workspace.title;
        elements.workspace.append(option);
      });
      const params = new URLSearchParams(window.location.search);
      const workspace = workspaces.find((row) => row.id === params.get("workspace")) || workspaces[0];
      if (workspace) renderWorkspace(workspace, params.get("theorem") || "", params.get("step") || "");
    })
    .catch((error) => {
      elements.answer.textContent = `Could not load research workspaces: ${error.message}`;
    });

  elements.workspace.addEventListener("change", () => {
    const workspace = workspaces.find((row) => row.id === elements.workspace.value);
    if (workspace) renderWorkspace(workspace);
  });
  elements.theorem.addEventListener("change", () => {
    const theorem = selectedWorkspace?.theorems.find((row) => row.id === elements.theorem.value);
    if (theorem) renderTheorem(theorem);
  });
  elements.copy.addEventListener("click", async () => {
    if (!selectedStep) return;
    const copied = await copyText(buildPrompt("research"));
    elements.answer.textContent = copied
      ? "Copied a bounded, source-labelled prompt for ChatGPT or Codex. No AI response or Lean verification occurred."
      : "Could not access the clipboard. Download the context packet instead.";
  });
  elements.actions.forEach((button) => {
    button.addEventListener("click", () => runAction(button.dataset.rwAction));
  });
  checkAssistant();
})();
