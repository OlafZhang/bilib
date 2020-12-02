# -*- coding: utf-8 -*-

# 这是一个lib，引用大量B站API，目前用户信息和弹幕工作正常，其它存在潜在的bug
# bilib = bili + lib
import csv
import os
import re
import sys
import time
import traceback
import platform

sysstr = platform.system()

# 额外安装的包，如果出错，请检查requirements.txt
# fake_useragent的使用可能会抛出异常，请直接忽略
try:
    import requests
    from bs4 import BeautifulSoup
    from fake_useragent import UserAgent
except:
    if sysstr == "Windows":
        os.system("pip install -r requirements.txt")
    else:
        os.system("pip3 install -r requirements.txt")
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


# 默认超时时间为5秒，应用到所有requests.get()
timeout = 5


# 设置超时时间
def set_timeout(set_time):
    global timeout
    try:
        timeout = int(set_time)
    except:
        timeout = 5


if sysstr == "Windows":
    ua_json = os.getcwd() + '\\fake_useragent_0.1.11.json'
else:
    ua_json = os.getcwd() + '/fake_useragent_0.1.11.json'

# 默认没有cookie，应用到所有requests.get()
# 由于带入cookie有些番剧还是不能得到正确消息，故不做cookie模块
cookies = ""
with_cookies = False


# 获取视频最高清晰度
# 传入参数：av号,bv号或ep号
# 由于同时支持视频和番剧，故单独做了API，作为备份
# 已集成到video_info()，anime_base_info()则使用了另外的方法
def get_resolution(id_input, getid=False):
    id_input = str(id_input)
    # 判断用户输入的是av号还是bv号
    if str(id_input[0:2]).isalpha():
        mode = str(id_input[0:2].lower())
        if str("av") == mode:
            id_input = str("av") + str(id_input[2:])
        elif str("bv") == mode:
            id_input = str("BV") + str(id_input[2:])
        else:
            mode = str("ep")
            id_input = str("ep") + str(id_input[2:])
    else:
        raise InfoError("You should input av/bv/ep.")
    ua = str(UserAgent(path=ua_json).random)
    headers = {"User-Agent": ua}
    try:
        if mode == str("ep"):
            main_url = str("https://www.bilibili.com/bangumi/play/" + str(id_input))
        else:
            main_url = str("https://www.bilibili.com/video/" + str(id_input))
        main_url = requests.get(main_url, headers=headers, timeout=timeout, cookies=cookies)
    except:
        raise Timeout("Timeout.")
    quality = str("不支持")
    quality_id = str("不支持")
    soup = BeautifulSoup(main_url.text, "html.parser")
    for x in soup.find_all('script'):
        if str("window.__playinfo__=") in str(x.string):
            # 匹配简介的正则表达式(关键字accept_quality)
            text = str(x.string)
            break
        else:
            pass
    quality_id = str(re.findall(r'"accept_quality":.\d+.,', text)[0])
    quality_id = str(str(quality_id.split("[")[1]).split("]")[0])
    if str(",") in quality_id:
        quality_id = quality_id.split(",")[0]
    else:
        pass

    # 自动(0)不应该出现在清晰度信息里
    if quality_id.isdigit():
        quality_id = int(quality_id)
        if quality_id == 125:
            quality = str("HDR")
        elif quality_id == 120:
            quality = str("4K")
        elif quality_id == 116:
            quality = str("1080P 高帧率")
        elif quality_id == 112:
            quality = str("1080P+")
        elif quality_id == 80:
            quality = str("1080P")
        elif quality_id == 74:
            quality = str("720P 高帧率")
        elif quality_id == 64:
            quality = str("720P")
        elif quality_id == 32:
            quality = str("480P")
        elif quality_id == 16:
            quality = str("360P")
        else:
            quality = str("疑似错误的编号(" + str(quality_id) + ")")
    else:
        quality = str("疑似错误的编号(" + str(quality_id) + ")")
    if getid:
        return quality_id
    else:
        return quality


