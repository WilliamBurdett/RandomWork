import json
import os
from datetime import datetime, timedelta
from typing import List
from zipfile import ZipFile, ZIP_DEFLATED

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from prefect import Flow, task, context, unmapped

from utils.file_utils import get_file_name, delete_file, get_delete_folder_tasks
from utils.request_manager import RequestManager
from utils.prefect_utils import flatten_iterable_of_variables

DOWNLOADS_URL = "https://api.fda.gov/download.json"
LOGGER = context.get("logger")

BUCKET_NAME = "will-burdett-interview-2021-11-11"
S3_PREFIX = "/".join(
    [
        "fda",
        "ndc",
        "drugs",
        str(datetime.now().year),
        str(datetime.now().month),
        str(datetime.now().day),
    ]
)
SCRIPT_PATH = os.path.dirname(__file__)

load_dotenv(os.path.join(SCRIPT_PATH, "..", ".env"))

AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")
FDA_API_KEY = os.environ.get("FDA_API_KEY")

RECORDS_PER_FILE = 10_000
MAX_SKIP = 1_000


@task(max_retries=3, retry_delay=timedelta(minutes=1))
def get_file_urls(request_manager: RequestManager) -> List[str]:
    response = request_manager.make_request(DOWNLOADS_URL).json()
    return [
        partition["file"]
        for partition in response["results"]["drug"]["ndc"]["partitions"]
    ]


# Taken from: https://docs.python-requests.org/en/master/user/quickstart/#raw-response-content
@task(max_retries=3, retry_delay=timedelta(minutes=1))
def download_file_from_url(
    file_url: str, folder_path: str, request_manager: RequestManager
) -> str:
    file_name = file_url.split("/")[-1]
    stream = request_manager.stream(file_url)
    full_path = os.path.join(folder_path, file_name)
    with open(full_path, "wb") as fd:
        for chunk in stream.iter_content(chunk_size=128):
            fd.write(chunk)
    return full_path


@task()
def unzip_file(file_path: str, folder_path: str) -> str:
    with ZipFile(file_path, "r") as zip_ref:
        zip_ref.extractall(folder_path)
    return file_path.replace(".zip", "")


# Taken from: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html
@task()
def upload_file(file_path: str):
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
    )
    file_name = get_file_name(file_path)
    s3_key = f"{S3_PREFIX}/{file_name}"
    LOGGER.debug(s3_key)
    try:
        response = s3_client.upload_file(file_path, BUCKET_NAME, s3_key)
    except ClientError as e:
        LOGGER.error(e)
        return False
    return True


@task()
def split_files(file_path: str, key: str):
    with open(file_path, "r") as file:
        full_data = json.loads(file.read())
    file_path = file_path.replace(".", f"_{key}.")
    with open(file_path, "w") as file:
        file.write(json.dumps(full_data[key], indent=2))
    return file_path


@task()
def get_do_full_refresh() -> bool:
    today = datetime.now()
    # Refresh on Sundays
    if today.weekday() == 6:
        return True

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
    )
    files = s3_client.list_objects(Bucket=BUCKET_NAME, Prefix=S3_PREFIX)

    # Contents is missing then full refresh is needed
    return "Contents" not in files


@task()
def create_data_folder() -> str:
    folder_path = os.path.join(SCRIPT_PATH, "raw_data")
    os.makedirs(folder_path, exist_ok=True)
    return folder_path


@task()
def zip_file(file_path: str) -> str:
    zip_file_path = f"{file_path}.zip"
    with ZipFile(zip_file_path, "w", compression=ZIP_DEFLATED) as zip_ref:
        zip_ref.write(file_path)
    return zip_file_path


@task()
def get_minimum_date(do_full_refresh: bool, folder_path: str) -> datetime:
    minimum_date = datetime.now().replace(1000, 1, 1)
    if do_full_refresh:
        return minimum_date

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
    )
    files = s3_client.list_objects(Bucket=BUCKET_NAME, Prefix=S3_PREFIX)
    s3_keys = [file["Key"] for file in files["Contents"]]
    s3_meta_keys = [s3_key for s3_key in s3_keys if "meta.json" in s3_key]
    s3_meta_keys.sort(reverse=True)
    latest_meta_key = s3_meta_keys[0]
    file_name = get_file_name(latest_meta_key)
    file_path = os.path.join(folder_path, file_name)
    s3_client.download_file(Bucket=BUCKET_NAME, Key=latest_meta_key, Filename=file_path)

    with open(file_path, "r") as file:
        meta_data = json.loads(file.read())
    return datetime.strptime(meta_data["max_marketing_start_date"], "%Y-%m-%d")


@task()
def get_maximum_date() -> datetime:
    return datetime.now() - timedelta(days=1)


@task()
def format_url(
    url: str,
    minimum_date: datetime,
    maximum_date: datetime,
    datetime_format: str = "%Y-%m-%d",
) -> str:
    return url.replace("MIN_DATE", minimum_date.strftime(datetime_format)).replace(
        "MAX_DATE", maximum_date.strftime(datetime_format)
    )


