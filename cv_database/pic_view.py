from pyecharts.charts import Bar
from pyecharts import options as opts
import pymysql
from pyecharts.options.global_options import ThemeType

db = pymysql.connect("localhost","root","123456","bili",charset='utf8')
find = db.cursor()
data_exist = find.execute("select title,views from anime")
all_list = list(find.fetchall())
find.close()
anime_list = []
view_list = []
all_dict = {}
for i in all_list:
    anime = str(i[0])
    view = int(i[1])
    all_dict[anime] = view
all_dict = sorted(all_dict.items(),  key=lambda d: d[1], reverse=False)
for i in all_dict:
    anime = str(i[0])
    view = int(i[1])
    anime_list.append(anime)
    view_list.append(view)


bar = Bar()
bar = Bar(init_opts=opts.InitOpts(bg_color='rgba(255,250,205,0.2)',
                width='2500px',
                height='1400px',
                page_title='数据库内番剧播放量',
                theme=ThemeType.MACARONS
                )
            )
bar.add_xaxis(anime_list)
bar.add_yaxis("播放量", view_list)
bar.set_global_opts(title_opts=opts.TitleOpts(title="数据库内番剧播放量"),xaxis_opts=opts.AxisOpts(axislabel_opts={"interval":"0"}))
bar.reversal_axis()
bar.render()


