from pydantic import BaseModel, Field


class ClasificarRequest(BaseModel):
    texto: str = Field(..., min_length=1, description="Texto a clasificar")


class ClasificarResponse(BaseModel):
    rama: str


class SaludResponse(BaseModel):
    estado: str


class ClasesResponse(BaseModel):
    clases: list[str]
