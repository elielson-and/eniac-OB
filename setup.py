from view.SplashScreen import SplashScreen
from app.Checkers.Checker import Checker
from engine.Runner import Runner
from view.Messages import Message
from database.Connection import ConexaoMySQL
import datetime

# try:
#     # Crie uma instância da classe ConexaoMySQL
#     conexao = ConexaoMySQL()
#     conexao.connect()

#     # Chame o método insert na instância criada, fornecendo o argumento 'query'
#     conexao.insert("insert into error (title,description,date_occurred,is_test) values ('Erro generico','Descricao do erro','{datetime.datetime.now()}',1)")

#     print("Deu certo")
# except Exception as e:
#     print(e)

# SplashScreen.show()
# checker = Checker()

rn = Runner()

rn.start_application()

