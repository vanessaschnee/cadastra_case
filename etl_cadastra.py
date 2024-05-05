import pandas as pd
import mysql.connector

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Gabriela1",
            database="CAMPANHA_CADASTRA"
        )
        return connection
    except mysql.connector.Error as err:
        print("Erro ao conectar ao banco de dados: {}".format(err))
        return None

def insert_into_dim_tempo(connection, data):
    try:
        cursor = connection.cursor()
        datas_unicas = sorted(set(data['Data']))
        for data_unica in datas_unicas:
            ano = data_unica.year
            mes = data_unica.month
            dia = data_unica.day
            cursor.execute("SELECT id_data FROM dim_tempo WHERE data = %s", (data_unica,))
            result = cursor.fetchone()
            if not result:
                cursor.execute("INSERT INTO dim_tempo (data, ano, mes, dia) VALUES (%s, %s, %s, %s)", (data_unica, ano, mes, dia))
        connection.commit()
        cursor.close()
        print("Dados inseridos na tabela dim_tempo.")
    except mysql.connector.Error as err:
        print("Erro ao inserir dados na tabela dim_tempo: {}".format(err))

def insert_into_dim_marca(connection, data):
    try:
        cursor = connection.cursor()
        marcas_unicas = set(data['Marca'])
        for marca in marcas_unicas:
            cursor.execute("SELECT id_marca FROM dim_marca WHERE marca = %s", (marca,))
            result = cursor.fetchone()
            if not result:
                cursor.execute("INSERT INTO dim_marca (marca) VALUES (%s)", (marca,))
        connection.commit()
        cursor.close()
        print("Dados inseridos na tabela dim_marca.")
    except mysql.connector.Error as err:
        print("Erro ao inserir dados na tabela dim_marca: {}".format(err))

def insert_into_dim_campanha(connection, data):
    try:
        cursor = connection.cursor()
        campanhas_unicas = set(data['Campanha'])
        for campanha in campanhas_unicas:
            cursor.execute("SELECT id_campanha FROM dim_campanha WHERE campanha = %s", (campanha,))
            result = cursor.fetchone()
            if not result:
                cursor.execute("INSERT INTO dim_campanha (campanha) VALUES (%s)", (campanha,))
        connection.commit()
        cursor.close()
        print("Dados inseridos na tabela dim_campanha.")
    except mysql.connector.Error as err:
        print("Erro ao inserir dados na tabela dim_campanha: {}".format(err))

def insert_into_dim_midia(connection, data):
    try:
        cursor = connection.cursor()
        midias_unicas = set(data['Midia'])
        for midia in midias_unicas:
            cursor.execute("SELECT id_midia FROM dim_midia WHERE midia = %s", (midia,))
            result = cursor.fetchone()
            if not result:
                cursor.execute("INSERT INTO dim_midia (midia) VALUES (%s)", (midia,))
        connection.commit()
        cursor.close()
        print("Dados inseridos na tabela dim_midia.")
    except mysql.connector.Error as err:
        print("Erro ao inserir dados na tabela dim_midia: {}".format(err))

def insert_into_fato_analise(connection, data):
    try:
        cursor = connection.cursor()
        for index, row in data.iterrows():
            cursor.execute("SELECT * FROM fato_analise WHERE id_data = (SELECT id_data FROM dim_tempo WHERE data = %s) "
                           "AND id_marca = (SELECT id_marca FROM dim_marca WHERE marca = %s) "
                           "AND id_midia = (SELECT id_midia FROM dim_midia WHERE midia = %s) "
                           "AND id_campanha = (SELECT id_campanha FROM dim_campanha WHERE campanha = %s) "
                           "AND investimento = %s AND receita = %s AND impressoes = %s AND cliques = %s "
                           "AND sessoes = %s AND usuarios = %s AND visualizacoes = %s AND conversoes = %s",
                           (row['Data'], row['Marca'], row['Midia'], row['Campanha'], row['Investimento'],
                            row['Receita'], row['Impressões'], row['Cliques'], row['Sessões'], row['Usuários'],
                            row['Visualizações'], row['Conversões']))
            result = cursor.fetchone()
            if not result:
                cursor.execute("INSERT INTO fato_analise (id_data, id_marca, id_midia, id_campanha, investimento, "
                               "receita, impressoes, cliques, sessoes, usuarios, visualizacoes, conversoes) "
                               "VALUES ((SELECT id_data FROM dim_tempo WHERE data = %s), "
                               "(SELECT id_marca FROM dim_marca WHERE marca = %s), "
                               "(SELECT id_midia FROM dim_midia WHERE midia = %s), "
                               "(SELECT id_campanha FROM dim_campanha WHERE campanha = %s), "
                               "%s, %s, %s, %s, %s, %s, %s, %s)",
                               (row['Data'], row['Marca'], row['Midia'], row['Campanha'], row['Investimento'],
                                row['Receita'], row['Impressões'], row['Cliques'], row['Sessões'], row['Usuários'],
                                row['Visualizações'], row['Conversões']))
        connection.commit()
        cursor.close()
        print("Dados inseridos na tabela fato_analise.")
    except mysql.connector.Error as err:
        print("Erro ao inserir dados na tabela fato_analise: {}".format(err))


data = pd.read_excel(r'C:\Users\vanes\Desktop\Cadastra_Case\base_dados_case_cadastra.xlsx')

data.columns = data.columns.str.strip()

connection = connect_to_database()

if connection:
    insert_into_dim_tempo(connection, data)
    insert_into_dim_marca(connection, data)
    insert_into_dim_midia(connection, data)
    insert_into_dim_campanha(connection, data)
    insert_into_fato_analise(connection, data)
    connection.close()
else:
    print("Não foi possível conectar ao banco de dados.")
