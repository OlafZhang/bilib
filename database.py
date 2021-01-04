import pymysql
import bilib
import time
import opencc
from media_id_pool import *

cc = opencc.OpenCC('t2s')
db = pymysql.connect("localhost","root","123456","bili",charset='utf8')

def write_into_database(mediaID):
    mediaID = mediaID
    find_mediaID = db.cursor()
    data_exist = find_mediaID.execute("select * from anime where media_id = " + str(mediaID))
    if data_exist == 0:
        pass
    else:
        get_result = str(list(find_mediaID.fetchall())[0][1])
        print(str(mediaID) + ": Data existed.(" + get_result + ")")
        find_mediaID.close()
        return

    try:
        base_info = bilib.anime_base_info(mediaID)
        season_id = int(base_info["season_id"])
        episode_info = bilib.anime_episode_info(season_id)
    except:
        print(str(mediaID) + ": No info")

    try:
        write_timestamp = str(int(time.time()))
        database_cursor = db.cursor()
        quality_ID = str(base_info["quality_ID"])
        if quality_ID.isdigit():
            pass
        else:
            quality_ID = str("0")
        command = str('insert into anime values(%s,"%s","%s","%s","%s","%s","%s","%s","%s",%s,%s,%s,%s,%s,%s,%s,%s,%s,"%s","%s","%s","%s",%s,"%s","%s","%s",%s)' %
                   (str(base_info["media_id"]),str(base_info["title"]),str(base_info["origin_name"]),str(base_info["type"])
                    ,str(base_info["area"]),str(base_info["share_url"]),str(base_info["desc"]),str(base_info["cover_url"])
                    ,str(base_info["episode"]),str(base_info["rating_count"]),str(base_info["score"]),str(base_info["season_id"])
                    ,str(base_info["coins"]),str(base_info["danmakus"]),str(base_info["follow"]),str(base_info["series_follow"])
                    ,str(base_info["views"]),str(base_info["tag_id"]),str(base_info["vip_info"]),str(base_info["aid"])
                    ,str(base_info["bvid"]),str(base_info["quality"]),quality_ID,str(base_info["is_finish"])
                    ,str(base_info["is_started"]),str(base_info["showtime"]),str(write_timestamp)))
        database_cursor.execute(command)
        db.commit()
        database_cursor.close()


        alias_list = base_info["alias_list"]
        for alias in alias_list:
            if str(alias) == str(""):
                continue
            elif str(" ") in str(alias):
                continue
            else:
                pass
            database_cursor = db.cursor()
            command = str('insert into alias values(%s,"%s","%s")' % (str(base_info["media_id"]),str(base_info["title"]),str(alias)))
            database_cursor.execute(command)
            db.commit()
            database_cursor.close()

        actor_list = base_info["actor_list"]
        after_input_user = False
        for name in actor_list:
            if str(":") in str(name):
                name = name.split(":")
                actor = cc.convert(str(name[1]))
                character = cc.convert(str(name[0]))
                actor = actor.replace(" ","")
                character = character.replace(" ","")
                if str("篇") in character:
                    continue
                else:
                    pass
                if str("、") in str(actor):
                    actor = actor.replace(" ", "")
                    actor = actor.replace("，", "、")
                    actor_list = actor.split("、")
                    for part_actor in actor_list:
                        database_cursor = db.cursor()
                        command = str('insert into actor values(%s,"%s","%s","%s")' % (
                            str(base_info["media_id"]), str(base_info["title"]),str(character), str(part_actor)))
                        database_cursor.execute(command)
                        db.commit()
                        database_cursor.close()

                elif str("/") in str(actor):
                    actor = actor.replace(" ", "")
                    actor_list = actor.split("/")
                    for part_actor in actor_list:
                        database_cursor = db.cursor()
                        command = str('insert into actor values(%s,"%s","%s","%s")' % (
                            str(base_info["media_id"]), str(base_info["title"]), str(character), str(part_actor)))
                        database_cursor.execute(command)
                        db.commit()
                        database_cursor.close()

                else:
                    database_cursor = db.cursor()
                    command = str('insert into actor values(%s,"%s","%s","%s")' % (
                        str(base_info["media_id"]), str(base_info["title"]), str(character), str(actor)))
                    database_cursor.execute(command)
                    db.commit()
                    database_cursor.close()

            elif str("：") in str(name):
                name = name.split("：")
                actor = cc.convert(str(name[1]))
                character = cc.convert(str(name[0]))
                actor = actor.replace(" ","")
                character = character.replace(" ","")
                if str("篇") in character:
                    continue
                else:
                    pass
                if str("、") in str(actor):
                    actor = actor.replace(" ", "")
                    actor = actor.replace("，", "、")
                    actor_list = actor.split("、")
                    for part_actor in actor_list:
                        database_cursor = db.cursor()
                        command = str('insert into actor values(%s,"%s","%s","%s")' % (
                            str(base_info["media_id"]), str(base_info["title"]), str(character), str(part_actor)))
                        database_cursor.execute(command)
                        db.commit()
                        database_cursor.close()

                elif str("/") in str(actor):
                    actor = actor.replace(" ", "")
                    actor_list = actor.split("/")
                    for part_actor in actor_list:
                        database_cursor = db.cursor()
                        command = str('insert into actor values(%s,"%s","%s","%s")' % (
                            str(base_info["media_id"]), str(base_info["title"]), str(character), str(part_actor)))
                        database_cursor.execute(command)
                        db.commit()
                        database_cursor.close()

                else:
                    database_cursor = db.cursor()
                    command = str('insert into actor values(%s,"%s","%s","%s")' % (
                        str(base_info["media_id"]), str(base_info["title"]), str(character), str(actor)))
                    database_cursor.execute(command)
                    db.commit()
                    database_cursor.close()
            else:
                database_cursor = db.cursor()
                actor = cc.convert(str(name))
                character = str("#未定义角色名#")
                after_input_user = True
                actor = actor.replace(" ","")
                command = str('insert into actor values(%s,"%s","%s","%s")' % (
                    str(base_info["media_id"]), str(base_info["title"]), str(character), str(actor)))
                database_cursor.execute(command)
                db.commit()
                database_cursor.close()

        flag_list = base_info["flag_list"]
        for flag in flag_list:
            database_cursor = db.cursor()
            command = str('insert into flag values(%s,"%s","%s")' % (
                str(base_info["media_id"]), str(base_info["title"]), str(flag)))
            database_cursor.execute(command)
            db.commit()
            database_cursor.close()

        staff_list = base_info["staff_list"]
        for name in staff_list:
            if str(":") in str(name):
                name = name.split(":")
                job = cc.convert(str(name[0]))
                name = cc.convert(str(name[1]))
                database_cursor = db.cursor()
                command = str('insert into staff values(%s,"%s","%s","%s")' % (
                    str(base_info["media_id"]), str(base_info["title"]), str(job), str(name)))
                database_cursor.execute(command)
                db.commit()
                database_cursor.close()

            elif str("：") in str(name):
                name = name.split("：")
                job = cc.convert(str(name[0]))
                name = cc.convert(str(name[1]))
                database_cursor = db.cursor()
                command = str('insert into staff values(%s,"%s","%s","%s")' % (
                    str(base_info["media_id"]), str(base_info["title"]), str(job), str(name)))
                database_cursor.execute(command)
                db.commit()
                database_cursor.close()

            else:
                job = str("")
                database_cursor = db.cursor()
                command = str('insert into staff values(%s,"%s","%s","%s")' % (
                    str(base_info["media_id"]), str(base_info["title"]), str(job), str(name)))
                database_cursor.execute(command)
                db.commit()
                database_cursor.close()


        for ep_id, ep_info in episode_info.items():
            if str(ep_id).isdigit() or (str(ep_id).split(".")[0]).isdigit():
                episode = str("第" + str(ep_id) + "集")
            else:
                episode = str(ep_id)
            title_long = str(ep_info["title_long"])
            ep_id = str(ep_info["ep_id"])
            cid = str(ep_info["cid"])
            cover_url = str(ep_info["cover_url"])
            share_url = str(ep_info["share_url"])

            database_cursor = db.cursor()
            command = str('insert into episode values(%s,%s,"%s","%s",%s,"%s","%s")' % (
                ep_id,str(base_info["media_id"]),episode,title_long,cid,cover_url,share_url))
            database_cursor.execute(command)
            db.commit()
            database_cursor.close()

        print(str(mediaID) + ": Done.(" + str(base_info["title"]) + ")")
        if after_input_user:
            print("Now you should search some character name, some of them in database is NONE.")
        return
    except Exception:
        db.rollback()

