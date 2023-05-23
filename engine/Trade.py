import sys
from view.Messages import Message
from config.Environment.Environment import Environment as Env
import time 
class Trade:
    def __init__(self, api) -> None:
        self.api = api


    # -- operational

    def buy(self, asset, direction):
        print(Message.txt_yellow(f'[{asset}]') + '- Iniciando operação - ' + Message.txt_red(direction))

        _,id=(self.api.buy_digital_spot(asset,5,direction,1))
        print(id)
        if id !="error":
            while True:
                check,win=self.api.check_win_digital_v2(id)
                if check==True:
                    break
            if win<0:
                print("you loss "+str(win)+"$")
            else:
                print("you win "+str(win)+"$")
        else:
            print("please try again")
        
        sys.exit()

    def sell(): # Put
        pass

    def sell_before_finish():
        pass

