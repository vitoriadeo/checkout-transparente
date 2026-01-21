from ...database.database_manager import get_db
import logging, os, requests


logger = logging.getLogger(__name__)


def cria_ou_consultaCliente(dados_pessoais):
    db = get_db()
    cursor = db.cursor()

    try:
        cpf_cnpj = dados_pessoais["cpfCnpj"]

        cursor.execute("select id_cliente_asaas from cliente where cpf_cnpj = %s", (cpf_cnpj,))
        resultado = cursor.fetchone()

        if resultado:
            id_cliente_asaas = resultado[0]
            logging.info(f"ID existente: {id_cliente_asaas}")
            return id_cliente_asaas
        else:
            url = "https://sandbox.asaas.com/api/v3/customers"
            headers = {
                "Content-Type": "application/json",
                "access_token": os.environ.get('ACCESS_TOKEN'),
            }

            response = requests.post(url, json=dados_pessoais, headers=headers)

            if response.status_code == 200:
                dados_asaas = response.json()
                novo_id_asaas = dados_asaas['id']

                #logica para salvar aqui

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

