(function () {
  "use strict";

  const root = document.documentElement;
  const schemeToggles = document.querySelectorAll(".scheme-toggle");
  const navToggle = document.querySelector(".nav-toggle");
  const sidebar = document.getElementById("site-sidebar");
  const sidebarScrim = document.querySelector("[data-sidebar-scrim]");
  const siteScriptUrl = document.currentScript?.src || "";
  const assetsRoot = siteScriptUrl
    ? new URL(".", siteScriptUrl)
    : new URL("../assets/", window.location.href);

  const savedScheme = localStorage.getItem("samplinglib-color-scheme");
  if (savedScheme && ["light", "dark"].includes(savedScheme)) {
    root.dataset.colorScheme = savedScheme;
  } else if (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) {
    root.dataset.colorScheme = "dark";
  }
  schemeToggles.forEach((toggle) => {
    toggle.addEventListener("click", () => {
      root.dataset.colorScheme = root.dataset.colorScheme === "dark" ? "light" : "dark";
      localStorage.setItem("samplinglib-color-scheme", root.dataset.colorScheme);
    });
  });

  const closeSidebar = () => {
    sidebar?.classList.remove("open");
    document.body.classList.remove("sidebar-open");
    navToggle?.setAttribute("aria-expanded", "false");
  };
  if (navToggle && sidebar) {
    navToggle.addEventListener("click", () => {
      const open = sidebar.classList.toggle("open");
      document.body.classList.toggle("sidebar-open", open);
      navToggle.setAttribute("aria-expanded", String(open));
    });
    sidebarScrim?.addEventListener("click", closeSidebar);
    sidebar.querySelectorAll("a").forEach((link) => link.addEventListener("click", closeSidebar));
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && sidebar.classList.contains("open")) {
        closeSidebar();
        navToggle.focus();
      }
    });
  }

  function filterCards() {
    const search = document.getElementById("card-search");
    const status = document.getElementById("status-filter");
    const cards = document.querySelectorAll("#filterable-cards .correspondence-card");
    if (!cards.length) return;
    const run = () => {
      const query = (search?.value || "").trim().toLowerCase();
      const statusValue = status?.value || "";
      cards.forEach((card) => {
        const searchMatch = !query || card.textContent.toLowerCase().includes(query);
        const statusMatch = !statusValue || card.dataset.status === statusValue;
        card.hidden = !(searchMatch && statusMatch);
      });
    };
    search?.addEventListener("input", run);
    status?.addEventListener("change", run);
  }

  function filterImplementation() {
    const search = document.getElementById("implementation-search");
    const status = document.getElementById("implementation-status");
    const rows = document.querySelectorAll("#implementation-table tbody tr");
    if (!rows.length) return;
    const run = () => {
      const query = (search?.value || "").trim().toLowerCase();
      const statusValue = status?.value || "";
      rows.forEach((row) => {
        const searchMatch = !query || (row.dataset.search || row.textContent.toLowerCase()).includes(query);
        const statusMatch = !statusValue || row.dataset.status === statusValue;
        row.hidden = !(searchMatch && statusMatch);
      });
    };
    search?.addEventListener("input", run);
    status?.addEventListener("change", run);
  }

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function slugify(value) {
    const slug = String(value)
      .replace(/[^a-zA-Z0-9]+/g, "-")
      .replace(/^-+|-+$/g, "")
      .toLowerCase();
    return slug || "entry";
  }

  function currentPageSlug() {
    const name = decodeURIComponent(window.location.pathname.split("/").pop() || "");
    return name.replace(/\.html$/i, "");
  }

  function matchingEntries(entries, pageSlug) {
    return entries.filter((entry) =>
      Array.isArray(entry.declarations)
      && entry.declarations.some((declaration) => slugify(declaration) === pageSlug)
    );
  }

  async function renderRigorousLessonSupplement() {
    const article = document.querySelector(".theorem-layout > article");
    if (!article) return;
    const pageSlug = currentPageSlug();
    if (!pageSlug) return;

    try {
      const response = await fetch(new URL("rigorous-lessons.json", assetsRoot));
      if (!response.ok) throw new Error(`rigorous lessons: ${response.status}`);
      const data = await response.json();
      const entries = Array.isArray(data.entries) ? data.entries : [];
      const matches = matchingEntries(entries, pageSlug);
      if (!matches.length) return;

      const panel = document.createElement("section");
      panel.className = "rigorous-lesson-panel";
      panel.dataset.rigorousLesson = "true";
      panel.innerHTML = matches.map((entry) => {
        const formulas = Array.isArray(entry.formula_latex) ? entry.formula_latex : [];
        const steps = Array.isArray(entry.proof_steps) ? entry.proof_steps : [];
        const subtlePoints = Array.isArray(entry.subtle_points) ? entry.subtle_points : [];
        return `
          <div class="rigorous-lesson-group">
            <div class="eyebrow">ASTIS rigorous expansion · source ${escapeHtml(entry.source_item || "")}</div>
            <h2>${escapeHtml(entry.title || "Rigorous derivation")}</h2>
            <div class="note"><strong>Scope guard.</strong> ${escapeHtml(entry.scope_note || "")}</div>
            <h3>Exact formulas</h3>
            <div class="rigorous-formulas">${formulas.map((formula) => `<div class="math-statement">${escapeHtml(formula)}</div>`).join("")}</div>
            <h3>Proof, step by step</h3>
            <div class="proof-steps">
              ${steps.map((step) => {
                const nodes = Array.isArray(step.lean_nodes) ? step.lean_nodes : [];
                const stepFormula = step.formula_latex
                  ? `<div class="math-statement">${escapeHtml(step.formula_latex)}</div>`
                  : "";
                return `
                  <article class="proof-step">
                    <h4>${escapeHtml(step.title || "Proof step")}</h4>
                    <p>${escapeHtml(step.body || "")}</p>
                    ${stepFormula}
                    ${nodes.length ? `
                      <details class="lean-node-list">
                        <summary><strong>Lean nodes for this step</strong><span class="search-kind">These are the compiled leaves that make the paper proof explicit.</span></summary>
                        <ul>${nodes.map((node) => `<li><code>${escapeHtml(node)}</code></li>`).join("")}</ul>
                      </details>
                    ` : ""}
                  </article>
                `;
              }).join("")}
            </div>
            ${subtlePoints.length ? `
              <details class="rigor-details">
                <summary><strong>Subtle points the short textbook proof can hide</strong></summary>
                <ul>${subtlePoints.map((point) => `<li>${escapeHtml(point)}</li>`).join("")}</ul>
              </details>
            ` : ""}
          </div>
        `;
      }).join("");

      const conditionsHeading = [...article.children]
        .find((node) => node.tagName === "H2" && node.textContent.trim() === "Conditions");
      if (conditionsHeading) article.insertBefore(panel, conditionsHeading);
      else {
        const formalizationLens = [...article.children]
          .find((node) => node.matches?.("details.formalization-lens"));
        if (formalizationLens) article.insertBefore(panel, formalizationLens);
        else article.appendChild(panel);
      }

      if (window.MathJax?.typesetPromise) {
        window.MathJax.typesetPromise([panel]).catch(() => {});
      }
    } catch (error) {
      console.warn("Samplinglib rigorous lesson was not loaded:", error);
    }
  }

  async function renderRigorousReferences() {
    const article = document.querySelector(".theorem-layout > article");
    if (!article) return;
    const pageSlug = currentPageSlug();
    if (!pageSlug) return;

    try {
      const response = await fetch(new URL("rigorous-references.json", assetsRoot));
      if (!response.ok) throw new Error(`rigorous references: ${response.status}`);
      const data = await response.json();
      const entries = Array.isArray(data.entries) ? data.entries : [];
      const matches = matchingEntries(entries, pageSlug);
      if (!matches.length) return;

      const panel = document.createElement("section");
      panel.className = "rigorous-reference-panel";
      panel.dataset.rigorousReferences = "true";
      panel.innerHTML = matches.map((entry) => {
        const additions = Array.isArray(entry.astis_additions) ? entry.astis_additions : [];
        const references = Array.isArray(entry.references) ? entry.references : [];
        return `
          <div class="rigorous-reference-group">
            <h2>${escapeHtml(entry.heading || "Rigorous references")}</h2>
            <div class="note"><strong>Provenance boundary.</strong> Chewi supplies the source-facing statement. The bullets below record ASTIS-added rigorous detail; the linked papers, textbooks, and formal libraries are external references, not text attributed to Chewi.</div>
            <h3>What ASTIS makes explicit</h3>
            <ul>${additions.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>
            <h3>Original and rigorous sources</h3>
            <div class="reference-list">
              ${references.map((reference) => `
                <article class="reference-card">
                  <div class="card-meta"><span class="mini-tag">${escapeHtml(reference.kind || "reference")}</span></div>
                  <h4><a href="${escapeHtml(reference.url || "#")}" target="_blank" rel="noopener noreferrer">${escapeHtml(reference.label || reference.url || "Reference")}</a></h4>
                  <p>${escapeHtml(reference.note || "")}</p>
                </article>
              `).join("")}
            </div>
          </div>
        `;
      }).join("");

      const formalizationLens = [...article.children]
        .find((node) => node.matches?.("details.formalization-lens"));
      if (formalizationLens) article.insertBefore(panel, formalizationLens);
      else article.appendChild(panel);

      if (window.MathJax?.typesetPromise) {
        window.MathJax.typesetPromise([panel]).catch(() => {});
      }
    } catch (error) {
      console.warn("Samplinglib rigorous references were not loaded:", error);
    }
  }

  function foldLeanFormalizationLens() {
    const article = document.querySelector(".theorem-layout > article");
    if (!article) return;
    const leanHeading = [...article.children]
      .find((node) => node.tagName === "H2" && node.textContent.trim() === "Lean statement");
    if (!leanHeading) return;

    const details = document.createElement("details");
    details.className = "formalization-lens";
    const summary = document.createElement("summary");
    summary.innerHTML = '<strong>Formalization lens · Lean proof and interface</strong><span class="search-kind">Optional: inspect the exact Lean statement, interface notes, and proof-engineering choices.</span>';
    leanHeading.before(details);
    details.appendChild(summary);

    let cursor = leanHeading;
    while (cursor) {
      const next = cursor.nextSibling;
      details.appendChild(cursor);
      cursor = next;
    }
  }

  function globalSearch() {
    const input = document.querySelector("[data-global-search]");
    const results = document.querySelector("[data-global-results]");
    if (!input || !results) return;
    const rootPath = input.dataset.searchRoot || "";
    let indexPromise = null;

    const loadIndex = () => {
      if (!indexPromise) {
        indexPromise = fetch(`${rootPath}search-index.json`).then((response) => {
          if (!response.ok) throw new Error(`search index: ${response.status}`);
          return response.json();
        });
      }
      return indexPromise;
    };

    const hide = () => {
      results.hidden = true;
      results.innerHTML = "";
    };

    input.addEventListener("input", async () => {
      const query = input.value.trim().toLowerCase();
      if (query.length < 2) {
        hide();
        return;
      }
      const terms = query.split(/\s+/).filter(Boolean);
      try {
        const index = await loadIndex();
        const matches = index
          .filter((item) => {
            const haystack = `${item.name} ${item.kind} ${item.module} ${item.chapter} ${item.local_status} ${item.route_status}`.toLowerCase();
            return terms.every((term) => haystack.includes(term));
          })
          .slice(0, 18);
        results.innerHTML = matches.length
          ? matches.map((item) => (
            `<li><a href="${rootPath}${encodeURI(item.url)}"><code>${escapeHtml(item.name)}</code>` +
            `<span class="search-kind">${escapeHtml(item.kind)} · ${escapeHtml(item.module)} · ${escapeHtml(item.local_status)}</span></a></li>`
          )).join("")
          : '<li class="empty">No matching declaration or module.</li>';
        results.hidden = false;
      } catch (error) {
        results.innerHTML = `<li class="empty">${escapeHtml(error.message)}</li>`;
        results.hidden = false;
      }
    });
    document.addEventListener("click", (event) => {
      if (!event.target.closest(".search-shell")) hide();
    });
    input.addEventListener("keydown", (event) => {
      if (event.key === "Escape") hide();
    });
  }

  function filterCatalog() {
    const search = document.getElementById("declaration-search");
    const kind = document.getElementById("declaration-kind");
    const localStatus = document.getElementById("declaration-local-status");
    const count = document.getElementById("declaration-count");
    const rows = [...document.querySelectorAll("#declaration-table tbody tr")];
    if (!rows.length) return;
    const run = () => {
      const terms = (search?.value || "").trim().toLowerCase().split(/\s+/).filter(Boolean);
      const selectedKind = kind?.value || "";
      const selectedStatus = localStatus?.value || "";
      let visible = 0;
      rows.forEach((row) => {
        const haystack = row.dataset.search || row.textContent.toLowerCase();
        const matches = terms.every((term) => haystack.includes(term))
          && (!selectedKind || row.dataset.kind === selectedKind)
          && (!selectedStatus || row.dataset.localStatus === selectedStatus);
        row.hidden = !matches;
        if (matches) visible += 1;
      });
      if (count) count.textContent = `${visible.toLocaleString()} declarations`;
    };
    search?.addEventListener("input", run);
    kind?.addEventListener("change", run);
    localStatus?.addEventListener("change", run);
  }

  function filterGenericTables() {
    document.querySelectorAll("[data-table-search]").forEach((input) => {
      const table = document.getElementById(input.dataset.tableSearch);
      const rows = [...(table?.querySelectorAll("tbody tr") || [])];
      if (!rows.length) return;
      input.addEventListener("input", () => {
        const terms = input.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
        rows.forEach((row) => {
          const haystack = row.dataset.search || row.textContent.toLowerCase();
          row.hidden = !terms.every((term) => haystack.includes(term));
        });
      });
    });
  }

  function highlightLean() {
    const keywords = /\b(theorem|lemma|def|abbrev|structure|class|inductive|namespace|end|where|by|fun|let|have|show|exact|apply|refine|intro|constructor|cases|simpa|simp|rw|calc|match|with|if|then|else|∀|∃)\b/g;
    const types = /\b(Prop|Type|Set|Measure|Integrable|Tendsto|HasFDerivAt|DifferentiableAt|ContinuousLinearMap|EuclideanSpace|PiLp|ENNReal|ℝ|ℕ)\b/g;
    const numbers = /\b\d+(?:\.\d+)?\b/g;
    document.querySelectorAll("code.language-lean").forEach((node) => {
      let value = node.textContent;
      value = value
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
      const protectedParts = [];
      value = value.replace(/\/-![\s\S]*?-\/|\/--[\s\S]*?-\/|--[^\n]*/g, (part) => {
        protectedParts.push(`<span class="tok-comment">${part}</span>`);
        return `\uE000${String.fromCharCode(0xE100 + protectedParts.length - 1)}\uE001`;
      });
      value = value.replace(/"([^"\\]|\\.)*"/g, (part) => {
        protectedParts.push(`<span class="tok-string">${part}</span>`);
        return `\uE000${String.fromCharCode(0xE100 + protectedParts.length - 1)}\uE001`;
      });
      value = value.replace(keywords, '<span class="tok-keyword">$1</span>');
      value = value.replace(types, '<span class="tok-type">$1</span>');
      value = value.replace(numbers, '<span class="tok-number">$&</span>');
      value = value.replace(/\uE000([\uE100-\uF8FF])\uE001/g, (_, marker) => {
        return protectedParts[marker.charCodeAt(0) - 0xE100];
      });
      node.innerHTML = value;
    });
  }

  function loadMermaid() {
    if (!document.querySelector(".mermaid")) return;
    const script = document.createElement("script");
    script.type = "module";
    script.textContent = `
      import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
      mermaid.initialize({
        startOnLoad: true,
        theme: document.documentElement.dataset.colorScheme === "dark" ? "dark" : "neutral",
        flowchart: { curve: "basis", htmlLabels: true, useMaxWidth: true },
        themeVariables: { fontFamily: "Inter, system-ui, sans-serif", fontSize: "15px" }
      });
    `;
    document.body.appendChild(script);
  }

  filterCards();
  filterImplementation();
  globalSearch();
  filterCatalog();
  filterGenericTables();
  highlightLean();
  foldLeanFormalizationLens();
  renderRigorousLessonSupplement();
  renderRigorousReferences();
  loadMermaid();
})();
