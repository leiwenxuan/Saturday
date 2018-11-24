from copy import deepcopy

from django.db.models import Q


from utils import mypage
from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.contrib import auth
from crm.forms import RegisteredForm, Addfrom, RecordForms, EnrollmentForms
from crm.models import UserProfile, Customer, ConsultRecord, Enrollment
from django.urls import reverse
from django.http import JsonResponse, request, QueryDict
from geetest import GeetestLib
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# 导入日志
import logging

logger = logging.getLogger(__name__)


# Create your views here.

class LoginViews(View):
    def get(self, request):
        return render(request, 'login2.html')

    def post(self, request):
        stu_name = request.POST.get('stu_name')
        stu_pwd = request.POST.get('stu_pwd')
        # 判断checkbox 是否选中
        is_check = (request.POST.get('check_un') == 'ok')
        # 验证密码是否正确
        user_obj = auth.authenticate(request, email=stu_name, password=stu_pwd)
        if user_obj:
            print('7' * 20)
            # 把登陆用户加入
            auth.login(request, user_obj)
            # 判断是否选中７天免登陆
            if is_check:
                request.session.set_expiry(7 * 24 * 60 * 60)
            else:
                request.session.set_expiry(0)
            next_url = reverse('crm:cus_list')
            print(next_url)
            return redirect(next_url)
        else:
            print('-' * 30)
            return render(request, 'login2.html', {"error_msg": '用户名密码错误'})


class RegViews(View):
    def get(self, request):
        form_obj = RegisteredForm()
        print('@' * 80)
        return render(request, 'reg.html', {"form_obj": form_obj})

    def post(self, request):

        # 实例化一个form　对象, 接受request.post
        form_obj = RegisteredForm(request.POST)

        # 创建一个ajax 验证字典
        res = {'code': 0}
        # 校验是否通过验证
        if form_obj.is_valid():
            # 清理数据　 cleaned_data() 数据里面多出了确认密码的选项，ｐｏｐ出去
            data = form_obj.cleaned_data
            data.pop("re_password")
            # 创建用户
            UserProfile.objects.create_user(**data)
            # 打入日志
            logger.info(data)
            # 规范化的地址
            next_url = reverse('crm:login')
            print(next_url)
            res['url'] = next_url
            return JsonResponse(res)
        else:
            print('&' * 80, 'new')
            res['code'] = 1
            # python json 不能传对象
            res['essor_msg'] = form_obj.errors
            return JsonResponse(res)


class IndexViews(View):
    @method_decorator(login_required)
    def get(self, request):
        customer_lsit = Customer.objects.all()
        return render(request, 'index.html', {"customer_list": customer_lsit})


def check_user(request):
    ''' 检测input 输入是否可靠'''
    form_obj = RegisteredForm(request.POST)
    res = {'code': 0}
    if request.method == "POST":
        # 解析　request.POST 形成一个可靠数据
        for key, val in request.POST.items():
            # 字段唯一判断
            if key in ['phone', 'email']:
                data = {key: val}
                is_user = UserProfile.objects.filter(**data)
                # print(is_user)
                # 如果is_user 存在返回错误消息
                if is_user:
                    res['code'] = 1
                    res['error_msg'] = '该选项已存在！'
                    print('!' * 80)
                    return JsonResponse(res)
            if val is None:
                print('%' * 20)
                res['code'] = 1
                res['error_msg'] = '请正确输入！'
                print('!' * 80)
                return JsonResponse(res)

    return JsonResponse(res)


class Logout(View):
    def get(self, request):
        return render(request, 'logout.html')

    def post(self, request):
        print('+' * 20)
        if request.method == 'POST':
            from django.contrib import auth
            auth.logout(request)
            print('%' * 20)
            next_change = reverse('crm:login')
            return JsonResponse({'code': 0, 'url': next_change})


class ChangeVires(View):
    def get(self, request):
        return render(request, 'change.html')


