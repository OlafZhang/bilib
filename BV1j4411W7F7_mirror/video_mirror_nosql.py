import bilib
import time
import requests
from log import log_write

def human_time(sec):
    hour = sec // 3600
    day = hour // 24
    hour = hour % 24
    temp_1 = sec % 3600
    minu = temp_1 // 60
    sec = temp_1 % 60
    output = ""
    if day == 0:
        pass
    else:
        output += str(("%s天")%(str(day)))
    if hour == 0:
        pass
    else:
        output += str(("%s小时")%(str(hour)))
    if minu == 0:
        pass
    else:
        output += str(("%s分钟")%(str(minu)))
    if sec == 0:
        pass
    else:
        output += str(("%s秒")%(str(sec)))
    return output

def time_match(mode=5):
    if mode <= 59:
        pass
    else:
        print("Error.")
        return
    first_time = True
    time_wait = 0
    while True:
        if first_time:
            log_message = str(("正在等待时间对齐...(模式为%s分钟)")%(mode))
            log_write(message=log_message,path=log_path,level=1,service=service_name)
            first_time = False
        else:
            pass
        time_local = time.localtime(int(time.time()))
        wait_minu = int(time.strftime("%M",time_local))
        wait_sec = int(time.strftime("%S",time_local))
        if wait_sec == 0 and wait_minu % int(mode) == 0:
            pass
        elif wait_sec == 0 and wait_minu == 0:
            pass   
        else:
            time.sleep(1)
            time_wait += 1
            continue
        log_message = str(("完成时间对齐，耗时%s秒")%(time_wait))
        log_write(message=log_message,path=log_path,level=1,service=service_name)
        break

# 新宝岛：BV1j4411W7F7
# 影流之主：BV1Qt411T7VS

bvid = str("BV1j4411W7F7")
log_path = str("/home/" + str(bvid) + "_mirror.txt")
service_name = str("mirror.py")
threshold_views = 100000000

log_message = str(("(%s)即将完成初始化，数据库离线")%(bvid))
log_write(message=log_message,path=log_path,level=1,service=service_name)

last_view = 0
time_wait = 0
time_match_mode = 5
sleep_time = 300

