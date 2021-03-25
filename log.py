import time
from colorama import Fore, Back, Style

def color_print(string,color):
    output = ""
    if color == str("BLACK"):
        output = str(Fore.BLACK + str(string) + Style.RESET_ALL)
    elif color == str("RED"):
        output = str(Fore.RED + str(string) + Style.RESET_ALL)
    elif color == str("GREEN"):
        output = str(Fore.GREEN + str(string) + Style.RESET_ALL)
    elif color == str("YELLOW"):
        output = str(Fore.YELLOW + str(string) + Style.RESET_ALL)
    elif color == str("BLUE"):
        output = str(Fore.BLUE + str(string) + Style.RESET_ALL)
    elif color == str("MAGENTA"):
        output = str(Fore.MAGENTA + str(string) + Style.RESET_ALL)
    elif color == str("CYAN"):
        output = str(Fore.CYAN + str(string) + Style.RESET_ALL)
    elif color == str("WHITE"):
        output = str(Fore.WHITE + str(string) + Style.RESET_ALL)
    else:
        output = str(string)
    return output

def log_write(message,path,level,service,outprint=True,color_enable=True):
    time_raw = time.localtime(time.time())
    time_now = time.strftime("%Y-%m-%d %H:%M:%S",time_raw)
    time_now_raw = str("[" + str(time_now) + "]")
    log_message = str("")
    log_message_raw = str("")
    log_message_raw += time_now_raw
    if color_enable:
        time_now = str("[" + color_print(str(time_now),"CYAN") + "]")
    else:
        time_now = str("[" + str(time_now) + "]")
    log_message += time_now
    level_no = int(level)
    if level_no == 0:
        level = str("DEBUG")
    elif level_no == 1:
        level = str("INFO")
    elif level_no == 2:
        level = str("REMIND")
    elif level_no == 3:
        level = str("WARNING")
    elif level_no == 4:
        level = str("CRITICAL")
    elif level_no == 5:
        level = str("ERROR")
    elif level_no == 6:
        level = str("CRISIS")
    elif level_no == 7:
        level = str("CRASH")
    else:
        level = str("NOTYPE")
    level_raw = str(" <" + level + "> ")
    log_message_raw += level_raw
    if color_enable:
        if level_no == 0:
            level = str(" <" + level + "> ")
        elif level_no == 1:
            level = str(" <" + color_print(str(level),"GREEN") + "> ")
        elif level_no == 2 or level_no == 3:
            level = str(" <" + color_print(str(level),"YELLOW") + "> ")
        elif level_no == 4:
            level = str(" <" + color_print(str(level),"MAGENTA") + "> ")
        elif level_no >= 5 and level_no <= 7:
            level = str(" <" + color_print(str(level),"RED") + "> ")
        else:
            level = str(" <" + level + "> ")
    else:
        level = str(" <" + level + "> ")
    log_message += level
    
    try:
        service_raw = str("" + service + "")
        log_message_raw += service_raw
        if color_enable:
            service = str("" + color_print(service,"BLUE") + "")
        else:
            service = str("" + service + "")
        log_message += service
    except:
        pass
    log_message += str(": ")
    log_message += str(message)
    log_message_raw += str(": ")
    log_message_raw += str(message)
    if outprint:
        print(log_message)
    try:
        log_file = open(path,"a+",encoding="utf-8")
        log_file.write(log_message_raw)
        log_file.write("\n")
        log_file.close()
    except:
        pass

