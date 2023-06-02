from view.SplashScreen import SplashScreen
from app.Checkers.Checker import Checker
from engine.Runner import Runner
from view.Messages import Message
from database.Connection import ConexaoMySQL
import datetime

SplashScreen.show()
checker = Checker()

rn = Runner()
rn.start_application()

