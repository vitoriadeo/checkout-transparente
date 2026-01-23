import logging
import os
import requests
from database.client_repo import busca_cliente_db, cria_cliente_db

logger = logging.getLogger(__name__)


def cria_ou_consulta_cliente(dados_pessoais):
    try:
        id_asaas = busca_cliente_db(dados_pessoais['cpfCnpj'])

        if id_asaas:
            logger.info(f"Cliente Asaas identificado, ID: {id_asaas}")
            return id_asaas
        else:
            url = "https://api-sandbox.asaas.com/v3/customers"
            headers = {
                "content-type": "application/json",
                "accept": "application/json",
                "access_token": os.environ.get("ACCESS_TOKEN"),
            }

            response = requests.post(url, json=dados_pessoais, headers=headers)

            if response.status_code == 200:
                dados_asaas = response.json()

                id_asaas = cria_cliente_db(dados_asaas)
                return id_asaas
            else:
                logger.warning(f"Status Code [{response.status_code}] - Problema ao retornar dados.")
                response.raise_for_status()

    except Exception as e:
        logger.error(f"Ocorreu um erro no gerenciamento da API (para cadastro de cliente). A transação foi desfeita: {e}")
        raise e
