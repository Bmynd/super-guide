from qiniu import Auth, put_file, etag
import qiniu.config

from swiper import config
from common import keys


def upload_qiniu(filepath, uid):
    #构建鉴权对象
    q = Auth(config.QN_AK, config.QN_SK)
    #要上传的空间
    bucket_name = config.QN_BUCKET
    #上传后保存的文件名
    key = keys.AVATAR_KEY % uid
    #生成上传Token,可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)
    #要上传文件的本地路径
    # localfile = './syno/bbb。jpg '
    ret, info = put_file(token, key, filepath)
    print(info)

