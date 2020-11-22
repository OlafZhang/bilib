# 🍻bilib🍻

整合多个B站API的Python lib

bili + lib = bilib

![cover](./back.jpg)

使用Python3.6.8开发，主要配合以下的模块运行:


| 模块 | 备注 |
| :---:| :---: |
| csv | 配合弹幕文件 | 
| re | 配合bs4 |
| requests | 用于所有请求，可能需要安装 |
| traceback | 显示报错信息 |
| bs4 | 用于查找HTML页信息，需要安装 |
| fake_useragent | 用于伪造UA，需要安装(可能会报错，但不影响使用) |



## ⚠声明

    1、截止至2020年11月1日，以下API正常使用，但不确定以后b站是否会改API，我们将尽可能保证在未来使用新的bilibili API的同时兼容您使用bilib编写的代码
    
    2、虽然这是lib，但我没有安装标准格式进行编写和整理，目前建议的场景是"外挂"lib（将此lib放在你的工作目录）
    
    3、由于营销号爬取视频进行再投放的行为相当可耻，故这里不会写关于视频下载的API

## 📢说明

    前身为danlib，如果你在我的GitHub找到了danlib，你可以继续使用它，但如果你要改为使用bilib，你需要修改你的代码
    
    这个lib可以帮助你完成用户基本信息（粉丝量关注数等）和弹幕（需提供cid）的爬取
    
    实验性功能：获取视频信息，获取番剧/电影信息和章节列表(虽然被我放到了前面但是遇到某些番剧就是会崩)
    
    请勿将此lib用于非法用途（包括敏感数据爬取和DoS/DDoS攻击），作者将不承担任何责任，使用此lib视为已遵守此规则
    
    另外，lib中注解可能与README冲突，请以README为准

## ❌异常

现在这个bilib已经包含较精确的错误类型，方便排错和优化自己的代码

除非特殊情况，接下来在API介绍不再说明错误，具体说明如下

### 1️⃣ InfoError(传参异常/未定义异常)
    
一般是因为用户输入了错误的数据，例如没有输入av号的av，以及目前小概率遇到的未定义异常
    
    
    
### 2️⃣ danmakuError(弹幕文件等异常)
    
一般是弹幕文件被删除，或者不符合规范
    
    
    
### 3️⃣ Timeout(请求超时)

服务器返回：请求错误。
    
可能是程序问题，或者是网络问题。
    
    
    
### 4️⃣ RequestError(请求错误)
    
服务器返回：啥都木有。
    
貌似没有此人的信息，可能已销号，原始API没有返回任何值。
    
    
    
### 5️⃣ SeemsNothing(返回空数据/传参不正确)
    
服务器返回：服务调用超时。
    
检查网络或重新尝试。
    
    
    
### 6️⃣ RequestRefuse(触发反爬取机制)
        
服务器返回：请求被拦截。
    
HTTP 412，服务器已启动反爬机制，请稍后尝试。
    
触发反爬取后会记录当前用户的UID（如果已经登陆），所以请尽量不要在源代码插入自己的用户cookie



## 😄稳定功能的API

这部分包含了我从2020年5月开始调试的代码，目前爬取100w+用户数据和100多部番剧/电影后仍能稳定工作



### ⛏```user_info_old(uid_input, get_ua=False)```

💡这是旧的API，新API在下面

#### 功能： 获取一个用户的基本信息（粉丝，关注，UID，昵称）

#### 必要的传参：用户的UID（uid_input）

#### 选择的传参：要求返回爬取此用户数据用到的User Agent(get_ua)，默认不返回UA（False）

#### 返回：字典，参数如下:

| 参数名(key) | 解释 | 备注 |
| :---:| :---: | :---: |
| uid_input | 用户输入的UID |  |
| name | 昵称 |  |
| fans | 粉丝数 |  |
| following | 关注数 |  |
| st_code | HTTP状态码 | 目前只遇到200，404，412 |
| ua | User Agent | 爬取时使用的UA |
    
    
### ⛏```user_info(uid_input)```

💡这是新的API

相比于旧的需要爬取一个API和一个HTML，新的直接使用两个API获得数据，更节省流量

#### 功能： 获取一个用户的详细信息（粉丝，关注，UID，昵称）

#### 必要的传参：用户的UID（uid_input）

#### 选择的传参：无

#### 返回：字典，参数如下

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

#### 补充：由于愚人节会临时将大会员改为小会员，bilib已做好相应对策，但可能会失效，故在此提醒



