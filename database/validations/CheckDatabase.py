import mysql.connector
from colorama import Fore, Style
import os
import sys
from ..Connection import ConexaoMySQL
sql = ConexaoMySQL



class CheckDatabase:
    def __init__(self):
        pass

    def checkDatabase():
        default_tables = ['logs'] # Add more tables here if necessary

        # print(Message.info("Verificando integridade da base de dados..."))
    
        for table in default_tables:
            if(sql.run("SHOW TABLES LIKE '{table}'")):
                #print(Message.success(table))
                pass
            else:
                #print(Message.danger(table))
                pass
        

        
    # def create_logs_table():
    #     cursor = conexao.cursor()
    #     tabela = """
    #     CREATE TABLE logs (
    #     id INT AUTO_INCREMENT PRIMARY KEY,
    #     nome VARCHAR(50) NOT NULL,
    #     idade INT
    #     )
    #     """
    #     cursor.execute(tabela)

    #     # Fechar a conexão com o banco de dados
    #     conexao.close()