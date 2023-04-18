import mysql.connector
from colorama import Fore, Style
import os
import sys
sys.path.append("../../")
from view.Messages import Message

class ConexaoMySQL:
    connection = None
    
    def __init__(self):
         with open("./env.eniac", "r") as f:
            data = f.readlines()

            for line in data:
                if "DB_HOST" in line:
                    self.host = line.split("=")[1].strip()

                elif "DB_NAME" in line:
                    self.dbname = line.split("=")[1].strip()

                elif "DB_USER" in line:
                    self.user = line.split("=")[1].strip()

                elif "DB_PASSWORD" in line:
                    self.passwd = line.split("=")[1].strip()

                elif "DB_SLF_CONN" in line:
                    self.connection = line.split("=")[1].strip()
    
    # Open connection
    def connect(self):
        try:
            ConexaoMySQL.connection = mysql.connector.connect(
                host=self.host,
                database=self.dbname,
                user=self.user,
                passwd=self.passwd
            )
            if self.connection.is_connected():
                os.system('cls||clear')
                return Message.success("Base de dados conectada!")
        except mysql.connector.Error as error:
            os.system('cls||clear')
            return Message.danger("Erro ao conectar à base de dados! Detalhamento: \n {}".format(error))
        
    # Consult
    def consult(self, query): # This one returns a value
        try:
            sql = self.connection.cursor(dictionary=True)
            sql.execute(query)
            return sql.fetchall()
        
        except mysql.connector.Error as error:
            return "Erro na consulta: {}".format(error)
        
    # Run a script
    def run(query):
        try:
            sql = ConexaoMySQL.connection.cursor(dictionary=True)
            sql.execute(query)
            return sql.fetchone()
            
        except mysql.connector.Error as error:
            return Message.danger("Erro na execução de código SQL: \n {}".format(error))
        # finally:
        #     if connection.is_connected():
        #         sql.close()
        #         connection.close()


    # Close connection
    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()
            return "Conexão fechada com sucesso!"
