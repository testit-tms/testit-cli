import glob
import os


class FileWorker:
    @classmethod
    def get_files(cls, path_to_files: str, files_type: str = None) -> list:
        if os.path.isdir(path_to_files):
            return glob.glob(cls.__get_pathname(path_to_files, files_type))

        files = []

        if os.path.isfile(path_to_files):
            files.append(path_to_files)

        return files

    @staticmethod
    def __get_pathname(path_to_files: str, files_type: str):
        if files_type:
            return f"{path_to_files}/*.{files_type}"

        return f"{path_to_files}/*"
