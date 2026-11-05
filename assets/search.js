/* Search every entry, with filters and accessible pagination. */
document.addEventListener('DOMContentLoaded', () => {
  const input=document.querySelector('[data-search]'), results=document.querySelector('[data-results]');
  if (!input || !results) return;
  const filters=[...document.querySelectorAll('[data-filter]')], pagination=document.querySelector('[data-pagination]');
  let status=document.querySelector('[data-search-status]');
  if (!status) { status=document.createElement('p');status.setAttribute('role','status');results.before(status); }
  const norm=v=>String(v||'').toLowerCase().replace(/œ/g,'oe').normalize('NFD').replace(/[\u0300-\u036f]/g,'');
  const params=new URLSearchParams(location.search);
  input.value=params.get('q')||'';
  let documents=[],page=1,ready=false;
  const size=20, values=(doc,key)=>Array.isArray(doc[key])?doc[key]:doc[key]?[doc[key]]:[];
  const updateURL=()=>{
    const p=new URLSearchParams();
    if(input.value.trim())p.set('q',input.value.trim());
    for(const f of filters)if(f.value)p.set(f.dataset.filter,f.value);
    if(page>1)p.set('page',String(page));
    history.replaceState(null,'',location.pathname+(p.size?'?'+p:'')+location.hash);
  };
  const draw=(update=true)=>{
    if(!ready)return;
    const terms=norm(input.value.trim()).split(/\s+/).filter(Boolean);
    const found=documents.filter(d=>terms.every(t=>d._search.includes(t))&&filters.every(f=>!f.value||values(d,f.dataset.filter).includes(f.value)));
    if(terms.length){const score=d=>terms.reduce((n,t)=>n+(norm(d.title).includes(t)?10:0)+(values(d,'works').some(w=>norm(w).includes(t))?5:0),0);found.sort((a,b)=>score(b)-score(a)||a.title.localeCompare(b.title,'fr'));}
    const total=Math.max(1,Math.ceil(found.length/size));page=Math.min(Math.max(1,page),total);
    results.replaceChildren();
    status.textContent=found.length?`${found.length} résultat${found.length>1?'s':''} · page ${page} sur ${total}`:'Aucun résultat. Essayez un autre mot ou retirez un filtre.';
    for(const doc of found.slice((page-1)*size,page*size)){
      const item=document.createElement('article');item.className='search-result';
      const h=document.createElement('h2'),a=document.createElement('a');a.href=doc.url;a.textContent=doc.title;h.append(a);item.append(h);
      const meta=document.createElement('p');meta.className='search-result-meta';
      meta.textContent=[doc.collection,...values(doc,'civilizations'),doc.minutes?`${doc.minutes} min de lecture environ`:''].filter(Boolean).join(' · ');item.append(meta);
      if(doc.excerpt){const p=document.createElement('p');p.textContent=doc.excerpt;item.append(p);}
      if(results.dataset.catalogue){const id=document.createElement('small');id.textContent=`${doc.id} · page disponible dans le catalogue`;item.append(id);}
      results.append(item);
    }
    if(pagination){
      pagination.replaceChildren();
      const button=(label,target,disabled)=>{const b=document.createElement('button');b.type='button';b.textContent=label;b.disabled=disabled;b.onclick=()=>{page=target;draw();status.scrollIntoView({block:'start'});};pagination.append(b);};
      button('Précédent',page-1,page===1);const label=document.createElement('span');label.textContent=`${page} / ${total}`;pagination.append(label);button('Suivant',page+1,page===total);
    }
    if(update)updateURL();
  };
  input.addEventListener('input',()=>{page=1;draw();});
  for(const f of filters)f.addEventListener('change',()=>{page=1;draw();});
  const form=document.querySelector('[data-discovery-form]');
  if(form){form.addEventListener('submit',e=>{e.preventDefault();page=1;draw();});form.addEventListener('reset',e=>{e.preventDefault();input.value='';filters.forEach(f=>f.value='');page=1;draw();});}
  const getIndex=url=>fetch(url,{cache:'no-cache'}).then(r=>{
    if(!r.ok)throw new Error('Index indisponible');
    return r.json();
  });
  // Rechercher dans une projection légère, sans toucher à l'index scientifique.
  // Conserver la rétrocompatibilité si un cache sert une ancienne publication.
  getIndex('/catalog/search-light.json').catch(()=>getIndex('/search.json')).then(data=>{
    if(!Array.isArray(data)||!data.length)throw new Error('Index vide');
    documents=data.map(d=>({...d,_search:d.search_text||
      norm([d.title,d.excerpt,d.headings,d.collection,...values(d,'authors'),
            ...values(d,'works'),...values(d,'themes')].join(' '))}));
    for(const f of filters){for(const value of [...new Set(documents.flatMap(d=>values(d,f.dataset.filter)))].sort((a,b)=>a.localeCompare(b,'fr'))){const o=document.createElement('option');o.value=value;o.textContent=value;f.append(o);}f.value=params.get(f.dataset.filter)||'';}
    page=Math.max(1,parseInt(params.get('page'),10)||1);ready=true;draw(false);
  }).catch(()=>{status.textContent='La recherche est temporairement indisponible.';results.replaceChildren();const a=document.createElement('a');a.href='/rubriques/';a.textContent='Consulter l’index alphabétique complet';results.append(a);});
});
