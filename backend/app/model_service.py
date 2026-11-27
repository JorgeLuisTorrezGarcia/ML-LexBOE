import json
import os
import re
from functools import lru_cache
from pathlib import Path

import joblib

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # carpeta proyecto/

MODEL_PATH = Path(os.getenv("MODEL_PATH", BASE_DIR / "modelo_lexboe.joblib"))
INFO_PATH = Path(os.getenv("INFO_PATH", BASE_DIR / "modelo_lexboe_info.json"))

URL_RE = re.compile(r"https?://\S+|www\.\S+")
ESPACIOS_RE = re.compile(r"\s+")


def limpiar_texto(texto: str, max_chars: int) -> str:
    """Recorta, quita URLs y normaliza espacios (igual que en el notebook)."""
    texto = texto[:max_chars]
    texto = URL_RE.sub(" ", texto)
    texto = ESPACIOS_RE.sub(" ", texto)
    return texto.strip()


@lru_cache(maxsize=1)
def cargar_modelo():
    """Carga el pipeline y los metadatos una sola vez."""
    modelo = joblib.load(MODEL_PATH)
    with open(INFO_PATH, "r", encoding="utf-8") as f:
        info = json.load(f)
    return modelo, info


def predecir(texto: str) -> str:
    modelo, info = cargar_modelo()
    texto_limpio = limpiar_texto(texto, max_chars=info["max_chars"])
    rama = modelo.predict([texto_limpio])[0]
    return str(rama)


def obtener_info() -> dict:
    _, info = cargar_modelo()
    return info
