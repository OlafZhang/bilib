# 🍻bilib🍻

整合多个B站原生API，并结合爬取技术的Python爬取用lib

bili + lib = bilib

**注：** 2020.12.2，此代码除错误可能不够妥当，不带后台相关、tag搜索、下载(写了，但不放)外，功能已经完善，现可正式使用

![image](https://raw.githubusercontent.com/OlafZhang/bilib/master/images/back.jpg)

![](https://raw.githubusercontent.com/OlafZhang/bilib/master/images/python.svg)
![](https://raw.githubusercontent.com/OlafZhang/bilib/master/images/license.svg)
![](https://raw.githubusercontent.com/OlafZhang/bilib/master/images/state.svg)

主要配合以下的模块运行:

| 模块 | 备注 |
| :---: | :---: |
| csv | 配合弹幕文件 | 
| re | 配合bs4 |
| requests | 用于所有请求，可能需要安装 |
| traceback | 显示报错信息 |
| bs4 | 用于查找HTML页信息，需要安装 |
| fake_useragent | 用于伪造UA，需要安装 |

注意，现在已经彻底修复fake_useragent带来的各种问题，请一同下载fake_useragent_0.1.11.json，并与bilib.py放在同一目录

此仓库的fake_useragent_0.1.11.json已完全移除IE相关的UA，不使用可能会造成爬取遇到异常



⚠ 声明
===

* 1、截止至2021年1月3日，以下API正常使用，但不确定以后b站是否会改API，我们将尽可能保证在未来使用新的bilibili API的同时兼容您使用bilib编写的代码
    
* 2、虽然这是lib，但我没有安装标准格式进行编写和整理，目前建议的场景是"外挂"lib（将此lib放在你的工作目录）
    
* 3、由于营销号爬取视频进行再投放的行为相当可耻，故这里不会写关于视频下载的API

📢 说明
===

前身为danlib，如果你在我的GitHub找到了danlib，你可以继续使用它，但如果你要改为使用bilib，你需要修改你的代码
    
这个lib可以帮助你完成用户基本信息（粉丝量关注数等）和弹幕（需提供cid）的爬取
    
**实验性功能：** 获取视频评论信息
    
请勿将此lib**用于非法用途**（如DoS/DDoS攻击），**作者将不承担任何责任**，使用此lib视为已遵守此规则
    
另外，lib中注解可能与README冲突，请以README为准

🌈 原则和出发点
===

虽然GItHub不缺这样的爬虫代码，但作者希望bilib能作为开发者和初级爬虫玩家，初级编程玩家的利器

核心已经尽可能抛弃bs4，而使用正则表达式，稳定性更好

所有方法均返回字典和列表，极少数返回字符串，这样你可以只需一行代码将全部内容存入变量，然后从变量直接访问key以提取

作者希望能将爬取工作量降到最低，只需要调用方法，除非bilib代码出现bug，否则根本不需要去bilib中修改某些参数，开发者只需做少量工作而获得收益

美中不足就是整体代码维护困难，可读性一般，且部分语句过于繁琐

确实字典返回内容很多，但已经做到了最低难度

🧻 JSON（续上）
===

api.bilibili.com下几乎所有API均返回JSON格式，bilib将JSON重新格式化为字典，这里是一段将bilib某方法返回结果重新JSON格式化的代码：

    import json
    import bilib
    input = bilib.anime_base_info(28229676)
    print(json.dumps(input,ensure_ascii=False,indent=4,separators=(',',':')))

    控制台输出>>>
    {
        "title":"总之就是非常可爱",
        "type":"番剧",
        "area":"日本",
        "share_url":"https://www.bilibili.com/bangumi/media/md28229676",
        "desc":"由崎星空对神秘美少女——司一见钟情。面对星空决死的告白，她的回答是“如果你愿意和我结婚，那我就跟你交往”？！充满了星空与司的爱，可爱&高贵的新婚生活开始了！",
        "cover_url":"http://i0.hdslb.com/bfs/bangumi/image/3b97bfc609e08417eb391ef975a8648c28c55e04.png",
        "media_id":28229676,
        "ep_id":341255,
        "episode":"全12话",
        "rating_count":65293,
        "score":9.5,
        "season_id":34230,
        "coins":1273408,
        "danmakus":1799536,
        "follow":3999810,
        "series_follow":3997683,
        "views":97200286,
        "tag_id":7011428,
        "vip_info":"大会员/付费",
        "aid":"av499874852",
        "bvid":"BV1pK411N7xH",
        "quality":"1080P 高码率",
        "quality_ID":112,
        "is_finish":"是",
        "is_started":"是",
        "actor_list":[
            "由崎司：鬼头明里",
            "由崎星空：榎木淳弥",
            "有栖川要：芹泽优",
            "有栖川绫：上坂堇",
            "键之寺千岁：小原好美"
        ],
        "staff_list":[
            "原作：畑健二郎",
            "导演：博史池畠",
            "总编剧：兵头一步",
            "角色设计：佐佐木政胜",
            "道具设计：岩畑刚一",
            "色彩设计：歌川律子",
            "美术监督：涩谷幸弘",
            "音响监督：本山哲",
            "音乐：ENDO.",
            "动画制作：SevenArcs"
        ],
        "flag_list":[
            "日常",
            "恋爱",
            "漫画改"
        ],
        "alias_list":[
            ""
        ],
        "showtime":"2020年10月3日",
        "origin_name":"トニカクカワイイ"
    }

不用过于在意JSON和字典，只需要调用方法返回的字典的key即可

🍪 Cookies
===

访问bilibili会用到很多cookie，其中最重要的是SESSDATA，用于区别不同用户

SESSDATA可在浏览器开发人员工具找到，有效时间为1个月

只有以下方法必须使用cookie，否则将无法使用(或非完全使用)此方法：

    list_follower(uid,page=1,step=20)
    如果不使用cookie，5页之后不能获取

    list_following(uid,page=1,step=20)
    如果不使用cookie，5页之后不能获取

所有方法要想使用Cookie，必须先做Cookie初始化：

    import bilib
    bilib.with_cookie = True               //打开全局Cookie传入开关
    bilib.cookies = str("rq27tr0fa")       //设置SESSDATA

❌ 异常
===

现在这个bilib已经包含较精确的错误类型，方便排错和优化自己的代码

除非特殊情况，接下来在API介绍不再说明错误，具体说明如下

| 名称 | 概要 | 说明 |
| :---:| :---: | :---: |
| InfoError | 传参异常/未定义异常 | 一般是因为用户输入了错误的数据，例如没有输入bv号的"BV",以及目前小概率遇到的未定义异常 |
| danmakuError | 弹幕文件等异常 | 一般是弹幕文件被删除，或者不符合规范 |
| Timeout | 请求超时 | 服务器返回“请求超时”，或程序超时，尝试通过set_timeout()调整超时时间 |
| RequestError | 请求错误 | 服务器返回“啥都木有”，貌似没有此信息，原始API没有返回任何值，如果是用户相关，可能此用户已销号或不存在，bilib内部错误也可能会造成此异常 |
| SeemsNothing | 返回空数据/传参不正确 | 服务器返回“服务调用超时”，检查超时时间或重新尝试，bilib内部错误或传参异常也可能会造成此异常 |
| RequestRefuse | 触发反爬取机制 | 服务器返回“请求被拦截”，HTTP状态码为412，建议更换IP或等待至少30分钟后尝试，如果请求含cookie，服务器会记录违规UID |

💦 demo
===

这个仓库有两个demo用于获取番剧信息: demo_tamako.py 和 demo_takagi.py

两个都把bilib番剧和弹幕相关方法用的比较完全，同时也可用于协助番剧信息爬取和收集

它们都可以获得番剧信息，番剧弹幕收集

**遇到非正片可能会出现描述异常，但不影响输出**


 📕 ```demo_tamako.py```
 -----

* 方法：传入md号(不带md)

* 优点：除非遇到404，412和错误的md号，不可能出现异常，稳定性较好，不仅仅支持番剧

* 缺点：不够智能，只能认md号

 📙 ```demo_takagi.py```
 -----

继承自demo_tamako.py，在执行demo_tamako.py的方法前，把番剧/影视作品名转换为md号，再传入

* 方法：传入番剧/影视作品名称(越准确越好)

* 优点：收集数据更快，不必去URL抓md号

* 缺点：不如demo_tamako.py稳定，结果大于2时要么能全字匹配，要么让用户选择(也可以自动全爬取)

demo中的方法```get_full_info()```有以下传参

| 参数名 | 解释 | 默认值 | 备注 |
| :---: | :---: | :---: | :---: |
| mediaID | md号 | 无，需要用户传参 | demo_tamako.py为手动传参，demo_takagi.py为自动传参 |
| get_dan | 获取所有集的弹幕(ass) | False | 格式为"集数 番剧/影视作品 danmaku_file.ass" |
| tofile | 导出番剧/影视作品信息到一个txt文件 | False | 格式为"md号_番剧/影视作品名称.txt" |
| cleanup | 清理获取弹幕时的xml文件 | True | 仅get_dan为True时有效 |

另外，在```demo_takagi.py```有一个方法```anime2md()```

| 参数名 | 解释 | 默认值 | 备注 |
| :---: | :---: | :---: | :---: |
| keyword | 关键字 | 无，需要用户传参 | 自动将md号传参到get_full_info() |
| wait | 等待用户选择 | False | True时遇到多结果要求用户输入(单选/全选/全不选)， False时则全部爬取 |
| strict | 严格匹配模式 | True | 传参到search_media()， 注意事项见search_media()介绍 |
| unreachable | 包含港澳台结果 | False | 如果显示仅限港澳台播放内容，可能会报错 |

这个仓库有一个demo用于获取视频评论: demo_yui.py

比较粗糙，仅用于```video_comment()```的调试工作

📘 ```demo_yui.py```
 -----

 * 方法：传入av号(不带av)，可选择传入页码

 在```demo_yui.py```有一个方法```show_comment()```，均传入到```video_comment()```

| 参数名 | 解释 | 默认值 | 备注 |
| :---: | :---: | :---: | :---: |
| aid | 视频av号 | 无，需要用户传参 | 其实是oid，但测试发现与av号相同，兼容番剧 |
| page | 页码 | 1 |  |

 **部分番剧或视频可能会出现异常**

 demo取名原因：

    demo_tamako.py对应《玉子市场》的北白川玉子。在年糕方面研究专注，但有点傻乎乎的。
    所以此demo仅接受md号传参，但稳定性极好。

    demo_takagi.py对应《擅长捉弄的高木同学》的高木同学。虽和玉子都属于类似人妻型，但高木明显更机灵。
    所以此demo可接受番剧/影视作品名称传参。

    demo_yui.py对应《轻音少女》的平泽唯。在演唱会上能说会道，但非常大条和呆。
    所以此demo用于评论API的调试。

🔌 额外选项
===

在bilib中，你可能需要设置其它参数，故这里有若干个方法

⛏ ```set_timeout(set_time)```
-----

设置所有requests.get()的超时时间，默认超时时间为5(秒)



😄 稳定功能的API
===

这部分包含了我从2020年5月开始调试的代码，目前爬取100w+用户数据/100多部番剧、电影和若干部视频后仍能稳定工作

⛏ ```user_info(uid_input)```
-----

相比于旧的需要爬取一个API和一个HTML，新的直接使用两个API获得数据，更节省流量

* 功能： 获取一个用户的详细信息（粉丝，关注，UID，昵称）

* 必要的传参：用户的UID（uid_input）

* 选择的传参：无

* 返回：字典，参数如下

| 参数名(key) | 解释 | 备注 |
| :---:| :---: | :---: |
| name | 昵称 |  |
| uid | UID |  |
| fans | 粉丝数 |  |
| following | 关注数 |  |
| sex | 性别 | 男/女/保密 |
| level | 等级 |  |
| face_url | 头像URL |  |
| sign | 个性签名 | 可以为空值 |
| birthday | 生日 | 可以为空值 |
| coins | 硬币 | 意义不明，可能是获币数量 |
| vip_type | 是否为大会员 | 空值/大会员/年度大会员 |

* 补充：由于愚人节会临时将大会员改为小会员，bilib已做好相应对策，但可能会失效，故在此提醒



⛏ ```get_danmaku(cid_input, reset=False)```
-----

💡 使用UCS-2(UTF-16)替换UTF-8编解码。UCS-2编码弹幕的表现：类似某些supreme，awsl等艺术字弹幕

* 功能： 获取一个视频的弹幕，包括番剧/电影（最多返回8000条）

* 必要的传参：视频的cid（cid_input）， 只能输入数字， 可以通过实验性功能或者浏览器F12功能获得cid

* 选择的传参：文件存在时强制刷新（reset），默认不刷新（False）

* 返回：弹幕文件的绝对路径，文件为csv，直接使用cid命名，同时打印绝对路径

可能会报错"cid error, check cid."，一般是此视频没有弹幕或cid错误。



⛏ ```listall_danmaku(file_path, stamp=False)```
-----

💡 已经修复UnicodeEncodeError，使用UCS-2的特殊字符可能不能在IDLE显示，PyCharm正常显示

* 功能：处理弹幕文件，并输出

* 必要的传参：弹幕文件的绝对路径（file_path）

* 选择的传参：返回现实时间的时间戳而非转化的时间（stamp），默认返回转化的时间（False）

* 返回：字典，key为序号(int)，value为列表，参数如下：

| 列表编号 | 解释 | 备注 | 举例 |
| :---:| :---: | :---: | :---: |
| 0 | 发送位置 | 原始信息为秒 | 00:13:45.17700 |
| 1 | 弹幕类型 |  | 滚动弹幕 |
| 2 | 弹幕字号 |  | 25 |
| 3 | 弹幕颜色 | 原始信息为十六进制颜色值再转为十进制 | ffffff |
| 4 | 现实发送时间 | 原始信息为时间戳 | 2020-11-18 19:02:15 |
| 5 | 弹幕池 |  | 普通弹幕池 |
| 6 | 用户ID | 被加密，不推荐解密，因为解密结果不唯一 | 733f59 |
| 7 | rowID |  | 41185527935795205 |
| 8 | 发送内容 | 如果是高级弹幕，还会在这里包含一些参数 | awsl |

原始信息：

| 解释 | 举例 |
| :---: | :---: |
| 发送位置 | 825.17700 |
| 弹幕类型 | 1 |
| 弹幕字号 | 25 |
| 弹幕颜色 | 16777215 |
| 现实发送时间 | 1605697335 |
| 弹幕池 | 0 |
| 用户ID | 733f59 |
| rowID | 41185527935795205 |
| 发送内容 | awsl |

如果遇到了全新的弹幕类型，会不处理，返回原生数据

⛏ ```count_danmaku(file_path)```
-----

* 功能：获取弹幕文件行数

* 必要的传参：弹幕文件的绝对路径（file_path）

* 选择的传参：无

* 返回：一个数字，此为弹幕文件总行数

⚠ **请不要配合get_danmaku_raw使用**，因为得出的数值不正确



⛏ ```get_danmaku_raw(cid_input, reset=False)```
-----

由于此API设计初衷是配合ass转换工具的，所以没有单独做xml转csv的API

另外，为配合转换工具，设置了UTF-8编码而非UTF-16

如果需要数据分析，请直接使用get_danmaku()

* 功能： 获取一个视频的弹幕(原始文件，即xml)

* 必要的传参：视频的cid（cid_input）， 只能输入数字, 可以通过实验性功能或者浏览器F12功能获得cid

* 选择的传参：文件存在时强制刷新（reset），默认不刷新（False）

* 返回：弹幕文件的绝对路径，文件为xml，直接使用cid命名，同时打印绝对路径



⛏ ```raw2ass(file_path)```
-----

💡需要调用[Niconvert](https://github.com/muzuiget/niconvert)

如果你要自己去下载官方版，请注意：作者针对此API将Niconvert进行了小改，以便能在命令行运行，下载原版需要自行调整

* 功能： 将xml标准格式转换为ass字幕文件，以便能在第三方播放器实现弹幕效果

* 必要的传参：xml文件绝对路径(file_path）

* 选择的传参：无

* 返回：ass字幕文件的绝对路径，文件为ass，直接使用cid命名，同时打印绝对路径

* 异常：遇到大文件极小概率抛出FAIL异常，请手动修改for循环的超时等待时间



⛏ ```anime_base_info(media_id)```
-----

⚠ 在极个别爬取冷门番剧(例如没有评分)时会因为```anime_episode_info```中API不返回任何值导致bilib报错(Something error)

考虑到这可能是一个不太重要的bug，故暂时不修复

**💡 此API为本次开发重点**

经历多次改动，现功能性相当强，可以用作番剧信息收集或声优信息整理

虽然说爬取番剧/电影，但同时也能兼容一些综艺类节目，以此推测这类的架构都是一样的

**在说明API前，需要说明一些B站在番剧方面API的一些参数（比较复杂），这些参数一般可在URL中找到**

(电影/番剧/综艺等在此表统称番剧)

| 名称 | 中文名 | 解释 | 例子 | 获取途径 |
| :---:| :---: | :---: | :---: | :---: |
| media_id | 番剧md号 | 每个番剧的特征号(和av号一样的作用) | md135652(JOJO的奇妙冒险 第五季) | 在番剧介绍页URL中出现，在此API作为必须传入的参数 |
| season_id | 番剧id | 也是每个番剧的特征号(个别番剧的md号和ss号相同) | ss3398(冰菓) | 小概率会在番剧介绍页URL中出现，可以通过此API获取，也会在番剧播放页小概率出现，此时通过?id=1的形式传参达到播放不同集的效果 |
| ep_id | 剧集编号 | 每集的特征号，全B站唯一 | ep234488(玉子市场 第一集) | 在番剧播放页的URL中就可以找到，可以通过此API获取，anime_base_info(media_id)返回的ep_id为最后一集的 |
	
这些参数一般会一起在B站API出现，md号在介绍页URL必能找到

还有一个不太重要的参数：tag_id，标签ID，每个番剧都不同，根据观察，这个可能和向用户推送关于此番剧的二创视频有关

* 功能：获取番剧基本信息

* 必要的传参：番剧的md号（media_id），输入数字

* 选择的传参：无

* 返回：字典， 参数如下:

| 参数名(key) | 解释 | 备注 | 返回值举例 |
| :---:| :---: | :---: | :---: |
| title | 标题 | | 玉子市场 |
| type | 类型 | 番剧/电影(TV版和剧场版均为番剧) | 番剧 |
| area | 地区 |  | 日本 |
| share_url | 介绍页URL | 并不是播放页URL，此URL含mediaID | https://www.bilibili.com/bangumi/media/md116772 |
| desc | 简介 | “xxx译制”信息会被删除 | 座落某个小镇的兔子商店街上，有一间日式饼店，住着一位... ... |
| cover_url | 介绍页封面URL| | http://i0.hdslb.com/bfs/bangumi/67da3dae76e526a925b78b1d8abe21c870333491.jpg |
| media_id | md号 | 每部番剧唯一 | 116772 |
| ep_id | 剧集编号 | 此ep号为最后一集的 | 234499 |
| episode | 集数 | 对于一些电影来说则是上映时间（例如“2018-01-18上映”），请注意过滤 | 全12话 |
| rating_count | 等级编号 | 猜测是总排行榜的RANK | 21343 |
| score | 评分 | | 9.8 |
| season_id | 番剧ID  | | 4262 |
| coins | 总投币数 | | 139495 |
| danmakus | 总弹幕量 | | 795287 |
| follow | 追番数 | | 1906603 |
| series_follow | 系列追番数 | | 2533501 |
| views | 总播放量 | | 21325692 |
| tag_id | 标签ID | bilibili用于向用户推送其它番剧/电影或此番剧/电影的二创 | 278208 |
| vip_info | 免费/大会员/付费 | 有时不是很准，在修复 | 免费 |
| aid | av号 | **第一集**或**全集**的av号 | av27045209 |
| bvid | bv号 | **第一集**或**全集**的bv号 | BV1fs41177WY |
| quality | 最高质量 | 一般表示游客支持的最高质量 | 1080P 高码率 |
| quality_ID | 最高画质编号 | 用于辅助分析 | 112 |
| is_finish | 是否完结 |  | 是 |
| is_started | 是否开播 | 目前暂时没遇到未开播的作品 | 是 |
| actor_list | 演员/声优列表 | 这是一个列表 | 此处略，每个列表元素的组合是“角色：声优”或者只有演员 |
| staff_list | STAFF列表 | 这是一个列表 | 此处略，每个列表元素的组合是“职位：姓名” |
| flag_list | 标签列表 | 这是一个列表 | ['萌系', '少女', '治愈', '日常'] |
| alias_list | 别称列表 | 这是一个列表 | ['玉子市场'] |
| showtime | 开播/上映时间 | | 2013年1月9日 |
| origin_name | 原名 | 语言为来源地区所使用的默认语言，国漫等大陆作品会返回不支持 | たまこまーけっと |

对于比较早的番剧(测试《玉子市场》)，番剧所有集**都在一个av号下**，对于新出的番剧(测试《公主连结Re:Dive》)，**每集**都有**单独的av号**

如果你要做类似下载等同时需要av号和cid号的场景，请使用```anime_episode_info(season_id)```中的数据

 **🎞 质量编号科普：**
 
| 质量编号 | 对应画质 |
| :---:| :---: |
| 125 | 4K HDR(10bit)|
| 120 | 4K |
| 116 | 1080P 60FPS高帧率 |
| 112 | 1080P+ 高比特率 |
| 80 | 1080P |
| 74 | 720P 60FPS高帧率 |
| 64 | 720P |
| 32 | 480P |
| 16 | 360P | 
| 0 | 自动 |
    
⚠ 注意，这里的desc和video_info的desc性质不同，不能混用

相比于视频的介绍（desc），番剧的介绍看起来不能通过API来获取，只能截取HTML后使用bs4和正则表达式来搜索，比较麻烦

加入识别原生分辨率，是否收费等功能，已经集成av和bv的获取
    
另外，部分番剧不能返回正确的清晰度，因为有限制，且并不打算在每个ep求清晰度，因为会造成大量请求

* 另外说明：目前所有在media_id_pool.py的番剧全部通过测试，已配置反爬取告警。仍然存在潜在bug。
    
⛏ ```anime_episode_info(season_id)```
-----

* 功能：获取指定番剧/电影的av，cid，标题等高级信息，以及每集的信息

* 必要的传参：番剧的id号（season_id），输入数字

* 选择的传参：无

* 返回：字典，key为集编号（str而非int，因为在冰菓遇到了11.5），value为字典，参数如下:

| 参数名(key) | 解释 | 备注 | 返回值举例 |
| :---:| :---: | :---: | :---: |
| type_name | 所属大类 | 例如PV等，默认值为“正片” | 正片 |
| aid | av号 | 可能每集不同 | 52307583 |
| cid | cid号 | 弹幕池编号 | 91550935  |
| ep_id | 剧集编号 |  | 21278 |
| title_long | 当前集长标题 |  | Live House！ |
| cover_url | 当前集封面URL |  | http://i0.hdslb.com/bfs/bangumi/a2bbb9e95ed53d5ff85a7a2cca7524a9c8455edd.jpg |
| share_url | 当前集播放页URL | 此URL含epID或seasonID | https://www.bilibili.com/bangumi/play/ep21278 |

对于比较早的番剧(测试《玉子市场》)，番剧所有集**都在一个av号下**，对于新出的番剧(测试《公主连结Re:Dive》)，**每集**都有**单独的av号**

如果你要做类似下载等同时需要av号和cid号的场景，请使用```anime_episode_info(season_id)```中的数据

* 另外说明：目前所有在media_id_pool.py的番剧全部通过测试，已配置反爬取告警。仍然存在潜在bug。



⛏ ```get_resolution(id_input,getid = False)```
-----

**💡 一般仅表示游客支持的最高质量**

* 功能：获取视频最高清晰度

* 必要的传参：av号，bv号或ep号，必须带字母

* 选择的传参：getid，返回质量编号(True)而非清晰度描述(False)

* 返回：字符串，清晰度描述或质量编号

另外说明：由于同时支持视频和某些番剧，故单独做了此API，作为备份，已集成到video_info()，anime_base_info()则使用了另外的方法
    
由于我真的没料到B站出了HDR视频，为预防将来出现更高规格的视频，新编号一律返回类似“疑似错误的编号(250)”的形式

* 报错: 部分番剧可能会返回"不支持"



⛏ ```video_info(id_input)```
-----

不太推荐在番剧使用此API，除bv号和av号外，其它数据均可通过anime_base_info(media_id)获取
    
新加入原生分辨率识别功能，完美支持所有视频
    
强行在番剧可能会在清晰度相关key返回"不支持"

* 功能：获取视频的信息

* 必要的传参：视频av号或bv号（id_input），"av"和"bv"也要一同输入

* 选择的传参：无

* 返回：字典，参数如下:

| 参数名(key) | 解释 | 备注 |
| :---: | :---: | :---: |
| aid | av号 |  |
| bvid | bv号 |  |
| type_id | 类型编号 |  |
| type_name | 类型描述 |  |
| pic_url | 封面图片URL |  |
| put_time | 投稿时间 | 时间戳 |
| ctime | *未知参数* | 时间戳 |
| title | 视频标题 |  |
| desc | 视频描述 |  |
| argue_msg | 视频提醒信息 | 例如“视频内含有危险行为，请勿模仿” |
| state | 状态 | 推测被封杀的视频是另外的数值，正常是0 |
| evaluation | 评分描述 | 仅互动视频有此参数 |
| owner_name | up主昵称 |  |
| owner_uid | up主的UID |  |
| owner_face | up主的头像图片URL |  |
| view | 观看量 |  |
| danmaku | 弹幕量 |  |
| reply | 评论量 |  |
| favorite | 收藏量 |  |
| coin | 投币量 |  |
| share | 分享量 |  |
| like | 点赞量 |  |
| now_rank | 当前全站排名 | 仅此视频为当前热门时有效，否则为0 |
| his_rank | 历史最高全站排名 | 默认为0 |
| quality | 最高画质 | 仅表示游客和非大会员支持的最高画质，且为第一集的 |
| quality_id | 最高画质编号 | 用于辅助分析，且为第一集的 |
| total_page | 分集数量 | 至少为1 |
| staff | 联合投稿的staff名单 | 这是一个字典 |
| video | 视频分集信息(*即使只有一集*) | 这是一个字典 |

staff作为一个字典有另外的参数，**仅在联合投稿有效**，否则返回空字典

staff中，key为编号，从0开始，value为详细信息的字典

每个value中的参数如下：

| 参数名(key) | 解释 | 备注 |
| :---: | :---: | :---: |
| uid | 用户UID |  |
| work | 在视频中的分工 |  |
| name | 用户名 |  |
| face_url | 用户的头像图片URL |  |
| vip_type | 是否为大会员 | 年度大会员: 2 ,大会员: 1 ,普通用户: 0 |
| is_famous | 是否为知名UP(小闪电) | 是为1，否为0 |
| famous_name | 知名UP描述 | 非知名UP返回空值 |
| follower | 粉丝数量 |  |

video作为一个字典有另外的参数

video中，key为编号，value为详细信息的字典

如果是互动视频等情况，key从0开始，否则从1开始

另外，互动视频每个分集信息可能用了另外的API，暂时无解

每个value中的参数如下：

| 参数名(key) | 解释 | 备注 |
| :---: | :---: | :---: |
| cid | 弹幕cid | 每个分集不同，下载视频必要参数之一 |
| duration | 视频长度 | 单位为秒 |
| vid | *未知参数* | 默认空白 |
| weblink | *未知参数* | 默认空白 |
| width | 视频宽度 | 单位为像素，例如1920 |
| height | 视频高度 | 单位为像素，例如1080 |
| rotate | 是否翻转(*未知参数*) | 默认为0 |

**另外说明：由于番剧/电影也存在av号/bv号，所有此API对于番剧等可能有效，多p情况可能异常**

⛏ ```search_media(keyword, strict = True ,type = "bangumi")```
-----

此API因本人一个视频项目应运而生

由于本人最近学会正则表达式，故稳定性提高，但仍然有可能因为反爬取导致奇怪的bug

会自动检测页数，爬取一个页后会打印当前进度，并休眠5秒

* 功能：搜索番剧/影视名称，返回md号

* 必要的传参：要搜索的番剧名(keyword)

* 选择的传参：严格匹配模式(strict)，默认过滤掉没有关键字的结果(True)；查询种类(type)，默认为番剧

**查询种类通过改变查询URL中的关键字实现，具体解释如下：**

| 传入到URL的关键字 | 备注 |
| :---: | :---: |
| bangumi(番剧) | 对应番剧和某些剧场版电影 |
| pgc(影视) | 对应电影、综艺、电视剧和某些剧场版电影等 |


**⚠ 虽然严格模式可以提高准确性，但不支持别名/原名搜索**

例如搜索"*玉子市场剧场版*"或者"*たまこラブストーリー*"时，并不会返回"*玉子爱情故事*"，而是返回**空值**
    
关闭严格模式时有返回值

* 返回：字典，key为番剧名称，value为md号(带md)

* 报错：没有查到会返回空字典(无论是不是404)，412会抛出异常



⛏ ```search_video_all(keyword)```
-----

此API为有需要做统计类视频的同学奠定基础

由于本人最近学会正则表达式，故稳定性提高，但仍然有可能因为反爬取导致奇怪的bug

会自动检测页数，爬取一个页后会打印当前进度，并休眠5秒

* 功能：搜索视频名称，返回一个列表，每个元素由字典组成，包含标题，BV号，播放量，up主和发布时间

* 必要的传参：要搜索的关键字(keyword)

* 选择的传参：无

* 返回：列表，元素为字典，参数如下：

| 参数名(key) | 解释 | 备注 |
| :---:| :---: | :---: |
| bvid | bv号 |  |
| title | 视频标题 |  |
| put_time | 投稿时间 | 统计类视频重要参数 |
| up_name | up主 | 注意，搜索up名也会返回结果，即使关键字与视频不相关 |
| playback | 播放量 | 不以万为单位 |

* 报错：没有查到会返回空列表(无论是不是404)，412会抛出异常，并导出未完成的列表

另外还有一个方法```search_video(keyword,page=1)```,可以指定爬取页

相比```search_video_all(keyword)```爬取全部更自由，但不能返回总页数

😫 实验性API
===

这些API的实验样本较少，或其原生API参数过多，需要一定的研究时间和测试时间

⛏ ```video_comment(aid, page = 1, video = True)```
-----

此API参数过多，故存在不稳定性，也不打算全部照搬

另外还在继续研究，你可能发现了没有一些参数

默认第一页第一个是最新评论，热评和置顶可能与主评论区域有重复

**兼容专栏评论**

* 功能：此API用于获取一个视频的评论，仅接受av号传参

* 必要的传参：目标视频的av号（aid），或者专栏的cv号（其实就是视频/番剧/专栏的oid号，但是与av/cv一样）

* 选择的传参：评论页数（page），默认为1；是视频还是专栏(video)，默认是视频

* 返回：复合字典

如果没有人在任何评论下回复的话，那么key为编号，value则包含另外一个字典，以此举例参数如下：

（如果是主评论区域，编号为纯数字，否则就是类似于"HOT-1"，"UPPER"的值）

| 参数名(key) | 解释 | 备注 |
| :---:| :---: | :---: |
| ctime | 发送时间对应时间戳 |  |
| rpid | 此评论的特征号 |  |
| like | 点赞数 |  |
| rcount | 此楼评论总数 |  |
| mid | 用户UID |  |
| uname | 用户名 |  |
| sex | 性别 |  |
| sign | 个性签名 |  |
| message | 评论内容 |  |
| replies_item | 回复内容 | 在此例子中，由于没有评论，返回字符串None,若有，则会返回与此表相差无几的字典 |
| up_like | UP是否点赞 | 布尔值 |
| up_reply | UP是否评论此楼 | 布尔值 |
| total_page | 总评论页数 | 每20评论一页，偶尔页数会不正确，对于热评和置顶可能无意义 |

如果评论下有回复，则replies_item为字典，key为编号，value则包含另外一个字典，参数如下：

| 参数名(key) | 解释 | 备注 |
| :---:| :---: | :---: |
| ctime | 发送时间对应时间戳 |  |
| rpid | 此评论的特征号 | 与此楼的根评论不同 |
| like | 点赞数 |  |
| mid | 用户UID |  |
| uname | 用户名 |  |
| sex | 性别 |  |
| sign | 个性签名 |  |
| message | 评论内容 |  |
| up_like | UP是否点赞 | 布尔值 |
| up_reply | UP是否评论此楼 | 布尔值 |

评论API官方有两个，另一个更稳定，但需要jQuery，暂时未研究出来（同样只接受av号）

目前测试大部分视频和部分番剧（包括合集和非合集）都在demo_yui.py通过测试。

⛏ ```xml2csv(path)```
-----

* 功能：将xml格式弹幕转化为高可读性的csv文件

* 必要的传参：目标视频的cid号（cid）

* 选择的传参：无

* 返回：返回并打印csv文件的绝对路径

之前版本借鉴了他人的代码，但代码过长，现自行制作独立版本

```get_danmaku(cid_input, reset=False)```已经使用了```xml2csv(path)```，无需在意变化

唯一不足是可能不支持特殊弹幕

⛏ ```list_follower(uid,page=1,step=20)```
-----

**最多返回1000个用户**

* 功能：列出某个用户全部粉丝列表

* 必要的传参：用户的UID（uid）

* 选择的传参：指定页码(page)，默认为1；单次返回数量(step)，默认单次返回20条结果，最大单次返回50条

* 返回：字典，key为编号(0开始)，元素为字典，参数如下：

| 参数名(key) | 解释 | 备注 |
| :---:| :---: | :---: |
| mid | 用户UID |  |
| uname | 用户名 |  |
| mtime | 被关注时间 | 时间戳 |

必须带Cookie，否则只能返回5*20条结果

⛏ ```list_following(uid,page=1,step=20)```
-----

**最多返回1000个用户**

* 功能：列出某个用户全部关注列表

* 必要的传参：用户的UID（uid）

* 选择的传参：指定页码(page)，默认为1；单次返回数量(step)，默认单次返回20条结果，最大单次返回50条

* 返回：字典，key为编号(0开始)，元素为字典，参数如下：

| 参数名(key) | 解释 | 备注 |
| :---:| :---: | :---: |
| mid | 用户UID |  |
| uname | 用户名 |  |
| mtime | 关注时间 | 时间戳 |

必须带Cookie，否则只能返回5*20条结果

🎈 感谢
===

本lib部分API参考来自https://www.bilibili.com/read/cv5293665

感谢[Niconvert](https://github.com/muzuiget/niconvert)

同时也感谢自己和自己的：

* Python 3.8.6

* PyCharm 2019.3.3

* Visual Studio Code 1.51.1

* Firefox的开发者工具

也感谢B站不把我打死（确信）

💾 MEMO
===

**最优先做：弹幕同屏数量热度图**

目前发现了收藏夹的的API，考虑做

只需要fid和page，不需要Refener，需要cookie

https://api.bilibili.com/x/v3/fav/resource/list?media_id=820144418&pn=2&ps=20&keyword=&order=mtime&type=0&tid=0&platform=web&jsonp=jsonp

专栏等收藏夹：

https://api.bilibili.com/x/article/favorites/list/all?pn=1&ps=16&jsonp=jsonp

需要Refener，需要cookie：

https://api.bilibili.com/x/article/favorites/list/all?pn=1&ps=16&jsonp=jsonp
