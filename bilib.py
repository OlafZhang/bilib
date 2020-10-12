# -*- coding: utf-8 -*-

# 这是一个lib，引用大量B站API，目前用户信息和弹幕工作正常，其它存在潜在的bug
# bilib = bili + lib

# user_info(uid_input,get_ua = False),uid_input推荐只输入int型的UID
# 这个会爬取指定UID的用户名，粉丝数，关注数
# 列表默认情况下最后一位是状态码，用于判断某些特殊情况，如销号但仍然有粉丝的情况
# get_ua为真时，会在列表末尾补充爬取时使用的User Agent，此为fake_useragent随机产生的
# 404时，返回用户名'(##BLANK_USER##)',特殊情况导致无法爬取用户名时则返回用户名'(##WDNMD_USER##)'
# 返回字典

# video_info(id_input,mode="bv"),id_input默认输入bv号，修改mode为av后则输入av号
# 这个是实验性功能，因为容错机制不完善，且不支持多p，功能：获取指定bv/av的播放信息
# 注意！对于番剧/电影等的信息获取可能存在问题！但并非不可用！
# 主要是番剧要去查对应的av/bv号，比较麻烦
# 返回字典，包含cid

# anime_base_info(id_input)，输入media_id(纯数字)
# 这个是实验性功能，因为容错机制不完善，功能：获取指定番剧/电影的播放信息
# 目前在番剧测试API有效，media_id可在番剧/电影介绍页的URL找到，如md116772
# 返回字典

# anime_episode_info(season_id),输入season_id(纯数字)
# season_id需要通过anime_base_info求得，部分番剧播放页中URL含有类似ss1134,也是season_id
# 这个是实验性功能，因为容错机制不完善,且貌似不支持含有SP的情况，功能：获取指定番剧/电影的av,cid,标题等高级信息
# 返回字典，字典key为集数(string)

# get_danmaku(cid_input, reset = False)只允许输入cid数字
# 它会爬取弹幕文件并返回一个弹幕文件完整路径，且在目录生成文件
# 默认是以cid命名的csv文件
# 强制刷新(reset)为真时会强制刷新弹幕文件，假时会询问是否刷新

# listall_danmaku(file_path,stamp = False)只需要指定文件路径
# 除非你想返回时间戳而非转换好的东八区时间，那就让stamp为真
# 这个会以字典的形式返回所有弹幕消息，这些消息同样被处理，key为序号
# 同样，如果遇到未知类型弹幕，则会返回原始信息，也建议做监视的同学改原始代码
# 可以嵌套get_danmaku()，但是重复查询则不推荐

# count_danmaku(file_path),只需要指定弹幕文件路径
# 返回弹幕文件长度，b站的弹幕API最多只能返回8000条弹幕记录


import csv
import os
import time

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


class danmakuError(Exception):
    pass


# 被ban时会抛出此异常
class InfoError(Exception):
    pass


def anime_base_info(media_id):
    ua = str(UserAgent().random)
    id_input = str(media_id)
    headers = {"Host": "api.bilibili.com", "User-Agent": ua}
    play_info = requests.get("https://api.bilibili.com/pgc/review/user?media_id=" + str(id_input), headers=headers)
    play_info = play_info.json()
    try:
        area = play_info["result"]["media"]["areas"][0]["name"]
        cover_url = play_info["result"]["media"]["cover"]
        media_id = play_info["result"]["media"]["media_id"]
        ep_id = play_info["result"]["media"]["new_ep"]["id"]
        episode = play_info["result"]["media"]["new_ep"]["index"]
        rating_count = play_info["result"]["media"]["rating"]["count"]
        score = play_info["result"]["media"]["rating"]["score"]
        season_id = play_info["result"]["media"]["season_id"]
        share_url = play_info["result"]["media"]["share_url"]
        title = play_info["result"]["media"]["title"]
        type = play_info["result"]["media"]["type_name"]
        ua = str(UserAgent().random)
        headers = {"Host": "api.bilibili.com", "User-Agent": ua}
        other_info = requests.get("https://api.bilibili.com/pgc/web/season/stat?season_id=" + str(season_id),
                                  headers=headers)
        other_info = other_info.json()
        coins = other_info["result"]["coins"]
        danmakus = other_info["result"]["danmakus"]
        follow = other_info["result"]["follow"]
        series_follow = other_info["result"]["series_follow"]
        views = other_info["result"]["views"]
        return_dict = {"title": title, "type": type, "area": area, "share_url": share_url, "cover_url": cover_url,
                       "media_id": media_id, "ep_id": ep_id, "episode": episode, "rating_count": rating_count,
                       "score": score, "season_id": season_id, "coins": coins, "danmakus": danmakus, "follow": follow,
                       "series_follow": series_follow, "views": views}
        return return_dict
    except:
        if str("啥都木有") in str(play_info['message']):
            raise InfoError("You might input a wrong aid/bvid.")
        else:
            print(str(play_info))
            raise InfoError("You might be banned now, because we can not get info from API for now.")


