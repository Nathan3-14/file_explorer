import json
import os
import shutil
from typing import List
from rich.console import Console
from rich.tree import Tree
import sys

#* For clarifying importance or function of line(s) of code     *#
#? Giving more information on meaning of parts of data types    ?#
#! Important information that is needed (such as debug info)    !#


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
    def __init__(self, default_dir: str="~/", extra_icons: List[str]=[]) -> None:
        self.initialised = False
        self.current_directory = default_dir
        self.console = Console(record=True)

        self.file_icons = GLOBAL_FILE_ICONS.copy()
        for file_path in extra_icons:
            self.console.print(f"Loading [magenta bold]{file_path}[/magenta bold]")

            if not os.path.exists(file_path):
                self.console.print(f"  [red]Err:[/red] [bright_cyan]Path {file_path} is not a valid icon path[/bright_cyan]")
                return

            data = json.load(open(file_path))
            self.console.print(f"Data read")

            self.file_icons = self.file_icons | data
            self.initialised = True
    
    def error(self, message: str | List[str], start: str="Err:", end_program: bool=False) -> None:
        message_altered = ""
        if isinstance(message, List):
            #* Create multiline error messages *#
            for index, line in enumerate(message):
                message_altered += f"{"  Err:" if index == 0 else "      "}{line}\n"
            message_altered = message_altered.strip()
        else:
            #* Create single line error messages *#
            message_altered = f"  {start} {message}"
        
        self.console.print(message_altered)
        if end_program:
            quit()

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

    def loop(self) -> None:
        if not self.initialised:
            self.error("Explorer is not initialised", end_program=True)
            return
        
        file_tree = Tree(os.path.normpath(f"{os.getcwd()}/{self.current_directory}"))
        for file_display in self.list_dir(self.current_directory):
            file_tree.add(file_display)
        self.console.print(file_tree)

def test():
    explorer = Explorer(default_dir="./test-files", extra_icons=["./icons.json", "a"])

    explorer.loop()

if __name__ == "__main__":
    test()
