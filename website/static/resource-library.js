/* Progressive enhancement: all references remain readable without JavaScript. */
(() => {
  const input = document.getElementById('resource-query');
  if (!input) return;
  const rows = Array.from(document.querySelectorAll('[data-resource-entry]'));
  const count = document.querySelector('[data-resource-count]');
  const update = () => {
    const words = input.value.toLocaleLowerCase().trim().split(/\s+/).filter(Boolean);
    let visible = 0;
    for (const row of rows) {
      row.hidden = !words.every(word => row.dataset.search.includes(word));
      visible += !row.hidden;
    }
    count.textContent = `${visible} of ${rows.length} references`;
  };
  input.addEventListener('input', update);
  update();
})();
