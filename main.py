import os
import shutil
from typing import List
from rich.console import Console
from rich.tree import Tree

GLOBAL_FILE_ICONS = {
            "py": "python",
            "txt": "text",
            "png": "image",
            "jpg": "image",
            "jpeg": "image",
            "folder": "folder",
            "default": "default"
}
GLOBAL_FILE_ICONS_KEYS = list(GLOBAL_FILE_ICONS.keys())

class Explorer:
    def __init__(self) -> None:
        self.current_directory = "."
        self.console = Console()

    def list_dir(self, dir: str) -> List[str]:
        to_return = []
        
        for file_name in os.listdir(dir):
            file_path = f"{self.current_directory}/{file_name}"
            print(f"{os.path.isdir(file_path)}")
            file_name_split = file_name.split(".")

            file_type = file_name_split[-1]
            file_icon = GLOBAL_FILE_ICONS[
                "folder" if os.path.isdir(file_name)
                else file_type
                    if file_type in GLOBAL_FILE_ICONS_KEYS
                    else "default"
            ]

            to_return.append(f"{file_icon} {file_name}")
        
        return to_return

    def init(self) -> None:
        file_tree = Tree(f"{self.current_directory}")
        for file_display in self.list_dir(self.current_directory):
            file_tree.add(file_display)
        self.console.print(file_tree)
    
    def loop(self) -> None:
        pass

def test():
    explorer = Explorer()

    explorer.init()

if __name__ == "__main__":
    test()
