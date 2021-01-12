import bilib
import time
def show_comment(aid,page = 1,video = True):
    info = bilib.video_comment(aid = aid,page=page,video=video)
    for key,value in info.items():
        total_page = value["total_page"]
        print("第" + str(page) + "页/共" + str(total_page) + "页")
        break
    for key,value in info.items():
        if str(key).isdigit():
            main_key = str(int(key) + 1)
        else:
            main_key = str(key)
        print("---------------------")
        print("第" + main_key + "条评论：")
        ctime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(value["ctime"]))
        print("发送时间：" + ctime)
        print("评论ID：" + str(value["rpid"]))
        print("此楼评论总数：" + str(value["rcount"]))
        print("来自 " + value["uname"] + "(" + value["mid"] + ")," + value["sex"])
        print("其评论：" + value["message"])
        print("点赞数：" + str(value["like"]))
        if value["up_like"] == True:
            print("UP主觉得很赞")
        else:
            pass
        if value["up_reply"] == True:
            print("UP主在此层回复了")
        else:
            pass
        if str(value["replies_item"]) == str("None"):
            print("此层无回复")
        else:
            replies_item = {}
            replies_item = value["replies_item"]
            for part_key,part_value in replies_item.items():
                if str(key).isdigit():
                    part_key = str(int(part_key))
                else:
                    part_key = str(part_key)
                print("  |")
                print("---第" + main_key + "层下的第" + part_key + "条评论：")
                ctime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(part_value["ctime"]))
                print("   ---发送时间：" + ctime)
                print("   ---评论ID：" + str(part_value["rpid"]))
                print("   ---来自 " + part_value["uname"] + "(" + part_value["mid"] + ")," + part_value["sex"])
                print("   ---其评论：" + part_value["message"])
                print("   ---点赞数：" + str(part_value["like"]))
                if part_value["up_like"] == True:
                    print("   ---UP主觉得很赞")
                else:
                    pass
                if part_value["up_reply"] == True:
                    print("   ---UP主在此层回复了")
                else:
                    pass
show_comment(bilib.video_info("BV117411p7US")["aid"])

for i in range(14,57 + 1):
    show_comment(2543959,page = i)
    time.sleep(3)
