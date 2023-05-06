from view.SplashScreen import SplashScreen
from app.Checkers.Checker import Checker
from engine.Runner import Runner
from view.Messages import Message

SplashScreen.show()
checker = Checker()
rn = Runner()

try:    
    rn.start_application()
except Exception as exp:
    print(Message.general_error(exp))
