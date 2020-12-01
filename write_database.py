import pymysql
import bilib
import time
import opencc
from media_id_pool import *
from write_database import *

def write_into_database(mediaID):
    cc = opencc.OpenCC('t2s')
    db = pymysql.connect("localhost","root","123456","bili")

    mediaID = mediaID

    find_mediaID = db.cursor()
    data_exist = find_mediaID.execute("select * from anime where media_id = " + str(mediaID))
    if data_exist == 0:
        pass
    else:
        print("Data existed.")
        return

    try:
        base_info = bilib.anime_base_info(mediaID)
        season_id = int(base_info["season_id"])
        episode_info = bilib.anime_episode_info(season_id)
    except:
        print("No info")

    try:
        write_timestamp = str(int(time.time()))
        database_cursor = db.cursor()
        command = str('insert into anime values(%s,"%s","%s","%s","%s","%s","%s","%s","%s",%s,%s,%s,%s,%s,%s,%s,%s,%s,"%s","%s","%s","%s",%s,"%s","%s","%s",%s)' %
                   (str(base_info["media_id"]),str(base_info["title"]),str(base_info["origin_name"]),str(base_info["type"])
                    ,str(base_info["area"]),str(base_info["share_url"]),str(base_info["desc"]),str(base_info["cover_url"])
                    ,str(base_info["episode"]),str(base_info["rating_count"]),str(base_info["score"]),str(base_info["season_id"])
                    ,str(base_info["coins"]),str(base_info["danmakus"]),str(base_info["follow"]),str(base_info["series_follow"])
                    ,str(base_info["views"]),str(base_info["tag_id"]),str(base_info["vip_info"]),str(base_info["aid"])
                    ,str(base_info["bvid"]),str(base_info["quality"]),str(base_info["quality_ID"]),str(base_info["is_finish"])
                    ,str(base_info["is_started"]),str(base_info["showtime"]),str(write_timestamp)))
        database_cursor.execute(command)
        db.commit()
        database_cursor.close()


        alias_list = base_info["alias_list"]
        for alias in alias_list:
            database_cursor = db.cursor()
            command = str('insert into alias values(%s,"%s","%s")' % (str(base_info["media_id"]),str(base_info["title"]),str(alias)))
            database_cursor.execute(command)
            db.commit()
            database_cursor.close()

        actor_list = base_info["actor_list"]
        for name in actor_list:
            if str(":") in str(name):
                name = name.split(":")
                actor = cc.convert(str(name[1]))
                character = cc.convert(str(name[0]))
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
                character = str(" ")
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

        print("Done.")
        return

    except Exception:
        db.rollback()