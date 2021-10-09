import time
from datetime import datetime
from colorama import init,Fore,Back,Style
init(autoreset=True)

def color_print(string,color):
    output = ""
    color == str(color)
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
    date_now = time.strftime("%Y-%m-%d",time_raw)
    human_read_week = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    week_now = human_read_week[int(datetime.now().weekday())]
    time_now = time.strftime("%H:%M:%S",time_raw)
    time_now = str(date_now + " " + week_now + " " + time_now)
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
    level_list = ["DEBUG","INFO","REMIND","WARNING","CRITICAL","ERROR","CRISIS"]
    try:
        level = str(level_list[level_no])
    except IndexError:
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

