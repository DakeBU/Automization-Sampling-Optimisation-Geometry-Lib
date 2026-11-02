/* Up to eight rows, fitted to small screens; all history remains scrollable. */
(() => {
  document.querySelectorAll('.project-news-list').forEach(list => {
    const resize = () => {
      const rows = [...list.children];
      list.style.maxHeight = rows.length > 8
        ? `${Math.min(Math.ceil(rows[7].getBoundingClientRect().bottom - list.getBoundingClientRect().top + list.scrollTop), Math.floor(innerHeight * .72))}px`
        : 'none';
    };
    resize();
    window.addEventListener('resize', resize);
    if (document.fonts?.ready) document.fonts.ready.then(resize);
  });
})();
