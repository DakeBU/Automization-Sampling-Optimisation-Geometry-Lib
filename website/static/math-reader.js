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

  let fitFrame;
  const observedMathSizes = new WeakMap();
  const mathSizer = window.ResizeObserver ? new ResizeObserver((entries) => {
    let changed = false;
    entries.forEach((entry) => {
      if (!entry.target.isConnected) {
        mathSizer.unobserve(entry.target);
        observedMathSizes.delete(entry.target);
      } else if (observedMathSizes.get(entry.target) !== entry.contentRect.width) {
        observedMathSizes.set(entry.target, entry.contentRect.width);
        changed = true;
      }
    });
    if (changed) scheduleMathFit();
  }) : null;

  // Presentation only: keep TeX and MathJax's mathematical tree unchanged.
  // Modest fitting makes long summaries readable on desktop; never shrink a
  // normal-size formula below 16px to squeeze it into a phone viewport.
  function fitProofMath() {
    document.querySelectorAll(".proof-reader-equation").forEach((box) => {
      const containers = box.querySelectorAll('mjx-container[display="true"]');
      if (containers.length !== 1 || !box.clientWidth) return;
      const container = containers[0];
      const math = container.querySelector("mjx-math");
      if (!math) return;
      [box, container].forEach((node) => {
        if (mathSizer && !observedMathSizes.has(node)) {
          observedMathSizes.set(node, node.getBoundingClientRect().width);
          mathSizer.observe(node);
        }
      });
      if (!container.hasAttribute("data-reader-original-font")) {
        container.dataset.readerOriginalFont = container.style.fontSize;
      }
      container.style.fontSize = container.dataset.readerOriginalFont;
      const style = getComputedStyle(box);
      const available = box.clientWidth - parseFloat(style.paddingLeft) - parseFloat(style.paddingRight);
      const width = math.getBoundingClientRect().width;
      const baseline = parseFloat(getComputedStyle(container).fontSize);
      if (!width || available <= 2 || !Number.isFinite(baseline)) return;
      if (width > available) {
        container.style.fontSize = `${Math.max(Math.min(16, baseline), baseline * (available - 2) / width)}px`;
      }
      const overflow = math.getBoundingClientRect().width > available + 1;
      let hint = box.nextElementSibling;
      if (!hint?.classList.contains("math-scroll-hint")) {
        hint = document.createElement("div");
        hint.className = "math-scroll-hint";
        hint.textContent = "Long formula: scroll horizontally to read the rest.";
        box.after(hint);
      }
      hint.hidden = !overflow;
      if (overflow && !box.hasAttribute("tabindex")) {
        box.tabIndex = 0;
        box.dataset.readerScrollFocus = "true";
      } else if (!overflow && box.dataset.readerScrollFocus) {
        box.removeAttribute("tabindex");
        delete box.dataset.readerScrollFocus;
      }
    });
  }

  function scheduleMathFit() {
    cancelAnimationFrame(fitFrame);
    fitFrame = requestAnimationFrame(fitProofMath);
  }
  window.addEventListener("resize", scheduleMathFit);
  document.addEventListener("toggle", scheduleMathFit, true);
  document.fonts?.ready.then(scheduleMathFit);
  document.fonts?.addEventListener("loadingdone", scheduleMathFit);

  function revealMath() {
    document.querySelectorAll("[data-math-statement]").forEach((statement) => {
      const rendered = !!statement.querySelector("mjx-container") &&
        !statement.querySelector("mjx-merror, [data-mjx-error]");
      statement.classList.toggle("math-rendered", rendered);
      statement.classList.toggle("math-fallback-active", !rendered);
      statement.querySelector(".math-tex")?.setAttribute("aria-hidden", String(!rendered));
      statement.querySelector(".math-fallback")?.setAttribute("aria-hidden", String(rendered));
    });
    fitProofMath();
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
