
import time
from view.SplashScreen import SplashScreen
from app.Checkers.Checker import Checker
from database.Connection import ConexaoMySQL
import curses


SplashScreen.show()

# Running checkers before start
checker = Checker()
