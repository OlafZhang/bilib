from pyecharts.charts import Bar
from pyecharts import options as opts
import pymysql
from pyecharts.options.global_options import ThemeType

db = pymysql.connect("localhost","root","123456","bili",charset='utf8')
find = db.cursor()
data_exist = find.execute("select title,score from anime order by score")
all_list = list(find.fetchall())
find.close()
anime_list = []
score_list = []

for i in all_list:
    anime = str(i[0])
    score = float(i[1])
    anime_list.append(anime)
    score_list.append(score)



bar = Bar()
bar = Bar(init_opts=opts.InitOpts(bg_color='rgba(255,250,205,0.2)',
                width='800px',
                height='1400px',
                page_title='数据库内番剧评分',
                theme=ThemeType.MACARONS
                )
            )
bar.add_xaxis(anime_list)
bar.add_yaxis("评分", score_list)
bar.set_global_opts(title_opts=opts.TitleOpts(title="数据库内番剧评分"),xaxis_opts=opts.AxisOpts(axislabel_opts={"interval":"0"}))
bar.reversal_axis()
bar.render()


