from utils.api_events import (
    listar_eventos_por_usuario,
    listar_eventos_publicos
)

def merge_eventos(usuario_eventos, publicos_eventos):
    mapa = {}

    for ev in publicos_eventos:
        mapa[str(ev["id"])] = ev

    for ev in usuario_eventos:
        mapa[str(ev["id"])] = ev

    return list(mapa.values())


def recarregar_eventos(user_id: str):
    eventos_usuario = listar_eventos_por_usuario(user_id)
    eventos_publicos = listar_eventos_publicos()

    return merge_eventos(eventos_usuario, eventos_publicos)