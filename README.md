# bilib

整合多个B站API的Python lib

bili + lib = bilib

前身为danlib，如果你在我的GitHub找到了danlib，你可以继续使用它，但如果你要改为使用bilib，你需要修改你的代码

这个lib可以帮助你完成用户基本信息（粉丝量关注数等）和弹幕（需提供cid）的爬取

实验性功能：获取视频信息，获取番剧/电影信息和章节列表

除弹幕功能以bs4为核心外，其它功能均以requests为核心，你可能还需要安装fake_useragent和csv包来让bilib正常工作

请勿将此lib用于非法用途（包括敏感数据爬取和DoS/DDoS攻击），作者将不承担任何责任，使用此lib视为已遵守此规则

另外，lib中注解可能与README冲突，请以README为准



## 稳定功能的API

这部分包含了我从2020年5月开始调试的代码，目前爬取100w+数据后仍能稳定工作



### user_info(uid_input, get_ua=False)

功能： 获取一个用户的基本信息（粉丝，关注，UID，昵称）

必要的传参：用户的UID（uid_input）

选择的传参：要求返回爬取此用户数据用到的User Agent(get_ua)，默认不返回UA（False）

返回：字典，形式为return_dict = {"uid_input": 用户输入的UID, "name": 昵称, "fans": 粉丝数, "following": 关注数, "st_code": HTTP状态码, "ua": User Agent}

异常：此API只会遇到三个异常：HTTP 404, HTTP 412，HTTP 200但无法分离昵称

	• HTTP 404
  
    表示此用户不存在/已销号，返回昵称为'(##BLANK_USER##)'，包含单引号
    
    注意，销号用户也有可能查到其粉丝量等
    
	• HTTP 412（事实上时指除200和404以外的情况，只有412）
  
    表示已触发反爬取机制，一般在30-40分钟后恢复
    
    会抛出InfoError，不返回任何值
  
	• HTTP 200但无法分离昵称
  
    这可能是B站彩蛋？具体表现之一为访问其主页只会看到几个字
    
    返回昵称为'(##WDNMD_USER##)'，包含单引号
    


### get_danmaku(cid_input, reset=False)

#### 2020.10.13，使用UCS-2(UTF-16)替换UTF-8编解码。UCS-2编码弹幕的表现：类似某些supreme，awsl等艺术字弹幕

功能： 获取一个视频的弹幕，包括番剧/电影（最多返回8000条）

必要的传参：视频的cid（cid_input）, 只能输入数字, 可以通过实验性功能或者浏览器F12功能获得cid

选择的传参：文件存在时强制刷新（reset），默认询问是否刷新（False），此处可能会修改为可以选择强制不刷新

返回：弹幕文件的绝对路径，文件为csv，直接使用cid命名，同时打印绝对路径

异常：目前没有检查到这个API会触发反爬取，但保险起见，遇到任何异常会直接抛出



### listall_danmaku(file_path, stamp=False)

#### 2020.10.13，修复UnicodeEncodeError，使用UCS-2的特殊字符可能不能在IDLE显示，PyCharm正常显示

功能：处理弹幕文件，并输出

必要的传参：弹幕文件的绝对路径（file_path）

选择的传参：返回现实时间的时间戳而非转化的时间（stamp），默认返回转化的时间（False）

返回：字典，key为序号(int),value分别为：视频内发送时间，弹幕类型，弹幕字号，弹幕颜色，现实发送时间，弹幕池，用户ID（被加密），rowID，发送内容（如果是高级弹幕，还会在这里包含一些参数）。如果遇到了全新的弹幕类型，会不处理直接返回

异常：现有的弹幕文件结构不会造成此API的异常



### count_danmaku(file_path)

功能：获取弹幕文件行数

必要的传参：弹幕文件的绝对路径（file_path）

选择的传参：无

返回：一个数字，此为弹幕文件总行数

异常： 除非弹幕文件不存在，否则不太可能会触发异常



## 实验性API

