import os
import re

from django.conf import settings
from django.core.cache import cache

from common import errors
from lib.sms import send_vcode
from lib.http import render_json
from common import keys
from swiper import config
from user.models import User
from user.forms import ProfileForm
from user.logic import handler_avatar_upload


# 获取短信验证码
def get_vcode(request):
    # 接收手机号码
    phone = request.POST.get('phone')
    if phone is None:
        return render_json(data='手机号码为空', code=errors.PHONE_EMPTY)
    if not re.match(r'1[356789]\d{9}', phone):
        return render_json(data='非法手机号码', code=errors.PHONE_ILLEGAL)

    # 发送短信验证码
    send_vcode(phone)

    return render_json()


# 通过验证码登录、注册
def submit_vcode(request):
     phone = request.POST.get('phone')
     vcode = request.POST.get('vcode')

     # 从缓存中取出验证码
     cached_vcode = cache.get(keys.VCODE % phone)
     if vcode == cached_vcode:
         # 验证码正确，可以登录和注册
         # try:
         #     user = User.objects.get(phonenum=phone)
         # except User.DoesNotExist:
         #     # 说明是注册
         #     user = User.objects.create(phonenum=phone)

         user, _ = User.objects.get_or_create(phonenum=phone) # True 创建  False 找

         request.session['uid'] = user.id

         # 登录完成之后，返回个人信息
         return render_json(data=user.to_dict())
     return render_json(code=errors.VCODE_ERROR, data='验证码错误')


# 获取个人资料
def get_profile(request):
    uid = request.session.get['uid']
    if not uid:
        return render_json(code=errors.NOT_LOGIN, data='未登录')
    user = User.objects.get(id=uid)
    # 通过用户拿到交友资料
    return render_json(data=user.profile.to_dict())


# 修改个人资料
def edit_profile(request):
    form = ProfileForm(request.POST)
    uid = request.session.get['uid']
    if uid:
        if form.is_valid():
            profile = form.save(commit=False)
            profile.id = uid
            profile.save()
            return render_json(data=profile.to_dict())
    return render_json(code=errors.NOT_LOGIN, data='未登录')


# # 头像上传
def upload_avatar(request):
    # 获取用户上传的头像文件
    uid = request.session.get('uid')
    avatar = request.FILES.get('avatar')
    filepath = os.path.join(settings.MEADIA_ROOT, keys.AVATAR_KEY % uid)
    handler_avatar_upload(filepath, avatar, uid)
    # 修改用户avatar属性
    user = User.objects.get(id=uid)
    user.avatar = config.QN_URL + keys.AVATAR_KEY % uid
    user.save()
    return render_json()




