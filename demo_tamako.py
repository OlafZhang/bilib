# 这是一个demo，演示如何通过一个番剧的media ID(介绍页以md开头的数字)获取番剧详细信息，包括season_id,av,bv,cid等等
# 此 media ID 有多个，默认为玉子市场TV版
# 同时下载全部弹幕文件，转换为ass后重命名
# 这是一个API用的比较全面的demo，可供参考

# -*- coding: utf-8 -*-
import bilib
import os

full_text = str("")

def outprint(string):
    global full_text
    print(string)
    full_text += str(string)
    full_text += "\n"

def get_full_info(mediaID,get_dan = False,tofile = False):
    base_info = bilib.anime_base_info(mediaID)
    season_id = int(base_info["season_id"])
    episode_info = bilib.anime_episode_info(season_id)
    outprint("-----------大纲-----------")
    outprint("名称：" + str(base_info["title"]))
    anime_full_name = str(base_info["title"])
    outprint("简介：" + str(base_info["desc"]))
    outprint("地区：" + str(base_info["area"]))
    outprint("类型：" + str(base_info["type"]))
    if str("上映") in str(base_info["episode"]):
        outprint("上映时间：" + str(base_info["episode"]))
    else:
        outprint("集数：" + str(base_info["episode"]))
    outprint("是否开播：" + str(base_info["is_started"]))
    outprint("是否完结：" + str(base_info["is_finish"]))
    outprint("评分：" + str(base_info["score"]))
    outprint("观看可用性：" + str(base_info["vip_info"]))
    outprint("-----------演员-----------")
    actor_list = base_info["actor_list"]
    for name in actor_list:
        if str(":") in str(name):
            name = name.split(":")
            actor = name[1]
            character = name[0]
            outprint(character + " --> " + actor)
        elif str("：") in str(name):
            name = name.split("：")
            actor = name[1]
            character = name[0]
            outprint(character + " --> " + actor)
        else:
            outprint(name)
    outprint("----------工作人员----------")
    staff_list = base_info["staff_list"]
    for name in staff_list:
        if str(":") in str(name):
            name = name.split(":")
            job = name[0]
            name = name[1]
            outprint(job + " --> " + name)
        elif str("：") in str(name):
            name = name.split("：")
            job = name[0]
            name = name[1]
            outprint(job + " --> " + name)
        else:
            outprint(name)
    outprint("-----------数据-----------")
    outprint("AV号：" + str(base_info["aid"]))
    outprint("BV号：" + str(base_info["bvid"]))
    outprint("当前用户最高画质：" + str(base_info["quality_ID"]) + "(" + str(base_info["quality"]) + ")")
    outprint("media_id(md)：" + str(base_info["media_id"]))
    outprint("season_id(ss)：" + str(base_info["season_id"]))
    outprint("tag_id：" + str(base_info["tag_id"]))
    # 这里的ep号对应最后一集！
    outprint("最新一集的剧集编号(ep)：" + str(base_info["ep_id"]))
    outprint("等级编号：" + str(base_info["rating_count"]))
    outprint("封面图片URL：" + str(base_info["cover_url"]))
    outprint("介绍页URL：" + str(base_info["share_url"]))
    outprint("总投币数：" + str(base_info["coins"]))
    outprint("总弹幕量：" + str(base_info["danmakus"]))
    outprint("追番数：" + str(base_info["follow"]))
    outprint("系列追番数：" + str(base_info["series_follow"]))
    outprint("总播放量：" + str(base_info["views"]))
    flag = str("")
    for i in base_info["flag_list"]:
        flag += str(i)
        flag += str(" ")
    outprint("标签：" + str(flag))
    outprint("可用性：" + str(base_info["vip_info"]))
    outprint("-----------剧集-----------")
    no = 1
    for ep_id, ep_info in episode_info.items():
        if str(ep_id).isdigit() or (str(ep_id).split(".")[0]).isdigit():
            outprint("第" + str(ep_id) + "集")
        else:
            outprint(str(ep_id))
        outprint("集标题：" + str(ep_info["title_long"]))
        outprint("剧集编号(ep)：" + str(ep_info["ep_id"]))
        outprint("弹幕cid：" + str(ep_info["cid"]))
        outprint("封面图片URL：" + str(ep_info["cover_url"]))
        outprint("播放页URL：" + str(ep_info["share_url"]))
        outprint("--------------------------")
        if get_dan:
            cid_no = int(ep_info["cid"])
            danmaku_path = bilib.get_danmaku_raw(cid_no)
            bilib.get_danmaku(cid_no)
            ass_path = bilib.raw2ass(danmaku_path)
            if len(str(no)) == 1:
                target_no = str("0") + str(no)
            else:
                target_no = str(no)
            change_name = str(os.getcwd()) + "\\" + str(target_no) + " " + str(anime_full_name) + " danmaku_file.ass"
            os.rename(ass_path,change_name)
        else:
            pass
        no += 1
    if tofile:
        global anime_name
        global md_no
        anime_name = str(base_info["title"]).replace(" ","_")
        anime_name = str(anime_name).replace("　", "_")
        md_no = str("md" + str(base_info["media_id"]))
        file_name = str(anime_name + "_" + md_no + ".txt")
        file_name = str(os.path.abspath('.') + "\\") + file_name
        txt = open(file_name, "a", encoding="utf-8")
        txt.write(full_text)
        txt.close()
    else:
        pass

# mediaID池
# 轻音少女系列(大会员)
kon_1 = 28220978
kon_2 = 28220984
# 轻音少女剧场版无法返回清晰度信息，请带上cookie
kon_movie = 28220988

# 玉子市场系列(免费)
tamako_market = 116772
tamako_love_story = 4155

# 吹响吧！上低音号(京吹) 第一季
enphonium_1 = 1547

# 擅长捉弄的高木同学 第二季(大会员，分集名称有转义字符)
takagi_2 = 28221403

# 冰菓(大会员，有11.5集)
hyouka = 3398

# 境界的彼方(大会员)
beyond_the_boundary = 3365

# 天气之子(降级为大会员，且因为此电影曾触发了大量lib中错误所以决定保留在demo)
weathering_with_you = 28228734

# 猫和老鼠旧版(免费，最大画质480P)
tom_and_jerry = 132112

# 环太平洋(大会员)
pacific_rim = 28227720

# 在这里输入mediaID
get_full_info(tamako_market,get_dan = False,tofile = True)





