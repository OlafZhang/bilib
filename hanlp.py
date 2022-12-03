import crack
import bilib
import os
from pyhanlp import HanLP # 使用前导入 HanLP工具
segment = HanLP.newSegment().enableNameRecognize(True)
crack.main()
import time

# 参数在这里

#video_id = "BV1J4411m7wk"
#cid = bilib.video_info(video_id)['video'][0]["cid"]
cid = 452005717
reason = 4

# 需自行创建COOKIE_FILE.txt，编码UTF-8
# 直接将所有Cookie粘贴即可，只允许有一行
# 例如： b_ut=-1; i-wanna-go-back=-1; _uuid=*******; buvid3=*****; CURRENT_BLACKGAP=0; ...
cookie_file = open("COOKIE_FILE.txt","r",encoding="utf-8")
for line in cookie_file.readlines():
    cookie = str(line).replace("\n","")
    break

ua = str("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0")

reason_list = {'0':'违法违禁','1':'色情低俗','2':'恶意刷屏','3':'赌博诈骗','4':'人身攻击','5':'侵犯隐私','6':'垃圾广告','7':'视频无关','8':'引战','9':'剧透','10':'青少年不良信息','11':'其它'}

dan_path = str(bilib.get_danmaku(cid,reset=False))
alist = bilib.listall_danmaku(str(dan_path))
for x,y in alist.items():
    result = segment.seg(str(y[8]))
    if str("/nr") in str(result):
        for i in result:
            if str("/nr") in str(i):
                keyword = str(i).replace("/nr","")
                break
            else:
                keyword = ""
        decode = crack.crackl4(str(y[6]))[0]
        dmid = str(y[7])
        os.system("cls")
        print(("弹幕ID：%s")%(dmid))
        print(("发送时间：%s")%(str(y[4])))
        print(("解析前的用户ID：%s")%(str(y[6])))
        try:
            user_info = bilib.user_info(decode)
            name = user_info["name"]
            uid = user_info["uid"]
            level = user_info["level"]
            print(("反解析的UID：%s")%(uid))
            print(("UID长度：%s")%(str(len(str(uid)))))
            print(("昵称：%s")%(name))
            print(("等级：%s")%(str(level)))
        except bilib.SeemsNothing:
            print("用户不存在或反解析失败")
        print(("发送的内容：%s")%(str(y[8])))
        if str(keyword[-1]) == str("f"):
            keyword = str(keyword)[0:-1]
        print(("识别出的关键词：%s")%(keyword))
        print("  ")
        while True:
            user_input = input(str(("以“%s”的原因举报此用户吗？[y/n]")%(reason_list[str(reason)])))
            user_input = str(user_input).lower()
            user_input = user_input.replace(" ","")
            if str(user_input) == str("y"):
                content =str("")
                if str(reason) == str("11"): 
                    while True:
                        content = str(input("需要说明原因，放弃举报输入“放弃”两个字："))
                        if len(content) == 0:
                            print("输入有误")
                        else:
                            if str(content) == str("放弃"):
                                content = ""
                                break
                            else:
                                break
                    if str(content) == str(""):
                        print("你选择了放弃举报")
                        break
                    else:
                        result = str(bilib.report_danmaku(cid, dmid, reason, cookie, ua, content=content))
                        print(str(("处理结果：%s")%(result)))
                        time.sleep(1.5)
                        break
                else:
                    result = str(bilib.report_danmaku(cid, dmid, reason, cookie, ua, content=content))
                    print(str(("处理结果：%s")%(result)))
                    time.sleep(1.5)
                    break
            elif str(user_input) == str("n"):
                print("此弹幕将不会举报",end="")
                time.sleep(0.25)
                print("\r此弹幕将不会举报.",end="")
                time.sleep(0.25)
                print("\r此弹幕将不会举报..",end="")
                time.sleep(0.25)
                print("\r此弹幕将不会举报...",end="")
                time.sleep(0.25)
                print("\r                   ",end="")
                print("\r此弹幕将不会举报",end="")
                time.sleep(0.25)
                print("\r此弹幕将不会举报.",end="")
                time.sleep(0.25)
                print("\r此弹幕将不会举报..",end="")
                time.sleep(0.25)
                print("\r此弹幕将不会举报...")
                time.sleep(0.25)
                break
            else:
                print("输入有误")
"""
| nr | 人名 |
| n | 名词 |
| v | 动词 |
| p | 介词 |
| g | 语素词 |
| h | 前接部分 |
"""