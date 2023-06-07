

class DirectionAnalizer:
    def __init__(self,api) -> None:
        #------- Trade execution variables --------
        self.sup_res = ""
        self.mhi_sugestion = ""
        self.chart_trend = ""
        #--- 
        self.call_option = 0
        self.put_option = 0
        # self.is_candles_small = False


    
    def trade_direction(self, sup_res, mhi, trend):
        # Sup and res
        if sup_res == 'support':
            self.call_option += 1
        elif sup_res == 'resistance':
            self.put_option += 1

        # Mhi 
        if mhi == 'call':
            self.call_option += 2
        elif mhi == 'put':
            self.put_option += 2   
        
        # Chart trend
        if trend == 'high':
            self.call_option += 1
        elif trend == 'low':
            self.put_option +=1


        # Decision

        if self.call_option > self.put_option:
            print("OPERACAO: CALL")
            return 'call'
        elif self.put_option > self.call_option:
            print("OPERACAO: PUT")
            return 'put'
        elif self.call_option == self.put_option:
            print("OPERACAO: EMPATE DE PARAMETROS")
            return 'error'


