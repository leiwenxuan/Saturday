from django import template
register = template.Library()
import time



@register.filter()
def mytime(web_time):
    # web_time = '2018-11-1 20:10:20'
    #字符串转化成格式化
    ttime = time.strptime(web_time, '%Y-%m-%d %H:%M:%S')
    print(ttime)
    # 格式化转化成时间戳
    stime = time.mktime(ttime)
    # print(stime)
    #时间戳
    now_time = time.time()
    # print(now_time)
    ret = now_time - int(stime)
    print(int(ret))
    # 格式时间转化为时间戳
    # print(time.mktime(ttime))
    # print(time.gmtime(ret).tm_min)

    # ret = time.time()
    if ret < 60:
        print(ret)
        return ret
    elif ret < 60*10:
        stu_time = time.gmtime(ret)
        print(stu_time.tm_min)
        #分钟
        return stu_time.tm_min
    else:
        str_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        # str_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

        print(str_time ,time.localtime())
        return str_time



# if __name__ == '__main__':
#     mytime()
#     mydateutil()