# -*- coding: utf-8 -*-
# 这是一个demo，演示如何通过一个番剧的media ID(介绍页以md开头的数字)获取番剧详细信息，包括season_id,av,bv,cid等等
# 此 media ID 有多个，默认为玉子市场TV版
# 同时下载全部弹幕文件，转换为ass后重命名
# 这是一个API用的比较全面的demo，可供参考

import os
import time
import bilib
from media_id_pool import *

# pip install opencc-python-reimplemented
# 用于强制转简体，方便集中管理
import opencc

def get_full_info(mediaID, get_dan=False, tofile=False, cleanup=True):
    # 配合outprint，将print内容暂时存储在一个字符串，稍后输出
    global full_text
    full_text = str("")

    def outprint(string):
        global full_text
        print(string)
        full_text += str(string)
        full_text += "\n"

    base_info = bilib.anime_base_info(mediaID)
    season_id = int(base_info["season_id"])
    episode_info = bilib.anime_episode_info(season_id)
    now_time = str(time.strftime('%Y-%m-%d,%H:%M:%S', time.localtime(time.time())))
    outprint("-----此信息于" + str(now_time) + "生成-----")
    outprint(" ")
    outprint("-----------大纲-----------")
    outprint("名称：" + str(base_info["title"]))
    outprint("原名：" + str(base_info["origin_name"]))
    anime_full_name = str(base_info["title"])
    alias = str("")
    alias_list = base_info["alias_list"]
    for i in range(0,len(alias_list)):
        alias += str(alias_list[i])
        if i == len(alias_list) - 1:
            pass
        else:
            alias += str(", ")
    outprint("别称：" + str(alias))
    flag = str("")
    flag_list = base_info["flag_list"]
    for i in range(0,len(flag_list)):
        flag += str(flag_list[i])
        if i == len(flag_list) - 1:
            pass
        else:
            flag += str(", ")
    outprint("标签：" + str(flag))
    outprint("简介：" + str(base_info["desc"]))
    outprint("地区：" + str(base_info["area"]))
    outprint("类型：" + str(base_info["type"]))
    type = str(base_info["type"])
    if str("上映") in str(base_info["episode"]):
        outprint("上映时间：" + str(base_info["episode"]))
    else:
        outprint("集数：" + str(base_info["episode"]))
        outprint("开播时间：" + str(base_info["showtime"]))
    outprint("是否开播：" + str(base_info["is_started"]))
    outprint("是否完结：" + str(base_info["is_finish"]))
    outprint("评分：" + str(base_info["score"]))
    outprint("观看可用性：" + str(base_info["vip_info"]))
    outprint("-----------数据-----------")
    # 这里的av号对应第一集！
    outprint("第一集/全集 AV号：" + str(base_info["aid"]))
    outprint("第一集/全集 BV号：" + str(base_info["bvid"]))
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
    cc = opencc.OpenCC('t2s')
    if str(type) == str("番剧"):
        outprint("-----------声优-----------")
    else:
        outprint("-----------演员-----------")
    actor_list = base_info["actor_list"]
    for name in actor_list:
        if str(":") in str(name):
            name = name.split(":")
            actor = cc.convert(str(name[1]))
            character = cc.convert(str(name[0]))
            # 针对"POP子和PIPI美的日常"(md11712)做了专项优化(虽然不优化不会报错或排版异常)
            if str("、") in str(actor):
                actor = actor.replace(" ","")
                actor = actor.replace("，", "、")
                actor_list = actor.split("、")
                for part_actor in actor_list:
                    outprint(character + " --> " + part_actor)
            elif str("/") in str(actor):
                actor = actor.replace(" ","")
                actor_list = actor.split("/")
                for part_actor in actor_list:
                    outprint(character + " --> " + part_actor)
            else:
                outprint(character + " --> " + actor)
        elif str("：") in str(name):
            name = name.split("：")
            actor = cc.convert(str(name[1]))
            character = cc.convert(str(name[0]))
            if str("、") in str(actor):
                actor = actor.replace(" ", "")
                actor = actor.replace("，", "、")
                actor_list = actor.split("、")
                for part_actor in actor_list:
                    outprint(character + " --> " + part_actor)
            elif str("/") in str(actor):
                actor = actor.replace(" ", "")
                actor_list = actor.split("/")
                for part_actor in actor_list:
                    outprint(character + " --> " + part_actor)
            else:
                outprint(character + " --> " + actor)
        else:
            outprint(cc.convert(str(name)))
    outprint("----------工作人员----------")
    staff_list = base_info["staff_list"]
    for name in staff_list:
        if str(":") in str(name):
            name = name.split(":")
            job = cc.convert(str(name[0]))
            name = cc.convert(str(name[1]))
            outprint(job + " --> " + name)
        elif str("：") in str(name):
            name = name.split("：")
            job = cc.convert(str(name[0]))
            name = cc.convert(str(name[1]))
            outprint(job + " --> " + name)
        else:
            outprint(cc.convert(str(name)))
    outprint("-----------剧集-----------")
    no = 1
    for ep_id, ep_info in episode_info.items():
        if str(ep_id).isdigit() or (str(ep_id).split(".")[0]).isdigit():
            outprint("第" + str(ep_id) + "集")
        else:
            outprint(str(ep_id))
        outprint("集标题：" + str(ep_info["title_long"]))
        outprint("剧集编号(ep)：" + str(ep_info["ep_id"]))
        outprint("av号：" + str(ep_info["aid"]))
        outprint("弹幕cid：" + str(ep_info["cid"]))
        outprint("封面图片URL：" + str(ep_info["cover_url"]))
        outprint("播放页URL：" + str(ep_info["share_url"]))
        outprint("--------------------------")
        if get_dan:
            cid_no = int(ep_info["cid"])
            danmaku_path = bilib.get_danmaku_raw(cid_no)
            ass_path = bilib.raw2ass(danmaku_path)
            if len(str(no)) == 1:
                target_no = str("0") + str(no)
            else:
                target_no = str(no)
            anime_full_name = anime_full_name.replace("\\", " ")
            anime_full_name = anime_full_name.replace("/", " ")
            anime_full_name = anime_full_name.replace("?", "？")
            anime_full_name = anime_full_name.replace(":", "：")
            anime_full_name = anime_full_name.replace("*", "#")
            anime_full_name = anime_full_name.replace('"', "'")
            anime_full_name = anime_full_name.replace('<', "(")
            anime_full_name = anime_full_name.replace('>', ")")
            anime_full_name = anime_full_name.replace('|', " ")
            change_name = str(os.getcwd()) + "\\" + str(target_no) + " " + str(anime_full_name) + " danmaku_file.ass"
            os.rename(ass_path, change_name)
            if cleanup:
                os.remove(str(cid_no) + str(".xml"))
            else:
                pass
            # 如果爬取集超过30(24+6OVA情况)，降低速度，之后到50和100也会降低速度
            if int(target_no) > 100:
                time.sleep(5)
            elif int(target_no) > 50:
                time.sleep(2)
            elif int(target_no) > 30:
                time.sleep(1)
            else:
                pass
        else:
            pass
        no += 1
    if tofile:
        global anime_name
        global md_no
        anime_name = str(base_info["title"]).replace(" ", "_")
        anime_name = str(anime_name).replace("　", "_")
        md_no = str("md" + str(base_info["media_id"]))
        anime_name = anime_name.replace("\\", " ")
        anime_name = anime_name.replace("/", " ")
        anime_name = anime_name.replace("?", "？")
        anime_name = anime_name.replace(":", "：")
        anime_name = anime_name.replace("*", "#")
        anime_name = anime_name.replace('"', "'")
        anime_name = anime_name.replace('<', "(")
        anime_name = anime_name.replace('>', ")")
        anime_name = anime_name.replace('|', " ")
        file_name = str(md_no + "_" + anime_name + ".txt")
        import platform
        sysstr = platform.system()
        if sysstr == "Windows":
            file_name = str(os.path.abspath('.') + "\\") + file_name
        else:
            file_name = str(os.path.abspath('.') + "/") + file_name
        txt = open(file_name, "a", encoding="utf-8")
        txt.write(full_text)
        txt.close()
    else:
        pass

# 在这里输入mediaID
# get_dan为真时下载弹幕文件
# tofile为真时导出全部信息到一个txt
get_full_info(tamako_market, get_dan=False, tofile=False, cleanup=False)