class IndexViews(View):
    '''
    程序分析：１．获取前端点击的页数
            2. 计算总的页数, 设置页面显示的数据量
            3. 计算要用多少页来显示　divmod(table_count, per_page)　商和余
            4. 处理下不是正确的页数
            5. 设置一个　页面显示多少页码
            ６. 处理页面显示各种特殊情况
            7. 拼接html 代码
    :param request:
    :return:
    '''

    # 获取操作的指令
    @method_decorator(login_required())
    def get(self, request):
        url_prefix = request.path_info
        print(url_prefix)
        # 深copy queryset 类型 11.22
        # qd = deepcopy(request.GET)
        # qd._mutable = True
        # request 自带copy  11.23
        qd = request.GET.copy()

        # 从URL获取参数
        current_page = request.GET.get("page", 1)
        if request.path_info == reverse('crm:pirvate'):
            # 私户
            customer_lsit = Customer.objects.filter(
                consultant=self.request.user)
            flag_page = 'pirvate'
        else:
            # 公户
            customer_lsit = Customer.objects.filter(consultant__isnull=True)
            flag_page = 'cus_list'
        # 模糊查找, 如果query为空不走模糊搜索
        if self.request.GET.get('query', ''):
            q = self._get_query_q(['name', 'qq', 'qq_name'])
            customer_lsit = customer_lsit.filter(q)

        # 总数据量
        table_count = customer_lsit.count()

        # 获取开始页和结束页
        page_obj = mypage.Pagination(current_page, table_count, url_prefix, qd)

        customer_lsit = customer_lsit[page_obj.start:page_obj.end]
        # 获取页面
        page_html = page_obj.page_html()

        # 拼接url函数
        # a_href = request.GET.urlencode()

        # 11.23 获取当前的url
        url = request.get_full_path()
        query_params = QueryDict(mutable=True)
        query_params['next'] = url
        next_url = query_params.urlencode()
        return render(request, 'index.html',
                      {'customer_list': customer_lsit, 'next_url': next_url, 'page_list': page_html, 'flag_page': flag_page})

    @method_decorator(login_required())
    def post(self, request):
        cid = request.POST.getlist('cid')
        print(cid)
        action = request.POST.get('action')
        # 反射 判断是否有一个_action 的方法有就执行没有， 返回一个提示
        if not hasattr(self, "_{}".format(action)):
            return HttpResponse("nihao")
        print(action, type(action))
        # 反射调用
        getattr(self, '_{}'.format(action))(cid)
        return redirect(reverse("crm:cus_list"))

    def _to_private(self, cid):
        # 1 给我的客户列表添加 add函数
        self.request.user.customers.add(*Customer.objects.filter(id__in=cid))
        # 2 把要操作的客户添加到我的客户列表里
        Customer.objects.filter(id__in=cid).update(
            consultant=self.request.user)

    def _to_all(self, cid):
        # 找到要操作的的客户，把他们的销售字段设置为空
        Customer.objects.filter(id__in=cid).update(consultant=None)
        # 或者从我的客户列表中把指定的客户删除
        # request.user.customers.remove(*Customer.objects.filter(id__in=cid)

    def _get_query_q(self, field_list, op="OR"):
        # 从GET请求的url中找到要检索的内容
        query_value = self.request.GET.get('query', '')
        q = Q()
        # 指定Q查询内部的操作是OR还是AND
        q.connector = op

        # 遍历要检索的字段， 挨个添加Q对象
        # field_list 传进来的一些自断
        for filed in field_list:
            q.children.append(Q(('{}__icontains'.format(filed), query_value)))
        return q


