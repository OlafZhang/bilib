# bilib

整合多个B站API的Python lib

bili + lib = bilib

## 声明

1、截止至2020年11月1日，以下API正常使用，但不确定以后b站是否会改API，我们将尽可能保证在未来使用新的bilibili API的同时兼容您使用bilib编写的代码

2、虽然这是lib，但我没有安装标准格式进行编写和整理，目前建议的场景是"外挂"lib（将此lib放在你的工作目录）

3、由于营销号爬取视频进行再投放的行为相当可耻，故这里不会写关于视频下载的API

## 说明

前身为danlib，如果你在我的GitHub找到了danlib，你可以继续使用它，但如果你要改为使用bilib，你需要修改你的代码

这个lib可以帮助你完成用户基本信息（粉丝量关注数等）和弹幕（需提供cid）的爬取

实验性功能：获取视频信息，获取番剧/电影信息和章节列表

除弹幕功能以bs4为核心外，其它功能均以requests为核心，你可能还需要安装fake_useragent和csv包来让bilib正常工作

请勿将此lib用于非法用途（包括敏感数据爬取和DoS/DDoS攻击），作者将不承担任何责任，使用此lib视为已遵守此规则

另外，lib中注解可能与README冲突，请以README为准

## 异常

现在这个bilib已经包含较精确的错误类型，方便排错和优化自己的代码

除非特殊情况，接下来在API介绍不再说明错误，具体说明如下

### InfoError(传参异常/未定义异常)

一般是因为用户输入了错误的数据，例如没有输入av号的av，以及目前小概率遇到的未定义异常

### danmakuError(弹幕文件等异常)

一般是弹幕文件被删除，或者不符合规范

### Timeout(请求超时)

服务器返回：请求错误。

可能是程序问题，或者是网络问题。

### RequestError(请求错误)

服务器返回：啥都木有。

貌似没有此人的信息，可能已销号，原始API没有返回任何值。

### SeemsNothing(返回空数据/传参不正确)

服务器返回：服务调用超时。

检查网络或重新尝试。

### RequestRefuse(触发反爬取机制)
	
服务器返回：请求被拦截。

HTTP 412，服务器已启动反爬机制，请稍后尝试。

#### 触发反爬取后会记录当前用户的UID（如果已经登陆），所以请不要在源代码插入自己的用户cookie



## 稳定功能的API

这部分包含了我从2020年5月开始调试的代码，目前爬取100w+数据后仍能稳定工作



### user_info_old(uid_input, get_ua=False)

这是旧的API，新API在下面

功能： 获取一个用户的基本信息（粉丝，关注，UID，昵称）

必要的传参：用户的UID（uid_input）

选择的传参：要求返回爬取此用户数据用到的User Agent(get_ua)，默认不返回UA（False）

返回：字典，形式为return_dict = {"uid_input": 用户输入的UID, "name": 昵称, "fans": 粉丝数, "following": 关注数, "st_code": HTTP状态码, "ua": User Agent}
    
    
    
### user_info(uid_input)

这是新的API，相比于旧的需要爬取一个API和一个HTML，新的直接使用两个API获得数据，更节省流量

功能： 获取一个用户的详细信息（粉丝，关注，UID，昵称）

必要的传参：用户的UID（uid_input）

选择的传参：无

返回：字典，形式为return_dict = {"name": 昵称, "uid": UID, "fans": 粉丝量, "following": 关注量, "sex": 性别, "level": 等级, "face_url": 头像URL, "sign": 个性签名, "birthday": 生日, "coins": 硬币，可能是获币数量, "vip_type": 是否为大会员且为哪种大会员}

补充：由于愚人节会临时将大会员改为小会员，可能API也会如此呈现，故在此提醒



### get_danmaku(cid_input, reset=False)

#### 2020.10.13，使用UCS-2(UTF-16)替换UTF-8编解码。UCS-2编码弹幕的表现：类似某些supreme，awsl等艺术字弹幕

功能： 获取一个视频的弹幕，包括番剧/电影（最多返回8000条）

必要的传参：视频的cid（cid_input）, 只能输入数字, 可以通过实验性功能或者浏览器F12功能获得cid

选择的传参：文件存在时强制刷新（reset），默认询问是否刷新（False），此处可能会修改为可以选择强制不刷新

返回：弹幕文件的绝对路径，文件为csv，直接使用cid命名，同时打印绝对路径



### listall_danmaku(file_path, stamp=False)

#### 2020.10.13，修复UnicodeEncodeError，使用UCS-2的特殊字符可能不能在IDLE显示，PyCharm正常显示

功能：处理弹幕文件，并输出

必要的传参：弹幕文件的绝对路径（file_path）

选择的传参：返回现实时间的时间戳而非转化的时间（stamp），默认返回转化的时间（False）

返回：字典，key为序号(int),value分别为：视频内发送时间，弹幕类型，弹幕字号，弹幕颜色，现实发送时间，弹幕池，用户ID（被加密），rowID，发送内容（如果是高级弹幕，还会在这里包含一些参数）。如果遇到了全新的弹幕类型，会不处理直接返回



### count_danmaku(file_path)

功能：获取弹幕文件行数

必要的传参：弹幕文件的绝对路径（file_path）

选择的传参：无

返回：一个数字，此为弹幕文件总行数

#### 请不要配合get_danmaku_raw使用，因为得出的数值不正确



### get_danmaku_raw(cid_input, reset=False)

#### 由于此API设计初衷是配合ass转换工具的，所以没有单独做xml转csv的API

#### 另外，为配合转换工具，设置了UTF-8编码而非UTF-16

#### 如果需要数据分析，请直接使用get_danmaku()

功能： 获取一个视频的弹幕(原始文件，即xml)

