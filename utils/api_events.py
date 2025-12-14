import requests
import pages.url as urls

#print("ARQUIVO url.py CARREGADO:", urls.__file__)
#print("ATRIBUTOS:", dir(urls))

def criar_evento(evento: dict):
    url = f"{urls.URL_BASE}{urls.USER_EVENTS}"
    resp = requests.post(
        url,
        json=evento
    )
    resp.raise_for_status()
    return resp.json()


def atualizar_evento(evento: dict):
    resp = requests.put(
        f"{urls.URL_BASE}{urls.UPDATE_EVENT}",
        json=evento,
        timeout=10
    )
    resp.raise_for_status()
    return resp.json()


def excluir_evento(event_id: str, user_id: str):
    payload = {
        "eventId": event_id,
        "userId": user_id
    }

    resp = requests.delete(
        f"{urls.URL_BASE}{urls.DELETE_EVENT}",
        json=payload,
        timeout=10
    )
    resp.raise_for_status()

def listar_eventos_publicos():
    url = f"{urls.URL_BASE}{urls.ADMIN_EVENTOS_PUB}"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

def listar_eventos_por_usuario(user_id: str):
    url = f"{urls.URL_BASE}{urls.USER_FEED}/?userId={user_id}"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()
