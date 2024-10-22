
# creating a GUI without tkinter to clown on ted
gui_row = '_'
gui_column = '|'
gui_width = 80

def draw_gui (lines, left_paddings, up_padding, down_padding):
    print(" OCRTUNES.EXE " + '#' * (gui_width-21) + "[-][+][X]")

    for _ in range(up_padding):
        print(gui_column + ' '*gui_width + gui_column)

    for index, line in enumerate(lines):
        print(gui_column + ' '*left_paddings[index] + line + ' '*(gui_width - len(line) - left_paddings[index]) + gui_column)
    
    for _ in range(down_padding):
        print(gui_column + ' '*gui_width + gui_column)
    
    print(gui_column + gui_row * (gui_width) + gui_column)

# <centre>, <left>
def draw_gui_aligned (lines, left_aligned_margin):
    # parse lines
    paddings = []
    max_length = -1
    visited_lines = 0

    out_lines = []

    for line in lines:
        if line == '<centre>':
            # set alignment to centre
            # flush any visited lines
            for _ in range(visited_lines):
                paddings.append((gui_width - max_length) // 2)
            max_length = -1
            visited_lines = 0
        elif line == '<left>':
            # set alignment to left
            # flush any visited lines
            for _ in range(visited_lines):
                paddings.append(left_aligned_margin)
            max_length = -1
            visited_lines = 0
        else: 
            visited_lines += 1
            out_lines.append(line)
            if (len(line) > max_length):
                max_length = len(line)

    draw_gui(out_lines, paddings, 1, 1)