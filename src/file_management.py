from dataclasses import dataclass
import os
import sys


@dataclass
class FileDirectory:
    name: str # Name of file or folder.
    path: str # Path to file or folder.

    def get_name_raw(self) -> str:
        return os.path.splitext(self.name)[0]
    
    def get_extension(self) -> str:
        return os.path.splitext(self.name)[1]
    
@dataclass
class FileManagement:
    
    @staticmethod
    def assert_path_exists(path: str, hint: str = "") -> None:
        if os.path.exists(path) == False:
            print(f"ERROR: Path does not exist! \"{path}\"")

            if len(hint) != 0:
                print(f"INFO: {hint}")

            sys.exit(1)

    @staticmethod
    def try_create_dir(path: str) -> None:
        if os.path.exists(path) == False:
            print(f"INFO: Creating folder: {path}")
            os.mkdir(path)