这些都是获取视频/番剧或电影信息的API，由于有多分p的情况，目前推荐在单p下使用，对于番剧，请尽可能避免遇到存在SP的情况（季度的情况估计不会有问题）

这些API将在最近开始测试，下面的说明不会包含遇到的异常

### 简单说明

在说明API前，需要说明一些B站在番剧方面API的一些参数（比较复杂），这些参数一般可在URL中找到

	•season_id 番剧id （例如ss3398，冰菓），小概率才会在URL中出现

	•media_id 番剧md号（例如md135652，JOJO的奇妙冒险 第五季）

	•ep 剧集编号（例如ep84787，冰菓）
	
这些参数一般会一起在B站API出现，md号在介绍页URL必能找到
	


### video_info(id_input)

功能：获取视频的信息

必要的传参：视频av号或bv号（id_input），"av"和"bv"也要一同输入

选择的传参：无

返回：字典，{"aid": av号, "bvid": bv号, "cid": 弹幕池编号cid, "title": 视频标题, "desc": 视频描述, "owner_name": up主昵称， "owner_uid": up主的UID, "view": 观看量, "danmaku": 弹幕量, "reply": 评论量, "favorite": 收藏量,"coin": 投币量, "share": 分享量, "like": 点赞量}

另外说明：由于番剧/电影也存在av号/bv号，所有此API对于番剧等可能有效，多p情况可能异常，不会返回联合投稿的stuff



### anime_base_info(media_id)

功能：获取番剧基本信息

必要的传参：番剧的md号（media_id），输入数字

选择的传参：无

返回：字典， {"title": 标题, "type": 类型, "area": 地区, "share_url": 介绍页URL（并不是播放页URL）, "cover_url": 介绍页封面URL,"media_id": md号, "ep_id": 剧集编号, "episode": 集数, "rating_count": 等级编号，猜测是总排行榜的RANK,"score": 评分, "season_id": 番剧ID, "coins": 总投币数, "danmakus": 总弹幕量, "follow": 追番数,"series_follow": 系列追番数, "views": 总播放量}

另外说明：目前测试了单季不带剧场版番剧（如冰菓），单季带剧场版番剧（如玉子市场），多季番剧（如JOJO的奇妙冒险 第五季），均没有遇到问题，已配置反爬取告警。仍然存在潜在bug。



### anime_episode_info(season_id)

功能：获取指定番剧/电影的av,cid,标题等高级信息，以及每集的信息

必要的传参：番剧的id号（season_id），输入数字

选择的传参：无

返回：字典，key为集编号（String，因为在冰菓遇到了11.5，而我不想混合使用float），value为一个列表，分别是：av号，弹幕池编号，剧集编号，当前集长标题，当前集封面URL，当前集播放页URL。

另外说明：目前测试了单季不带剧场版番剧（如冰菓），单季带剧场版番剧（如玉子市场），多季番剧（如JOJO的奇妙冒险 第五季），均没有遇到问题，已配置反爬取告警。仍然存在潜在bug。

## demo

	• 获取一个番剧的视频分p信息，并显示这些分p的信息，弹幕列表，同时也返回此番剧的信息（番剧本质是一个多分p的视频）
	
	season_id = bilib.anime_base_info(116772)["season_id"]
	
	episode_info = bilib.anime_episode_info(season_id)
	
	for i,j in episode_info.items():
	
	    print(i,j)
	    
	    av_no = j[0]
	    
	    cid_no = int(j[1])
	    
	    danmaku_path = bilib.get_danmaku(cid_no)
	    
	    length_danmaku = bilib.count_danmaku(danmaku_path)
	    
	    for index in range(0,length_danmaku):
	    
		print(bilib.listall_danmaku(danmaku_path)[index])
		
	print(bilib.video_info(av_no,mode="av"))

## 感谢

本lib部分API参考来自https://www.bilibili.com/read/cv5293665

同时也感谢自己Firefox的开发者工具和自己的Python 3.6.8和PyCharm 2019.3.3（认真）

也感谢B站不把我打死（确信）


