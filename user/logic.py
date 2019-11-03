from lib.qiniu import upload_qiniu

# 头像上传
def handler_avatar_upload(filepath, avatar, uid):
    with open(filepath, mode='wb') as fp:
        for chunk in avatar.chunks():
            fp.write(chunk)
    # 保存到本地
    # 把本地的文件上传到七牛云
    upload_qiniu(filepath, uid)