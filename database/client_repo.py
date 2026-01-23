from .database_manager import get_db
import logging

logger = logging.getLogger(__name__)


def busca_cliente_db(cpf):
    cursor = None

    try:
        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            "select id_cliente_asaas from cliente where cpf_cnpj = %s", (cpf,)
        )

        id_asaas = cursor.fetchone()
        # de tupla para string
        if id_asaas and id_asaas[0]: 
            id_asaas = id_asaas[0] 
            logger.info(f"ID existente: {id_asaas}")
            return id_asaas
    
    except Exception as e:
        logger.error(f"Ocorreu um erro na busca pelo cliente no banco de dados. A transação foi desfeita: {e}")
        raise e
    finally:
        if cursor != None:
            cursor.close()


def cria_cliente_db(retorno_assas):
    cursor = None

    try:
        db = get_db()
        cursor = db.cursor()

        name = retorno_assas["name"]
        email = retorno_assas["email"]
        cpfCnpj = retorno_assas["cpfCnpj"]
        postalCode = retorno_assas["postalCode"]
        addressNumber = retorno_assas["addressNumber"]
        id_cliente_asaas = retorno_assas["id"]

        cursor.execute(
            "insert into cliente (nome, email, cpf_cnpj, cep, num_residencia, id_cliente_asaas) values (%s, %s, %s, %s, %s, %s)", (name, email, cpfCnpj, postalCode, addressNumber, id_cliente_asaas)
        )
        
        db.commit()

        return id_cliente_asaas
    
    except Exception as e:
        db.rollback()
        logger.error(f"Ocorreu um erro na criação do cliente no banco de dados. A transação foi desfeita: {e}")
        raise e
    finally:
        if cursor != None:
            cursor.close()