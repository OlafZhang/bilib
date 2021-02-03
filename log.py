import time
def log_write(message,path,level,service,outprint=True):
    time_raw = time.localtime(time.time())
    time_now = time.strftime("%Y-%m-%d %H:%M:%S",time_raw)
    time_now = str("[" + str(time_now) + "]")
    level = int(level)
    if level == 0:
        level = str("DEBUG")
    elif level == 1:
        level = str("INFO")
    elif level == 2:
        level = str("REMIND")
    elif level == 3:
        level = str("WARNING")
    elif level == 4:
        level = str("CRITICAL")
    elif level == 5:
        level = str("ERROR")
    elif level == 6:
        level = str("CRISIS")
    elif level == 7:
        level = str("CRASH")
    else:
        level = str("NOTYPE")
    level = str(" <" + str(level) + "> ")
    log_message = str("")
    log_message += time_now
    log_message += level
    try:
        service = str("" + service + "")
        log_message += service
    except:
        pass
    log_message += str(": ")
    log_message += str(message)
    if outprint:
        print(log_message)
    try:
        log_file = open(path,"a+",encoding="utf-8")
        log_file.write(log_message)
        log_file.write("\n")
        log_file.close()
    except:
        pass