import requests
from pages.url import *
import streamlit as st

def criar_evento(evento: dict):
    url = f"{URL_BASE}{USER_EVENTS}"
    resp = requests.post(
        url,
        json=evento
    )
    resp.raise_for_status()
    return resp.json()


def atualizar_evento(evento_id: str, evento: dict):
    resp = requests.put(
        f"{URL_BASE}{ADMIN_EVENTOS}/{evento_id}",
        json=evento,
        timeout=10
    )
    resp.raise_for_status()
    return resp.json()


def excluir_evento(evento_id: str):
    resp = requests.delete(
        f"{URL_BASE}{ADMIN_EVENTOS}/{evento_id}",
        timeout=10
    )
    resp.raise_for_status()

def listar_eventos_publicos():
    url = f"{URL_BASE}{ADMIN_EVENTOS_PUB}"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

def listar_eventos_por_usuario(user_id: str):
    url = f"{URL_BASE}{USER_FEED}/?userId={user_id}"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()
