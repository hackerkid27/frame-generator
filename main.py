# An XML Generator for the Virtual Conductor Android App by Jude Pellegrin
# By Jude Pellegrin
# December 16, 2024


from math import sqrt


def main() -> None:
    frame_density = get_frame_density()
    marker_positions = get_marker_pos(frame_density)
    ball_size = get_ball_size()
    offset_coordinates = convert_to_offset(marker_positions, ball_size)
    generate_XML(offset_coordinates)
    print('You\'r frames are done. Check the "frames" directory of this program\'s directory.')
    generate_animation_xml(frame_density)


def get_frame_density() -> int:
    return int(input("How many frames per cycle do you want available?\n(A Multiple of 4 is HIGHLY preferred.) "))


def get_marker_pos(frame_num) -> list:
    intervals = 1/frame_num
    working_frame = 1
    xy_coordinates = []
    for frame in range(frame_num):
        z_pos = intervals*working_frame-intervals
        if z_pos < 0.25:
            x_pos = 0
            y_pos = func_1_y(z_pos)
        elif z_pos >= 0.25 and z_pos < 0.5:
            x_pos = func_2_x(z_pos)
            y_pos = func_2_y(z_pos)
        elif z_pos >= 0.5 and z_pos < 0.75:
            x_pos = func_3_x(z_pos)
            y_pos = func_3_y(z_pos)
        else:
            x_pos = func_4_x(z_pos)
            y_pos = func_4_y(z_pos)
        xy_coordinates.append([x_pos, y_pos])
        working_frame += 1
    return xy_coordinates


def get_ball_size() -> int:
    return int(input("What is the size of the indicator that you would like? "))


def convert_to_offset(coordinates, ball_diameter) -> list:
    offsets = []
    for pair in coordinates:
        left_offset = 125*pair[0]+500-ball_diameter
        right_offset = -125*pair[0]+500-ball_diameter
        bottom_offset = 125*pair[1]+500-ball_diameter
        top_offset = -125*pair[1]+500-ball_diameter
        offsets.append([left_offset, right_offset, bottom_offset, top_offset])
    return offsets        


def generate_XML(indicator_pos) -> None:
    for index, item in enumerate(indicator_pos):
        with open(f"output/frame_4_{index}.xml", "w") as file:
            file.write(f'''<?xml version="1.0" encoding="utf-8"?>
            <layer-list xmlns:android="http://schemas.android.com/apk/res/android">
                  \t<item
                \t\tandroid:drawable="@drawable/pos_indicator"
                \t\tandroid:id="@+id/animation_pos_indicator"
                \t\tandroid:top="{item[3]}dp"
                \t\tandroid:bottom="{item[2]}dp"
                \t\tandroid:left="{item[0]}dp"
                \t\tandroid:right="{item[1]}dp"/>
            </layer-list>''')

def generate_animation_xml(frame_density) -> None:
    with open("output/conductor_animation.xml", "w") as file:
        file.write(f'''<?xml version="1.0" encoding="utf-8"?>
        <animation-list xmlns:android="http://schemas.android.com/apk/res/android" android:oneshot="false">''')
        for i in range(frame_density):
            file.write(f'''<item android:drawable="@drawable/frame_4_{i}" android:duration="50"/>\n''')
        file.write("</animation-list>")

def func_1_y(z) -> float:
    return -32*z+4


def func_2_x(z) -> float:
    possible_x = -16*z+2+sqrt(-4096*z**2+3072*z-448)/4
    if possible_x <= -4 or possible_x >= 0:
        return -16*z+2-sqrt(-4096*z**2+3072*z-448)/4
    else:
        return possible_x


def func_2_y(z) -> float:
    possible_y = 16*z-10+sqrt(-4096*z**2+3072*z-448)/4
    if possible_y <= -4 or possible_y >= 0:
        return 16*z-10-sqrt(-4096*z**2+3072*z-448)/4
    else:
        return possible_y


def func_3_x(z) -> float:
    return 32*(z-0.625)


def func_3_y(z) -> float:
    possible_y = -6.928203+sqrt(64-1024*(z-0.625)**2)
    if possible_y <= 0:
        return -6.928203-sqrt(64-1024*(z-0.625)**2)
    else:
        return possible_y


def func_4_x(z) -> float:
    possible_x = -16*z+18+2*sqrt(-64*(z**2)+112*z-47)
    if possible_x <= 0 or possible_x >= 4:
        return -16*z+18-2*sqrt(-64*(z**2)+112*z-47)
    else:
        return possible_x        


def func_4_y(z) -> float:
    possible_y = 16*z-10+2*sqrt(-64*(z**2)+112*z-47)
    if possible_y <= 0 or possible_y >= 4:
        return 16*z-10-2*sqrt(-64*(z**2)+112*z-47)
    else:
        return possible_y
    

if __name__ == "__main__":
    main()