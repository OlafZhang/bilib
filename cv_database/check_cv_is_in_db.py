import pymysql
import log
db = pymysql.connect("localhost","root","123456","bili",charset='utf8')

log.log_write(message="开始数据库CV检查...",path="C:\\Users\\10245\\OneDrive\\Python\\bilib\\global_log.txt",level=1,service="check_cv_in_db.py")
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
info = str("在 完整数据库 加载了 " + str(length) + " 个声优")
log.log_write(message=info,path="C:\\Users\\10245\\OneDrive\\Python\\bilib\\global_log.txt",level=1,service="check_cv_in_db.py")

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
info = str("在 已知番剧库 加载了 " + str(length) + " 个声优")
log.log_write(message=info,path="C:\\Users\\10245\\OneDrive\\Python\\bilib\\global_log.txt",level=1,service="check_cv_in_db.py")

not_in = 0
for name in full_list:
    database_cursor = db.cursor()
    command = str('select * from full_actor where name = "%s"' % str(name))
    data_exist = database_cursor.execute(command)
    if int(data_exist) == 0:
        error_1 = str(str(name) + " 看上去不在完整声优库中")
        not_in += 1
        error_cursor = db.cursor()
        command = str('select * from actor where actor like \"' + str(name) + '\"')
        error_cursor.execute(command)
        db.commit()
        find = error_cursor.fetchall()
        for i in find:
            error_2 = str("，问题发生在：" + str(i))
            error = str(error_1 + error_2)
            log.log_write(message=error,path="C:\\Users\\10245\\OneDrive\\Python\\bilib\\global_log.txt",level=2,service="check_cv_in_db.py")
    else:
        pass
    db.commit()
    database_cursor.close()
if not_in == 0:
    log.log_write(message="完成数据库检查，未发现问题",path="C:\\Users\\10245\\OneDrive\\Python\\bilib\\global_log.txt",level=1,service="check_cv_in_db.py")
else:
    error = str("总共 " + str(not_in) + " 个未匹配")
    log.log_write(message="完成数据库检查，" +str(error),path="C:\\Users\\10245\\OneDrive\\Python\\bilib\\global_log.txt",level=2,service="check_cv_in_db.py")