### ⛏```get_danmaku(cid_input, reset=False)```

💡使用UCS-2(UTF-16)替换UTF-8编解码。UCS-2编码弹幕的表现：类似某些supreme，awsl等艺术字弹幕

#### 功能： 获取一个视频的弹幕，包括番剧/电影（最多返回8000条）

#### 必要的传参：视频的cid（cid_input）, 只能输入数字, 可以通过实验性功能或者浏览器F12功能获得cid

#### 选择的传参：文件存在时强制刷新（reset），默认不刷新（False）

#### 返回：弹幕文件的绝对路径，文件为csv，直接使用cid命名，同时打印绝对路径



### ⛏```listall_danmaku(file_path, stamp=False)```

💡已经修复UnicodeEncodeError，使用UCS-2的特殊字符可能不能在IDLE显示，PyCharm正常显示

#### 功能：处理弹幕文件，并输出

#### 必要的传参：弹幕文件的绝对路径（file_path）

#### 选择的传参：返回现实时间的时间戳而非转化的时间（stamp），默认返回转化的时间（False）

#### 返回：字典，key为序号(int),value为列表，参数如下：

| 列表编号 | 解释 | 备注 | 举例 |
| :---:| :---: | :---: | :---: |
| 0 | 视频内发送时间 | 原始信息为秒 | 00:13:45.17700 |
| 1 | 弹幕类型 |  | 滚动弹幕 |
| 2 | 弹幕字号 |  | 25 |
| 3 | 弹幕颜色 | 原始信息为十六进制颜色值再转为十进制 | ffffff |
| 4 | 现实发送时间 | 时间戳 | 2020-11-18 19:02:15 |
| 5 | 弹幕池 |  | 普通弹幕池 |
| 6 | 用户ID | 被加密，不推荐解密，因为解密结果不唯一 | 733f59 |
| 7 | rowID |  | 41185527935795205 |
| 8 | 发送内容 | 如果是高级弹幕，还会在这里包含一些参数 | awsl |

原始信息：

| 解释 | 举例 |
| :---: | :---: |
| 视频内发送时间 | 825.17700 |
| 弹幕类型 | 1 |
| 弹幕字号 | 25 |
| 弹幕颜色 | 16777215 |
| 现实发送时间 | 1605697335 |
| 弹幕池 | 0 |
| 用户ID | 733f59 |
| rowID | 41185527935795205 |
| 发送内容 | awsl |

如果遇到了全新的弹幕类型，会不处理，返回原生数据

### ⛏```count_danmaku(file_path)```

#### 功能：获取弹幕文件行数

#### 必要的传参：弹幕文件的绝对路径（file_path）

#### 选择的传参：无

#### 返回：一个数字，此为弹幕文件总行数

⚠ 请不要配合get_danmaku_raw使用，因为得出的数值不正确



### ⛏```get_danmaku_raw(cid_input, reset=False)```

    由于此API设计初衷是配合ass转换工具的，所以没有单独做xml转csv的API

    另外，为配合转换工具，设置了UTF-8编码而非UTF-16

    如果需要数据分析，请直接使用get_danmaku()

#### 功能： 获取一个视频的弹幕(原始文件，即xml)

#### 必要的传参：视频的cid（cid_input）, 只能输入数字, 可以通过实验性功能或者浏览器F12功能获得cid

#### 选择的传参：文件存在时强制刷新（reset），默认不刷新（False）

#### 返回：弹幕文件的绝对路径，文件为xml，直接使用cid命名，同时打印绝对路径



### ⛏```raw2ass(file_path)```

