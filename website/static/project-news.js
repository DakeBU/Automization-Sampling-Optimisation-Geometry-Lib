/* Eight visible rows; all older entries remain in the accessible scroll region. */
(() => {
  document.querySelectorAll('.project-news-list').forEach(list => {
    const resize = () => {
      const rows = [...list.children];
      list.style.maxHeight = rows.length > 8
        ? `${Math.ceil(rows[7].getBoundingClientRect().bottom - list.getBoundingClientRect().top + list.scrollTop)}px`
        : 'none';
    };
    resize();
    window.addEventListener('resize', resize);
    if (document.fonts?.ready) document.fonts.ready.then(resize);
  });
})();