必要的传参：视频的cid（cid_input）, 只能输入数字, 可以通过实验性功能或者浏览器F12功能获得cid

选择的传参：文件存在时强制刷新（reset），默认询问是否刷新（False），此处可能会修改为可以选择强制不刷新

返回：弹幕文件的绝对路径，文件为xml，直接使用cid命名，同时打印绝对路径



### raw2ass(file_path)

#### 需要调用[Niconvert](https://github.com/muzuiget/niconvert)

#### 如果你要自己去下载官方版，请注意：作者针对此API将Niconvert进行了小改，以便能在命令行运行，下载原版需要自行调整

功能： 将xml标准格式转换为ass字幕文件，以便能在第三方播放器实现弹幕效果

必要的传参：xml文件绝对路径(file_path）

选择的传参：无

返回：ass字幕文件的绝对路径，文件为ass，直接使用cid命名，同时打印绝对路径

异常：遇到大文件极小概率抛出FAIL异常，请手动修改for循环的超时等待时间



## 实验性API

这些都是获取视频/番剧或电影信息的API，由于有多分p的情况，目前推荐在单p下使用，对于番剧，请尽可能避免遇到存在SP的情况（季度的情况估计不会有问题）

这些API将在最近开始测试，下面的说明不会包含遇到的异常

### 简单说明

在说明API前，需要说明一些B站在番剧方面API的一些参数（比较复杂），这些参数一般可在URL中找到

	•media_id 番剧md号（例如md135652，JOJO的奇妙冒险 第五季），会在介绍页URL中出现，在此API作为必须传入的参数
	
	•season_id 番剧id （例如ss3398，冰菓），小概率才会在介绍页URL中出现，可以通过此API获取

	•ep 剧集编号（例如ep84787，冰菓，某一集），这个是单集才有的概念，每一集的ep_id都不一样。对于anime_base_info(media_id)，此ep_id为最后一集的
	
这些参数一般会一起在B站API出现，md号在介绍页URL必能找到

还有一个不太重要的参数：tag_id，标签ID，每个番剧都不同，根据观察，这个可能和向用户推送关于此番剧的二创视频有关



### video_info(id_input)

### 不太推荐在番剧使用此API，除bv号和av号外，其它数据均可通过anime_base_info(media_id)获取

### 新加入原生分辨率识别功能，早期的视频/番剧可能不支持，正在尝试其他方法

功能：获取视频的信息

必要的传参：视频av号或bv号（id_input），"av"和"bv"也要一同输入

选择的传参：无

返回：字典，{"aid": av号, "bvid": bv号, "cid": 弹幕池编号cid, "title": 视频标题, "desc": 视频描述, "owner_name": up主昵称， "owner_uid": up主的UID, "view": 观看量, "danmaku": 弹幕量, "reply": 评论量, "favorite": 收藏量,"coin": 投币量, "share": 分享量, "like": 点赞量，"resolution": 原生分辨率}

另外说明：由于番剧/电影也存在av号/bv号，所有此API对于番剧等可能有效，多p情况可能异常，不会返回联合投稿的stuff



### anime_base_info(media_id)

### 注意，这里的desc和video_info的desc性质不同，不能混用

### 相比于视频的介绍（desc），番剧的介绍看起来不能通过API来获取，只能截取HTML后使用bs4和正则表达式来搜索，比较麻烦

### 另外新加入了判断免费/大会员/付费的功能，目前不太稳定

功能：获取番剧基本信息

必要的传参：番剧的md号（media_id），输入数字

选择的传参：无

返回：字典， {"title": 标题, "type": 类型, "area": 地区, "share_url": 介绍页URL（并不是播放页URL）, "desc":简介,"cover_url": 介绍页封面URL,"media_id": md号, "ep_id": 剧集编号, "episode": 集数, "rating_count": 等级编号，猜测是总排行榜的RANK,"score": 评分, "season_id": 番剧ID, "coins": 总投币数, "danmakus": 总弹幕量, "follow": 追番数,"series_follow": 系列追番数, "views": 总播放量,"tag_id" : 标签ID,"vip_info": 免费/大会员/付费}

#### ep_id是对于单集番剧才有的概念，这里的ep_id是最后一集的

#### episode对于番剧只能是总集数，但是对于一些电影来说则是上映时间（例如“2018-01-18上映”），请注意过滤

另外说明：目前测试了单季不带剧场版番剧（如冰菓），单季带剧场版番剧（如玉子市场），多季番剧（如JOJO的奇妙冒险 第五季），均没有遇到问题，已配置反爬取告警。仍然存在潜在bug。



### anime_episode_info(season_id)

功能：获取指定番剧/电影的av,cid,标题等高级信息，以及每集的信息

必要的传参：番剧的id号（season_id），输入数字

选择的传参：无

返回：字典，key为集编号（String，因为在冰菓遇到了11.5，而我不想混合使用float），value为一个字典，格式： {"aid" : av号, "cid" : 弹幕池编号cid, "ep_id" : 剧集编号, "title_long" : 当前集长标题, "cover_url" : 当前集封面URL, "share_url" : 当前集播放页URL}。

另外说明：目前测试了单季不带剧场版番剧（如冰菓），单季带剧场版番剧（如玉子市场），多季番剧（如JOJO的奇妙冒险 第五季），均没有遇到问题，已配置反爬取告警。仍然存在潜在bug。



## 感谢

本lib部分API参考来自https://www.bilibili.com/read/cv5293665

感谢[Niconvert](https://github.com/muzuiget/niconvert)

同时也感谢自己Firefox的开发者工具和自己的Python 3.6.8和PyCharm 2019.3.3（认真）

也感谢B站不把我打死（确信）


