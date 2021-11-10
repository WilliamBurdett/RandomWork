import json
import os
import zipfile
from datetime import datetime
from typing import List

import boto3
import prefect
import requests
from botocore.exceptions import ClientError
from prefect import Flow, task, context, unmapped

DOWNLOADS_URL = "https://api.fda.gov/download.json"
LOGGER = context.get("logger")
LOCAL_PATH = "C:\\tmp"

BUCKET_NAME = "my_bucket_name"
S3_PREFIX = "nda/drugs"
SCRIPT_PATH = os.path.dirname(__file__)


@task()
def get_file_urls() -> List[str]:
    response = requests.get(DOWNLOADS_URL).json()
    return [
        partition["file"]
        for partition in response["results"]["drug"]["ndc"]["partitions"]
    ]


# Taken from: https://docs.python-requests.org/en/master/user/quickstart/#raw-response-content
@task()
def download_file_from_url(file_url: str, folder_path: str) -> str:
    file_name = file_url.split("/")[-1]
    r = requests.get(file_url, stream=True)
    full_path = os.path.join(folder_path, file_name)
    with open(full_path, "wb") as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)
    return full_path


@task()
def unzip_file(file_path: str, folder_path: str) -> str:
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(folder_path)
    return file_path.replace(".zip", "")


# Taken from: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html
@task()
def upload_file(file_name: str, s3_prefix: str):
    s3_client = boto3.client("s3")
    s3_key = f"{s3_prefix}/{file_name}"
    try:
        response = s3_client.upload_file(file_name, BUCKET_NAME, s3_key)
    except ClientError as e:
        logger = prefect.context.get("logger")
        logger.error(e)
        return False
    return True

@task()
def list_files_in_s3():
    s3_client = boto3.client("s3")
    files = s3_client.list_objects(
        Bucket=BUCKET_NAME,
        Prefix=S3_PREFIX
    )


@task()
def get_s3_prefix() -> str:
    current_date = datetime.now()
    return "/".join(
        [
            S3_PREFIX,
            str(current_date.year),
            str(current_date.month),
            str(current_date.day),
        ]
    )

@task() #TODO: REMOVE
def print_whatever(anything):
    prefect.context.get("logger").debug(str(anything))

@task()
def create_data_folder() -> str:
    folder_path = os.path.join(SCRIPT_PATH, "raw_data")
    os.makedirs(folder_path, exist_ok = True)
    return folder_path


@task()
def split_files(file_path: str):
    with open(file_path, "r") as full_file:
        full_data = json.loads(full_file.read())
    meta_file_path = file_path.replace(".", "_meta.")
    results_file_path = file_path.replace(".", "_results.")
    with open(meta_file_path, "w") as meta_file:
        meta_file.write(json.dumps(full_data["meta"], indent=2))
    with open(results_file_path, "w") as results_file:
        results_file.write(json.dumps(full_data["results"], indent=2))


def main_full_refresh() -> Flow:
    with Flow("pull-nda-data-refresh") as flow:
        folder_path = create_data_folder()
        s3_prefix = get_s3_prefix()
        file_urls = get_file_urls()
        zipped_file_paths = download_file_from_url.map(file_url=file_urls, folder_path=unmapped(folder_path))
        unzipped_file_paths = unzip_file.map(
            file_path=zipped_file_paths, folder_path=unmapped(folder_path)
        )
        splitting_files = split_files.map(file_path=unzipped_file_paths)
        # print_whatever(unzipped_files)
        # uploading_files = upload_file.map(
        #     file_name=local_files,
        #     s3_prefix=unmapped(s3_prefix)
        # )
    return flow


def main_incremental() -> Flow:
    with Flow("pull-nda-data-incremental") as flow:
        pass
    return flow


if __name__ == "__main__":
    main_full_refresh().run()
