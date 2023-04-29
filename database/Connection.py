import mysql.connector
from colorama import Fore, Style
import os
import sys
sys.path.append("../../")
from view.Messages import Message
from config.Environment.Environment import Environment

class ConexaoMySQL:
    connection = None
    
    def __init__(self):
         pass

    # Open connection
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host        = Environment.get_mysql_server_credentials()["host"],
                user        = Environment.get_mysql_server_credentials()["user"],
                password    = Environment.get_mysql_server_credentials()["password"],
                database    = Environment.get_mysql_server_credentials()["name"],
            )
            return True
        except mysql.connector.Error as e:
            return False
    
    def check_db_connection(self):
        if self.connection is not None:
            return True
        else:
            return False
        
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
