import pymysql
db = pymysql.connect("localhost","root","123456","bili",charset='utf8')

database_cursor = db.cursor()
command = str('select name from full_actor')
database_cursor.execute(command)
db.commit()
find = database_cursor.fetchall()
full_list = []
for i in find:
    name = str(i[0])
    if name in full_list:
        pass
    else:
        full_list.append(name)
database_cursor.close()
length = len(full_list)
print("在 完整数据库 加载了 " + str(length) + " 个声优")

database_cursor = db.cursor()
command = str('select actor from actor')
database_cursor.execute(command)
db.commit()
find = database_cursor.fetchall()
full_list = []
for i in find:
    name = str(i[0])
    if name in full_list:
        pass
    else:
        full_list.append(name)
database_cursor.close()
length = len(full_list)
print("在 已知番剧库 加载了 " + str(length) + " 个声优")

not_in = 0
for name in full_list:
    database_cursor = db.cursor()
    command = str('select * from full_actor where name = "%s"' % str(name))
    data_exist = database_cursor.execute(command)
    if int(data_exist) == 0:
        print(str(name) + " 看上去不在完整声优库中")
        not_in += 1
    else:
        pass
    db.commit()
    database_cursor.close()
if not_in == 0:
    print("已知番剧库 均能与 完整数据库 匹配")
else:
    print("总共 " + str(not_in) + " 个未匹配")