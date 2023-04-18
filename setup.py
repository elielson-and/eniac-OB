
import time
from .view.SplashScreen import SplashScreen

from config.database.Connection import ConexaoMySQL
from config.database.validations.CheckDatabase import CheckDatabase 


SplashScreen.show()



#dbCheck = CheckDatabase

# Apresentação da splash

#dbCheck.checkDatabase()
# conexao = ConexaoMySQL()
# print(conexao.connect())