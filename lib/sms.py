import random

import requests
from django.core.cache import cache

from swiper import config
from common import errors
from lib.http import render_json
from common import keys


def gen_vcode(size=4):
    start = 10 ** (size - 1)
    end = 10 ** size - 1
    vcode = random.randint(start, end)

    return str(vcode)


def send_vcode(phone):
    params = config.YZX_PARAMS.copy()
    vcode = gen_vcode()
    cache.set(keys.VCODE % phone, vcode, 180)
    params['param'] = gen_vcode()
    params['mobile'] = phone

    response = requests.post(config.YZX_URL, json=params)
    if response.status_code == 200:
        json_response = response.json()
        if json_response['code'] == '000000':
            return 'ok'
        else:
            return json_response['msg']
    else:
        return render_json(data='短信验证码发送失败',  code=errors.SMS_FAILED)