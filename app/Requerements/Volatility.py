

class Volatility:
    def __init__(self) -> None:
        pass

    def is_favorable(IqOptionInstance): # True for high | False to low.
        intervalo = 5
        ativo = 'EURUSD'
        opcao = 'turbo'

        # Calcula a quantidade de segundos no intervalo de tempo desejado
        segundos_intervalo = intervalo * 60

        # Busca os dados de tick do ativo
        timestamp_atual = time.time()
        timestamp_inicial = timestamp_atual - segundos_intervalo
        dados_tick = IQ_Option_API.get_candles(ativo, 60, 100, timestamp_inicial)

        # Calcula a volatilidade do ativo
        somatorio = 0
        for i in range(0, 99):
            somatorio += abs(dados_tick[i]['close'] - dados_tick[i+1]['close'])

        volatilidade = somatorio / 99

        # Desconecta da API da IQOption
        IQ_Option_API.disconnect()

        # Verifica se a volatilidade está alta ou baixa
        if volatilidade > 0.0015:
            return True
        else:
            return False