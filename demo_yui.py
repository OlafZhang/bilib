import bilib
info = bilib.video_comment(414943229)
for key,value in info.items():
    main_key = str(int(key) + 1)
    print("---------------------")
    print("第" + main_key + "条评论：")
    print("来自 " + value["uname"] + "(" + value["mid"] + ")," + value["sex"])
    print("其评论：" + value["message"])
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
            part_key = str(int(part_key))
            print("  |")
            print("---第" + main_key + "层下的第" + part_key + "条评论：")
            print("---来自 " + part_value["uname"] + "(" + part_value["mid"] + ")," + part_value["sex"])
            print("---其评论：" + part_value["message"])
            if part_value["up_like"] == True:
                print("---UP主觉得很赞")
            else:
                pass
            if part_value["up_reply"] == True:
                print("---UP主在此层回复了")
            else:
                pass
