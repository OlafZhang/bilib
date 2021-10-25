import crack
import bilib
import os
from pyhanlp import HanLP # 使用前导入 HanLP工具
segment = HanLP.newSegment().enableNameRecognize(True)
crack.main()
import time

# 参数在这里

video_id = "BV1gL4y1a7Fs"
reason = 4
cookie = str(r"b_ut=-1; i-wanna-go-back=-1; _uuid=9F63B883-5436-2510-C0E8-FCA2CD415ACC08758infoc; buvid3=968CF330-C292-4110-AA7B-54BE9D251004148804infoc; CURRENT_BLACKGAP=0; CURRENT_FNVAL=976; blackside_state=1; rpdid=|(k|k)mR~~kk0J'uYJkRmuRkk; DedeUserID=4670418; DedeUserID__ckMd5=4c838627b4f771e8; SESSDATA=0f5c33cb%2C1648043458%2Ce5a84*91; bili_jct=03ae531804a4e9a54b87f69b2a5a1e75; PVID=2; bp_video_offset_4670418=580192133996157076; CURRENT_QUALITY=80; bp_t_offset_4670418=579766541390622780; dy_spec_agreed=1; LIVE_BUVID=AUTO3616333962855780; fingerprint3=de99c73ecbc97fcc75c0fdc8c69456fe; fingerprint=d6e8026be183bbb1abaa02ebf1c3b32c; fingerprint_s=6b9dcd8748af972e3e53a4bca2dfbcf8; buvid_fp=968CF330-C292-4110-AA7B-54BE9D251004148804infoc; buvid_fp_plain=968CF330-C292-4110-AA7B-54BE9D251004148804infoc; innersign=1; sid=j3hyedlt; bfe_id=1bad38f44e358ca77469025e0405c4a6")
ua = str("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0")

reason_list = {'0':'违法违禁','1':'色情低俗','2':'恶意刷屏','3':'赌博诈骗','4':'人身攻击','5':'侵犯隐私','6':'垃圾广告','7':'视频无关','8':'引战','9':'剧透','10':'青少年不良信息','11':'其它'}

cid = bilib.video_info(video_id)['video'][0]["cid"]
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
                        time.sleep(3)
                        break
                else:
                    result = str(bilib.report_danmaku(cid, dmid, reason, cookie, ua, content=content))
                    print(str(("处理结果：%s")%(result)))
                    time.sleep(3)
                    break
            elif str(user_input) == str("n"):
                print("此弹幕将不会举报",end="")
                time.sleep(0.5)
                print("\r此弹幕将不会举报.",end="")
                time.sleep(0.5)
                print("\r此弹幕将不会举报..",end="")
                time.sleep(0.5)
                print("\r此弹幕将不会举报...",end="")
                time.sleep(0.5)
                print("\r                   ",end="")
                print("\r此弹幕将不会举报",end="")
                time.sleep(0.5)
                print("\r此弹幕将不会举报.",end="")
                time.sleep(0.5)
                print("\r此弹幕将不会举报..",end="")
                time.sleep(0.5)
                print("\r此弹幕将不会举报...")
                time.sleep(0.5)
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