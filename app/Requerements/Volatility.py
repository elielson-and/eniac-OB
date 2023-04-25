
import time
import sys
class Volatility:
    def __init__(self, api) -> None:
        self.api = api

    def is_volatility_high(self): # True for high | False to low.
        
        intervalo = 5
        ativo = 'EURUSD'
        opcao = 'turbo'

        # Calcula a quantidade de segundos no intervalo de tempo desejado
        segundos_intervalo = intervalo * 60

        # Busca os dados de tick do ativo
        timestamp_atual = time.time()
        timestamp_inicial = timestamp_atual - segundos_intervalo
        dados_tick = self.api.get_candles(ativo, 60, 100, timestamp_inicial)

        # Calcula a volatilidade do ativo
        somatorio = 0
        for i in range(0, 99):
            somatorio += abs(dados_tick[i]['close'] - dados_tick[i+1]['close'])

        volatilidade = somatorio / 99

        # Desconecta da API da IQOption
        #self.api.disconnect()

        # Verifica se a volatilidade está alta ou baixa
        if volatilidade > 0.0015:
            print("Alta volatilizade identificada")
            # return True
        else:
            print("Baixa volatilidade identificada")
            # return False


            