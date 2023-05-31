from view.Messages import Message
from database.Connection import ConexaoMySQL 
import sys
import datetime

class DataSeeder:
    
    def __init__():
        pass

    def save_trade_info(pos_id, asset, direction, modality, payout, amount, profit,result, project_version, is_test, is_otc, started_at, finished_at):
        cnn = ConexaoMySQL()
        cnn.connect()
        # ---
        try:
            print(Message.txt_yellow("Saving trade info..."))
            query = "INSERT INTO trade (position_id, asset, direction, modality, payout, investment, profit, trade_result, project_version, is_test, is_otc, started_at, finished_at) " + \
                    f"VALUES ('{pos_id}', '{asset}', '{direction}', '{modality}', '{payout}', '{amount}', '{profit}', '{result}','{project_version}', '{is_test}', '{is_otc}', '{started_at}', '{finished_at}');"
            
            cnn.insert(query)
            cnn.close_connection()
           
        except Exception as e:
            print(f"A tentativa de salvar a operacao deu errado: {e}")

    def save_error_info(self,is_test):
        cnn = ConexaoMySQL()
        cnn.connect()
        try:
            print(Message.txt_red("Saving error log..."))
            print(Message.txt_yellow("Saving trade info..."))
            query = f"INSERT INTO error (title,description,date_occurred,is_test) values ('Erro generico','Descricao do erro','{datetime.datetime.now()}',{is_test})" 
                    
            self.cnn.insert(query)
            self.cnn.close_connection()
           
        except Exception as e:
            print(f"A tentativa de salvar a operacao deu errado: {e}")