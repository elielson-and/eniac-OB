
import time
from view.SplashScreen import SplashScreen
from app.Checkers.Checker import Checker
from engine.Runner import Runner
from database.Connection import ConexaoMySQL
import curses

SplashScreen.show()
checker = Checker()

rn = Runner()
rn.start_application()