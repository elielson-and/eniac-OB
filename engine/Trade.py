import sys
import os
from view.Messages import Message
from config.Environment.Environment import Environment as Env
from database.DataSeeder import DataSeeder as ds
import datetime, time 




class Trade:
    def __init__(self, api):
        self.api = api
        self.position_id = ''
        self.modality = Env.trade_modality()
        self.investment = Env.cash_amount()
        self.project_version = Env.project_version()
        self.is_test = Env.is_test()
        self.is_otc = Env.allow_otc()
    # -- Trade temp variables


    def buy(self, asset, direction, payout):
    
        print(Message.txt_yellow(f'[{asset}]') + '- Iniciando operação - ' + Message.txt_red(direction))
        start_time = datetime.datetime.now()
        try:
            if direction != 'error':
                _,self.position_id = (self.api.buy_digital_spot(asset, Env.cash_amount(),direction, Env.candle_period()))
                print("Waiting for result...")
            
            if self.position_id != "error":
                while True:
                    check,status=self.api.check_win_digital_v2(self.position_id)
                    if check == True:
                        break
                if status < 0:
                    result = 'loss'
                    print(Message.txt_red(f"LOSS: ${status}"))
                else:
                    print(Message.txt_green(f"WIN: ${status}"))
                    result = 'win'
                
                end_time = datetime.datetime.now()
                ds.save_trade_info(self.position_id, asset, direction, self.modality, payout, Env.cash_amount(), str(round(status, 2)),result, Env.project_version(), Env.project_name(), Env.is_test(), Env.allow_otc(), start_time, end_time)
            else:
                print(Message.txt_red("ERROR WHEN MAKE TRADE"))
                ds.save_error_info('Trade error',self.position_id, Env.is_test())

            # Save all trde information
            
        except Exception as error:
            # Save error details
            ds.save_error_info('Buy error Exception',error, Env.is_test())

        

            
        
    


