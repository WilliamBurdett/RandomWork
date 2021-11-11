import os
from typing import List

from prefect import Task, task


@task()
def delete_file(file_path: str):
    os.remove(file_path)


@task()
def delete_folder(folder_path: str):
    os.rmdir(folder_path)


@task()
def get_all_file_paths(folder_path: str) -> List[str]:
    file_paths = []
    for root, sub_dirs, files in os.walk(folder_path):
        for file in files:
            file_paths.append(os.path.join(root, file))
    return file_paths


@task()
def get_all_folder_paths(folder_path: str) -> List[str]:
    folder_paths = []
    for root, sub_dirs, files in os.walk(folder_path):
        for sub_dir in sub_dirs:
            folder_paths.append(os.path.join(root, sub_dir))
    return folder_paths


def get_delete_folder_tasks(
    folder_path: str, upstream_task: Task = None, upstream_tasks: List[Task] = None
) -> Task:
    all_file_paths = get_all_file_paths(folder_path)
    if upstream_task is not None:
        all_file_paths.set_upstream(upstream_task)
    if upstream_tasks is not None:
        for upstream_task in upstream_tasks:
            all_file_paths.set_upstream(upstream_task)
    deleting_files = delete_file.map(file_path=all_file_paths)
    all_folder_paths = get_all_folder_paths(folder_path)
    deleting_sub_folders = delete_folder.map(folder_path=all_folder_paths)
    deleting_sub_folders.set_upstream(deleting_files)
    return deleting_sub_folders


def get_file_name(file_path: str) -> str:
    potential_file_names = []
    if "/" in file_path:
        potential_file_names.append(file_path.split("/")[-1])
    if "\\" in file_path:
        potential_file_names.append(file_path.split("\\")[-1])
    potential_file_names.sort(reverse=True)
    return potential_file_names[0]