# 获取视频信息
# 对于番剧/电影，除了能配合anime_episode_info获得bv号、视频原生分辨率以外，没有任何作用，且数据比较不可信
# 而av号和bv号对番剧/电影来说没有意义
def video_info(id_input):
    ua = str(UserAgent(path=ua_json).random)
    id_input = str(id_input)
    headers = {"Host": "api.bilibili.com", "User-Agent": ua}
    # 判断用户输入的是av号还是bv号
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
    # 返回的结果全部来自此API
    try:
        if mode == "bv":
            play_info = requests.get("https://api.bilibili.com/x/web-interface/view?bvid=" + str(id_input),
                                     headers=headers, timeout=timeout, cookies=cookies)
        elif mode == "av":
            play_info = requests.get("https://api.bilibili.com/x/web-interface/view?aid=" + str(id_input),
                                     headers=headers, timeout=timeout, cookies=cookies)
        else:
            raise InfoError("You should input 'av' or 'bv'.")
    except requests.exceptions.ReadTimeout:
        raise Timeout("Timeout.")
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
        headers = {"User-Agent": ua}
        try:
            main_url = str("https://www.bilibili.com/video/" + str(bvid))
            main_url = requests.get(main_url, headers=headers, timeout=timeout, cookies=cookies)
        except:
            raise Timeout("Timeout.")
        soup = BeautifulSoup(main_url.text, "html.parser")
        quality = str("不支持")
        quality_id = str("不支持")
        for x in soup.find_all('script'):
            if str("window.__playinfo__=") in str(x.string):
                # 匹配简介的正则表达式(关键字accept_quality)
                text = str(x.string)
                quality_id = str(re.findall(r'"accept_quality":.\d+.,', text)[0])
                quality_id = str(str(quality_id.split("[")[1]).split("]")[0])
                if str(",") in quality_id:
                    quality_id = quality_id.split(",")[0]
                else:
                    pass

                if quality_id.isdigit():
                    quality_id = int(quality_id)
                    if quality_id == 125:
                        quality = str("HDR")
                    elif quality_id == 120:
                        quality = str("4K")
                    elif quality_id == 116:
                        quality = str("1080P 高帧率")
                    elif quality_id == 112:
                        quality = str("1080P+")
                    elif quality_id == 80:
                        quality = str("1080P")
                    elif quality_id == 74:
                        quality = str("720P 高帧率")
                    elif quality_id == 64:
                        quality = str("720P")
                    elif quality_id == 32:
                        quality = str("480P")
                    elif quality_id == 16:
                        quality = str("360P")
                    else:
                        quality = str("疑似错误的编号(" + str(quality_id) + ")")
                else:
                    quality = str("疑似错误的编号(" + str(quality_id) + ")")
                break
            else:
                pass

        return_dict = {"aid": aid, "bvid": bvid, "cid": cid, "title": title, "desc": desc, "owner_name": owner_name,
                       "owner_uid": owner_uid, "view": view, "danmaku": danmaku, "reply": reply, "favorite": favorite,
                       "coin": coin, "share": share, "like": like, "quality": quality, "quality_id": quality_id}
        # 返回字典，总共使用1个API和一个HTML页
        return return_dict
    except:
        message = play_info['message']
        if str(message) == str("请求错误"):
            raise RequestError("Request error.")
        elif str(message) == str("啥都木有"):
            raise SeemsNothing("Seems no such info.")
        elif str(message) == str("服务调用超时"):
            raise Timeout("Timeout.")
        elif str(message) == str("请求被拦截"):
            raise RequestRefuse("Banning.")
        else:
            print(message)
            traceback.print_exc()
            raise InfoError("Something error.")


