# 我知道你会再来这里，所以我放出监视你（偷我视频的人）的代码
# 我怀疑就是发出issue的人搞的，不然就不会删除issue
# 等着瞧，这个代码会在树莓派长期运行

from os import execv
import bilib
FUCKER_video_list = bilib.up_video_list(402157092,1)['video_list']
FUCKER_video_counter = 0


while True:
    try:
        FUCKER_video_list[FUCKER_video_counter]
        print(("===第%s个视频===")%(str(FUCKER_video_counter+1)))
        print("标题：",end="")
        print(FUCKER_video_list[FUCKER_video_counter]["title"])
        print("BVID：",end="")
        print(FUCKER_video_list[FUCKER_video_counter]["bvid"])
        print("描述：",end="")
        print(FUCKER_video_list[FUCKER_video_counter]["description"])
        FUCKER_video_counter += 1
    except KeyError:
        break
    
