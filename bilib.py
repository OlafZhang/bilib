# -*- coding: utf-8 -*-

# 这是一个lib，引用大量B站API，目前用户信息和弹幕工作正常，其它存在潜在的bug
# bilib = bili + lib

import csv
import os
import re
import sys
import time

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


# 传参异常/未定义异常
class InfoError(Exception):
    pass


# 弹幕文件相关异常
class danmakuError(Exception):
    pass


# 服务调用超时
class Timeout(Exception):
    pass


# 请求错误
class RequestError(Exception):
    pass


# 啥都木有
class SeemsNothing(Exception):
    pass


# 请求被拦截
class RequestRefuse(Exception):
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
        try:
            episode = play_info["result"]["media"]["new_ep"]["index_show"]
        except:
            episode = play_info["result"]["media"]["new_ep"]["index"]
        rating_count = play_info["result"]["media"]["rating"]["count"]
        score = play_info["result"]["media"]["rating"]["score"]
        season_id = play_info["result"]["media"]["season_id"]
        share_url = play_info["result"]["media"]["share_url"]
        title = play_info["result"]["media"]["title"]
        headers = {"Host": "api.bilibili.com", "User-Agent": ua}
        tag_info = requests.get("https://api.bilibili.com/x/tag/info?tag_name=" + str(title),
                                headers=headers)
        tag_info = tag_info.json()
        tag_id = tag_info["data"]["tag_id"]
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
        try:
            headers = {"User-Agent": ua}
            url = requests.get("https://www.bilibili.com/bangumi/media/md%s" % str(media_id), headers=headers)
            soup = BeautifulSoup(url.text, "html.parser")
            for x in soup.find_all('script'):
                if str("window.__INITIAL_STATE__=") in str(x.string):
                    text = str(x.string)
                    desc = str(re.findall(r'"(?:evaluate)":".+"', text)[0])
                    desc = str(str(desc.split(":")[1]).split('"')[1])
                    desc = desc.replace("\n", "")
                    desc = desc.replace("\r", "")
                    desc = desc.replace("\\n", "")
                    desc = desc.replace("\\r", "")
                    desc = desc.replace(" ", "")
                    desc = desc.replace("　", "")
                    if str(desc[0]) == str("【"):
                        head_desc = str(re.findall(r'【\w+】', desc)[0])
                        desc = desc.replace(head_desc, "")
                    else:
                        pass
                    try:
                        vip_info = str(re.findall(r'"(?:vip_promotion)":".+"', text)[0])
                        vip_info = str(str(vip_info.split(":")[1]).split('"')[1])
                        vip_info = vip_info.replace("\n", "")
                        vip_info = vip_info.replace("\r", "")
                        vip_info = vip_info.replace("\\n", "")
                        vip_info = vip_info.replace("\\r", "")
                        vip_info = vip_info.replace(" ", "")
                        vip_info = vip_info.replace("　", "")
                    except IndexError:
                        try:
                            vip_info = str(re.findall(r'"(?:promotion)":".+"', text)[0])
                            vip_info = str(str(vip_info.split(":")[1]).split('"')[1])
                            vip_info = vip_info.replace("\n", "")
                            vip_info = vip_info.replace("\r", "")
                            vip_info = vip_info.replace("\\n", "")
                            vip_info = vip_info.replace("\\r", "")
                            vip_info = vip_info.replace(" ", "")
                            vip_info = vip_info.replace("　", "")
                        except IndexError:
                            vip_info = str("免费")
                    if str("开通大会员观看") == str(vip_info):
                        vip_info = str("大会员")
                    elif str("免费") == str(vip_info):
                        vip_info = str("免费")
                    else:
                        vip_info = str("付费")
                else:
                    pass
        except:
            desc = str(" ")

        return_dict = {"title": title, "type": type, "area": area, "share_url": share_url, "desc": desc,
                       "cover_url": cover_url, "media_id": media_id, "ep_id": ep_id, "episode": episode,
                       "rating_count": rating_count, "score": score, "season_id": season_id, "coins": coins,
                       "danmakus": danmakus, "follow": follow, "series_follow": series_follow, "views": views,
                       "tag_id": tag_id, "vip_info": vip_info}
        return return_dict
    except:
        if str("啥都木有") in str(play_info['message']):
            raise SeemsNothing("You might input a wrong aid/bvid.")
        else:
            message = str(play_info)['message']
            raise RequestRefuse(
                ("You might be banned now, because we can not get info from API for now.(%s)") % (message))


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
            dict_list = {"aid": aid, "cid": cid, "ep_id": ep_id, "title_long": title_long, "cover_url": cover_url,
                         "share_url": share_url}
            return_dict[title_no] = dict_list
        except:
            if str("啥都木有") in str(play_info['message']):
                raise SeemsNothing("You might input a wrong season_id.")
            else:
                message = str(play_info)['message']
                raise RequestRefuse(
                    ("You might be banned now, because we can not get info from API for now.(%s)") % (message))

    return return_dict


