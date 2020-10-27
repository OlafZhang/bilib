# 这是一个demo，演示如何通过一个番剧的media ID(介绍页以md开头的数字)获取番剧详细信息，包括season_id,av,bv,cid等等
# 此 media ID 对于玉子市场TV版
# 同时下载全部弹幕文件，转换为ass后重命名
# 这是一个用的比较全面的demo，可供参考

# -*- coding: utf-8 -*-
import bilib
import time
import os

season_id = bilib.anime_base_info(116772)["season_id"]

episode_info = bilib.anime_episode_info(season_id)
no = 1
for i, j in episode_info.items():
    print(i, j)
    av_no = "av" + str(j[0])
    cid_no = int(j[1])
    danmaku_path = bilib.get_danmaku_raw(cid_no)
    ass_path = bilib.raw2ass(danmaku_path)
    if len(str(no)) == 1:
        target_no = str("0") + str(no)
    else:
        target_no = str(no)
    change_name = str(os.getcwd()) + "\\" + str(target_no) + " 玉子 danmaku_file.ass"
    os.rename(ass_path,change_name)
    no += 1
print(episode_info)
print(av_no)
print(bilib.video_info(av_no))

