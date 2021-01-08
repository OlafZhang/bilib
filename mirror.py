import bilib
import log
import time
def user_mirror(uid,outprint=True):
    user_data = bilib.user_info(uid)
    name = str(user_data["name"])
    uid = str(user_data["uid"])
    level = str("level" + str(user_data["level"]))
    sex = user_data["sex"]
    fans = str(user_data["fans"])
    following = str(user_data["following"])
    user_info = str(("用户 %s(%s，%s，%s)，目前粉丝量 %s，目前关注量 %s") % (name,uid,sex,level,fans,following))
    log.log_write(message=user_info,path="C:\\Users\\10245\\OneDrive\\Python\\bilib\\global_log.txt",level=1,service="mirror.py",outprint=outprint)
    return

def video_mirror(id,outprint=True):
    video_data = bilib.video_info(str(id))
    bvid = str(video_data["bvid"])
    title = str(video_data["title"])
    view = str(video_data["view"])
    danmaku = str(video_data["danmaku"])
    reply = str(video_data["reply"])
    favorite = str(video_data["favorite"])
    coin = str(video_data["coin"])
    share = str(video_data["share"])
    like = str(video_data["like"])
    video_info = str(("视频 %s(%s),播放量 %s，弹幕量 %s，回复数 %s，收藏数 %s，投币数 %s，分享量 %s，点赞量 %s") % (bvid,title,view,danmaku,reply,favorite,coin,share,like))
    log.log_write(message=video_info,path="C:\\Users\\10245\\OneDrive\\Python\\bilib\\global_log.txt",level=1,service="mirror.py",outprint=outprint)
    return

def anime_mirror(mid,outprint=True):
    anime_data = bilib.anime_base_info(int(mid))
    title = str(anime_data["title"])
    type_name = str(anime_data["type"])
    media_id = str(anime_data["media_id"])
    score = str(anime_data["score"])
    coins = str(anime_data["coins"])
    danmakus = str(anime_data["danmakus"])
    follow = str(anime_data["follow"])
    series_follow = str(anime_data["series_follow"])
    views = str(anime_data["views"])
    anime_info = str(("%s %s(%s),评分 %s，播放量 %s，弹幕量 %s，投币数 %s，追番数 %s，系列追番数 %s") % (type_name,title,media_id,score,views,danmakus,coins,follow,series_follow))
    log.log_write(message=anime_info,path="C:\\Users\\10245\\OneDrive\\Python\\bilib\\global_log.txt",level=1,service="mirror.py",outprint=outprint)
    return
