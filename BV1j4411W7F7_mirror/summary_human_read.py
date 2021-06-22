import re
summary = open("C:\\Users\\10245\\OneDrive\\Python\\bilib\\BV1j4411W7F7_mirror\\BV1j4411W7F7_summary.txt","r+",encoding="utf-8")
weekday_enus = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
weekday_zhcn = ["星期一","星期二","星期三","星期四","星期五","星期六","星期天"]
last_playback = 0
for line in summary.readlines():
    text = str(line).replace("\n","")
    full_time = str(re.findall("\[.+?\]",string=text)[0])
    date = str(re.findall("\d{4}-\d{2}-\d{2}",string=full_time)[0])
    date_list = date.split("-")
    date = str("%s月%s日")%(str(date_list[1]),str(date_list[2]))
    week = str(re.findall("[a-zA-Z]{3}",string=full_time)[0])
    week = str(weekday_zhcn[weekday_enus.index(week)])
    now_playback = str(re.findall("当前播放量 \d{5,11}",string=text)[0])
    now_playback = int(str(now_playback).replace("当前播放量 ",""))
    if last_playback == 0:
        info = str(("%s %s 播放量%s")%(date,week,now_playback))
    else:
        increase = now_playback - last_playback
        info = str(("%s %s 播放量%s 增长%s")%(date,week,now_playback,str(increase)))
    last_playback = now_playback
    print(info)
summary.close()