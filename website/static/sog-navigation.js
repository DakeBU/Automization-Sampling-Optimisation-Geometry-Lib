(() => {
  'use strict';
  for (const button of document.querySelectorAll('[data-sog-copy-prompt]')) {
    button.addEventListener('click', async () => {
      const status=button.closest('.sog-prompt-actions').querySelector('[data-sog-copy-status]');
      try {
        const response=await fetch(button.dataset.sogCopyPrompt);
        if (!response.ok) throw new Error('Prompt download failed');
        await navigator.clipboard.writeText(await response.text());
        status.textContent='Copied prompt-only task';
      } catch (_) { status.textContent='Copy unavailable; use the prompt-only download.'; }
    });
  }
  for (const list of document.querySelectorAll('[data-sog-task-list]')) {
    const rows=[...list.querySelectorAll('.sog-task-row')], input=list.querySelector('input[type="search"]');
    const more=list.querySelector('[data-sog-show-more]'), status=list.querySelector('[data-sog-list-status]');
    let limit=6;
    const render=()=>{
      const query=(input?.value||'').trim().toLowerCase();
      const matched=rows.filter(row=>row.textContent.toLowerCase().includes(query));
      rows.forEach(row=>{row.hidden=!matched.includes(row)||matched.indexOf(row)>=limit;});
      more.hidden=matched.length<=limit;
      status.textContent=`Showing ${Math.min(limit,matched.length)} of ${matched.length} task cores`;
    };
    input?.addEventListener('input',()=>{limit=6;render();});
    more?.addEventListener('click',()=>{limit+=6;render();});
    render();
  }
})();
