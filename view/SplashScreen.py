import time
import os
from .Messages import Message

class SplashScreen:

    def show():
        os.system('cls||clear')
        print('\n')
        time.sleep(1)
        print(Message.success("2023 ENIAC - BOT | By: @elielson_and"))
        print("Carregando", end="")
        for i in range(30):
            print(".", end="", flush=True)
            time.sleep(0.08)
        print("\nConcluído!")
        os.system('cls||clear')