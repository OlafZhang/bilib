# 我知道你会再来这里，所以我放出监视你（偷我视频的人）的代码
# 我怀疑就是发出issue的人搞的，不然就不会删除issue
# 等着瞧，这个代码会在树莓派长期运行

from os import execv
import bilib
import requests
import json
import time


FUCKER_video_counter = 0
FUCKER_newest_video_number = 0

def send_notice_ifttt(text):
	url = f"https://maker.ifttt.com/trigger/home_inside_network_issue/with/key/"
	payload = {"value1": text}
	headers = {"Content-Type": "application/json"}
	while True:
                response = requests.request("POST",url,data=json.dumps(payload),headers=headers)
                if str(response.text)[0:15] == 'Congratulations':
                    print(str(text))
                    break
                else:
                    print("Resending...")

while True:
    FUCKER_video_list = bilib.up_video_list(402157092,1)['video_list']
    while True:
        try:
            FUCKER_video_list[FUCKER_video_counter]
            print(("===第%s个视频===")%(str(FUCKER_video_counter+1)))
            print("标题：",end="")
            print(FUCKER_video_list[FUCKER_video_counter]["title"])
            print("BVID：",end="")
            print(FUCKER_video_list[FUCKER_video_counter]["bvid"])
            print("描述：",end="")
            print(FUCKER_video_list[FUCKER_video_counter]["description"])
            if FUCKER_video_counter > FUCKER_newest_video_number:
                message = str("那个逼发视频了：%s（%s）")%(str(FUCKER_video_list[FUCKER_video_counter]["title"]),str(FUCKER_video_list[FUCKER_video_counter]["bvid"]))
                send_notice_ifttt(message)
            else:
                pass
            FUCKER_video_counter += 1
        except KeyError:
            break
    time.sleep(600)
    
