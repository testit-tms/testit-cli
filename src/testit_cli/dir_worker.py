import os

from pathlib import PurePath


class DirWorker:
    @classmethod
    def create_dir(cls, path_to_file: str) -> None:
        dir_names = cls.__split_path_to_dir_names(path_to_file)
        path = "."

        for dir_name in dir_names:
            path = os.path.join(path, dir_name)
            if not cls.__check_dir(path):
                cls.__create_dir(path)

    @staticmethod
    def __check_dir(path_to_dir: str) -> bool:
        return os.path.exists(path_to_dir) and os.path.isdir(path_to_dir)

    @staticmethod
    def __split_path_to_dir_names(path_to_dir: str) -> tuple:
        return PurePath(path_to_dir).parts[:-1]

    @staticmethod
    def __create_dir(path_to_dir: str) -> None:
        os.mkdir(path_to_dir)
