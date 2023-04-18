import time
import os

class SplashScreen:

    def show():
        print("Carregando... ", end="")
        for i in range(10):
            print(".", end="", flush=True)
            time.sleep(0.3)
            print("\nConcluído!")
        os.system('cls||clear')