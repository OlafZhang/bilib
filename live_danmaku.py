import bilib
import time
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

now_timestamp = 0
timesleep = 3
roomid = 1456133

print(("房间号：%s")%(str(roomid)))
print(("加载弹幕冷却时间：%s秒")%(str(timesleep)))
time.sleep(2)

while True:
    danmaku_list = bilib.listall_danmaku_live(roomid,type="room")
    for index,include in danmaku_list.items():
        if now_timestamp < int(include['timestamp']):
            now_timestamp = int(include['timestamp'])
            now_time = color_print(str(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(now_timestamp))),"GREEN")
            text = color_print(include['text'],"CYAN")
            name = color_print(include['name'],"YELLOW")
            uid = color_print(include['uid'],"YELLOW")
            print(("[%s](%s,%s)%s")%(str(now_time),str(name),str(uid),str(text)))
        else:
            continue
    time.sleep(timesleep)