while True:
    time_match(mode=time_match_mode)
    now_time = str(int(time.time()))
    log_message = str(("(%s)通过bilib API查询...")%(bvid))
    log_write(message=log_message,path=log_path,level=1,service=service_name)
    try:
        info = bilib.video_info(bvid)
    except requests.exceptions.ConnectionError:
        log_message = str(("(%s)疑似网络异常，即将重试...")%(bvid))
        log_write(message=log_message,path=log_path,level=5,service=service_name)
        time.sleep(5)
        log_message = str(("(%s)重试...")%(bvid))
        log_write(message=log_message,path=log_path,level=2,service=service_name)
        continue
    except bilib.Timeout:
        log_message = str(("(%s)网络请求超时，即将重试...")%(bvid))
        log_write(message=log_message,path=log_path,level=5,service=service_name)
        time.sleep(5)
        log_message = str(("(%s)重试...")%(bvid))
        log_write(message=log_message,path=log_path,level=2,service=service_name)
        continue
    except bilib.InfoError:
        log_message = str(("(%s)疑似网络请求超时，即将重试...")%(bvid))
        log_write(message=log_message,path=log_path,level=5,service=service_name)
        time.sleep(5)
        log_message = str(("(%s)重试...")%(bvid))
        log_write(message=log_message,path=log_path,level=2,service=service_name)
        continue
    log_message = str(("(%s)通过bilib API查询完成")%(bvid))
    log_write(message=log_message,path=log_path,level=2,service=service_name)
    title = str(info["title"])
    view = str(info["view"])
    danmaku = str(info["danmaku"])
    reply = str(info["reply"])
    favorite = str(info["favorite"])
    coin = str(info["coin"])
    share = str(info["share"])
    like = str(info["like"])
    log_message = str(("(%s)当前播放量 %s")%(bvid,view))
    log_write(message=log_message,path=log_path,level=1,service=service_name)
    log_message = str(("(%s)当前点赞量 %s ,当前弹幕量 %s ,当前评论量 %s ,当前收藏量 %s ,当前硬币量 %s ,当前分享量 %s")%(bvid,like,danmaku,reply,favorite,coin,share))
    log_write(message=log_message,path=log_path,level=0,service=service_name)
    if int(view) >= int(threshold_views):
        log_message = str(("(%s)当前播放量已超过设定阀值 %s")%(bvid,threshold_views))
        log_write(message=log_message,path=log_path,level=3,service=service_name)
    elif int(view) + 2000 >= int(threshold_views):
        log_message = str(("(%s)当前播放量即将到达设定阀值 %s，剩余不到2000")%(bvid,threshold_views))
        log_write(message=log_message,path=log_path,level=4,service=service_name)
        sleep_time = 60
        time_match_mode = 2
        log_message = str(("(%s)重置间隔时间为%s")%(bvid,human_time(sleep_time)))
        log_write(message=log_message,path=log_path,level=2,service=service_name)
    elif int(view) + 10000 >= int(threshold_views):
        log_message = str(("(%s)当前播放量即将到达设定阀值 %s，剩余不到10000")%(bvid,threshold_views))
        log_write(message=log_message,path=log_path,level=4,service=service_name)
        sleep_time = 120
        time_match_mode = 2
        log_message = str(("(%s)重置间隔时间为%s")%(bvid,human_time(sleep_time)))
        log_write(message=log_message,path=log_path,level=2,service=service_name)
    elif int(view) + 100000 >= int(threshold_views):
        log_message = str(("(%s)当前播放量即将到达设定阀值 %s，剩余不到100000")%(bvid,threshold_views))
        log_write(message=log_message,path=log_path,level=4,service=service_name)
        sleep_time = 180
        time_match_mode = 3
        log_message = str(("(%s)重置间隔时间为%s")%(bvid,human_time(sleep_time)))
        log_write(message=log_message,path=log_path,level=2,service=service_name)
    else:
        pass
    speed = int(int(view) - int(last_view)) / time_match_mode
    last = int(threshold_views - int(view))
    use_time = int(last / speed) * 60
    if use_time == 0:
        if last_view == 0:
            pass
        else:
            log_message = str(("(%s)此次没有增加播放量")%(bvid))
            log_write(message=log_message,path=log_path,level=2,service=service_name)
    else:
        use_time = human_time(int(use_time))
        speed_per = int(speed * time_match_mode)
        log_message = str(("(%s)预计将于%s后到达阈值（%s次/%s分钟，剩余%s）")%(bvid,str(use_time),str(speed_per),str(time_match_mode),str(last)))
        log_write(message=log_message,path=log_path,level=2,service=service_name)
    if last_view == 0:
        pass
    else:
        warn_3 = 10000
        warn_2 = 5000
        warn_1 = 1000
        if int(view) - int(last_view) >= int(warn_1):
            log_message = str(("(%s)当前播放量增幅大于 %s/%s，警报1级")%(bvid,str(warn_1),human_time(sleep_time)))
            log_write(message=log_message,path=log_path,level=3,service=service_name)
        elif int(view) - int(last_view) >= int(warn_2):
            log_message = str(("(%s)当前播放量增幅大于 %s/%s，警报2级")%(bvid,str(warn_2),human_time(sleep_time)))
            log_write(message=log_message,path=log_path,level=3,service=service_name)
        elif int(view) - int(last_view) >= int(warn_3):
            log_message = str(("(%s)当前播放量增幅大于 %s/%s，警报3级")%(bvid,str(warn_3),human_time(sleep_time)))
            log_write(message=log_message,path=log_path,level=3,service=service_name)
        else:
            pass
    time_wait = 0
    log_message = str(("(%s)强制暂停5秒")%(bvid))
    log_write(message=log_message,path=log_path,level=1,service=service_name)
    time.sleep(5)
    last_view = view