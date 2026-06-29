from airflow.providers.amazon.aws.hooks.s3 import S3Hook
import json
import logging
from airflow.models import Variable

logger = logging.getLogger(__name__)


def upload_to_s3(data, s3_key):
    bucket_name = Variable.get("S3_BUCKET_NAME")
    """
    Uploads data to an S3 bucket.

    :param data: Data to upload
    :param bucket_name: Name of the S3 bucket
    :param s3_key: S3 key (path in the bucket) where the file will be stored
    """
    s3_hook = S3Hook(aws_conn_id='aws_default')
    s3_hook.load_string(
        string_data=json.dumps(data),
        bucket_name=bucket_name,
        key=s3_key,
        replace=True
    )

    return s3_key

def read_json_from_s3(s3_key):
    bucket_name = Variable.get("S3_BUCKET_NAME")
    hook = S3Hook(aws_conn_id='aws_default')

    content = hook.read_key(key=s3_key, bucket_name=bucket_name)
    if content:
        return json.loads(content)
    else:
        logger.warning(f"No content found in S3 bucket '{bucket_name}' with key '{s3_key}'")
        return []