# 番剧/电影剧集信息（返回每集的cid，封面URL等，cid可用于爬取弹幕）
def anime_episode_info(season_id):
    ua = str(UserAgent(path=ua_json).random)
    id_input = str(season_id)
    headers = {"Host": "api.bilibili.com", "User-Agent": ua}
    # 返回的结果全部来自此API
    try:
        play_info = requests.get("https://api.bilibili.com/pgc/web/season/section?season_id=" + str(id_input),
                                 headers=headers, timeout=timeout, cookies=cookies)
        play_info = play_info.json()
    except requests.exceptions.ReadTimeout:
        raise Timeout("Timeout.")
    # 读取剧集数量
    try:
        episode_list = len(play_info["result"]["main_section"]["episodes"])
        return_dict = {}
        # 剧集遍历
        for index in range(0, episode_list):
            try:
                # 剧集索引号,不一定是剧集编号
                index = int(index)
                aid = play_info["result"]["main_section"]["episodes"][index]["aid"]
                cid = play_info["result"]["main_section"]["episodes"][index]["cid"]
                # ep_id，每集独立存在的编号
                ep_id = play_info["result"]["main_section"]["episodes"][index]["id"]
                cover_url = play_info["result"]["main_section"]["episodes"][index]["cover"]
                share_url = play_info["result"]["main_section"]["episodes"][index]["share_url"]
                # 真正的剧集编号，必须是string
                title_no = str(play_info["result"]["main_section"]["episodes"][index]["title"])
                # 剧集标题
                title_long = str(play_info["result"]["main_section"]["episodes"][index]["long_title"])
                dict_list = {"aid": aid, "cid": cid, "ep_id": ep_id, "title_long": title_long, "cover_url": cover_url,
                             "share_url": share_url}
                # 根据剧集编号返回词典
                return_dict[title_no] = dict_list
            except:
                message = play_info['message']
                if str(message) == str("请求错误"):
                    raise RequestError("Request error.")
                elif str(message) == str("啥都木有"):
                    raise SeemsNothing("Seems no such info.")
                elif str(message) == str("服务调用超时"):
                    raise Timeout("Timeout.")
                elif str(message) == str("请求被拦截"):
                    raise RequestRefuse("Banning.")
                else:
                    print(message)
                    traceback.print_exc()
                    raise InfoError("Something error.")
    except:
        # 此处针对2020年11月30日开播的Love Live! 剧场版导致的bug而修复的(当时没有开播)
        # 可能在后续不支持，之后会修复
        episode_list = len(play_info["result"]["section"][0]["episodes"])
        return_dict = {}
        # 剧集遍历
        for index in range(0, episode_list):
            try:
                # 剧集索引号,不一定是剧集编号
                index = int(index)
                aid = play_info["result"]["section"][0]["episodes"][index]["aid"]
                cid = play_info["result"]["section"][0]["episodes"][index]["cid"]
                # ep_id，每集独立存在的编号
                ep_id = play_info["result"]["section"][0]["episodes"][index]["id"]
                cover_url = play_info["result"]["section"][0]["episodes"][index]["cover"]
                share_url = play_info["result"]["section"][0]["episodes"][index]["share_url"]
                # 真正的剧集编号，必须是string
                title_no = str(play_info["result"]["section"][0]["episodes"][index]["title"])
                # 剧集标题
                title_long = str(play_info["result"]["section"][0]["episodes"][index]["long_title"])
                dict_list = {"aid": aid, "cid": cid, "ep_id": ep_id, "title_long": title_long, "cover_url": cover_url,
                             "share_url": share_url}
                # 根据剧集编号返回词典
                return_dict[title_no] = dict_list
            except:
                message = play_info['message']
                if str(message) == str("请求错误"):
                    raise RequestError("Request error.")
                elif str(message) == str("啥都木有"):
                    raise SeemsNothing("Seems no such info.")
                elif str(message) == str("服务调用超时"):
                    raise Timeout("Timeout.")
                elif str(message) == str("请求被拦截"):
                    raise RequestRefuse("Banning.")
                else:
                    print(message)
                    traceback.print_exc()
                    raise InfoError("Something error.")

    # 返回一个含字典的大字典，总共使用了1个API
    return return_dict


