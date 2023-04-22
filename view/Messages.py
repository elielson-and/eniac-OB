from colorama import Fore, Style

class Message:
    
    def success(message):
        return Fore.GREEN +  "\u2714 " + message + Style.RESET_ALL
    
    def info(message):
        return Fore.BLUE + "\u2192 " + message + Style.RESET_ALL
    
    def alert(message):
        return Fore.YELLOW + "\u26A0 " + message + Style.RESET_ALL
    
    def danger(message):
        return Fore.RED + "\u2717 " + message + Style.RESET_ALL
    