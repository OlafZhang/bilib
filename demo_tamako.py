# 这是一个demo，演示如何通过一个番剧的media ID(介绍页以md开头的数字)获取番剧详细信息，包括season_id,av,bv,cid等等
# 此 media ID 有多个，默认为玉子市场TV版
# 同时下载全部弹幕文件，转换为ass后重命名
# 这是一个API用的比较全面的demo，可供参考

# -*- coding: utf-8 -*-
import bilib
import time
import os

# 是否下载弹幕文件
get_dan = True

# mediaID池
# 轻音少女系列
kon_1 = 28220978
kon_2 = 28220984
kon_movie = 28220988

# 玉子市场系列
tamako_market = 116772
tamako_love_story = 4155

# 擅长捉弄的高木同学 第二季
takagi_2 = 28221403

# Re：从零开始的异世界生活
re_zero_1_new = 3461

# 冰菓
hyouka = 3398

# JOJO的奇妙冒险系列
jojo_1_2 = 28223479
jojo_3_ep1 = 28223481
jojo_3_ep2 = 28223483
jojo_4 = 140552
jojo_5 = 135652

#境界的彼方
beyond_the_boundary = 3365

# 小林家的龙女仆 第一季
maid_dragon_1 = 5800

base_info = bilib.anime_base_info(beyond_the_boundary)
season_id = int(base_info["season_id"])
episode_info = bilib.anime_episode_info(season_id)

av_no = "av" + str(episode_info['1']["aid"])
v_info = bilib.video_info(av_no)
print("-----------大纲-----------")
print("名称：" + str(base_info["title"]))
anime_full_name = str(base_info["title"])
print("简介：" + str(base_info["desc"]))
print("地区：" + str(base_info["area"]))
print("类型：" + str(base_info["type"]))
print("集数：" + str(base_info["episode"]))
print("评分：" + str(base_info["score"]))
print("-----------数据-----------")
print("AV号：" + str(v_info["aid"]))
print("BV号：" + str(v_info["bvid"]))
print("media_id(md)：" + str(base_info["media_id"]))
print("season_id(ss)：" + str(base_info["season_id"]))
# 这里的ep号对应最后一集！
print("最新一集的剧集编号(ep)：" + str(base_info["ep_id"]))
print("tag_id：" + str(base_info["tag_id"]))
print("season_id(ss)：" + str(base_info["season_id"]))
print("等级编号：" + str(base_info["rating_count"]))
print("封面图片URL：" + str(base_info["cover_url"]))
print("介绍页URL：" + str(base_info["share_url"]))
print("总投币数：" + str(base_info["coins"]))
print("总弹幕量：" + str(base_info["danmakus"]))
print("追番数：" + str(base_info["follow"]))
print("系列追番数：" + str(base_info["series_follow"]))
print("总播放量：" + str(base_info["views"]))
print("-----------剧集-----------")
no = 1

for i, j in episode_info.items():
    print("第" + str(i) + "集")
    print("集标题：" + str(j["title_long"]))
    print("剧集编号(ep)：" + str(j["ep_id"]))
    print("弹幕cid：" + str(j["cid"]))
    print("封面图片URL：" + str(j["cover_url"]))
    print("播放页URL：" + str(j["share_url"]))
    print("--------------------------")
    if get_dan:
        cid_no = int(j["cid"])
        danmaku_path = bilib.get_danmaku_raw(cid_no)
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




