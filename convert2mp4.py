import tempfile
from smb.SMBConnection import SMBConnection
import subprocess
from os import listdir
from os.path import isfile, isdir, join, splitext
from subprocess import CalledProcessError

#open 'smb://mchimento:#########@r-zfssvr01.top.orn.mpg.de' run this in terminal first to mount smb


basepath = "/Volumes/grpLucy/Videos_GRETI/"

directories_to_convert = [join(basepath,d) for d in listdir(basepath) if isdir(join(basepath, d))]
directories_to_convert = sorted(directories_to_convert, key=str.lower, reverse=True)

for d in directories_to_convert:
    files_to_convert = [f for f in listdir(d) if isfile(join(d, f))]

    for f in files_to_convert:
        command = 'MP4Box -add {}{}{}:fps=30 -new {}{}{}.mp4'.format(d, "/", f, d, "/", splitext(f)[0])
        if splitext(f)[1] == ".h264":
            print(f)
            try:
                output = subprocess.check_output("".join(command), stderr=subprocess.STDOUT, shell=True)
            except CalledProcessError as e:
                print('FAIL:\ncmd:{}\noutput:{}'.format(e.cmd, e.output))

    #be careful here, will permanently delete files
    for f in files_to_convert:
        delete_command = 'rm -Rf {}{}{}'.format(d, "/", f)
        if splitext(f)[1] == ".h264":
            try:
                print(delete_command)
                output = subprocess.check_output("".join(delete_command), stderr=subprocess.STDOUT, shell=True)
            except CalledProcessError as e:
                print('FAIL:\ncmd:{}\noutput:{}'.format(e.cmd, e.output))