class Add_cus(View):
    '''
    １．修改和增加一起操作
        思路利用formsmodel 操作, 修改和添加主要区别是id 问题，
        forms模块，　instance 可以等于None，在处理orm 获取对象时候，空QuerySet对象调用first为None
    '''
    @method_decorator(login_required)
    def get(self, request, cus_id=0):
        print(cus_id)
        cus_obj = Customer.objects.filter(id=cus_id).first()
        form_obj = Addfrom(instance=cus_obj)
        return render(request, 'add_cus.html', {'form_obj': form_obj, 'edit_id': cus_id})

    @method_decorator(login_required)
    def post(self, request, cus_id=0):
        # cus_id = request.GET.get('id')
        cus_obj = Customer.objects.filter(id=cus_id).first()
        print(cus_obj)

        form_obj = Addfrom(request.POST, instance=cus_obj)
        if form_obj.is_valid():
            form_obj.save()  # 保存的基础是调用上上一句实例话
            # url = reverse('crm:cus_list')
            # 如果能从URL获取到next参数就跳转到制定的URL,没有就默认跳转到客户列表页

            next_url = request.GET.get('next', reverse('crm:cus_list'))

            return redirect(next_url)
        else:
            return render(request, 'add_cus.html', {"form_obj": form_obj})


# 使用极验滑动验证码的登录

def login(request):
    # if request.is_ajax():  # 如果是AJAX请求
    print('11111')
    if request.method == "POST":
        # 初始化一个给AJAX返回的数据
        ret = {"status": 0, "msg": ""}
        # 从提交过来的数据中 取到用户名和密码
        username = request.POST.get("username")
        pwd = request.POST.get("password")
        print(username, pwd)
        print(username, pwd)
        # 获取极验 滑动验证码相关的参数
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]

        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        if result:
            # 验证码正确
            # 利用auth模块做用户名和密码的校验
            user = auth.authenticate(email=username, password=pwd)
            print(user, '%' * 20)
            if user:
                # 用户名密码正确
                # 给用户做登录
                auth.login(request, user)

                # 判断checkbox 是否选中
                is_check = (request.POST.get('check_un') == 'ok')
                # 判断是否选中７天免登陆
                if is_check:
                    request.session.set_expiry(7 * 24 * 60 * 60)
                else:
                    request.session.set_expiry(0)
                next_url = reverse('crm:cus_list')
                print(next_url)
                ret["msg"] = next_url
            else:
                # 用户名密码错误
                ret["status"] = 1
                ret["msg"] = "用户名或密码错误！"
        else:
            ret["status"] = 1
            ret["msg"] = "验证码错误"

        return JsonResponse(ret)
    print('%' * 20)
    return render(request, "login.html")


# 获取验证码图片的视图
def get_valid_img(request):
    # with open("valid_code.png", "rb") as f:
    #     data = f.read()
    # 自己生成一个图片
    from PIL import Image, ImageDraw, ImageFont
    import random

    # 获取随机颜色的函数
    def get_random_color():
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

    # 生成一个图片对象
    img_obj = Image.new(
        'RGB',
        (220, 35),
        get_random_color()
    )
    # 在生成的图片上写字符
    # 生成一个图片画笔对象
    draw_obj = ImageDraw.Draw(img_obj)
    # 加载字体文件， 得到一个字体对象
    font_obj = ImageFont.truetype("static/font/kumo.ttf", 28)
    # 开始生成随机字符串并且写到图片上
    tmp_list = []
    for i in range(5):
        u = chr(random.randint(65, 90))  # 生成大写字母
        l = chr(random.randint(97, 122))  # 生成小写字母
        n = str(random.randint(0, 9))  # 生成数字，注意要转换成字符串类型

        tmp = random.choice([u, l, n])
        tmp_list.append(tmp)
        draw_obj.text((20 + 40 * i, 0), tmp,
                      fill=get_random_color(), font=font_obj)

    print("".join(tmp_list))
    print("生成的验证码".center(120, "="))
    # 不能保存到全局变量
    # global VALID_CODE
    # VALID_CODE = "".join(tmp_list)

    # 保存到session
    request.session["valid_code"] = "".join(tmp_list)
    # 加干扰线
    # width = 220  # 图片宽度（防止越界）
    # height = 35
    # for i in range(5):
    #     x1 = random.randint(0, width)
    #     x2 = random.randint(0, width)
    #     y1 = random.randint(0, height)
    #     y2 = random.randint(0, height)
    #     draw_obj.line((x1, y1, x2, y2), fill=get_random_color())
    #
    # # 加干扰点
    # for i in range(40):
    #     draw_obj.point((random.randint(0, width), random.randint(0, height)), fill=get_random_color())
    #     x = random.randint(0, width)
    #     y = random.randint(0, height)
    #     draw_obj.arc((x, y, x+4, y+4), 0, 90, fill=get_random_color())

    # 将生成的图片保存在磁盘上
    # with open("s10.png", "wb") as f:
    #     img_obj.save(f, "png")
    # # 把刚才生成的图片返回给页面
    # with open("s10.png", "rb") as f:
    #     data = f.read()

    # 不需要在硬盘上保存文件，直接在内存中加载就可以
    from io import BytesIO
    io_obj = BytesIO()
    # 将生成的图片数据保存在io对象中
    img_obj.save(io_obj, "png")
    # 从io对象里面取上一步保存的数据
    data = io_obj.getvalue()
    return HttpResponse(data)