def find_actor(actor_name,fuzzy = False):
    find = db.cursor()
    if fuzzy:
        data_exist = find.execute("select * from actor where `actor` like '%" + str(actor_name) + "%'")
    else:
        data_exist = find.execute("select * from actor where `actor` = '" + str(actor_name) + "'")
    if data_exist == 0:
        print('没有在数据库查询到名为"' + str(actor_name) + '"的声优。')
        find.close()
        if not fuzzy:
            print("模糊搜索未开启，请尝试模糊搜索")
        else:
            pass
        return
    else:
        pass
    actor_list = list(find.fetchall())
    find.close()
    count = len(actor_list)
    print("@查询到" + str(count) + "条结果")
    print("|- 搜索内容：" + str(actor_name))
    result_actor = []
    for item in actor_list:
        if str(item[3]) in result_actor:
            continue
        else:
            result_actor.append(str(item[3]))
    for lock_actor in result_actor:
        print("|--- 声优：" + str(lock_actor))
        for item in actor_list:
            if str(item[3]) == str(lock_actor):
                pass
            else:
                continue
            character = str(item[2])
            anime = str(item[1])
            print("      |--- " + character + " - 《" + anime + "》")
    

def find_character(character_name,fuzzy = False):
    character_name = str(character_name)
    find = db.cursor()
    if fuzzy:
        data_exist = find.execute("select * from actor where `character` like '%" + str(character_name) + "%'")
    else:
        data_exist = find.execute("select * from actor where `character` = '" + str(character_name) + "'")
    if data_exist == 0:
        print('没有在数据库查询到名为"' + str(character_name) + '"的角色。')
        find.close()
        if not fuzzy:
            print("模糊搜索未开启，请尝试模糊搜索")
        else:
            pass
        return
    else:
        pass
    character_list = list(find.fetchall())
    find.close()
    result_list = []
    count = 0
    for item in character_list:
        if str(item[2]) in result_list:
            pass
        else:
            result_list.append(str(item[2]))
        count += 1
    if fuzzy:
        print("@ 模糊查询到" + str(count) + "条有关\"" + str(character_name) +"\"的结果")
    else:
        pass
    find.close()
    for item in result_list:
        print("|")
        anime = ""
        cv = ""
        count = 0
        character_name = str(item)
        find = db.cursor()
        data = find.execute("select * from actor where `character` = '" + str(character_name) + "'")
        data_list = list(find.fetchall())
        data_anime_used = []
        for item in data_list:
            if str(item[1]) in data_anime_used:
                continue
            else:
                pass
            data_anime_used.append(str(item[1]))
            anime += str("《" + item[1] + "》")
            anime += str("、")
            count += 1
        print("--- 查询到" + str(count) + "条有关\"" + str(character_name) +"\"的结果")
        cv_list = []
        for i in range(0,len(data_list)):
            cv = str(data_list[i][3])
            if cv in cv_list:
                continue
            else:
                cv_list.append(cv)
            character = str(data_list[i][2])
            anime_info = anime[0:len(anime)-1]
            print("  @ 角色\"" + str(character_name) + "\"出自" + str(anime_info) + "，其声优是 " + str(cv),end="")
            find = db.cursor()
            data_exist = find.execute("select * from actor where `actor` = '" + str(cv) + "'")
            actor_list = list(find.fetchall())
            find.close()
            find_full = db.cursor()
            full = find_full.execute("select * from full_actor where `name` = '" + str(cv) + "'")
            if int(full) == 0:
                print("，此声优看起来不在完整声优数据库中。")
            else:
                print("，此声优在完整声优数据库中。")
                finded = list(find_full.fetchall())
                is_alive = finded[0][4]
                if int(is_alive) == 0:
                    print("    。。。且此声优已故，R.I.P.")
                elif int(is_alive) == 2:
                    print("    。。。且此声优已隐退声优界")
                else:
                    pass
            find_full.close()
            count = 0
            for thing in actor_list:
                if str(thing[1]) in str(anime_info) and str(thing[2]) == str(character_name):
                    continue
                else:
                    count += 1
            if count == 0:
                print('   没有在数据库查询到声优为 ' + str(cv) + ' 的其它角色。')
                find.close()
            else:
                print("  @ 根据此声优，查询到" + str(count) + "条结果")
                for item in actor_list:
                    character = str(item[2])
                    part_anime = str(item[1])
                    if str(anime) in str(anime_info) and str(character) in str(character_name):
                        continue
                    else:
                        pass
                    if character == character_name:
                        continue
                    elif character_name in character:
                        continue
                    else:
                        print("  |--- " + character + " - 《" + part_anime + "》")
                print("           ")
    return

