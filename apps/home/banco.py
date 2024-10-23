
import psycopg2
from psycopg2 import sql
from datetime import datetime
from .Functions import *

# Database connection parameters
db_params = {
    'host': '192.168.3.11',
    'port': '5432',
    'database': 'mydatabase',
    'user': 'myuser',
    'password': 'mypassword'
}
hora_atual = datetime.now().time()
def select(numberid):
    # SQL SELECT statement
    query = f"""SELECT 
            message->'body'->'key'->>'remoteJid' as telefone, 
            message->'body'->'pushName' AS name,
            CASE 
                WHEN message->'body'->'key'->>'fromMe' = 'true' THEN 'enviadas' 
                ELSE 'recebidas' 
            END AS tipo,
            TO_CHAR(TO_TIMESTAMP(CAST(message->'body'->>'messageTimestamp' AS bigint)), 'DD/MM') AS data,
            TO_CHAR(TO_TIMESTAMP(CAST(message->'body'->>'messageTimestamp' AS bigint)), 'HH24:MI') AS hora,
            CASE 
                WHEN message->'body'->'message'->'extendedTextMessage'->>'text' IS NULL THEN message->'body'->'message'->>'conversation'
                ELSE message->'body'->'message'->'extendedTextMessage'->>'text'
            END AS message
            
        FROM recebidas
        WHERE  
            message->'body'->'key'->>'remoteJid' = '{numberid}' order by 4,6 asc"""
    
    html = """
            """
    select_query = sql.SQL(query)
    try:
        connection = psycopg2.connect(**db_params)
        with connection.cursor() as cursor:
            cursor.execute(select_query)
            rows = cursor.fetchall()
            for row in rows:
                telefone, name, tipo, data, hora, message = row
                if tipo == 'enviadas':
                    html= html +  f"""
                            <li class="d-flex justify-content-between mb-4">
                            <div class="card"  style="width: 100%; height: 100%;">
                            <div class="card-header d-flex justify-content-between p-3">
                                <p class="text-muted small mb-0"><i class="far fa-clock"></i>{hora}</p>
                            </div>
                            <div class="card-body">
                                <p class="mb-0">
                                {message}
                                </p>
                            </div>
                            </div>
                        </li>
                    """
                else:
                    html= html +  f"""
                        <li class="d-flex justify-content-between mb-4" >
                            <div class="card" style="background-color: #B7EAB9; width: 100%; height: 100%;">
                            <div class="card-header d-flex justify-content-between p-3" style="background-color: #B7EAB9;">
                                <p class="text-muted small mb-0"><i class="far fa-clock"></i>{hora}</p>
                            </div>
                            <div class="card-body">
                                <p class="mb-0">
                                {message}
                                </p>
                            </div>
                            </div>
                        </li>
                    
                    """
                    

    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
    finally:
        # Close the database connection
        if connection:
            connection.close()
           # print(html)
            print("Database connection closed.")
    return html

def insert(tipo,j):
    # SQL INSERT statement
    print("entrou no insert")
    print(j)
    j = str(j)
    jsont = j.replace("'", '"')
    print(jsont)
    insert_query = f"INSERT INTO recebidas (instancia, tipo, message)VALUES ('123','{tipo}','{jsont}')"
    print(insert_query)
   # print(insert_query)
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(**db_params)

        # Create a cursor object to execute SQL queries
        with connection.cursor() as cursor:
            # Execute the INSERT query for each set of data
            cursor.execute(insert_query)

            # Commit the changes to the database
            connection.commit()

        print("Data inserted successfully!")

    except psycopg2.Error as e:
        print("Error inserting data:", e)

    finally:
        # Close the database connection
        if connection:
            connection.close()
            print("Database connection closed.")

def recebidas():
    # SQL SELECT statement
    select_query = sql.SQL("SELECT * FROM teste")

    try:
        connection = psycopg2.connect(**db_params)
        with connection.cursor() as cursor:
            cursor.execute(select_query)
            rows = cursor.fetchall()
            for row in rows:
                print(row)

    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
    finally:
        if connection:
            connection.close()
            print("Database connection closed.")

def barra_chat():
    # SQL SELECT statement
    query = """select distinct message->'from'
        from recebidas r 
        """
                    
    html = ''
    select_query = sql.SQL(query)

    try:
        connection = psycopg2.connect(**db_params)
        with connection.cursor() as cursor:
            cursor.execute(select_query)
            rows = cursor.fetchall()
            #print(rows)
            cont = 0 
            for row in rows:
                cont = cont + 1
                number = row
            #
                html= html +  f"""
                    <li>
                        <li class="itemLi border-bottom" onclick="selecionarLi(this)">
                        <a href="#!" class="d-flex justify-content-between">
                            <div class="d-flex flex-row">
                            <img src="https://img.freepik.com/vetores-premium/icone-de-perfil-de-avatar_188544-4755.jpg?w=826" alt="avatar"
                                class="rounded-circle d-flex align-self-center me-3 shadow-1-strong" width="60">
                            <div class="pt-1">
                                <p class="name mb-0">{number}</p>
                             
                            </div>
                            </div>
                            <div class="pt-1">
                            </div>
                        </a>
                        </li>
                """



    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
    finally:
        # Close the database connection
        if connection:
            connection.close()
            #print(html)
            print("Database connection closed.")
    return html

def insert_menssage(number,msg):
    connection = psycopg2.connect(**db_params)
    cur = connection.cursor()
    try:
        cur.execute(f"INSERT INTO mensagens (id_number, mensagem,status) VALUES ('{number}', '{msg}','nao enviada')")
        connection.commit()
    except Exception as e:
        connection.rollback()
    finally:
        # Fechar o cursor e a conexão
        cur.close()
        connection.close()

def get_number(name):
    # Nome a ser pesquisado
    nome_pesquisado = name.replace('minhaVariavel=','').replace(' .','')

    # Cria a conexão com o banco de dados
    conexao = psycopg2.connect(**db_params)

    # Cria o cursor para executar consultas SQL
    cursor = conexao.cursor()

    # Consulta SQL
    consulta = f"""
        SELECT message->'body'->'key'->>'remoteJid'
        FROM recebidas r
        WHERE replace(cast(message->'body'->'pushName' as text),'"','') || ' ' = '{nome_pesquisado}'
        LIMIT 1;
    """
    # Executa a consulta com o nome como parâmetro
    cursor.execute(consulta, (nome_pesquisado,))

    # Recupera o resultado da consulta
    resultado = cursor.fetchone()

    # Fecha o cursor e a conexão
    cursor.close()
    conexao.close()

    # Se houver resultado, imprime o telefone
    if resultado:
        telefone = resultado[0]
        return telefone
    else:
        return 'telefone não localizado'
    
def get_qrcode():
    # Cria a conexão com o banco de dados
    conexao = psycopg2.connect(**db_params)

    # Cria o cursor para executar consultas SQL
    cursor = conexao.cursor()

    # Consulta SQL
    consulta = f"""
    select dado_bytea  from dados_base64
    """
    # Executa a consulta com o nome como parâmetro
    cursor.execute(consulta)

    # Recupera o resultado da consulta
    resultado = cursor.fetchone()
    #print(resultado)
    # Fecha o cursor e a conexão
    cursor.close()
    conexao.close()

    # Se houver resultado, imprime o telefone
    if resultado:
        qrcode = resultado[0]
        return qrcode
    else:
        return None