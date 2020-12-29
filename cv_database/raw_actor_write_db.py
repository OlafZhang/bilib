import pymysql
db = pymysql.connect("localhost","root","123456","bili",charset='utf8')
raw_file = open(".\\Desktop\\raw.txt","r",encoding="utf-8")
target_file = open(".\\Desktop\\target.txt","a",encoding="utf-8")
region = str("JP")
for line in raw_file.readlines():
    # 识别组
    if str("| group") in str(line):
        line = str(line)
        line = str(line.split("=")[1])
        line = line.replace(" ","")
        line = line.replace("\n","")
        type_name = str(line)
        continue
    # 识别性别
    elif str(r"{{plate") in str(line):
        line = str(line)
        line = str(line.split("|")[1])
        line = line.replace(" ","")
        line = line.replace("\n","")
        line = line.replace("}","")
        sex = str(line)
        continue
    # 表示退出声优界的声优
    elif str(r"''") in str(line):
        line = str(line)
        line = line.replace(r"''","")
        line = line.replace("•","")
        line = line.replace(" ","")
        line = line.replace("\n","")
        line = line.replace("[","")
        line = line.replace("]","")
        command = str("insert into full_actor values('%s','%s','%s','%s',%s)"%(str(line),str(sex),str(region),str(type_name),str("2")))
        print(command)
        database_cursor = db.cursor()
        database_cursor.execute(command)
        db.commit()
        database_cursor.close()
    # 表示已故声优
    elif str("dead") in str(line):
        line = str(line)
        line = line.replace("{","")
        line = line.replace("}","")
        line = line.replace("dead","")
        line = line.replace("|","")
        line = line.replace("•","")
        line = line.replace(" ","")
        line = line.replace("\n","")
        command = str("insert into full_actor values('%s','%s','%s','%s',%s)"%(str(line),str(sex),str(region),str(type_name),str("0")))
        print(command)
        database_cursor = db.cursor()
        database_cursor.execute(command)
        db.commit()
        database_cursor.close()
    # 表示正常状态的声优
    elif str(line)[0] == str("["):
        line = str(line)
        line = line.replace("•","")
        line = line.replace(" ","")
        line = line.replace("\n","")
        line = line.replace("[","")
        line = line.replace("]","")
        if str("|") in str(line):
            line = str(line.split("|")[0])
        else:
            pass
        if str("(") in str(line):
            line = str(line.split("(")[0])
        else:
            pass
        command = str("insert into full_actor values('%s','%s','%s','%s',%s)"%(str(line),str(sex),str(region),str(type_name),str("1")))
        print(command)
        database_cursor = db.cursor()
        database_cursor.execute(command)
        db.commit()
        database_cursor.close()
target_file.close()