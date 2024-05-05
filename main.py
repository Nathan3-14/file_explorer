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


#TODO Create classes for each file type (kinda) TODO#
class Folder:
    def __init__(self) -> None:
        pass
        #TODO Do stuff here
    
    def __str__(self) -> str:
        return "f\" folder icon {name}"

class File:
    def __init__(self) -> None:
        pass
        #TODO Do stuff here
        #TODO with extension and name stored seperate
    def __str__(self) -> str:
        return "f\" file icon <from extension> {name}"

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

        
    def __init__(self, default_dir: str="~/", extra_icons: List[str]=[]) -> None:
        self.initialised = False
        self.current_directory = default_dir
        self.console = Console(record=True)

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
    

    def list_dir(self, dir: str) -> List[str]:
        to_return = []
        
        for file_name in os.listdir(dir):
            file_path = f"{self.current_directory}/{file_name}"
            file_name_split = file_name.split(".")

            file_type = file_name_split[-1]

            file_icon = self.file_icons[
                "folder" if os.path.isdir(file_path)
                else file_type
                    if file_type in self.file_icon_keys
                    else "default"
            ]
            file_icon = chr(int(file_icon, 16))

            to_return.append(f"{"#" if os.path.isdir(file_path) else ""}{file_icon} {file_name}")
        
        return to_return

    def create_tree(self, dir: str, name: str, expand_layer: int=1) -> Tree:
        if expand_layer <= 0:
            return Tree("me!!!!")
        expand_layer -= 1
        
        to_return = Tree(dir)

        for file in self.list_dir(dir):
            if file.startswith("#"): #? is a folder
                child = to_return.add(self.create_tree(os.path.normpath(f"{dir}/{file.split(" ")[-1]}"), file))
            child = to_return.add(file)

        return to_return

    def loop(self, expand_layer: int=0) -> None:
        if not self.initialised:
            self.error("Explorer is not initialised", end_program=True)
            return
        
        file_tree = self.create_tree(os.path.normpath(f"{os.getcwd()}/{self.current_directory}"), f"{self.current_directory}", 4)
        self.console.print(file_tree)

def test():
    explorer = Explorer(default_dir="./test-files", extra_icons=["./icons.json"])

    explorer.loop()

if __name__ == "__main__":
    test()
