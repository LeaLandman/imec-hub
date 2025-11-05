
# IMEC Intelligence Hub — App avec Agent intégré

## Lancer en local
```
docker compose up -d --build
docker exec -it imec_api python /app/../db/bootstrap_imec_db.py
cd frontend && export NEXT_PUBLIC_API_BASE="http://localhost:8000" && npm install && npm run dev
# http://localhost:3000
```

## Déploiement gratuit
- DB : Neon (free)
- API : Render (free)
- Front : Vercel (free)
- Agent : GitHub Actions (cron)
Voir `DEPLOY_GUIDE.md`.
