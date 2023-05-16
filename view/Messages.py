from colorama import Fore, Style
import time
class Message:
    
    # Dynamic Messages ---------------------

    def success(message):
        return Fore.GREEN +  "\u2714 " + message + Style.RESET_ALL
    
    def info(message):
        return Fore.BLUE + "\u2192 " + message + Style.RESET_ALL
    
    def alert(message):
        return Fore.YELLOW + "\u26A0 " + message + Style.RESET_ALL
    
    def danger(message):
        return Fore.RED + "\u2717 " + message + Style.RESET_ALL
    

    # Text colors ---------------------
    def txt_blue(text):
        return Fore.BLUE + text + Style.RESET_ALL
    
    def txt_red(text):
        return Fore.RED + text + Style.RESET_ALL
    
    def txt_yellow(text):
        return Fore.YELLOW + text + Style.RESET_ALL
    
    def txt_green(text):
        return Fore.GREEN + text + Style.RESET_ALL
    
    def txt_cyan(text):
        return Fore.CYAN + text + Style.RESET_ALL
  
    # Static Messages ---------------------
    
    def general_error(error_details):
        # Send log to database here with the error_details
        return Fore.RED + "\n[GENERAL ERROR - "+ str(time.time()) + "]" + "\nA general error has ocurred. please see logs for more information." + Style.RESET_ALL