import logging
import os
import requests
import re
from database.database_manager import get_db


logger = logging.getLogger(__name__)


def cria_ou_consulta_cliente(dados_pessoais):
    db = get_db()
    cursor = db.cursor()

    try:
        cpf_cnpj = dados_pessoais["cpfCnpj"]

        cursor.execute(
            "select id_cliente_asaas from cliente where cpf_cnpj = %s", (cpf_cnpj,)
        )
        resultado = cursor.fetchone()

        if resultado and resultado[0]:
            id_cliente_asaas = resultado[0]
            logging.info(f"ID existente: {id_cliente_asaas}")
            return id_cliente_asaas
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
                novo_id_asaas = dados_asaas["id"]

                nome = dados_asaas["name"]
                email = dados_asaas["email"]
                cpfCnpj = dados_asaas["cpfCnpj"]
                cep = dados_asaas["postalCode"]
                num_residencia = dados_asaas["addressNumber"]
                id_cliente_asaas = dados_asaas["id"]

                cursor.execute(
                    "insert into cliente (nome, email, cpf_cnpj, cep, num_residencia, id_cliente_asaas) values (%s, %s, %s, %s, %s, %s)", (nome, email, cpfCnpj, cep, num_residencia, id_cliente_asaas)
                )
                db.commit()

                return novo_id_asaas
            else:
                # Trate o erro (ex: CPF inválido)
                return None

    except Exception as e:
        db.rollback()
        logging.error(f"Ocorreu um erro. A transação foi desfeita: {e}")
        raise e
    finally:
        cursor.close()