# 番剧/电影基本信息（返回seasonID,以便请求剧集的详情）
def anime_base_info(media_id):
    ua = str(UserAgent(path=ua_json).random)
    id_input = str(media_id)
    headers = {"Host": "api.bilibili.com", "User-Agent": ua}
    # 返回的结果基本来自此API
    try:
        play_info = requests.get("https://api.bilibili.com/pgc/review/user?media_id=" + str(id_input), headers=headers,
                                 timeout=timeout, cookies=cookies)
    except requests.exceptions.ReadTimeout:
        raise Timeout("Timeout.")
    play_info = play_info.json()
    message = play_info['message']
    try:
        area = play_info["result"]["media"]["areas"][0]["name"]
        cover_url = play_info["result"]["media"]["cover"]
        media_id = play_info["result"]["media"]["media_id"]
        ep_id = play_info["result"]["media"]["new_ep"]["id"]
        # episode对于某些电影不是剧集数，而是上映时间
        try:
            episode = play_info["result"]["media"]["new_ep"]["index_show"]
        except:
            episode = play_info["result"]["media"]["new_ep"]["index"]
        try:
            rating_count = play_info["result"]["media"]["rating"]["count"]
            score = play_info["result"]["media"]["rating"]["score"]
        except:
            rating_count = str("不支持")
            score = str("不支持")
        season_id = play_info["result"]["media"]["season_id"]
        share_url = play_info["result"]["media"]["share_url"]
        title = play_info["result"]["media"]["title"]
        type = play_info["result"]["media"]["type_name"]
        headers = {"Host": "api.bilibili.com", "User-Agent": ua}
        # 获取tagID，此参数可以获得番剧/电影的相关推荐，如其它相关番剧和二创
        try:
            tag_info = requests.get("https://api.bilibili.com/x/tag/info?tag_name=" + str(title),
                                    headers=headers, timeout=timeout, cookies=cookies)
        except requests.exceptions.ReadTimeout:
            raise Timeout("Timeout.")
        try:
            tag_info = tag_info.json()
            tag_id = tag_info["data"]["tag_id"]
        except KeyError:
            tag_id = str("不支持")
        # 获取av号和第一集cid，以便获取默认清晰度
        episode_info = anime_episode_info(season_id)
        # 获取第一个分集的key，以便传入video_info
        for key in episode_info.keys():
            key = str(key)
            break
        av_no = str(episode_info[key]["aid"])
        # 获取BV号
        bv_no = video_info(av_no)["bvid"]
        cid = str(episode_info[key]["cid"])
        try:
            quality_info = requests.get(
                "https://api.bilibili.com/pgc/player/web/playurl?aid=" + str(av_no) + "&cid=" + str(cid),
                headers=headers, timeout=timeout, cookies=cookies)
        except requests.exceptions.ReadTimeout:
            raise Timeout("Timeout.")

        av_no = str("av" + str(av_no))
        quality_info = quality_info.json()
        if quality_info["message"] == "大会员专享限制":
            quality = str("大会员专享限制")
            quality_ID = str("无ID")
        else:
            quality = quality_info["result"]["support_formats"][0]["new_description"]
            quality_ID = quality_info["result"]["support_formats"][0]["quality"]

        headers = {"Host": "api.bilibili.com", "User-Agent": ua}
        # 根据seasonID求总投币数，追番数等信息
        try:
            other_info = requests.get("https://api.bilibili.com/pgc/web/season/stat?season_id=" + str(season_id),
                                      headers=headers, timeout=timeout, cookies=cookies)
        except requests.exceptions.ReadTimeout:
            raise Timeout("Timeout.")
        other_info = other_info.json()
        coins = other_info["result"]["coins"]
        danmakus = other_info["result"]["danmakus"]
        follow = other_info["result"]["follow"]
        series_follow = other_info["result"]["series_follow"]
        views = other_info["result"]["views"]
        try:
            # 获取HTML页，检查介绍信息和是否收费观看
            headers = {"User-Agent": ua}
            url = requests.get("https://www.bilibili.com/bangumi/media/md%s" % str(media_id), headers=headers,
                               timeout=timeout, cookies=cookies)
        except requests.exceptions.ReadTimeout:
            raise Timeout("Timeout.")
        soup = BeautifulSoup(url.text, "html.parser")
        for x in soup.find_all('script'):
            if str("window.__INITIAL_STATE__=") in str(x.string):
                # 匹配简介的正则表达式(关键字evaluate)
                text = str(x.string)
                desc = str(re.findall(r'"(?:evaluate)":".+"', text)[0])
                desc = str(str(desc.split(":")[1]).split('"')[1])
                desc = desc.replace("\n", "")
                desc = desc.replace("\r", "")
                desc = desc.replace("\\n", "")
                desc = desc.replace("\\r", "")
                desc = desc.replace(" ", "")
                desc = desc.replace("　", "")
                # 去除简介最前面的无用信息，如xxx译制
                if str(desc[0]) == str("【"):
                    try:
                        head_desc = str(re.findall(r'【\w+】', desc)[0])
                        desc = desc.replace(head_desc, "")
                    except:
                        try:
                            head_desc = str(re.findall(r'【.+】', desc)[0])
                            desc = desc.replace(head_desc, "")
                        except:
                            pass
                else:
                    pass
                try:
                    # 匹配VIP信息的正则表达式(关键字vip_promotion)
                    vip_info = str(re.findall(r'"vip_promotion":".+"', text)[0])
                    vip_info = str(str(vip_info.split(":")[1]).split('"')[1])
                    vip_info = vip_info.replace("\n", "")
                    vip_info = vip_info.replace("\r", "")
                    vip_info = vip_info.replace("\\n", "")
                    vip_info = vip_info.replace("\\r", "")
                    vip_info = vip_info.replace(" ", "")
                    vip_info = vip_info.replace("　", "")
                except IndexError:
                    try:
                        # 第二次匹配VIP信息的正则表达式(关键字promotion)
                        vip_info = str(re.findall(r'"(?:promotion)":".+"', text)[0])
                        vip_info = str(str(vip_info.split(":")[1]).split('"')[1])
                        vip_info = vip_info.replace("\n", "")
                        vip_info = vip_info.replace("\r", "")
                        vip_info = vip_info.replace("\\n", "")
                        vip_info = vip_info.replace("\\r", "")
                        vip_info = vip_info.replace(" ", "")
                        vip_info = vip_info.replace("　", "")
                    except IndexError:
                        # 均未匹配则表示免费
                        vip_info = str("免费")
                if str("开通大会员观看") == str(vip_info):
                    vip_info = str("大会员")
                elif str("成为大会员免费看") == str(vip_info):
                    vip_info = str("大会员")
                elif str("付费") == str(vip_info):
                    vip_info = str("付费")
                elif str("半价") == str(vip_info):
                    vip_info = str("付费")
                elif str("免费") == str(vip_info):
                    vip_info = str("免费")
                elif str("限时免费") == str(vip_info):
                    vip_info = str("限免")
                elif str("限免") == str(vip_info):
                    vip_info = str("限免")
                else:
                    # 由于付费的提示比较多样，所以放在最后
                    vip_info = str("大会员/付费")
            else:
                pass
        # 获取演员/声优列表
        re_text = text
        human_raw = str(re.findall(r'"actors":".+"', re_text)[0])
        human_raw = human_raw.split('"')
        re_text = str(human_raw[3])
        re_text = re_text.replace(r"\\n", "。")
        re_text = re_text.replace(r"\n", "。")
        re_text = re_text.replace(r"\\u002F", "/")
        re_text = re_text.replace(r"\u002F", "/")
        re_text = re_text.replace(r"\t", "")
        re_text = re_text.replace(r"\\t", "")
        actor_list = str(re_text).split("。")
        # 获取staff
        re_text = text
        staff_raw = str(re.findall(r'"staff":".+"', re_text)[0])
        staff_raw = staff_raw.split('"')
        re_text = str(staff_raw[3])
        re_text = re_text.replace(r"\\n", "。")
        re_text = re_text.replace(r"\n", "。")
        re_text = re_text.replace(r"\\u002F", "/")
        re_text = re_text.replace(r"\u002F", "/")
        re_text = re_text.replace(r"\t", "")
        re_text = re_text.replace(r"\\t", "")
        staff_list = str(re_text).split("。")
        # 获得番剧/电影标签
        re_text = text
        flag_raw = str(re.findall('"styles":\[\{.+\}\]', re_text)[0])
        flag_raw = flag_raw.split('[')[1]
        flag_raw = flag_raw.split(']')[0]
        flag_raw = flag_raw.split("},{")
        flag_list = []
        for raw in flag_raw:
            raw = str(raw)
            raw = raw.split('"')
            flag_list.append(str(raw[5]))
        # 获取完结/开播状态
        re_text = text
        end_raw = str(re.findall(r'"copyright":{"is_finish":.+,"is_started":.+}', re_text)[0])
        end_raw = end_raw.split('{')
        end_raw = end_raw[1].split('}')[0]
        end_raw = str(end_raw)
        end_raw = end_raw.replace('"', '')
        end_raw = end_raw.replace(':', '=')
        end_raw = end_raw.split(',')
        try:
            if end_raw[0] == str("is_finish=1"):
                is_finish = str("是")
            else:
                is_finish = str("否")
            if end_raw[1] == str("is_started=1"):
                is_started = str("是")
            else:
                is_started = str("否")
        except:
            is_finish = str("不支持")
            is_started = str("不支持")
        # 获取别名
        try:
            re_text = text
            re_text = str(re.findall(r'"alias":".+"', re_text)[0])
            alias_raw = re_text.split('"')
            alias_raw = str(alias_raw[3])
            alias_raw = alias_raw.replace(r"\\n", ",")
            alias_raw = alias_raw.replace(r"\n", ",")
            alias_raw = alias_raw.replace(r"\\u002F", "/")
            alias_raw = alias_raw.replace(r"\u002F", "/")
            alias_list = str(alias_raw).split(",")
        except:
            alias_list = str("不支持")
        # 获取开播时间
        try:
            re_text = text
            re_text = str(re.findall(r'"release_date_show":".+"', re_text)[0])
            showtime_raw = re_text.split('"')
            showtime_raw = str(showtime_raw[3])
            showtime_raw = showtime_raw.replace(r"\\n", ",")
            showtime_raw = showtime_raw.replace(r"\n", ",")
            showtime_raw = showtime_raw.replace(r"\\u002F", "/")
            showtime_raw = showtime_raw.replace(r"\u002F", "/")
            showtime = showtime_raw.replace("开播", "")
            showtime = showtime.replace("上映", "")
        except:
            showtime = "不支持"

        # 获取原名
        try:
            re_text = text
            re_text = str(re.findall(r'"origin_name":".+"', re_text)[0])
            origin_name_raw = re_text.split('"')
            origin_name_raw = str(origin_name_raw[3])
            origin_name_raw = origin_name_raw.replace(r"\\n", ",")
            origin_name_raw = origin_name_raw.replace(r"\n", ",")
            origin_name_raw = origin_name_raw.replace(r"\\u002F", "/")
            origin_name = origin_name_raw.replace(r"\u002F", "/")
        except:
            origin_name = "不支持"
        # 返回结果，总共使用3个Bilibili API，2个内建API和一个HTML页
        return_dict = {"title": title, "type": type, "area": area, "share_url": share_url, "desc": desc,
                       "cover_url": cover_url, "media_id": media_id, "ep_id": ep_id, "episode": episode,
                       "rating_count": rating_count, "score": score, "season_id": season_id, "coins": coins,
                       "danmakus": danmakus, "follow": follow, "series_follow": series_follow, "views": views,
                       "tag_id": tag_id, "vip_info": vip_info, "aid": av_no, "bvid": bv_no, "quality": quality,
                       "quality_ID": quality_ID, "is_finish": is_finish, "is_started": is_started,
                       "actor_list": actor_list,
                       "staff_list": staff_list, "flag_list": flag_list, "alias_list": alias_list, "showtime": showtime,
                       "origin_name": origin_name}
        if return_dict:
            return return_dict
        else:
            raise InfoError("No info.")
    except:
        try:
            if str(message) == str("请求错误"):
                raise RequestError("Request error.")
            elif str(message) == str("啥都木有"):
                raise SeemsNothing("Seems no such info.")
            elif str(message) == str("服务调用超时"):
                raise Timeout("Timeout.")
            elif str(message) == str("请求被拦截"):
                raise RequestRefuse("Banning.")
            else:
                # 目前不太可能出现未知错误
                print(message)
                traceback.print_exc()
                raise InfoError("Something error.")
        except:
            traceback.print_exc()
            raise InfoError("Something error.")


