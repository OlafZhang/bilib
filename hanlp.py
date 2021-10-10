import re
import crack
from pyhanlp import HanLP # 使用前导入 HanLP工具
segment = HanLP.newSegment().enableNameRecognize(True)
crack.main()
import bilib
bilib.get_danmaku(bilib.video_info("BV1JW411W7wM")['video'][0]["cid"])
alist = bilib.listall_danmaku(r"C:\Users\Olaf\OneDrive\Python\bilib\33465120.csv")
black_list = []
for x,y in alist.items():
    result = segment.seg(str(y[8]))
    if str("/nr") in str(result):
        for i in result:
            if str("/nr") in str(i):
                keyword = str(i).replace("/nr","")
                break
            else:
                keyword = ""
        decode = crack.crackl4(str(y[6]))[0]
        try:
            user_info = bilib.user_info(decode)
            name = user_info["name"]
            uid = user_info["uid"]
            level = user_info["level"]
            decode = str(("%s(%s with Level %s)")%(name,uid,level))
        except bilib.SeemsNothing:
            pass
        print(str("%s sended %s at %s,keyword is %s")%(decode,str(y[8]),str(y[4]),keyword))
        if str(y[6]) not in black_list:
            black_list.append(str(y[6]))
print(black_list)

"""
| nr | 人名 |

| n | 名词 |

| v | 动词 |

| p | 介词 |

| g | 语素词 |

| h | 前接部分 |
"""