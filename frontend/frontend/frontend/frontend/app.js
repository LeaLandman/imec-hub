const API_URL = window.API_URL; // défini dans index.html

const form = document.getElementById('search-form');
const qEl = document.getElementById('q');
const results = document.getElementById('results');

function card(item){
  const el = document.createElement('article');
  el.className = 'item';
  el.innerHTML = `
    <div class="badge">${item.type || 'item'}</div>
    <div class="badge">${item.country || item.source || ''}</div>
    <h3>${item.title || item.name || '(sans titre)'}</h3>
    <p>${item.summary || item.description || ''}</p>
    ${item.url ? `<a target="_blank" href="${item.url}">Ouvrir la source →</a>` : ''}
  `;
  return el;
}

async function search(q){
  results.innerHTML = '⏳ Recherche en cours…';
  try{
    // adapte l’endpoint selon ton API: ici /search?q=
    const r = await fetch(`${API_URL}/search?q=${encodeURIComponent(q)}`);
    if(!r.ok) throw new Error(`HTTP ${r.status}`);
    const data = await r.json(); // attendu: { items: [...] } ou [...]
    const items = Array.isArray(data) ? data : (data.items || []);
    results.innerHTML = '';
    if(items.length === 0){
      results.innerHTML = '<p>Aucun résultat.</p>';
      return;
    }
    items.slice(0,24).forEach(i => results.appendChild(card(i)));
  }catch(e){
    console.error(e);
    results.innerHTML = `<p>Erreur de connexion à l’API (${e.message}).</p>`;
  }
}

form.addEventListener('submit', (e)=>{
  e.preventDefault();
  const q = qEl.value.trim();
  if(q) search(q);
});
