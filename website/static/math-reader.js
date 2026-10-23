/* Shared reader contract: explicit inline math, local assets, async typesetting. */
(() => {
  "use strict";
  const skipped = "pre, textarea, script, style, noscript, svg, mjx-container, mjx-assistive-mml, [data-math-source]";
  const hasMath = (text) => /\\\(|\\\[|\$[^$\n]+\$/.test(text || "");

  // Old metadata exports escaped the delimiters twice. Recover paired
  // delimiters only; a TeX row break such as \\[2pt] must remain untouched.
  const normalizeDelimiters = (text) => text
    .replace(/(?<!\\)\\{2,}\(([\s\S]*?)\\{2,}\)/g, "\\($1\\)")
    .replace(/(?<!\\)\\{2,}\[([\s\S]*?)\\{2,}\]/g, "\\[$1\\]");

  function prepareMath(scope) {
    const walker = document.createTreeWalker(scope, NodeFilter.SHOW_TEXT, {
      acceptNode(node) {
        return node.parentElement?.closest(`${skipped}, code`)
          ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT;
      },
    });
    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach((node) => {
      const cleaned = normalizeDelimiters(node.nodeValue || "");
      if (cleaned !== node.nodeValue) node.nodeValue = cleaned;
    });
    promoteMathCode(scope);
  }

  // A complete, explicitly delimited formula is prose even when an old
  // Markdown exporter wrapped it in <code>. Real code and source copies stay code.
  function promoteMathCode(scope) {
    scope.querySelectorAll("code").forEach((code) => {
      if (code.closest(skipped) || code.children.length) return;
      const text = normalizeDelimiters(code.textContent.trim());
      if (!/^(?:\\\([\s\S]+\\\)|\\\[[\s\S]+\\\]|\$\$[\s\S]+\$\$|\$[^$\n]+\$)$/.test(text)) return;
      const span = document.createElement("span");
      span.className = "math-inline";
      span.textContent = text;
      code.replaceWith(span);
    });
  }

  function revealMath() {
    document.querySelectorAll("[data-math-statement]").forEach((statement) => {
      const rendered = !!statement.querySelector("mjx-container") &&
        !statement.querySelector("mjx-merror, [data-mjx-error]");
      statement.classList.toggle("math-rendered", rendered);
      statement.classList.toggle("math-fallback-active", !rendered);
      statement.querySelector(".math-tex")?.setAttribute("aria-hidden", String(!rendered));
      statement.querySelector(".math-fallback")?.setAttribute("aria-hidden", String(rendered));
    });
    document.dispatchEvent(new Event("reader-math-ready"));
  }

  const config = window.MathJax || {};
  config.tex = {
    ...config.tex,
    inlineMath: [["\\(", "\\)"], ["$", "$"]],
    displayMath: [["\\[", "\\]"], ["$$", "$$"]],
    processEscapes: true,
  };
  config.options = {
    ...config.options,
    skipHtmlTags: ["script", "noscript", "style", "textarea", "pre", "code"],
  };
  let chain = Promise.resolve();
  const pending = new Set();
  let timer;

  function queueMath(scope) {
    if (!scope || scope.closest(skipped)) return;
    pending.add(scope);
    clearTimeout(timer);
    timer = setTimeout(() => {
      const scopes = [...pending].filter((node) => node.isConnected);
      pending.clear();
      chain = chain.then(async () => {
        scopes.forEach(prepareMath);
        await window.MathJax.typesetPromise(scopes);
        revealMath();
      }).catch((error) => console.error("Reader math rendering failed", error));
    }, 30);
  }

  config.startup = {
    ...config.startup,
    pageReady() {
      prepareMath(document.body);
      return window.MathJax.startup.defaultPageReady().then(() => {
        revealMath();
        // Typeset only new mathematical text, never MathJax's own output.
        const observer = new MutationObserver((records) => {
          records.forEach((record) => {
            const parent = record.target.nodeType === Node.TEXT_NODE
              ? record.target.parentElement : record.target;
            if (!(parent instanceof Element) || parent.closest(skipped)) return;
            const nodes = record.type === "characterData" ? [record.target] : [...record.addedNodes];
            if (nodes.some((node) => {
              if (node.nodeType === Node.TEXT_NODE) return hasMath(node.nodeValue);
              return node instanceof Element && !node.matches(skipped) && hasMath(node.textContent);
            })) queueMath(parent);
          });
        });
        observer.observe(document.body, {childList: true, characterData: true, subtree: true});
      });
    },
  };
  window.MathJax = config;
})();
