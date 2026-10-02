from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel


class Horta(BaseModel):
    id: int
    nome: str
    localizacao: str
    responsavel: str
    area: float


class NovaHorta(BaseModel):
    nome: str
    localizacao: str
    responsavel: str
    area: float


app = FastAPI(
    title="Sistema de Gestão de Hortas Comunitárias",
    description="API REST para consulta e cadastro de hortas comunitárias.",
    version="1.0.0",
)


hortas = [
    Horta(
        id=1,
        nome="Horta Comunitária Esperança",
        localizacao="Bairro Jardim das Flores",
        responsavel="Maria Silva",
        area=450.0,
    ),
    Horta(
        id=2,
        nome="Horta Verde Vida",
        localizacao="Praça Central",
        responsavel="João Santos",
        area=320.5,
    ),
    Horta(
        id=3,
        nome="Horta Raízes do Bairro",
        localizacao="Vila Nova",
        responsavel="Ana Oliveira",
        area=275.0,
    ),
]


@app.get("/api/hortas", response_model=list[Horta])
def listar_hortas() -> list[Horta]:
    """Retorna todas as hortas comunitárias cadastradas em memória."""
    return hortas


@app.post("/api/hortas", response_model=Horta, status_code=201)
def cadastrar_horta(nova_horta: NovaHorta) -> Horta:
    """Cadastra uma nova horta comunitária na lista em memória."""
    proximo_id = max((horta.id for horta in hortas), default=0) + 1
    horta = Horta(id=proximo_id, **nova_horta.model_dump())
    hortas.append(horta)
    return horta


@app.get("/api/hortas/{horta_id}", response_model=Horta)
def recuperar_horta(horta_id: int) -> Horta:
    """Retorna uma horta comunitária específica a partir do seu ID."""
    for horta in hortas:
        if horta.id == horta_id:
            return horta
    raise HTTPException(status_code=404, detail="Horta não encontrada")


@app.put("/api/hortas/{horta_id}", response_model=Horta)
def atualizar_horta(horta_id: int, dados_horta: NovaHorta) -> Horta:
    """Atualiza os dados de uma horta comunitária cadastrada em memória."""
    for i, horta in enumerate(hortas):
        if horta.id == horta_id:
            horta_atualizada = Horta(id=horta_id, **dados_horta.model_dump())
            hortas[i] = horta_atualizada
            return horta_atualizada
    raise HTTPException(status_code=404, detail="Horta não encontrada")


@app.delete("/api/hortas/{horta_id}", status_code=204)
def deletar_horta(horta_id: int) -> Response:
    """Remove uma horta comunitária cadastrada em memória a partir do seu ID."""
    for i, horta in enumerate(hortas):
        if horta.id == horta_id:
            del hortas[i]
            return Response(status_code=204)
    raise HTTPException(status_code=404, detail="Horta não encontrada")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8080)
