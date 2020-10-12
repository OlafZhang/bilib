# bilib

整合多个B站API的Python lib

bili + lib = bilib

前身为danlib，如果你在我的GitHub找到了danlib，你可以继续使用它，但如果你要改为使用bilib，你需要修改你的代码

这个lib可以帮助你完成用户基本信息（粉丝量关注数等）和弹幕（需提供cid）的爬取

实验性功能：获取视频信息，获取番剧/电影信息和章节列表

除弹幕功能以bs4为核心外，其它功能均以requests为核心，你可能还需要安装fake_useragent和csv包来让bilib正常工作

请勿将此lib用于非法用途（包括敏感数据爬取和DoS/DDoS攻击），作者将不承担任何责任，使用此lib视为已遵守此规则

## 稳定功能的API

这部分包含了我从2020年5月开始调试的代码，目前爬取100w+数据后仍能稳定工作

### user_info(uid_input, get_ua=False)
