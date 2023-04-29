

class Environment:
    def __init__(self):
        pass

    def get_user_credentials():
        with open("./env.eniac", "r") as f:
            data = f.readlines()
            for line in data:
                if "IQOPTION_EMAIL" in line:
                    user_email = line.split("=")[1].strip()
                elif "IQOPTION_PASSWORD" in line:
                    user_password = line.split("=")[1].strip()
        return [user_email, user_password]