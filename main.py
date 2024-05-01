import os
import shutil
from typing import List

class Explorer:
    def __init__(self) -> None:
        self.GLOBAL_FILE_ICONS = {
            "py": "python",
            "txt": "text",
            "png": "image",
            "jpg": "image",
            "jpeg": "image",
            "folder": "folder",
            "default": "default"
        }
        self.GLOBAL_FILE_ICONS_KEYS = list(self.GLOBAL_FILE_ICONS.keys())

        self.current_directory = "~/"

    def f_list_dir(self, dir: str) -> List[str]:
        to_return = []
        
        for file_name in os.listdir(dir):
            file_path = f"{self.current_directory}/{file_name}"
            print(f"{os.path.isdir(file_name)}")
            file_name_split = file_name.split(".")

            file_type = file_name_split[-1]
            file_icon = self.GLOBAL_FILE_ICONS[
                "folder" if os.path.isdir(file_name)
                else file_type
                    if file_type in self.GLOBAL_FILE_ICONS_KEYS
                    else "default"
            ]

            to_return.append(f"{file_icon} {file_name}")
        
        return to_return

    def go(self) -> None:
        pass

def test():
    explorer = Explorer()

    explorer.go()

if __name__ == "__main__":
    test()
