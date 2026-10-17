/* Deep links must reveal, not merely scroll to, a folded proof. */
(() => {
  function reveal(hash) {
    if (!hash || hash === '#') return;
    let id;
    try { id = decodeURIComponent(hash.slice(1)); } catch { return; }
    const target = document.getElementById(id);
    if (!target) return;
    for (let node = target; node; node = node.parentElement) {
      if (node.tagName === 'DETAILS') node.open = true;
    }
    if (id === 'paper-lean-progress') {
      const index = target.querySelector('.paper-verified-index');
      if (index) index.open = true;
    }
  }
  document.addEventListener('click', event => {
    const link = event.target.closest('a[href^="#"]');
    if (link) reveal(link.getAttribute('href'));
  });
  window.addEventListener('hashchange', () => reveal(location.hash));
  reveal(location.hash);
})();
