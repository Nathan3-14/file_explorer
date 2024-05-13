from .main import Explorer, get_open_path_list

def test():
    explorer = Explorer(
        default_dir="./test-files",
        extra_icon_paths=["./icons/icons.json"],
        colours=["bright_cyan", "bright_green", "red", "gold1"]
    )

    open_paths = ["./test-files", "./test-files/files", "./test-files/js"]
    open_paths = get_open_path_list(open_paths)

    explorer.loop(open_paths=open_paths)
