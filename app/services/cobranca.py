import logging
import os
import requests
from requests.exceptions import HTTPError


logger = logging.getLogger(__name__)

def cria_cobranca(payload):
    try:
        url = 'https://api-sandbox.asaas.com/v3/lean/payments'
        headers = {
            "content-type": "application/json",
            "accept": "application/json",
            "access_token": os.environ.get("ACCESS_TOKEN")
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Erro ao criar cobrança: {response.text}")
            response.raise_for_status()

    except HTTPError as e:
        logger.error(f"Erro na requisição ao criar cobrança: {e}")
        raise e


def busca_qrcode_pix(id_cobranca):
    try:
        url = f"https://api-sandbox.asaas.com/v3/payments/{id_cobranca}/pixQrCode"
        
        headers = {
            "content-type": "application/json",
            "accept": "application/json",
            "access_token": os.environ.get('ACCESS_TOKEN')
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Erro ao buscar QR Code Pix: {response.text}")
            return None
    except HTTPError as e:
        logger.error(f"Erro na requisição ao buscar QRCode Pix: {e}")
        raise e
