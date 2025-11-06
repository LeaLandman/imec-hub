// Simulation d’une recherche simple
document.getElementById("search-btn").addEventListener("click", () => {
  const query = document.getElementById("q").value.trim();
  const results = document.getElementById("results");

  if (!query) {
    results.innerHTML = "<p>Veuillez entrer un mot-clé.</p>";
    return;
  }

  results.innerHTML = `<p>🔍 Recherche en cours sur <strong>${query}</strong>...</p>`;

  // Simulation d’un résultat
  setTimeout(() => {
    results.innerHTML = `
      <article class="result-card">
        <h3>Résultat pour "${query}"</h3>
        <p>Exemple d'analyse géopolitique et technologique générée par l'IMEC Hub.</p>
      </article>
    `;
  }, 1000);
});