# 请在官网申请ID使用，示例ID不可使用
pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"


# 处理极验 获取验证码的视图
def get_geetest(request):
    print('&' * 20)
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)


# 跟进客户
@login_required
def record_list(request):

    record_obj = ConsultRecord.objects.all()
    print(8888)
    return render(request, 'record_list.html', {"record_obj": record_obj, 'flag_page': 'record_list'})


@login_required
def change_record(request):

    eidt_id = request.GET.get('edit_id', None)
    record_obj = ConsultRecord.objects.filter(id=eidt_id).first()
    if not record_obj:
        record_obj = ConsultRecord(consultant=request.user)
    form_obj = RecordForms(instance=record_obj, initial={
        'consultant': request.user})
    if request.method == 'POST':
        print(eidt_id)
        form_obj = RecordForms(request.POST, instance=record_obj)
        if form_obj.is_valid():
            form_obj.save()
            next_url = reverse('crm:record_list')
            print(next_url)
            return redirect(next_url)

    return render(request, 'edit_record.html', {"form_obj": form_obj, "edit_id": eidt_id})


class EnrollmentViews(View):

    def get(self, request, customer_id=0):
        if int(customer_id) == 0:
            # 1. 所有的客户列表
            Enr_obj = Enrollment.objects.filter(
                customer__consultant=request.user)
        else:
            # 查看当前的客户的跟进表
            Enr_obj = Enrollment.objects.filter(customer_id=customer_id)

        return render(request, 'en_list.html', {'enr_obj': Enr_obj})


class enr_editViews(View):
    def get(self, request, customer_id=0, enrollment_id=0):
        print(customer_id, enrollment_id)
        # 先根据 id区去查，如果为空说明新增
        print('8' * 12)
        print(customer_id)
        enr_obj = Enrollment.objects.filter(id=enrollment_id).first()
        print(enr_obj, '修改')

        # 2.给表指定一个客户
        if not enr_obj:
            print('&'*12)
            # 1.get 请求为添加操作， 先查看当前的要添加客户的对象
            customer_obj = Customer.objects.filter(id=customer_id).first()
            enr_obj = Enrollment(customer=customer_obj)

        form_obj = EnrollmentForms(instance=enr_obj)
        return render(request, 'enr_edit.html', {"form_obj": form_obj})

    def post(self, request, edit_id=0):
        # 获取要修改的对象
        enr_obj = Enrollment(
            customer=(Customer.objects.filter(id=edit_id).first()))
        print(enr_obj, edit_id)
        print(request.POST)
        # 实例化一个form对象
        form_obj = EnrollmentForms(request.POST, instance=enr_obj)
        print(form_obj.is_valid())
        if form_obj.is_valid():
            # 如果验证成功, 改变状态，
            # 1.获取一个对象
            enr_obj = form_obj.save()
            # 2.改变状态
            enr_obj.customer.status = 'signed'
            # 3.保存
            enr_obj.customer.save()

            print(reverse('crm:enrollment', kwargs={'customer_id': 0}))
            return redirect(reverse('crm:enrollment', kwargs={'customer_id': 0}))
        else:
            print('enr_edit.html')
            return render(request, 'enr_edit.html', {"form_obj": form_obj})