# 获取用户信息
# 这个是实验性API，理论效果更好，功能更多，流量开销更小
def user_info(uid_input):
    uid_input = int(uid_input)
    ua = str(UserAgent(path=ua_json).random)
    headers = {"Host": "api.bilibili.com", "User-Agent": ua}
    # 返回的结果基本来自此API
    try:
        info_get = requests.get("https://api.bilibili.com/x/space/acc/info?mid=" + str(uid_input), headers=headers,
                                timeout=timeout, cookies=cookies)
    except requests.exceptions.ReadTimeout:
        raise Timeout("Timeout.")
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
    # B站用户大会员类型就三种：普通用户(不返回值)，大会员，年度大会员
    if vip_type == str("大会员") or vip_type == str("年度大会员"):
        pass
    # 防止愚人节的临时改动造成lib和用户代码异常
    elif vip_type == str("小会员"):
        vip_type == str("大会员")
    elif vip_type == str("年度小会员"):
        vip_type == str("年度大会员")
    else:
        vip_type == str("None")
    try:
        # 获取关注/粉丝量
        fans = requests.get("https://api.bilibili.com/x/relation/stat?vmid=" + str(uid_input), headers=headers,
                            timeout=timeout, cookies=cookies)
    except requests.exceptions.ReadTimeout:
        raise Timeout("Timeout.")
    fans = fans.json()
    following = fans['data']['following']
    fans = fans['data']['follower']
    return_dict = {"name": name, "uid": uid, "fans": fans, "following": following, "sex": sex, "level": level,
                   "face_url": face_url, "sign": sign, "birthday": birthday, "coins": coins, "vip_type": vip_type}
    # 返回字典，总共使用两个API
    return return_dict



