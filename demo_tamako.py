# 这是一个demo，演示如何通过一个番剧的media ID(介绍页以md开头的数字)获取番剧详细信息，包括season_id,av,bv,cid等等
# 此 media ID 有多个，默认为玉子市场TV版
# 同时下载全部弹幕文件，转换为ass后重命名
# 这是一个API用的比较全面的demo，可供参考

# -*- coding: utf-8 -*-
import bilib
import time
import os

# 是否下载弹幕文件
get_dan = False

# mediaID池
# 轻音少女系列(大会员)
kon_1 = 28220978
kon_2 = 28220984
# 轻音少女剧场版无法返回清晰度信息，请带上cookie
kon_movie = 28220988

# 玉子市场系列(免费)
tamako_market = 116772
tamako_love_story = 4155

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
base_info = bilib.anime_base_info(tamako_market)

season_id = int(base_info["season_id"])
episode_info = bilib.anime_episode_info(season_id)

print("-----------大纲-----------")
print("名称：" + str(base_info["title"]))
anime_full_name = str(base_info["title"])
print("简介：" + str(base_info["desc"]))
print("地区：" + str(base_info["area"]))
print("类型：" + str(base_info["type"]))
if str("上映") in str(base_info["episode"]):
    print("上映时间：" + str(base_info["episode"]))
else:
    print("集数：" + str(base_info["episode"]))
print("评分：" + str(base_info["score"]))
print("观看可用性：" + str(base_info["vip_info"]))
print("-----------数据-----------")
print("AV号：" + str(base_info["aid"]))
print("BV号：" + str(base_info["bvid"]))
print("当前用户最高画质：" + str(base_info["quality_ID"]) + "(" + str(base_info["quality"]) + ")")
print("media_id(md)：" + str(base_info["media_id"]))
print("season_id(ss)：" + str(base_info["season_id"]))
print("tag_id：" + str(base_info["tag_id"]))
# 这里的ep号对应最后一集！
print("最新一集的剧集编号(ep)：" + str(base_info["ep_id"]))
print("等级编号：" + str(base_info["rating_count"]))
print("封面图片URL：" + str(base_info["cover_url"]))
print("介绍页URL：" + str(base_info["share_url"]))
print("总投币数：" + str(base_info["coins"]))
print("总弹幕量：" + str(base_info["danmakus"]))
print("追番数：" + str(base_info["follow"]))
print("系列追番数：" + str(base_info["series_follow"]))
print("总播放量：" + str(base_info["views"]))
print("可用性：" + str(base_info["vip_info"]))
print("-----------剧集-----------")
no = 1

for ep_id, ep_info in episode_info.items():
    if str(ep_id).isdigit() or (str(ep_id).split(".")[0]).isdigit():
        print("第" + str(ep_id) + "集")
    else:
        print(str(ep_id))
    print("集标题：" + str(ep_info["title_long"]))
    print("剧集编号(ep)：" + str(ep_info["ep_id"]))
    print("弹幕cid：" + str(ep_info["cid"]))
    print("封面图片URL：" + str(ep_info["cover_url"]))
    print("播放页URL：" + str(ep_info["share_url"]))
    print("--------------------------")
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