def find_anime(title,fuzzy = False):
    title = str(title)
    find = db.cursor()
    if fuzzy:
        data_exist = find.execute("select * from actor where `title` like '%" + str(title) + "%'")
    else:
        data_exist = find.execute("select * from actor where `character` = '" + str(title) + "'")
    if data_exist == 0:
        print('没有在数据库查询到名为"' + str(title) + '"的番剧/电影。')
        find.close()
        if not fuzzy:
            print("模糊搜索未开启，请尝试模糊搜索")
        else:
            pass
        return
    else:
        pass
    anime_list = list(find.fetchall())
    anime_result_list = []
    for i in anime_list:
        if str(i[1]) in anime_result_list:
            pass
        else:
            anime_result_list.append(str(i[1]))
    if fuzzy:
        print("@ 模糊查询到" + str(len(anime_result_list)) + "条有关\"" + str(title) + "\"的结果")
    else:
        print("@ 查询到" + str(len(anime_result_list)) + "条有关\"" + str(title) + "\"的结果")
    for anime_name in anime_result_list:
        print("--- 《" + str(anime_name) +"》")
        for item in anime_list:
            if str(item[1]) == str(anime_name):
                print(str("     ") +str(item[2])  + " --> " + str(item[3]))
            else:
                pass
        for item in anime_list:
            if str(item[1]) == str(anime_name):
                find_character(str(item[2]),fuzzy=False)
            else:
                pass
    find.close()

find_character("由崎司",fuzzy=True)

