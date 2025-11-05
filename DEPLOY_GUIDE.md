
# Déploiement gratuit — Neon + Render + Vercel + GitHub Actions

1) **Neon (DB)** : crée la base et récupère l'URL `DATABASE_URL`.
2) **Render (API)** :
   - Root: `api/`
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn app:app --host 0.0.0.0 --port 10000`
   - Env: `DATABASE_URL`, `API_KEY`, `CORS_ORIGINS`
   - Initialise la DB avec `db/bootstrap_imec_db.py` (depuis une console ou localement avec l'URL Neon).
3) **Vercel (Front)** :
   - Project root: `frontend/`
   - Env: `NEXT_PUBLIC_API_BASE` = URL Render
4) **GitHub Actions (Agent)** :
   - Secrets: `API_BASE`, `API_KEY`
   - Workflow: `.github/workflows/agent.yml`
