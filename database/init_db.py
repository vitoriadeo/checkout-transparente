import os, logging
import psycopg2
from app.config import Config

logger = logging.getLogger(__name__)
conn_str = Config.DB_URL

def inicializa_db():
    conn = None
    cur = None

    try:
        logger.info("Conectando aos Supabase/PostgreSQL...")
        conn = psycopg2.connect(conn_str)
        logger.info("Conexão estabelecida!")

        cur = conn.cursor()

        logger.info("Lendo arquivo schema.sql...")

        caminho = os.path.join(os.path.dirname(__file__), 'schema.sql')

        with open(caminho, 'r', encoding='utf-8') as arquivo:
            sql_comandos = arquivo.read()
        
        logger.info("Executando scripts de criação de tabelas...")
        cur.execute(sql_comandos)

        conn.commit()
        logger.info("Tabelas criadas com sucesso!")

    except psycopg2.OperationalError as e:
        logger.error(f"Erro de conexão: {e}")
        conn.rollback()
        logger.warning(">> Desfazendo transação")
        raise e

    except Exception as e:
        logger.error(f"Falha na iniciallização do banco: {e}")
        conn.rollback()
        logger.warning(">> Desfazendo transação")
        raise e

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
            logger.info("Conexão fechada.")

if __name__ == "__main__":
    inicializa_db()