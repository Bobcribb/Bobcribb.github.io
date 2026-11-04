/* Reading preferences remain in this browser; no remote writes. */
document.addEventListener('DOMContentLoaded', () => {
  const article = document.querySelector('[data-mythos-reader]');
  if (!article) return;
  const toolbar = article.querySelector('.mythos-reader');
  const sections = [...article.querySelectorAll('[data-reading-section]')];
  if (!toolbar || !sections.length) return;
  const progress = toolbar.querySelector('progress');
  const resume = toolbar.querySelector('[data-reader="resume"]');
  const key = 'mythos-reading:' + location.pathname;
  const save = (k, v) => { try { localStorage.setItem(k, v); } catch (_) {} };
  const read = k => { try { return localStorage.getItem(k); } catch (_) { return null; } };
  let scale = Math.max(0.9, Math.min(1.4, Number(read('mythos-text-scale')) || 1));
  const resize = () => article.style.setProperty('--reading-scale', String(scale));
  resize(); toolbar.querySelector('.reader-buttons').hidden = false; progress.hidden = false;
  toolbar.querySelector('.reader-save-note').hidden = false;
  const saved = read(key);
  if (saved && document.getElementById(saved)) {
    resume.hidden = false;
    resume.onclick = () => document.getElementById(saved).scrollIntoView({behavior:'auto',block:'start'});
  }
  toolbar.addEventListener('click', event => {
    const button = event.target.closest('[data-reader]');
    if (!button) return;
    switch (button.dataset.reader) {
      case 'larger': scale = Math.min(1.4, scale + 0.1); resize(); save('mythos-text-scale', String(scale)); break;
      case 'smaller': scale = Math.max(0.9, scale - 0.1); resize(); save('mythos-text-scale', String(scale)); break;
      case 'focus': {
        const enabled = document.body.classList.toggle('mythos-focus');
        button.setAttribute('aria-pressed', String(enabled));
        button.textContent = enabled ? 'Vue complète' : 'Lecture épurée'; break;
      }
      case 'previous':
      case 'next': {
        let current=-1;
        sections.forEach((h,i)=>{if(h.getBoundingClientRect().top<innerHeight*0.45)current=i;});
        const target=sections[Math.max(0,Math.min(sections.length-1,current+(button.dataset.reader==='next'?1:-1)))];
        if(target){target.scrollIntoView({block:'start'});history.replaceState(null,'','#'+target.id);}
        break;
      }
      case 'print': window.print(); break;
    }
  });
  let scheduled = false;
  const update = () => {
    const rect = article.getBoundingClientRect();
    progress.value = Math.max(0, Math.min(100, -rect.top / Math.max(1,article.scrollHeight-innerHeight)*100));
    let active = null;
    for (const section of sections) {
      if (section.getBoundingClientRect().top < innerHeight*0.45) active=section;
      else break;
    }
    if (active) save(key,active.id);
    scheduled=false;
  };
  addEventListener('scroll', () => { if (!scheduled) { scheduled=true; requestAnimationFrame(update); } }, {passive:true});
  addEventListener('resize', update); update();
});
