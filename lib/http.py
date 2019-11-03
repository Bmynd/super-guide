import json

from django.http import HttpResponse
from django.conf import settings


def render_json(code=0, data=None):
    json_data = {
        'code': code,
        'data': data
    }
    if settings.DEBUG:
        # 格式化输出
        data = json.dumps(json_data, ensure_ascii=False, indent=4, sort_keys=True)
    else:
        data = json.dumps(json_data, ensure_ascii=False, separators=[',', ':'])
    return HttpResponse(data)