💡需要调用[Niconvert](https://github.com/muzuiget/niconvert)

    如果你要自己去下载官方版，请注意：作者针对此API将Niconvert进行了小改，以便能在命令行运行，下载原版需要自行调整

#### 功能： 将xml标准格式转换为ass字幕文件，以便能在第三方播放器实现弹幕效果

#### 必要的传参：xml文件绝对路径(file_path）

#### 选择的传参：无

#### 返回：ass字幕文件的绝对路径，文件为ass，直接使用cid命名，同时打印绝对路径

#### 异常：遇到大文件极小概率抛出FAIL异常，请手动修改for循环的超时等待时间



### ⛏```anime_base_info(media_id)```

#### 💡此API为本次开发重点

经历多次改动，现功能性相当强，可以用作番剧信息收集或声优信息整理

✅虽然说爬取番剧/电影，但同时也能兼容一些综艺类节目(《欢天喜地好哥们》，md28229430，测试通过)，以此推测这类的架构都是一样的

在说明API前，需要说明一些B站在番剧方面API的一些参数（比较复杂），这些参数一般可在URL中找到

(电影/番剧/综艺等在此表统称番剧)

| 名称 | 中文名 | 解释 | 例子 | 获取途径 |
| :---:| :---: | :---: | :---: | :---: |
| media_id | 番剧md号 | 每个番剧的特征号(和av号一样的作用) | md135652(JOJO的奇妙冒险 第五季) | 在番剧介绍页URL中出现，在此API作为必须传入的参数 |
| season_id | 番剧id | 也是每个番剧的特征号(个别番剧的md号和ss号相同) | ss3398(冰菓) | 小概率会在番剧介绍页URL中出现，可以通过此API获取,也会在番剧播放页小概率出现，此时通过?id=1的形式传参达到播放不同集的效果 |
| ep_id | 剧集编号 | 每集的特征号，全B站唯一 | ep234488(玉子市场 第一集) | 在番剧播放页的URL中就可以找到，可以通过此API获取，anime_base_info(media_id)返回的ep_id为最后一集的 |
	
这些参数一般会一起在B站API出现，md号在介绍页URL必能找到

还有一个不太重要的参数：tag_id，标签ID，每个番剧都不同，根据观察，这个可能和向用户推送关于此番剧的二创视频有关

#### 功能：获取番剧基本信息

#### 必要的传参：番剧的md号（media_id），输入数字

#### 选择的传参：无

#### 返回：字典， 参数如下:

| 参数名(key) | 解释 | 备注 | 返回值举例 |
| :---:| :---: | :---: | :---: |
| title | 标题 | | 玉子市场 |
| type | 类型 | 番剧/电影(TV版和剧场版均为番剧) | 番剧 |
| area | 地区 |  | 日本 |
| share_url | 介绍页URL | 并不是播放页URL，此URL含mediaID | https://www.bilibili.com/bangumi/media/md116772 |
| desc | 简介 | “xxx译制”信息会被删除 | 座落某个小镇的兔子商店街上，有一间日式饼店，住着一位... ... |
| cover_url | 介绍页封面URL| | http://i0.hdslb.com/bfs/bangumi/67da3dae76e526a925b78b1d8abe21c870333491.jpg |
| media_id | md号 | | 116772 |
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
| aid | av号 | 对于番剧/电影意义不大 | av27045209 |
| bvid | bv号 | 对于番剧/电影意义不大 | BV1fs41177WY |
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


 🎞质量编号科普：
 
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
    
    ⚠注意，这里的desc和video_info的desc性质不同，不能混用

    相比于视频的介绍（desc），番剧的介绍看起来不能通过API来获取，只能截取HTML后使用bs4和正则表达式来搜索，比较麻烦

    加入识别原生分辨率，是否收费等功能，已经集成av和bv的获取
    
    另外，部分番剧不能返回正确的清晰度，因为有限制，且并不打算在每个ep求清晰度，因为会造成大量请求

    另外说明：目前所有在media_id_pool.py的番剧全部通过测试，已配置反爬取告警。仍然存在潜在bug。
    
⚠ 截止到2020年11月19日，在Love Live! 剧场版(于2020年11月30日开播)引发了严重的bug，anime_episode_info中json字段名于修改前的bilib不一致

由于是针对性修复，以后会继续尝试优化它

以下为demo_tamako.py收集的部分信息：

    -----此信息于2020-11-19,11:03:14生成-----
 
    -----------大纲-----------
    名称：Love Live! 学园偶像 电影
    别称：Love Live! The School Idol Movie LoveLive剧场版 
    ... ...
    集数：全1话
    开播时间：2020年11月30日
    是否开播：是
    是否完结：是
    评分：不支持
    观看可用性：免费
    -----------数据-----------
    AV号：av372595132
    BV号：BV1GZ4y1V7HV
    当前用户最高画质：112(1080P 高码率)
    media_id(md)：28230704
    season_id(ss)：35182
    tag_id：17124394
    最新一集的剧集编号(ep)：0
    等级编号：不支持
    ... ...
    -----------剧集-----------
    预告
    集标题：11月30日0点，全网独播！
    剧集编号(ep)：351809
    弹幕cid：250290897
    ... ...
    
❌ 未开播的番剧，但“是否开播”为True

❌ 等级编号未显示

✔ 评分由于没有开播显示不支持很正常

✔ 此时的剧集标题，清晰度信息指向预告而非正片，但清晰度应当与正片一致

另外，在2020年11月19日测试《姜子牙》(md28230900)时也出现了上述情况，但不存在Love Live! 剧场版导致bilib崩溃的问题

### ⛏```anime_episode_info(season_id)```

#### 功能：获取指定番剧/电影的av,cid,标题等高级信息，以及每集的信息

#### 必要的传参：番剧的id号（season_id），输入数字

#### 选择的传参：无

#### 返回：字典，key为集编号（str而非int，因为在冰菓遇到了11.5）,value为字典，参数如下:

| 参数名(key) | 解释 | 备注 | 返回值举例 |
| :---:| :---: | :---: | :---: |
| aid | av号 | 正常来说，单部番剧唯一 | 52307583 |
| cid | cid号 | 弹幕池编号 | 91550935  |
| ep_id | 剧集编号 |  | 21278 |
| title_long | 当前集长标题 |  | Live House！ |
| cover_url | 当前集封面URL |  | http://i0.hdslb.com/bfs/bangumi/a2bbb9e95ed53d5ff85a7a2cca7524a9c8455edd.jpg |
| share_url | 当前集播放页URL | 此URL含epID或seasonID | https://www.bilibili.com/bangumi/play/ep21278 |

    另外说明：目前所有在media_id_pool.py的番剧全部通过测试，已配置反爬取告警。仍然存在潜在bug。



### ⛏```get_resolution(id_input,getid = False)```

💡一般仅表示游客支持的最高质量

#### 功能：获取视频最高清晰度

#### 必要的传参：av号,bv号或ep号，必须带字母

#### 选择的传参：getid，返回质量编号(True)而非清晰度描述(False)

#### 返回：字符串，清晰度描述或质量编号

    另外说明：由于同时支持视频和某些番剧，故单独做了此API，作为备份，已集成到video_info()，anime_base_info()则使用了另外的方法
    
    由于我真的没料到B站出了HDR视频，为预防将来出现更高规格的视频，新编号一律返回类似“疑似错误的编号(250)”的形式

#### 报错: 部分番剧可能会返回"不支持"



## 😫实验性API


### ⛏```video_info(id_input)```

    不太推荐在番剧使用此API，除bv号和av号外，其它数据均可通过anime_base_info(media_id)获取
    
    新加入原生分辨率识别功能，完美支持所有视频
    
    强行在番剧可能会在清晰度相关key返回"不支持"

#### 功能：获取视频的信息

#### 必要的传参：视频av号或bv号（id_input），"av"和"bv"也要一同输入

#### 选择的传参：无

#### 返回：字典，参数如下:

| 参数名(key) | 解释 | 备注 |
| :---:| :---: | :---: |
| aid | av号 |  |
| bvid | bv号 |  |
| cid | cid号 | 弹幕池编号 |
| title | 视频标题 |  |
| desc | 视频描述 |  |
| owner_name | up主昵称 |  |
| owner_uid | up主的UID |  |
| view | 观看量 |  |
| danmaku | 弹幕量 |  |
| reply | 评论量 |  |
| favorite | 收藏量 |  |
| coin | 投币量 |  |
| share | 分享量 |  |
| like | 点赞量 |  |
| quality | 最高画质 | 仅表示游客和非大会员支持的最高画质 |
| quality_id | 最高画质编号 | 用于辅助分析 |

    另外说明：由于番剧/电影也存在av号/bv号，所有此API对于番剧等可能有效，多p情况可能异常，不会返回联合投稿的stuff

### ⛏```search_anime(keyword)```

    此API因本人一个视频项目应运而生，基于轻音少女搜索结果开发
    
    这个API目前相当不稳定

#### 功能：搜索番剧名称，返回md号

#### 必要的传参：要搜索的番剧名(keyword)

#### 选择的传参：无

#### 返回：字典，key为番剧名字，value为md号(带md号)

#### 报错：没有查到会返回空字典(无论是不是404)，412会抛出异常



## 🎈感谢

本lib部分API参考来自https://www.bilibili.com/read/cv5293665

感谢[Niconvert](https://github.com/muzuiget/niconvert)

同时也感谢自己Firefox的开发者工具和自己的Python 3.6.8和PyCharm 2019.3.3（认真）

也感谢B站不把我打死（确信）