def video_info(id_input):
    ua = str(UserAgent().random)
    id_input = str(id_input)
    headers = {"Host": "api.bilibili.com", "User-Agent": ua}
    if id_input.isdigit():
        mode = "av"
    else:
        mode = str(id_input[0:2].lower())
        if str("av") == mode:
            id_input = str(id_input[2:])
        elif str("bv") == mode:
            id_input = str("BV") + str(id_input[2:])
        else:
            mode = str("bv")
            id_input = str("BV") + str(id_input[2:])

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
            raise SeemsNothing("You might input a wrong aid/bvid.")
        else:
            message = str(play_info)['message']
            raise RequestRefuse(
                ("You might be banned now, because we can not get info from API for now.(%s)") % (message))


# 这个是实验性API，理论效果更好，功能更多，但可能不如旧的API稳定
def user_info(uid_input):
    uid_input = int(uid_input)
    ua = str(UserAgent().random)
    headers = {"Host": "api.bilibili.com", "User-Agent": ua}
    info_get = requests.get("https://api.bilibili.com/x/space/acc/info?mid=" + str(uid_input), headers=headers)
    info_get = info_get.json()
    if str(info_get["message"]) == str("请求错误"):
        raise RequestError("Request error.")
    elif str(info_get["message"]) == str("啥都木有"):
        raise SeemsNothing("Seems no such info.")
    elif str(info_get["message"]) == str("服务调用超时"):
        raise Timeout("Timeout.")
    elif str(info_get["message"]) == str("请求被拦截"):
        raise RequestRefuse("Banning.")
    elif str(info_get["message"]) == str("0"):
        pass
    else:
        print(info_get)
        raise InfoError("Something error.")
    name = info_get["data"]["name"]
    uid = uid_input
    sex = info_get["data"]["sex"]
    level = info_get["data"]["level"]
    face_url = info_get["data"]["face"]
    sign = info_get["data"]["sign"]
    birthday = info_get["data"]["birthday"]
    coins = info_get["data"]["coins"]
    vip_type = info_get["data"]["vip"]["label"]["text"]
    fans = requests.get("https://api.bilibili.com/x/relation/stat?vmid=" + str(uid_input), headers=headers)
    fans = fans.json()
    following = fans['data']['following']
    fans = fans['data']['follower']
    return_dict = {"name": name, "uid": uid, "fans": fans, "following": following, "sex": sex, "level": level,
                   "face_url": face_url, "sign": sign, "birthday": birthday, "coins": coins, "vip_type": vip_type}
    return return_dict


def user_info_old(uid_input, get_ua=False):
    uid_input = int(uid_input)
    ua = str(UserAgent().random)
    headers = {"User-Agent": ua}
    name = requests.get("https://space.bilibili.com/" + str(uid_input), headers=headers)
    headers = {"Host": "api.bilibili.com", "User-Agent": ua}
    if name.status_code != 200:
        if name.status_code == 412:
            raise RequestRefuse("You might be banned now, because status code is 412.")
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
        raise RequestRefuse("You might be banned now, because we can not get info from API for now.")

    if not connect_ok:
        name = "'(##BLANK_USER##)'"
    else:
        try:
            name = name.text
            name = name.split('<title>')
            name = str(name[1])
            name = name.split('的个人空间 - 哔哩哔哩 ( ゜- ゜)つロ 乾杯~ Bilibili</title>')  ###主要防止某些神经病用特殊的昵称导致爬取异常
            name = str(name[0])
        except:
            name = "'(##WDNMD_USER##)'"
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
            raise InfoError('You should input cid ONLY.')

        if os.path.exists(file_name):
            if not reset:
                user_input = input(str(os.path.abspath(file_name)) + ' is existed，update it?[y/n]:')
            else:
                user_input = 'yes'
            while True:
                user_input = user_input.lower()
                if user_input == 'yes' or user_input == 'y':
                    break
                elif user_input == 'no' or user_input == 'n':
                    print(str(os.path.abspath(file_name)))
                    return os.path.abspath(file_name)
                else:
                    user_input = input(str(os.path.abspath(file_name)) + ' is existed，update it?[y/n]:')
        else:
            pass
        bvIndex = url.find('BV')
        id = url[bvIndex:]
        rr = requests.get(url=url)
        rr.encoding = 'uft-16'
        soup = BeautifulSoup(rr.text, 'lxml')
        danmu_info = soup.find_all('d')
        all_info = []
        all_text = []

        for i in danmu_info:
            all_info.append(i['p'])
            all_text.append(i)
        f = open('danmu_info.csv', 'w', encoding='utf-16')
        csv_writer = csv.writer(f)

        for i in all_info:
            i = str(i).split(',')
            csv_writer.writerow(i)
        f.close()

        f = open('danmu_text.csv', 'w', encoding='utf-16')
        csv_writer = csv.writer(f)

        for i in all_text:
            csv_writer.writerow(i)
        f.close()

        file1 = open('danmu_text.csv', 'r', encoding='utf-16')
        file2 = open('danmu_text_output.csv', 'w', encoding='utf-16')

        for line in file1.readlines():
            if line == '\n':
                line = line.strip("\n")
            file2.write(line)
        file1.close()
        file2.close()

        file1 = open('danmu_info.csv', 'r', encoding='utf-16')
        file2 = open('danmu_info_output.csv', 'w', encoding='utf-16')
        for line in file1.readlines():
            if line == '\n':
                line = line.strip("\n")
            file2.write(line)
        file1.close()
        file2.close()

        danmaku_list = []
        file1 = open('danmu_text_output.csv', 'r', encoding='utf-16')
        file2 = open('danmu_info_output.csv', 'r', encoding='utf-16')
        file_final = open(file_name, 'w', encoding='utf-16')

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
            raise InfoError('cid error, check cid.')
        else:
            if os.path.exists(file_name):
                print(os.path.abspath(file_name))
                return os.path.abspath(file_name)
            else:
                raise danmakuError('danmaku file was deleted or error.')

    except Exception as e:
        print(e)