def anime_episode_info(season_id):
    ua = str(UserAgent().random)
    id_input = str(season_id)
    headers = {"Host": "api.bilibili.com", "User-Agent": ua}
    play_info = requests.get("https://api.bilibili.com/pgc/web/season/section?season_id=" + str(id_input),
                             headers=headers)
    play_info = play_info.json()
    episode_list = len(play_info["result"]["main_section"]["episodes"])
    return_dict = {}
    for index in range(0, episode_list):
        try:
            index = int(index)
            aid = play_info["result"]["main_section"]["episodes"][index]["aid"]
            cid = play_info["result"]["main_section"]["episodes"][index]["cid"]
            ep_id = play_info["result"]["main_section"]["episodes"][index]["id"]
            cover_url = play_info["result"]["main_section"]["episodes"][index]["cover"]
            share_url = play_info["result"]["main_section"]["episodes"][index]["share_url"]
            title_no = str(play_info["result"]["main_section"]["episodes"][index]["title"])
            title_long = str(play_info["result"]["main_section"]["episodes"][index]["long_title"])
            dict_list = [aid, cid, ep_id, title_long, cover_url, share_url]
            return_dict[title_no] = dict_list
        except:
            if str("啥都木有") in str(play_info['message']):
                raise InfoError("You might input a wrong season_id.")
            else:
                print(str(play_info))
                raise InfoError("You might be banned now, because we can not get info from API for now.")
    return return_dict


def video_info(id_input, mode="bv"):
    ua = str(UserAgent().random)
    id_input = str(id_input)
    headers = {"Host": "api.bilibili.com", "User-Agent": ua}
    if mode == "bv":
        play_info = requests.get("https://api.bilibili.com/x/web-interface/view?bvid=" + str(id_input), headers=headers)
    elif mode == "av":
        play_info = requests.get("https://api.bilibili.com/x/web-interface/view?aid=" + str(id_input), headers=headers)
    else:
        raise InfoError("You should input 'av' or 'bv'.")
    play_info = play_info.json()
    try:
        aid = play_info['data']['aid']
        bvid = play_info['data']['bvid']
        title = play_info['data']['title']
        desc = play_info['data']['desc']
        owner_name = play_info['data']['owner']["name"]
        owner_uid = play_info['data']['owner']["mid"]
        view = play_info['data']["stat"]['view']
        danmaku = play_info['data']["stat"]['danmaku']
        reply = play_info['data']["stat"]['reply']
        favorite = play_info['data']["stat"]['favorite']
        coin = play_info['data']["stat"]['coin']
        share = play_info['data']["stat"]['share']
        like = play_info['data']["stat"]['like']
        cid = play_info['data']["cid"]
        return_dict = {"aid": aid, "bvid": bvid, "cid": cid, "title": title, "desc": desc, "owner_name": owner_name,
                       "owner_uid": owner_uid, "view": view, "danmaku": danmaku, "reply": reply, "favorite": favorite,
                       "coin": coin, "share": share, "like": like}
        return return_dict
    except:
        if str("请求错误") in str(play_info['message']):
            raise InfoError("You might input a wrong aid/bvid.")
        else:
            print(str(play_info))
            raise InfoError("You might be banned now, because we can not get info from API for now.")


def user_info(uid_input, get_ua=False):
    uid_input = int(uid_input)
    ua = str(UserAgent().random)
    headers = {"Host": "api.bilibili.com", "User-Agent": ua}
    name = requests.get("https://space.bilibili.com/" + str(uid_input))
    if name.status_code != 200:
        if name.status_code == 412:
            raise InfoError("You might be banned now, because status code is 412.")
        else:
            st_code = name.status_code
            connect_ok = False
    else:
        st_code = name.status_code
        connect_ok = True
    try:
        fans = requests.get("https://api.bilibili.com/x/relation/stat?vmid=" + str(uid_input), headers=headers)
        fans = fans.json()
        following = fans['data']['following']
        fans = fans['data']['follower']
    except:
        raise InfoError("You might be banned now, because we can not get info from API for now.")

    if connect_ok == False:
        name = ("'(##BLANK_USER##)'")
    else:
        try:
            name = name.text
            name = name.split('<title>')
            name = str(name[1])
            name = name.split('的个人空间 - 哔哩哔哩 ( ゜- ゜)つロ 乾杯~ Bilibili</title>')  ###主要防止某些神经病用特殊的昵称导致爬取异常
            name = str(name[0])
        except:
            name = ("'(##WDNMD_USER##)'")
    if get_ua:
        return_dict = {"uid_input": uid_input, "name": name, "fans": fans, "following": following, "st_code": st_code,
                       "ua": ua}
    else:
        return_dict = {"uid_input": uid_input, "name": name, "fans": fans, "following": following, "st_code": st_code}
    return return_dict