# 获取弹幕(自动转换为可读性较高的csv)
def get_danmaku(cid_input, reset=False):
    try:
        if str(cid_input).isdigit():
            url = str('http://comment.bilibili.com/' + str(cid_input) + '.xml')
            file_name = str(str(cid_input) + '.csv')
        else:
            raise InfoError('You should input cid ONLY.')

        if os.path.exists(file_name):
            if reset:
                pass
            else:
                print(str(os.path.abspath(file_name)))
                return os.path.abspath(file_name)
        else:
            pass

        bvIndex = url.find('BV')
        id = url[bvIndex:]
        try:
            rr = requests.get(url=url, timeout=timeout, cookies=cookies)
        except requests.exceptions.ReadTimeout:
            raise Timeout("Timeout.")
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


# 根据csv文件列出所有弹幕
# 列出的弹幕会被处理，例如转换时间戳
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


# 数弹幕行数
# 虽然没什么难的，但是意义在于辅助弹幕文件的遍历
def count_danmaku(file_path):
    if os.path.exists(file_path):
        pass
    else:
        raise danmakuError('danmaku file is not existed.')

    file_path = open(str(file_path), 'r', encoding='utf-16')
    return len(file_path.readlines())


# 获取弹幕(原始信息，即xml)
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
            if reset:
                pass
            else:
                return os.path.abspath(file_name)
        else:
            pass

        url = str('http://comment.bilibili.com/' + str(cid_input) + '.xml')
        try:
            rr = requests.get(url=url, timeout=timeout, cookies=cookies)
        except requests.exceptions.ReadTimeout:
            raise Timeout("Timeout.")
        rr.encoding = 'uft-8'
        xml = open(file_name, "w", encoding="utf-8")
        xml.write(rr.text)
        xml.close()
        print(os.path.abspath(file_name))
        return os.path.abspath(file_name)

    except Exception as e:
        print(e)


