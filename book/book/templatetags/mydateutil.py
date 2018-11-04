from django import template
register = template.Library()

from datetime import *
from dateutil.relativedelta import *


# print(parser.parse('1993-04-16-10-22'))

# @register.filter()
# def mydateutil(birthday):
#     '''
#     Daday = date.today()
#     print(Now)  # 2018-11-01 22:26:36.940373
#     print(Daday)  # 2018-11-01
#
#     print(Now+relativedelta(months=+1, weeks=+1))
#     # 2018-12-08 22:28:11.207878
#
#     print(Daday+relativedelta(months=+1, weeks=+1, hour=10))
#     # 2018-12-08 22:28:11.207878
#
#     print(Now+relativedelta(year=1, month=1))
#     # ＝是赋值
#     # 0001-01-01 22:28:52.223818
#
#     print(relativedelta(datetime(2003, 10, 24, 10, 0), Daday))
#     # relativedelta(years=-15, days=-7, hours=-14)
#     # 根据时间推算relativedelta
#
#     print(Now+relativedelta(years=+1, months=-1))
#     # 2019-10-01 22:32:07.196174
#
#     print(date(2018, 1, 27)+relativedelta(months=+1))
#     # 2018-02-27
#     print(date(2018, 1, 31)+relativedelta(months=+1))
#     # 2018-02-28
#     print(date(2018, 1, 31)+relativedelta(months=+2))
#     # 2018-03-31
#     '''
#
#     if birthday:
#         Now = datetime.now()
#         ret = relativedelta(Now, parser.parse(birthday))
#         print(ret)
#         # Now = datetime.now()
#         # ret = relativedelta(datetime(1993, 4, 16, 10, 10), Now)
#         birthday = '你活了{}年{}月{}天{}时{}分'.format(ret.years, ret.months, ret.days, ret.hours, ret.minutes)
#         return birthday
@register.filter()
def birthday(mytime):
    now = datetime.now()
    # mytime = '2011-11-01'
    if mytime:
        ret = datetime.strptime(mytime, "%Y-%m-%d")
        bir_obj = relativedelta(now, ret)
        return '你破壳{obj.years}年{obj.days}天{obj.hours}日'.format(obj=bir_obj)


if __name__ == '__main__':
    print(birthday('2011-11-01'))