def get_danmaku(cid_input, reset=False):
    try:
        if str(cid_input).isdigit():
            url = str('http://comment.bilibili.com/' + str(cid_input) + '.xml')
            file_name = str(str(cid_input) + '.csv')
        else:
            raise danmakuError('You should input cid ONLY.')

        if os.path.exists(file_name):
            if reset == False:
                user_input = input(str(os.path.abspath(file_name)) + 'is existed，update it?[y/n]:')
            else:
                user_input = 'yes'
            while True:
                user_input = user_input.lower()
                if user_input == 'yes' or user_input == 'y':
                    bvIndex = url.find('BV')
                    id = url[bvIndex:]
                    rr = requests.get(url=url)
                    rr.encoding = 'uft-8'
                    soup = BeautifulSoup(rr.text, 'lxml')
                    danmu_info = soup.find_all('d')
                    all_info = []
                    all_text = []

                    for i in danmu_info:
                        all_info.append(i['p'])
                        all_text.append(i)
                    f = open('danmu_info.csv', 'w', encoding='utf-8')
                    csv_writer = csv.writer(f)

                    for i in all_info:
                        i = str(i).split(',')
                        csv_writer.writerow(i)
                    f.close()

                    f = open('danmu_text.csv', 'w', encoding='utf-8')
                    csv_writer = csv.writer(f)

                    for i in all_text:
                        csv_writer.writerow(i)
                    f.close()

                    file1 = open('danmu_text.csv', 'r', encoding='utf-8')
                    file2 = open('danmu_text_output.csv', 'w', encoding='utf-8')

                    for line in file1.readlines():
                        if line == '\n':
                            line = line.strip("\n")
                        file2.write(line)
                    file1.close()
                    file2.close()

                    file1 = open('danmu_info.csv', 'r', encoding='utf-8')
                    file2 = open('danmu_info_output.csv', 'w', encoding='utf-8')
                    for line in file1.readlines():
                        if line == '\n':
                            line = line.strip("\n")
                        file2.write(line)
                    file1.close()
                    file2.close()

                    danmaku_list = []
                    file1 = open('danmu_text_output.csv', 'r', encoding='utf-8')
                    file2 = open('danmu_info_output.csv', 'r', encoding='utf-8')
                    file_final = open(file_name, 'w', encoding='utf-8')

                    for line in file1.readlines():
                        danmaku = str(line)[0:int(len(line)) - 1]
                        danmaku_list.append(str(danmaku))

                    count = 0

                    for line in file2.readlines():
                        info = str(line)[0:int(len(line)) - 1]
                        final_text = str(info + "," + danmaku_list[count] + "\n")
                        file_final.write(final_text)
                        count += 1

                    file1.close()
                    file2.close()
                    file_final.close()

                    os.remove("danmu_info.csv")
                    os.remove("danmu_text.csv")
                    os.remove("danmu_info_output.csv")
                    os.remove("danmu_text_output.csv")

                    if int(os.path.getsize(file_name)) == 0:
                        os.remove(file_name)
                        raise danmakuError('cid error, check cid.')
                    else:
                        if os.path.exists(file_name):
                            print(os.path.abspath(file_name))
                            return os.path.abspath(file_name)
                        else:
                            raise danmakuError('danmaku file was deleted or error.')
                    break
                elif user_input == 'no' or user_input == 'n':
                    return os.path.abspath(file_name)
                    break
                else:
                    user_input = input(str(os.path.abspath(file_name)) + 'is existed，update it?[y/n]:')
        else:
            bvIndex = url.find('BV')
            id = url[bvIndex:]
            rr = requests.get(url=url)
            rr.encoding = 'uft-8'
            soup = BeautifulSoup(rr.text, 'lxml')
            danmu_info = soup.find_all('d')
            all_info = []
            all_text = []

            for i in danmu_info:
                all_info.append(i['p'])
                all_text.append(i)
            f = open('danmu_info.csv', 'w', encoding='utf-8')
            csv_writer = csv.writer(f)

            for i in all_info:
                i = str(i).split(',')
                csv_writer.writerow(i)
            f.close()

            f = open('danmu_text.csv', 'w', encoding='utf-8')
            csv_writer = csv.writer(f)

            for i in all_text:
                csv_writer.writerow(i)
            f.close()

            file1 = open('danmu_text.csv', 'r', encoding='utf-8')
            file2 = open('danmu_text_output.csv', 'w', encoding='utf-8')

            for line in file1.readlines():
                if line == '\n':
                    line = line.strip("\n")
                file2.write(line)
            file1.close()
            file2.close()

            file1 = open('danmu_info.csv', 'r', encoding='utf-8')
            file2 = open('danmu_info_output.csv', 'w', encoding='utf-8')
            for line in file1.readlines():
                if line == '\n':
                    line = line.strip("\n")
                file2.write(line)
            file1.close()
            file2.close()

            danmaku_list = []
            file1 = open('danmu_text_output.csv', 'r', encoding='utf-8')
            file2 = open('danmu_info_output.csv', 'r', encoding='utf-8')
            file_final = open(file_name, 'w', encoding='utf-8')

            for line in file1.readlines():
                danmaku = str(line)[0:int(len(line)) - 1]
                danmaku_list.append(str(danmaku))

            count = 0

            for line in file2.readlines():
                info = str(line)[0:int(len(line)) - 1]
                final_text = str(info + "," + danmaku_list[count] + "\n")
                file_final.write(final_text)
                count += 1

            file1.close()
            file2.close()
            file_final.close()

            os.remove("danmu_info.csv")
            os.remove("danmu_text.csv")
            os.remove("danmu_info_output.csv")
            os.remove("danmu_text_output.csv")

            if int(os.path.getsize(file_name)) == 0:
                os.remove(file_name)
                raise danmakuError('cid error, check cid.')
            else:
                if os.path.exists(file_name):
                    print(os.path.abspath(file_name))
                    return os.path.abspath(file_name)
                else:
                    raise danmakuError('danmaku file was deleted or error.')


    except Exception as e:
        print(e)


