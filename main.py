import json
import os
import shutil
from typing import List
from rich.console import Console
from rich.tree import Tree

#* For clarifying importance or function of line(s) of code     *#
#? Giving more information on meaning of parts of data types    ?#
#! Important information that is needed (such as debug info)    !#


def icon(hex: str) -> str:
    return chr(int(hex, 16))

#TODO Create classes for each file type (kinda) TODO#
class Folder:
    def __init__(self, explorer: "Explorer", folder_dir: str) -> None:
        self.explorer = explorer
    
        self.icon = explorer.file_icons["folder"]
        self.folder_dir = folder_dir
        self.folder_name = folder_dir.split("/")[-1]
    
    def tree(self, level: int, open_paths: List[str]=[]) -> Tree:
        to_return = Tree(self.to_string(level))

        if os.path.normpath(self.folder_dir) not in open_paths and ":all:" not in open_paths:
            return to_return

        for child in os.listdir(self.folder_dir):
            if os.path.isdir(os.path.normpath(f"{self.folder_dir}/{child}")):
                child_tree = Folder(self.explorer, os.path.normpath(f"{self.folder_dir}/{child}")).tree(level+1, open_paths=open_paths)
            else:
                child_tree = File(self.explorer, child, self.folder_dir).tree(level)
            to_return.add(child_tree)

        return to_return

    def to_string(self, level: int=-1) -> str:
        colour = self.explorer.colours[level if level < len(self.explorer.colours) else -1]
        return f"[{colour}]{icon(self.icon)}  {self.folder_name}[/{colour}]"


    def __str__(self) -> str:
        return self.to_string()

class File:
    def __init__(self, explorer: "Explorer", file_name: str, root_dir: str) -> None:
        self.explorer = explorer
        self.icons = self.explorer.file_icons
        self.file_path = os.path.normpath(f"{root_dir}/{file_name}")
        self.file_name = file_name
        self.file_type = file_name.split(".")[-1]

    def tree(self, level: int) -> Tree:
        to_return = Tree(self.to_string(level))

        return to_return

    def to_string(self, level: int=-1) -> str:
        icon_keys = list(self.icons.keys())
        icon_key = self.file_type if self.file_type in icon_keys else "default"
        icon_code = self.icons[icon_key]
        icon_character = icon(icon_code)

        colour = self.explorer.colours[level if level < len(self.explorer.colours) else -1]

        return f"[{colour}]{icon_character} {self.file_name}[/{colour}]"


    def __str__(self) -> str:
        return self.to_string()

GLOBAL_FILE_ICONS = {
    "default": "ea7b",
    "folder": "ea83"
}

class Explorer:
    def error(self, message: str | List[str], start: str="Err:", end_program: bool=False) -> None:
        message_altered = ""
        if isinstance(message, List):
            #* Create multiline error messages *#
            for index, line in enumerate(message):
                message_altered += f"{f"  {start}:" if index == 0 else "      "}{line}\n"
            message_altered = message_altered.strip()
        else:
            #* Create single line error messages *#
            message_altered = f"  {start} {message}"
        
        self.console.print(message_altered)
        if end_program:
            quit()

        
    def __init__(self, default_dir: str="~/", extra_icons: List[str]=[], colours: List[str]=["white"]) -> None:
        self.initialised = False
        self.current_directory = default_dir
        self.console = Console(record=True)
        self.colours = colours

        self.file_icons = GLOBAL_FILE_ICONS.copy()
        for file_path in extra_icons:
            # self.console.print(f"Loading [magenta bold]{file_path}[/magenta bold]") #! DEBUG

            if not os.path.exists(file_path):
                self.error(f"[bright_cyan]Path {file_path} is not a valid icon path[/bright_cyan]")
                continue

            data = json.load(open(file_path))

            self.file_icons = self.file_icons | data
            self.file_icon_keys = list(self.file_icons.keys())
            self.initialised = True
    
    def loop(self, open_paths: List[str]=[]) -> None:
        if not self.initialised:
            self.error("Explorer is not initialised", end_program=True)
            return
        
        file_tree = Folder(self, self.current_directory).tree(0, open_paths=open_paths)
        self.console.print(file_tree)

def test():
    explorer = Explorer(default_dir="./test-files", extra_icons=["./icons.json"], colours=["bright_cyan", "bright_green", "red", "gold1"])

    open_paths = ["./test-files", "./test-files/files", "./test-files/js", ":all:"]
    open_paths = [os.path.normpath(f"{path}") for path in open_paths] #! May need to add cwd if change in how folders work

    explorer.loop(open_paths=open_paths)

if __name__ == "__main__":
    test()

#TODO Change folder paths to be global not local TODO# 

