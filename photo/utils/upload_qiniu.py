# import qiniu
# from cycle import settings
# from qiniu import Auth, put_file, etag, urlsafe_base64_encode, put_data
# import uuid
# from photo.libs import image_tools
# from PIL import Image  #pip install pillow
# import io
# import os
#
# url = settings.MEDIA_URL
# bucket_name = settings.QINIU_BUCKET_NAME
# q = qiniu.Auth(settings.QINIU_ACCESS_KEY, settings.QINIU_SECRET_KEY)
#
# def qiniu_upload_comparess(key, localfile):
#     _img = localfile.read()
#     size = len(_img) / (1024 * 1024)  # 上传图片的大小 M单位
#     image = Image.open(io.BytesIO(_img))
#     key = str(uuid.uuid1()).replace('-', '') + '.' + image.format
#     token = q.upload_token(bucket_name, key, 3600)
#     name = 'upfile.{0}'.format(image.format)  # 获取图片后缀（图片格式）
#     if size > 1:
#         x, y = image.size
#         im = image.resize((int(x / 1.73), int(y / 1.73)), Image.ANTIALIAS)  # 等比例压缩 1.73 倍
#         print('压缩')
#     else:
#         print('不压缩')
#         im = image
#
#     print(name)
#     im.save('./media/' + name)  # 在根目录有个media文件
#     im_c = image_tools.logo_watermark(im, './media/logo/logo.png')
#     im_c.save('./media/upload_image/' + name)
#
#     key1 = str(uuid.uuid1()).replace('-', '') + '.' + im_c.format
#     token1 = q.upload_token(bucket_name, key1, 3600)
#
#     path = './media/' + name
#     path1 = './media/upload_image/' + name
#
#     print(path)
#
#     ret, info = qiniu.put_file(token, key, path)
#     ret1, info1 = qiniu.put_file(token1, key1, path1)
#     if ret:
#         return '{0}{1}'.format(url, ret['key']),'{0}{1}'.format(url, ret1['key'])
#     else:
#         return 'error'