# 弹幕文件(xml)转字幕文件(ass)
# 对于某些不支持弹幕的播放器可以用这个API
# 现支持跨平台运行
# 已经测试Potplayer(Windows)和nPlayer(iOS)，弹幕无异常
def raw2ass(file_path):
    import platform
    sysstr = platform.system()
    final_file = str(str(file_path).split('.xml')[0]) + ".ass"
    if sysstr == "Windows":
        os.system("python .\\niconvert-master\\main.py \"" + str(file_path) + "\" -o \"" + str(final_file) + "\"")
    else:
        os.system("python3 ./niconvert-master/main.py \"" + str(file_path) + "\" -o \"" + str(final_file) + "\"")
    for i in range(0, 60):
        if os.path.exists(final_file):
            print(os.path.abspath(final_file))
            return os.path.abspath(final_file)
            break
        else:
            time.sleep(1)
    print("FAIL")


# 搜索番剧(beta)
# 目前只支持搜索番剧，输入关键词返回字典，含有md号
# 最多返回20条
def search_anime(keyword, strict=True):
    return_dict = {}
    ua = str(UserAgent(path=ua_json).random)
    headers = {"User-Agent": ua}
    # 搜索，拿到season_id
    search_info = requests.get("https://search.bilibili.com/bangumi?keyword=" + str(keyword), headers=headers,
                               timeout=timeout, cookies=cookies)
    if str(search_info.status_code) == str("404"):
        return return_dict
    elif str(search_info.status_code) == str("412"):
        raise RequestRefuse("Banning.")
    else:
        pass
    search_raw = str(search_info.text)
    page = str(re.findall('numPages\":\\d,\"',search_raw)[0])
    page = str(page.replace(':',''))
    page = str(page.replace(',', ''))
    page = int(page.split('"')[1])
    result_list_raw = re.findall('ss\\d+/\\?from=search\" title=\".+?\" target=\"_blank\" ',search_raw)
    title_list = []
    for id in range(0,len(result_list_raw)):
        raw = result_list_raw[id]
        season_id = str(str(raw).split("/")[0])
        title = str(str(raw).split("title=")[1])
        title = str(title.split("target=")[0])
        title = title.replace(" ","")
        title = str(title.replace('"',''))
        if title in title_list:
            continue
        else:
            title_list.append(title)

        if strict:
            if bool(re.search(keyword, title, re.IGNORECASE)):
                pass
            else:
                continue
        else:
            pass
            # 跳转到播放页，拿到season_id
        md_info = requests.get("https://www.bilibili.com/bangumi/play/" + str(season_id), headers=headers,
                                   timeout=timeout, cookies=cookies)
        md_info = md_info.text
        media_id = re.findall("md\d+", md_info)[0]
        return_dict[title] = media_id
    print("1 / " + str(page))
    if page == 1:
        pass
    else:
        time.sleep(5)
        for request_page in range(2, page + 1):
            search_info = requests.get("https://search.bilibili.com/bangumi?keyword=" + str(keyword) + "&page=" + str(request_page)
                                       , headers=headers,timeout=timeout, cookies=cookies)
            if str(search_info.status_code) == str("404"):
                return return_dict
            elif str(search_info.status_code) == str("412"):
                return return_dict
                raise RequestRefuse("Banning.")
            else:
                pass
            search_raw = str(search_info.text)
            result_list_raw = re.findall('ss\\d+/\\?from=search\" title=\".+?\" target=\"_blank\" ', search_raw)
            title_list = []
            for id in range(0, len(result_list_raw)):
                raw = result_list_raw[id]
                season_id = str(str(raw).split("/")[0])
                title = str(str(raw).split("title=")[1])
                title = str(title.split("target=")[0])
                title = title.replace(" ", "")
                title = str(title.replace('"', ''))
                if title in title_list:
                    continue
                else:
                    title_list.append(title)

                if strict:
                    if bool(re.search(keyword, title, re.IGNORECASE)):
                        pass
                    else:
                        continue
                else:
                    pass
                    # 跳转到播放页，拿到season_id
                md_info = requests.get("https://www.bilibili.com/bangumi/play/" + str(season_id), headers=headers,
                                       timeout=timeout, cookies=cookies)
                md_info = md_info.text
                media_id = re.findall("md\d+", md_info)[0]
                return_dict[title] = media_id
            print(str(request_page) + " / " + str(page))
            if request_page == page:
                pass
            else:
                time.sleep(5)

    return return_dict


