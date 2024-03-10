from iqoptionapi import IQOptionAPI

def get_last_candle_data(api, ativo, timeframe):
  """
  Obtém dados do último candle finalizado de um ativo.

  Args:
    api: Instância da classe IQOptionAPI.
    ativo: Nome do ativo (ex: "EURUSD").
    timeframe: Intervalo de tempo do candle (ex: "5m").

  Returns:
    Dicionário com os dados do candle:
      * "open": preço de abertura
      * "close": preço de fechamento
      * "max": preço máximo
      * "min": preço mínimo
  """

  # Obtém o timestamp do último candle finalizado
  candle_timestamp = api.get_server_timestamp() - timeframe * 60

  # Obtém os dados do candle
  candles = api.get_candles(ativo, timeframe, 1, candle_timestamp)

  # Retorna os dados do candle
  if candles:
    return candles[0]
  else:
    return None

# Exemplo de uso
api = IQOptionAPI("elielsonand123@gmail.com", "andre4002e")

ativo = "EURUSD-OTC"
timeframe = "5m"

dados_candle = get_last_candle_data(api, ativo, timeframe)

if dados_candle:
  print(f"Preço de abertura: {dados_candle['open']}")
  print(f"Preço de fechamento: {dados_candle['close']}")
  print(f"Preço máximo: {dados_candle['max']}")
  print(f"Preço mínimo: {dados_candle['min']}")
else:
  print("Erro ao obter dados do candle.")