def listall_danmaku(file_path, stamp=False):
    if os.path.exists(file_path):
        pass
    else:
        raise danmakuError('danmaku file is not existed.')

    file_path = open(str(file_path), 'r', encoding='utf-8')

    blank_count = 0

    try:
        return_thing = {}
        for line in file_path.readlines():
            raw_mode = False
            def_list = []

            line = line.split(',')

            # 整理发送时间
            send_time_left = int(str(line[0]).split('.')[0])
            send_time_right = int(str(line[0]).split('.')[1])

            hour = send_time_left // 3600
            temp_1 = send_time_left % 3600
            minu = temp_1 // 60
            sec = temp_1 % 60
            if len(str(hour)) == 1:
                hour = str('0') + str(hour)
            else:
                pass
            if len(str(minu)) == 1:
                minu = str('0') + str(minu)
            else:
                pass
            if len(str(sec)) == 1:
                sec = str('0') + str(sec)
            else:
                pass
            send_time_video = str(('%s:%s:%s.%s') % (hour, minu, sec, send_time_right))
            def_list.append(send_time_video)

            # 整理弹幕类型
            if int(line[1]) == 1:
                danmaku_type = ('滚动弹幕')
            elif int(line[1]) == 4:
                danmaku_type = ('底部弹幕')
            elif int(line[1]) == 5:
                danmaku_type = ('顶部弹幕')
            elif int(line[1]) == 6:
                danmaku_type = ('逆向弹幕')
            elif int(line[1]) == 7 and int(line[5]) == 0:
                danmaku_type = ('特殊弹幕')
            elif int(line[1]) == 7 and int(line[5]) == 1:
                danmaku_type = ('精确弹幕')
            else:
                raw_mode = True

            if raw_mode:
                pass
            else:
                def_list.append(danmaku_type)

            # 字号不需要整理
            def_list.append(str(line[2]))

            # 整理颜色
            color = str(hex(int(line[3])))[2:]
            if len(color) == 6:
                pass
            else:
                blank = ""
                for i in range(0, 6 - int(len(color))):
                    blank += "0"
                color = blank + color
            def_list.append(color)

            # 转换时间戳
            timestamp = int(line[4])
            if stamp == False:
                time_send = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(timestamp)))
            else:
                time_send = timestamp
            def_list.append(time_send)

            # 整理弹幕池
            if int(line[5]) == 0:
                danmaku_pool = '普通弹幕池'
            elif int(line[5]) == 1 or int(line[5]) == 2:
                danmaku_pool = '特殊弹幕池'
            else:
                raw_mode = True

            if raw_mode:
                pass
            else:
                def_list.append(danmaku_pool)

            # 用户ID和rowID不用整理
            def_list.append(str(line[6]))
            def_list.append(str(line[7]))

            # 调整发送内容
            send_what = str(line[8])
            def_list.append(send_what[0:len(send_what) - 1])

            if raw_mode:
                return_thing[int(blank_count)] = line
            else:
                return_thing[int(blank_count)] = def_list
                def_list = []

            blank_count += 1

    except Exception as e:
        print(e)

    finally:
        file_path.close()
        return return_thing


def count_danmaku(file_path):
    if os.path.exists(file_path):
        pass
    else:
        raise danmakuError('danmaku file is not existed.')

    file_path = open(str(file_path), 'r', encoding='utf-8')
    return len(file_path.readlines())
