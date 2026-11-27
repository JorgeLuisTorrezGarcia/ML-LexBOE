import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .model_service import cargar_modelo, obtener_info, predecir
from .schemas import ClasesResponse, ClasificarRequest, ClasificarResponse, SaludResponse

load_dotenv()

app = FastAPI(title="Clasificador LexBOE", version="1.0.0")

CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    # Carga el modelo una sola vez al arrancar.
    cargar_modelo()


@app.get("/api/salud", response_model=SaludResponse)
def salud():
    return SaludResponse(estado="ok")


@app.get("/api/clases", response_model=ClasesResponse)
def clases():
    info = obtener_info()
    return ClasesResponse(clases=info["clases"])


@app.post("/api/clasificar", response_model=ClasificarResponse)
def clasificar(req: ClasificarRequest):
    texto = req.texto.strip()
    if len(texto) < 20:
        raise HTTPException(status_code=400, detail="El texto es demasiado corto (mínimo 20 caracteres).")
    try:
        rama = predecir(texto)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al clasificar: {e}")
    return ClasificarResponse(rama=rama)


# Sirve el frontend compilado (React/Vite) si existe. En desarrollo con `pnpm dev`
# no está presente y simplemente no se monta nada.
FRONTEND_DIST = Path(os.getenv("FRONTEND_DIST", Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"))
if FRONTEND_DIST.is_dir():
    app.mount("/", StaticFiles(directory=FRONTEND_DIST, html=True), name="frontend")
