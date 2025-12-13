import requests
from pages.url import URL_BASE, USER_EVENTS, ADMIN_EVENTOS
import streamlit as st

def criar_evento(evento: dict):
    resp = requests.post(
        URL_BASE + USER_EVENTS,
        json=evento,
        timeout=10
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
