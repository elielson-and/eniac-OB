import time
import os
from .Messages import Message
from config.Environment.Environment import Environment as Env

class SplashScreen:

    def show():
        os.system('cls||clear')
        print('\n')
        time.sleep(1)
        print(Message.success(f"2023 ENIAC - BOT | By: @elielson_and | V - {Env.project_version()}"))
        print("Carregando", end="")
        for i in range(30):
            print(".", end="", flush=True)
            time.sleep(0.08)
        print("\nConcluído!")
        os.system('cls||clear')