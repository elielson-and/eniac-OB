import time
import sys
import os
from iqoptionapi.stable_api import IQ_Option
from app.Controller.Chart import Chart 
from engine.Analyzer import Analyzer
from engine.Asset import Asset
from view.Messages import Message
from engine.Trade import Trade
from config.Environment.Environment import Environment as Env
from .DirectionAnalizer import DirectionAnalizer as Direction
from database.Connection import ConexaoMySQL 

class Runner:
    def __init__(self) -> None:
        # MySQL
        self.cnn = ConexaoMySQL()
        self.cnn.connect()

        # IQ Option
        self.api = IQ_Option(Env.get_iqoption_user_credentials())
        header={"User-Agent":r"Mozilla/5.0 (X11; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0"}
        cookie={"Iq":"GOOD"}
        self.api.set_session(header,cookie)
        self.api.connect()
        self.api.change_balance("PRACTICE")
        
      

    def start_application(self):
        #---Instances---

        chart = Chart(self.api)
        analyzer = Analyzer(self.api)
        trade = Trade(self.api)
        direction = Direction(self.api)

        # Runner
        while True:
            for asset in chart.get_all_available_assets():
                if(analyzer.is_asset_elegible_to_trade(asset, chart.get_payout(asset))):

                    trade_direction = direction.trade_direction(
                        analyzer.get_support_resistance_v2(asset),
                        analyzer.analyze_mhi_strategy(asset),
                        chart.get_chart_trend(asset)
                    )

                    trade.buy(asset, trade_direction, chart.get_payout(asset))
                   
                else:
                    print("Chart conditions: " + Message.txt_red("[ BAD ]") + "\n--------------")

            # -------
            os.system('cls||clear')
            
            
            
                

            
           


       