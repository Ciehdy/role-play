import time
from typing import IO

from qiniu import Auth, BucketManager, put_data

from core.settings import settings

q = Auth(settings.qiniu.access_key, settings.qiniu.secret_key)
bucket = BucketManager(q)


def upload_stream(prefix: str, io: IO):
    key = f"{prefix}/{time.time_ns()}"
    token = q.upload_token(settings.qiniu.bucket_name, key, 3600)
    ret, info = put_data(up_token=token, key=key, data=io.read())
    return q.private_download_url(
        f"http://{bucket.bucket_domain(settings.qiniu.bucket_name)[0][0]}/{ret['key']}",
        expires=3600,
    )


def upload(prefix: str, suffix: str, data: bytes):
    key = f"{prefix}/{time.time_ns()}.{suffix}"
    token = q.upload_token(settings.qiniu.bucket_name, key, 3600)
    ret, info = put_data(up_token=token, key=key, data=data)
    return q.private_download_url(
        f"http://{bucket.bucket_domain(settings.qiniu.bucket_name)[0][0]}/{ret['key']}",
        expires=3600,
    )
