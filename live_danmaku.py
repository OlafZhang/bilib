import bilib
import time
import sys
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

# 模式0：直接输入直播间ID
# 模式1：根据UID查直播间ID
# 模式2：根据UID查直播间ID（即使未开播也尝试显示弹幕）
mode = 2

now_timestamp = 0
timesleep = 3
roomid = 5265
uid = 4549624

if mode == 0:
    pass
else:
    userinfo = bilib.user_info(uid)
    status = int(userinfo["liveStatus"])
    roomid = userinfo["stream_room_id"]
    name = userinfo["name"]
    print(("%s(UID：%s)的直播间号为%s")%(color_print(str(name),"CYAN"),color_print(str(uid),"MAGENTA"),color_print(str(roomid),"GREEN")))
    if mode == 1 and status == 0:
        print("[" + color_print("警告","RED") + "]该直播间没有开播！")
        print("使用" + color_print("模式2","YELLOW") + "以尝试强制输出弹幕")
        sys.exit(1)
    else:
        pass


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