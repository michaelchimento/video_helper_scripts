import threading
import re
import subprocess
from PIL import Image, ImageDraw, ImageFont
from moviepy.video.io.bindings import PIL_to_npimage
from datetime import datetime
from datetime import timedelta
import moviepy.editor as mp
from os import listdir
from os.path import isfile, isdir, join, splitext, ismount


basepath1 = "/Volumes/grpLucy/Videos_GRETI/PuzzleVideo/Puzzle_P4/"
basepath2 = "/Volumes/grpLucy/Videos_GRETI/PuzzleVideo/Puzzle_P5/"
fontname = "/Library/Fonts/Arial.ttf"
font = ImageFont.FreeTypeFont(fontname, 16)


class myThread(threading.Thread):
    def __init__(self, threadID, name, basepath):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.basepath = basepath
        self.directories_to_convert = [join(self.basepath, d) for d in listdir(self.basepath) if
                                       isdir(join(self.basepath, d))]
        self.directories_to_convert = sorted(self.directories_to_convert, key=str.lower, reverse=False)

    def thread_action(self):
        for d in self.directories_to_convert:
            files_to_convert = [f for f in listdir(d) if isfile(join(d, f)) and splitext(f)[0][0] != "."]
            files_to_convert = sorted(files_to_convert, key=str.lower, reverse=False)

            # be careful here, will permanently delete files
            for f in files_to_convert:
                self.rawstring = re.search('(2019.{13})', splitext(f)[0])
                starttime = datetime.strptime(self.rawstring[1], "%Y-%m-%d_%H%M%S")
                if starttime < datetime(2019, 2, 19, 16, 00, 00) and splitext(f)[0][0:2] != "TS":
                    path = '{}{}{}'.format(d, "/", f)
                    new_path_name = '{}{}TS_{}'.format(d, "/", f)
                    print(path)
                    myclip = mp.VideoFileClip(path)
                    newclip = myclip.fl(self.add_timestamp)
                    newclip.write_videofile(new_path_name, fps=30, codec="libx264", preset="superfast", threads=2,
                                            bitrate="9000k", audio=False)

                    delete_command = 'rm -Rf {}{}{}'.format(d, "/", f)
                    try:
                        print(delete_command)
                        output = subprocess.check_output("".join(delete_command), stderr=subprocess.STDOUT, shell=True)
                    except CalledProcessError as e:
                        print('FAIL:\ncmd:{}\noutput:{}'.format(e.cmd, e.output))

    def run(self):
        print("Starting " + self.name)
        for x in range(1):
            self.thread_action()
        print("Exiting " + self.name)


    def add_timestamp(self, get_frame, t):
        """
        This function returns a 'region' of the current frame.
        The position of this region depends on the time.
        """
        frame = get_frame(t)
        starttime = datetime.strptime(self.rawstring[1], "%Y-%m-%d_%H%M%S")
        ct = starttime + timedelta(0, t)
        ct_string = ct.strftime('%Y-%m-%d %H:%M:%S')
        im = Image.fromarray(frame)
        draw = ImageDraw.Draw(im)
        draw.text((50, 650), str(ct_string), font=font, fill="yellow")
        return PIL_to_npimage(im)


# Create new threads
thread1 = myThread(1, "Thread-1", basepath1)
thread2 = myThread(2, "Thread-2", basepath2)

# Start new Threads
thread1.start()
thread2.start()

print("Exiting Main Thread")
