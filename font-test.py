from fontTools.ttLib import TTFont

def list_nerd_icons(font_path):
    with TTFont(font_path) as font:
        for table in font['cmap'].tables:
            if table.isUnicode():
                for codepoint, glyph_name in table.cmap.items():
                    if glyph_name.startswith("folder-"):
                        print(f"Icon: {glyph_name}, Codepoint: {hex(codepoint)}")
                        # print(f"Icon: {glyph_name}, Codepoint: \u{str(hex(codepoint))}")

# Replace 'path_to_your_nerd_font.ttf' with the path to your Nerd Font TTF file
font_path = './hack.ttf'
list_nerd_icons(font_path)
print("\U000F19F9")

