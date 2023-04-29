

class Environment:
    def __init__(self):
        pass


    #---------------------------------------------------------
    #| Obtains and return all database credentials from env file
    #---------------------------------------------------------
    def get_mysql_server_credentials():
        with open("./env.eniac", "r") as f:
            data = f.readlines()

            for line in data:
                if "DB_HOST" in line:
                    db_host = line.split("=")[1].strip()

                elif "DB_NAME" in line:
                    db_name = line.split("=")[1].strip()

                elif "DB_USER" in line:
                    db_user = line.split("=")[1].strip()

                elif "DB_PASSWORD" in line:
                    db_passwd = line.split("=")[1].strip()

                elif "DB_SLF_CONN" in line:
                    db_connection = line.split("=")[1].strip()
        return {"host":db_host,"name": db_name, "user":db_user, "password":db_passwd, "slf":db_connection}
    
    #-----------------------------------------------------------------
    #| Obtains and return all iqoption user credentials from env file
    #-----------------------------------------------------------------
    def get_iqoption_user_credentials(): 
        with open("./env.eniac", "r") as f:
            data = f.readlines()
            for line in data:
                if "IQOPTION_EMAIL" in line:
                    user_email = line.split("=")[1].strip()
                elif "IQOPTION_PASSWORD" in line:
                    user_password = line.split("=")[1].strip()
        return {"email":user_email, "password":user_password}
    
    #-----------------------------------------------------------------
    #| Get user choice about operation modality
    #-----------------------------------------------------------------
    def get_iqoption_modality(): 
        with open("./env.eniac", "r") as f:
            data = f.readlines()
            for line in data:
                if "MODALITY" in line:
                    modality = line.split("=")[1].strip().lower()
                
        return modality
    
    #-----------------------------------------------------------------
    #| Get user choice about OTC/UTC
    #-----------------------------------------------------------------
    def can_trade_otc(): 
        with open("./env.eniac", "r") as f:
            data = f.readlines()
            for line in data:
                if "ALLOW_OTC" in line:
                    choice = line.split("=")[1].strip().lower()
                    if(choice == "yes"):
                        return True
                    else:
                        return False