@task(max_retries=3, retry_delay=timedelta(minutes=1))
def get_chunks(url: str, request_manager: RequestManager) -> List[int]:
    formatted_url = url.replace("SKIP", str(0))
    url.replace(str(MAX_SKIP), "1")
    response = request_manager.make_request(formatted_url).json()
    total = response["meta"]["results"]["total"]
    chunks = [0]

    for multiplier in range(round(total / RECORDS_PER_FILE)):
        chunks.append(multiplier + 1)
    return chunks


@task(max_retries=3, retry_delay=timedelta(minutes=1))
def save_chunk_to_file(
    multiplier: int, url: str, folder_path: str, request_manager: RequestManager
) -> str:
    LOGGER.info(f"multiplier {multiplier}")
    all_results = []
    for skip in range(
        multiplier * RECORDS_PER_FILE, (multiplier + 1) * RECORDS_PER_FILE, MAX_SKIP
    ):
        url_with_skip = url.replace("SKIP", str(skip))
        response = request_manager.make_request(url_with_skip).json()
        results = response["results"]
        all_results.extend(results)

    file_path = os.path.join(folder_path, f"results_{multiplier}.json")
    with open(file_path, "w") as file:
        file.write(json.dumps(all_results))
    return file_path


@task()
def get_max_marketing_start_date(file_path: str) -> str:
    with open(file_path, "r") as file:
        results = json.loads(file.read())
    max_marketing_start_date = "10000101"
    for result in results:
        current_marketing_start_date = result.get("marketing_start_date")
        if current_marketing_start_date is not None:
            if current_marketing_start_date > max_marketing_start_date:
                max_marketing_start_date = current_marketing_start_date
    return max_marketing_start_date


@task()
def save_max_marketing_start_dates(
    max_marketing_start_dates: List[str], folder_path: str
) -> str:
    max_marketing = max_marketing_start_dates.copy()
    max_marketing.sort(reverse=True)
    file_name = "max_marketing_start_date.json"
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, "w") as file:
        file.write(json.dumps({"max_marketing_start_date": max_marketing[0]}))
    return file_path


def main_full_refresh() -> Flow:
    request_manager = RequestManager(LOGGER)
    with Flow("pull-nda-data-refresh") as flow:
        folder_path = create_data_folder()
        file_urls = get_file_urls(request_manager)
        original_zipped_file_paths = download_file_from_url.map(
            file_url=file_urls,
            folder_path=unmapped(folder_path),
            request_manager=unmapped(request_manager),
        )
        unzipped_file_paths = unzip_file.map(
            file_path=original_zipped_file_paths, folder_path=unmapped(folder_path)
        )
        meta_file_paths = split_files.map(
            file_path=unzipped_file_paths, key=unmapped("meta")
        )
        meta_zipped_file_paths = zip_file.map(file_path=meta_file_paths)
        meta_uploading_files = upload_file.map(
            file_path=meta_zipped_file_paths,
        )

        results_file_paths = split_files.map(
            file_path=unzipped_file_paths, key=unmapped("results")
        )
        results_zipped_file_paths = zip_file.map(file_path=results_file_paths)
        results_uploading_files = upload_file.map(
            file_path=results_zipped_file_paths,
        )
        max_marketing_start_dates = get_max_marketing_start_date.map(
            file_path=results_file_paths
        )
        max_marketing_file_path = save_max_marketing_start_dates(
            max_marketing_start_dates=max_marketing_start_dates, folder_path=folder_path
        )

        uploading_max_marketing = upload_file(file_path=max_marketing_file_path)

        cleaning_up = get_delete_folder_tasks(
            folder_path=folder_path,
            upstream_tasks=[
                meta_uploading_files,
                results_uploading_files,
                uploading_max_marketing,
            ],
        )
    return flow


def main_incremental() -> Flow:
    url = (
        f"https://api.fda.gov/drug/ndc.json"
        f"?api_key={FDA_API_KEY}"
        f"&search=marketing_start_date:[MIN_DATE+TO+MAX_DATE]"
        f"&sort=marketing_start_date:asc"
        f"&limit={MAX_SKIP}"
        f"&skip=SKIP"
    )
    params = [
        ("api_key", FDA_API_KEY),
        ("search", "marketing_start_date:[MIN_DATE+TO+MAX_DATE]"),
        ("sort", "marketing_start_date:asc"),
        ("limit", MAX_SKIP),
        ("skip", 0),
    ]
    with Flow("pull-nda-data-incremental") as flow:
        request_manager = RequestManager(LOGGER)
        folder_path = create_data_folder()
        do_full_refresh = get_do_full_refresh()
        minimum_date = get_minimum_date(do_full_refresh, folder_path)
        maximum_date = get_maximum_date()
        formatted_url = format_url(url, minimum_date, maximum_date)
        chunks = get_chunks(formatted_url, request_manager)
        file_paths = save_chunk_to_file.map(
            multiplier=chunks,
            url=unmapped(formatted_url),
            folder_path=unmapped(folder_path),
            request_manager=unmapped(request_manager),
        )
    return flow


if __name__ == "__main__":
    main_full_refresh().run()
