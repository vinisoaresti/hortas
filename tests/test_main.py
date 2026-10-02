import runpy

import pytest
from fastapi import HTTPException

import main


@pytest.fixture
def hortas_isoladas(monkeypatch):
    hortas = [
        main.Horta(
            id=1,
            nome="Horta Um",
            localizacao="Local Um",
            responsavel="Responsável Um",
            area=100.0,
        ),
        main.Horta(
            id=3,
            nome="Horta Três",
            localizacao="Local Três",
            responsavel="Responsável Três",
            area=300.0,
        ),
    ]
    monkeypatch.setattr(main, "hortas", hortas)
    return hortas


def test_listar_hortas_retorna_hortas_cadastradas(hortas_isoladas):
    resultado = main.listar_hortas()

    assert resultado == hortas_isoladas


def test_cadastrar_horta_gera_proximo_id_e_adiciona_horta(hortas_isoladas):
    nova_horta = main.NovaHorta(
        nome="Horta Nova",
        localizacao="Local Novo",
        responsavel="Responsável Novo",
        area=150.5,
    )

    resultado = main.cadastrar_horta(nova_horta)

    assert resultado == main.Horta(
        id=4,
        nome="Horta Nova",
        localizacao="Local Novo",
        responsavel="Responsável Novo",
        area=150.5,
    )
    assert hortas_isoladas[-1] == resultado


def test_cadastrar_horta_inicia_id_em_um_quando_lista_vazia(monkeypatch):
    hortas = []
    monkeypatch.setattr(main, "hortas", hortas)
    nova_horta = main.NovaHorta(
        nome="Horta Inicial",
        localizacao="Local Inicial",
        responsavel="Responsável Inicial",
        area=75.0,
    )

    resultado = main.cadastrar_horta(nova_horta)

    assert resultado.id == 1
    assert hortas == [resultado]


def test_recuperar_horta_retorna_horta_existente(hortas_isoladas):
    resultado = main.recuperar_horta(1)

    assert resultado == hortas_isoladas[0]


def test_recuperar_horta_lanca_404_para_id_inexistente(hortas_isoladas):
    with pytest.raises(HTTPException) as erro:
        main.recuperar_horta(99)

    assert erro.value.status_code == 404
    assert erro.value.detail == "Horta não encontrada"


def test_atualizar_horta_substitui_horta_existente(hortas_isoladas):
    dados_horta = main.NovaHorta(
        nome="Horta Atualizada",
        localizacao="Novo Local",
        responsavel="Novo Responsável",
        area=325.0,
    )

    resultado = main.atualizar_horta(1, dados_horta)

    assert resultado == main.Horta(
        id=1,
        nome="Horta Atualizada",
        localizacao="Novo Local",
        responsavel="Novo Responsável",
        area=325.0,
    )
    assert hortas_isoladas[0] == resultado


def test_atualizar_horta_lanca_404_para_id_inexistente(hortas_isoladas):
    dados_horta = main.NovaHorta(
        nome="Horta Atualizada",
        localizacao="Local",
        responsavel="Responsável",
        area=200.0,
    )

    with pytest.raises(HTTPException) as erro:
        main.atualizar_horta(99, dados_horta)

    assert erro.value.status_code == 404
    assert erro.value.detail == "Horta não encontrada"
    assert len(hortas_isoladas) == 2


def test_deletar_horta_remove_horta_existente(hortas_isoladas):
    resultado = main.deletar_horta(1)

    assert resultado.status_code == 204
    assert len(hortas_isoladas) == 1
    assert hortas_isoladas[0].id == 3
    assert all(horta.id != 1 for horta in hortas_isoladas)


def test_deletar_horta_lanca_404_para_id_inexistente(hortas_isoladas):
    with pytest.raises(HTTPException) as erro:
        main.deletar_horta(99)

    assert erro.value.status_code == 404
    assert erro.value.detail == "Horta não encontrada"
    assert len(hortas_isoladas) == 2


def test_execucao_direta_inicia_uvicorn(monkeypatch):
    chamadas = []

    def executar_servidor(*args, **kwargs):
        chamadas.append((args, kwargs))

    monkeypatch.setattr("uvicorn.run", executar_servidor)

    runpy.run_module("main", run_name="__main__")

    assert len(chamadas) == 1
    args, kwargs = chamadas[0]
    assert args[0].title == main.app.title
    assert kwargs == {"host": "127.0.0.1", "port": 8080}


def test_cadastrar_horta_com_ids_nao_ordenados(monkeypatch):
    hortas = [
        main.Horta(
            id=10, nome="Horta Dez", localizacao="L", responsavel="R", area=50.0
        ),
        main.Horta(
            id=2, nome="Horta Dois", localizacao="L", responsavel="R", area=60.0
        ),
    ]
    monkeypatch.setattr(main, "hortas", hortas)
    nova_horta = main.NovaHorta(
        nome="Nova", localizacao="L", responsavel="R", area=70.0
    )

    resultado = main.cadastrar_horta(nova_horta)

    assert resultado.id == 11
    assert len(hortas) == 3


def test_modelos_pydantic_validam_tipos_invalidos():
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        main.NovaHorta(
            nome="Horta Invalida",
            localizacao="Local",
            responsavel="Resp",
            area="nao-eh-numero",
        )

    with pytest.raises(ValidationError):
        main.Horta(
            id="invalido",
            nome="Horta Invalida",
            localizacao="Local",
            responsavel="Resp",
            area=100.0,
        )
