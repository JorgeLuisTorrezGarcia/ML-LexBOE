# Clasificador de textos BOE

API en FastAPI + interfaz web en React para el modelo `modelo_lexboe.joblib` entrenado en Colab (TF-IDF + LinearSVC, 12 ramas del BOE).

## Estructura

- `backend/` — API FastAPI (`POST /api/clasificar`, `GET /api/salud`, `GET /api/clases`)
- `frontend/` — React + Vite
- `modelo_lexboe.joblib`, `modelo_lexboe_info.json` — modelo e información (en la raíz)

## Backend

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --port 8000
```

Documentación interactiva: http://localhost:8000/docs

Variables de entorno opcionales (`.env`):

- `MODEL_PATH` — ruta al `.joblib` (por defecto `../modelo_lexboe.joblib`)
- `INFO_PATH` — ruta al `.json` de info
- `CORS_ORIGINS` — orígenes permitidos, separados por coma (por defecto `http://localhost:5173`)

## Frontend

```bash
cd frontend
pnpm install
pnpm dev
```

Abre http://localhost:5173. La URL del API se configura con `VITE_API_URL` (por defecto `http://localhost:8000`).

## Docker

La imagen `lexboe-app` contiene el backend, el modelo y el frontend compilado: una sola imagen sirve la API y la web en el puerto 8000.

```bash
docker build -t lexboe-app .
docker run -p 8000:8000 lexboe-app
```

Abre http://localhost:8000 — la API está en `/api/*` y la interfaz en `/`.

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
