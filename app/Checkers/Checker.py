import time
import sys
import os
from database.Connection import ConexaoMySQL
from view.Messages import Message

from iqoptionapi.stable_api import IQ_Option

class Checker:
    def __init__(self):
        os.system('cls||clear')
        print(Message.info("Iniciando auto-teste de integridade do ambiente..."))
        time.sleep(4)
        os.system('cls||clear')
        self.check_connection()
        #self.check_iqoption_api()
        #Futuramente add verificacao de arquivos, pastas

    def check_connection(self):
        print(Message.info("Checando conexão com a base de dados...")) 
        cnn = ConexaoMySQL()
        cnn.connect()
        if(cnn.connect()):
            print(Message.success("Conexão com MySql remoto estabelecida!"))
        else:
            print(Message.danger("[Inicialização interrompida]: Erro ao conectar com o banco de dados, verifique \nas credenciais no arquivo (env.eniac) e tente novamente."))
            sys.exit() # Encerra o programa
        

    # def check_iqoption_api(self):
    #     print(Message.info("Conectando à API IQOption...")) 
        
    #     with open("./env.eniac", "r") as f:
    #         data = f.readlines()

    #         for line in data:
    #             if "IQOPTION_EMAIL" in line:
    #                 self.email = line.split("=")[1].strip()
    #             elif "IQOPTION_EMAIL" in line:
    #                 self.passwd = line.split("=")[1].strip()
        
    #     print(self.email)
    #     print(self.passwd)
                    
        # API = IQ_Option("elielsonandre123@gmail.com","Andre4002!")
        # print(API.check_connect())