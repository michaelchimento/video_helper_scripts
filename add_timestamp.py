import re
import subprocess
from PIL import Image, ImageDraw, ImageFont
from moviepy.video.io.bindings import PIL_to_npimage
from datetime import datetime
from datetime import timedelta
import moviepy.editor as mp
from os import listdir
from os.path import isfile, isdir, join, splitext, ismount

def add_timestamp(get_frame, t):
    """
    This function returns a 'region' of the current frame.
    The position of this region depends on the time.
    """
    frame = get_frame(t)
    starttime = datetime.strptime(rawstring[1], "%Y-%m-%d_%H%M%S")
    ct = starttime + timedelta(0, t)
    ct_string = ct.strftime('%Y-%m-%d %H:%M:%S')
    im = Image.fromarray(frame)
    draw = ImageDraw.Draw(im)
    draw.text((50, 650), str(ct_string), font=font, fill="yellow")
    return PIL_to_npimage(im)

fontname = "/Library/Fonts/Arial.ttf"
font = ImageFont.FreeTypeFont(fontname, 16)

basepath = "/Volumes/grpLucy/Videos_GRETI/PuzzleVideo/"


directories_to_convert = [join(basepath, d) for d in listdir(basepath) if isdir(join(basepath, d))]
directories_to_convert = sorted(directories_to_convert, key=str.lower, reverse=True)

for d in directories_to_convert:
    files_to_convert = [f for f in listdir(d) if isfile(join(d, f)) and splitext(f)[0][0] != "."]
    files_to_convert = sorted(files_to_convert, key=str.lower, reverse=False)

    #be careful here, will permanently delete files
    for f in files_to_convert:
        rawstring = re.search('(2019.{13})', splitext(f)[0])
        starttime = datetime.strptime(rawstring[1], "%Y-%m-%d_%H%M%S")
        if starttime < datetime(2019, 2, 19, 16, 00, 00) and splitext(f)[0][0:2] != "TS":
            path = '{}{}{}'.format(d, "/", f)
            new_path_name = '{}{}TS_{}'.format(d, "/", f)
            print(path)
            myclip = mp.VideoFileClip(path)
            newclip = myclip.fl(add_timestamp)
            newclip.write_videofile(new_path_name, fps=30)

            delete_command = 'rm -Rf {}{}{}'.format(d, "/", f)
            try:
                print(delete_command)
                output = subprocess.check_output("".join(delete_command), stderr=subprocess.STDOUT, shell=True)
            except CalledProcessError as e:
                print('FAIL:\ncmd:{}\noutput:{}'.format(e.cmd, e.output))


