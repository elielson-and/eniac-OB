

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


    
    # Engine to return Just Call or Put
    # def trade_direction(self, sup_res, mhi, trend):
    #     # Sup and res
    #     if sup_res == 'support':
    #         self.call_option += 1
    #     elif sup_res == 'resistance':
    #         self.put_option += 1

    #     # Mhi 
    #     if mhi == 'call':
    #         self.call_option += 2
    #     elif mhi == 'put':
    #         self.put_option += 2   
        
    #     # Chart trend
    #     if trend == 'high':
    #         self.call_option += 1
    #     elif trend == 'low':
    #         self.put_option +=1


    #     # Decision

    #     if self.call_option > self.put_option:
    #         print("OPERACAO: CALL")
    #         return 'call'
    #     elif self.put_option > self.call_option:
    #         print("OPERACAO: PUT")
    #         return 'put'
    #     elif self.call_option == self.put_option:
    #         print("OPERACAO: EMPATE DE PARAMETROS")
    #         return 'error'


    def trade_direction(self, sup_res, mhi, trend, other_indicator = 0):
        # Define os pesos para cada circunstância
        weights = {
            'support': 0.5,
            'resistance': 0.5,
            'call': 1,
            'put': 1,
            'high': 0.5,
            'low': 0.5,
            #'other_indicator': 1
        }

        # Calcula a pontuação para cada circunstância
        scores = {
            'call_option': weights['support'] * (sup_res == 'support') +
                        weights['call'] * (mhi == 'call') +
                        weights['high'] * (trend == 'high') ,
                        #weights['other_indicator'] * other_indicator,

            'put_option': weights['resistance'] * (sup_res == 'resistance') +
                        weights['put'] * (mhi == 'put') +
                        weights['low'] * (trend == 'low') 
                       # weights['other_indicator'] * (1 - other_indicator)
        }

        # Decision
        if scores['call_option'] > scores['put_option']:
            print("OPERACAO: CALL")
            return 'call'
        elif scores['put_option'] > scores['call_option']:
            print("OPERACAO: PUT")
            return 'put'
        else:
            print("OPERACAO: EMPATE DE PARAMETROS")
            return 'error'