def listall_danmaku(file_path, stamp=False):
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    if os.path.exists(file_path):
        pass
    else:
        raise danmakuError('danmaku file is not existed.')

    file_path = open(str(file_path), 'r', encoding='utf-16')

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
            send_time_video = str('%s:%s:%s.%s' % (hour, minu, sec, send_time_right))
            def_list.append(send_time_video)

            # 整理弹幕类型
            if int(line[1]) == 1:
                danmaku_type = '滚动弹幕'
            elif int(line[1]) == 4:
                danmaku_type = '底部弹幕'
            elif int(line[1]) == 5:
                danmaku_type = '顶部弹幕'
            elif int(line[1]) == 6:
                danmaku_type = '逆向弹幕'
            elif int(line[1]) == 7 and int(line[5]) == 0:
                danmaku_type = '特殊弹幕'
            elif int(line[1]) == 7 and int(line[5]) == 1:
                danmaku_type = '精确弹幕'
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
            if not stamp:
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
            send_what = send_what.translate(non_bmp_map)
            def_list.append(send_what[0:len(send_what) - 1])

            if raw_mode:
                return_thing[int(blank_count)] = line
            else:
                return_thing[int(blank_count)] = def_list

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

    file_path = open(str(file_path), 'r', encoding='utf-16')
    return len(file_path.readlines())


# 由于此API设计初衷是配合ass转换工具的，所以没有单独做xml转csv的API
# 另外，为配合转换工具，设置了UTF-8编码而非UTF-16
# 如果需要数据分析，请直接使用get_danmaku()

def get_danmaku_raw(cid_input, reset=False):
    try:
        file_name = str(str(cid_input) + '.xml')
        if str(cid_input).isdigit():
            pass
        else:
            raise InfoError('You should input cid ONLY.')

        if os.path.exists(file_name):
            if not reset:
                user_input = input(str(os.path.abspath(file_name)) + ' is existed，update it?[y/n]:')
            else:
                user_input = 'yes'
            while True:
                if user_input == 'yes' or user_input == 'y':
                    url = str('http://comment.bilibili.com/' + str(cid_input) + '.xml')
                    rr = requests.get(url=url)
                    rr.encoding = 'uft-8'
                    xml = open(file_name, "w", encoding="utf-8")
                    xml.write(rr.text)
                    xml.close()
                    print(os.path.abspath(file_name))
                    return os.path.abspath(file_name)
                    break
                elif user_input == 'no' or user_input == 'n':
                    return os.path.abspath(file_name)
                    break
                else:
                    user_input = input(str(os.path.abspath(file_name)) + ' is existed，update it?[y/n]:')
        else:
            url = str('http://comment.bilibili.com/' + str(cid_input) + '.xml')
            rr = requests.get(url=url)
            rr.encoding = 'uft-8'
            xml = open(file_name, "w", encoding="utf-8")
            xml.write(rr.text)
            xml.close()
            print(os.path.abspath(file_name))
            return os.path.abspath(file_name)

    except Exception as e:
        print(e)


def raw2ass(file_path):
    class NotWindows(Exception):
        pass

    import platform
    sysstr = platform.system()
    if sysstr == str("Windows"):
        import win32api
        final_file = str(str(file_path).split('.xml')[0]) + ".ass"
        win32api.ShellExecute(0, 'open', '.\\Danmu2Ass\\Kaedei.Danmu2Ass.exe', file_path, '', 0)
        for i in range(0, 60):
            if os.path.exists(final_file):
                print(os.path.abspath(final_file))
                return os.path.abspath(final_file)
                break
            else:
                time.sleep(1)
        print("FAIL")
    else:
        raise NotWindows("You must use it in Windows, why not try Wine?")
