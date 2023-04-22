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
        time.sleep(2)
        os.system('cls||clear')
        
        self.check_project_files()
        self.check_db_connection()
        self.check_iqoption_api()
        print("\n" + Message.success("AUTO-TESTE FINALIZADO! PROSSEGUINDO...")) 
        time.sleep(2)
        os.system('cls||clear')

    def check_project_files(self):
        print(Message.info("Verificando integridade dos arquivos...")) 
        project_files = ["app", "database", "iqoptionapi", "view","env.eniac","requirements.txt"]

        project_dir = os.getcwd()

        for file in project_files:
            if not os.path.exists(os.path.join(project_dir, file)):
                print(Message.danger("Estão faltando pastas e/ou arquivos nas dependências do projeto!")) 
                sys.exit()
        # Se todos os arquivos/pastas existirem, a função retorna True
        print(Message.success("Arquivos de dependência ok!")) 


    def check_db_connection(self):
        print(Message.info("Checando conexão com a base de dados...")) 
        cnn = ConexaoMySQL()
        cnn.connect()
        if(cnn.connect()):
            print(Message.success("Conexão com a base de dados estabelecida!"))
        else:
            print(Message.danger("[Inicialização interrompida]: Erro ao conectar com o banco de dados, verifique \nas credenciais no arquivo (env.eniac) e tente novamente."))
            sys.exit() # Encerra o programa
        

    def check_iqoption_api(self):
        print(Message.info("Conectando-se à API IQOption...")) 
        # self.email = ""
        # self.passwd = ""
        with open("./env.eniac", "r") as f:
            data = f.readlines()

            for line in data:
                if "IQOPTION_EMAIL" in line:
                    self.email = line.split("=")[1].strip()
                elif "IQOPTION_PASSWORD" in line:
                    self.passwd = line.split("=")[1].strip()

        iqoption = IQ_Option(self.email, self.passwd)
        check,reason = iqoption.connect()
        if (check):
            print("Conectado")
        else:
            print("Erro")
        sys.exit()