# 搜索视频功能，返回包含字典的列表，字典含标题，BV号，播放量，up主和发布时间
def search_video(keyword):
    return_list = []
    ua = str(UserAgent(path=ua_json).random)
    headers = {"User-Agent": ua}
    search_info = requests.get("https://search.bilibili.com/video?keyword=" + str(keyword), headers=headers,
                               timeout=timeout, cookies=cookies)
    if str(search_info.status_code) == str("404"):
        return return_list
    elif str(search_info.status_code) == str("412"):
        raise RequestRefuse("Banning.")
    else:
        pass
    search_txt = search_info.text
    page = str(re.findall("numPages\":\\d*?,\"", search_txt)[0])
    page = page.replace(":", "")
    page = page.replace(",", "")
    page = int(page.split('"')[1])
    if page == 0:
        raise SeemsNothing("No result.")
    bv_title_list = re.findall("/BV.*?\\?from=search\" title=\".+?\"", search_txt)
    time_list = re.findall(r"\d{4}-\d{2}-\d{2}", search_txt)
    name_list_raw = re.findall('class="up-name">.*?<', search_txt)
    playback_list_raw = re.findall(',"play":\d*,"', search_txt)
    for id in range(0,len(bv_title_list)):
        raw_text = bv_title_list[id]
        bv = str(str(raw_text).split("?")[0]).replace("/","")
        title = str(str(raw_text).split("title=")[1]).replace('"',"")
        title = title.replace('<em class="keyword">',"")
        title = str(title.replace('</em>', ""))
        put_time = str(time_list[id])
        up_name = str(str(name_list_raw[id]).split(">")[1]).split("<")[0]
        playback = str(str(str(playback_list_raw[id]).replace(",", "").replace(":", "")).split('"')[2])
        write_dict = {"bv":bv,"title":title,"put_time":put_time,"up_name":up_name,"playback":playback}
        return_list.append(write_dict)
    print("1 / " + str(page))
    if page == 1:
        pass
    else:
        time.sleep(5)
        for request_page in range(2,page + 1):
            headers = {"User-Agent": ua}
            search_info = requests.get("https://search.bilibili.com/video?keyword=" + str(keyword) + "&page=" + str(request_page),
                                       headers=headers,timeout=timeout, cookies=cookies)
            if str(search_info.status_code) == str("404"):
                return return_list
            elif str(search_info.status_code) == str("412"):
                return return_list
                raise RequestRefuse("Banning." )
            else:
                pass
            search_txt = search_info.text
            page = str(re.findall("numPages\":\\d*?,\"", search_txt)[0])
            page = page.replace(":", "")
            page = page.replace(",", "")
            page = int(page.split('"')[1])
            if page == 0:
                raise SeemsNothing("No result.")
            bv_title_list = re.findall("/BV.*?\\?from=search\" title=\".+?\"", search_txt)
            time_list = re.findall(r"\d{4}-\d{2}-\d{2}", search_txt)
            name_list_raw = re.findall('class="up-name">.*?<', search_txt)
            playback_list_raw = re.findall(',"play":\d*,"', search_txt)
            for id in range(0, len(bv_title_list)):
                raw_text = bv_title_list[id]
                bv = str(str(raw_text).split("?")[0]).replace("/", "")
                title = str(str(raw_text).split("title=")[1]).replace('"', "")
                title = title.replace('<em class="keyword">', "")
                title = str(title.replace('</em>', ""))
                put_time = str(time_list[id])
                up_name = str(str(name_list_raw[id]).split(">")[1]).split("<")[0]
                playback = str(str(str(playback_list_raw[id]).replace(",", "").replace(":", "")).split('"')[2])
                write_dict = {"bv": bv, "title": title, "put_time": put_time, "up_name": up_name, "playback": playback}
                return_list.append(write_dict)
            print(str(request_page) + " / " + str(page))
            if request_page == page:
                pass
            else:
                time.sleep(5)
    return return_list
