from flask import url_for
from datetime import date
from .asaas_service import cria_ou_consulta_cliente
from .cobranca import cria_cobranca, busca_qrcode_pix
import logging

logger = logging.getLogger(__name__)


def processar_pagamento(form_data, valor):
    try:
        dados_cliente = {
            "name": form_data.get("nome"),
            "email": form_data.get("email"),
            "cpfCnpj": form_data.get("id"),
            "mobilePhone": form_data.get("telefone"),
            "postalCode": form_data.get("cep"),
            "addressNumber": form_data.get("numero"),
        }

        customer_id = cria_ou_consulta_cliente(dados_cliente)
        metodo = form_data.get("payment_method")

        payload = {
            "customer": customer_id,
            "billingType": metodo,
            "value": valor,
            "dueDate": date.today().isoformat(),
        }

        resposta = cria_cobranca(payload)

        if metodo == "PIX":
            qr = busca_qrcode_pix(resposta["id"])
            if not qr:
                raise Exception("Falha ao gerar QR Code")

            return {
                "sucesso": True,
                "tipo": "pix",
                "dados": {"qr_code": qr["encodedImage"], "copia_cola": qr["payload"]},
            }

        elif metodo == "BOLETO":
            return {
                "sucesso": True,
                "tipo": "boleto",
                "dados": {
                    "link": resposta["bankSlipUrl"],
                    "vencimento": resposta["dueDate"],
                    "valor": resposta["value"],
                },
            }

    except Exception as e:
        logger.error(f"Erro no checkout: {str(e)}")
        return {
            "sucesso": False,
            "erro": "Erro ao processar pagamento. Tente novamente.",
        }

    return {"sucesso": False, "erro": "Método de pagamento inválido."}
