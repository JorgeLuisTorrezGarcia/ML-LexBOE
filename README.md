# Clasificador de textos BOE

API en FastAPI + interfaz web en React para el modelo `modelo_lexboe.joblib` entrenado en Colab (TF-IDF + LinearSVC, 12 ramas del BOE).

## Estructura

- `backend/` — API FastAPI (`POST /api/clasificar`, `GET /api/salud`, `GET /api/clases`), con su propio `Dockerfile` y `fly.toml` para Fly.io
- `frontend/` — React + Vite (se despliega como sitio estático)
- `modelo_lexboe.joblib`, `modelo_lexboe_info.json` — modelo e información (en la raíz y copias en `backend/` para el despliegue)

## Backend

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --port 8000
```

Documentación interactiva: http://localhost:8000/docs

Variables de entorno opcionales (`.env`):

- `MODEL_PATH` — ruta al `.joblib` (por defecto `modelo_lexboe.joblib` dentro de `backend/`)
- `INFO_PATH` — ruta al `.json` de info
- `CORS_ORIGINS` — orígenes permitidos, separados por coma (por defecto `http://localhost:5173`; en producción, la URL del frontend desplegado)

## Frontend

```bash
cd frontend
pnpm install
pnpm dev
```

Abre http://localhost:5173. La URL del API se configura con `VITE_API_URL` (por defecto `http://localhost:8000`).

## Despliegue

Backend y frontend se despliegan por separado.

### Backend en Fly.io

```bash
cd backend
fly launch        # la primera vez, crea la app y usa el Dockerfile/fly.toml existentes
fly deploy
```

La app queda en `https://<app>.fly.dev`. Antes de desplegar, configura CORS con la URL del frontend:

```bash
fly secrets set CORS_ORIGINS=https://tu-frontend.vercel.app
```

### Frontend (estático)

```bash
cd frontend
pnpm build
```

Sube el contenido de `frontend/dist/` a cualquier hosting estático (Vercel, Netlify, GitHub Pages…). Define `VITE_API_URL` con la URL del backend en Fly.io antes de compilar, por ejemplo `VITE_API_URL=https://lexboe-backend.fly.dev`.

## Notas

- El texto se limpia antes de predecir (`limpiar_texto` en `backend/app/model_service.py`): recorte a `max_chars`, eliminación de URLs y normalización de espacios, igual que en el entrenamiento.
- El modelo se entrenó con scikit-learn 1.6.1; con versiones nuevas puede aparecer un `InconsistentVersionWarning` (funciona, pero conviene fijar la versión en despliegue).

# Citation

@article{tamayo2026mrbert,
  title={MrBERT: Modern Multilingual Encoders via Vocabulary, Domain, and Dimensional Adaptation},
  author={Tamayo, Daniel and Lacunza, I{\~n}aki and Rivera-Hidalgo, Paula and Da Dalt, Severino and Aula-Blasco, Javier and Gonzalez-Agirre, Aitor and Villegas, Marta},
  journal={arXiv preprint arXiv:2602.21379},
  year={2026}
}
