import src as ex

explorer = ex.Explorer(
    default_dir="./",
    extra_icon_paths=["./icons/icons.json"],
    colours=["bright_cyan", "bright_green", "red", "gold1"]
)

open_folders = ["./src", "./test-files"]
explorer.loop(
    ex.get_open_path_list(open_folders)
)
