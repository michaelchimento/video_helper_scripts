import subprocess
import re
from datetime import datetime
from os import listdir
from os.path import isfile, isdir, join, splitext
from subprocess import CalledProcessError

basepath = "/Volumes/grpLucy/Videos_GRETI/"

directories_to_convert = [join(basepath,d) for d in listdir(basepath) if isdir(join(basepath, d))]
directories_to_convert = sorted(directories_to_convert, key=str.lower, reverse=True)

for d in directories_to_convert:
    files_to_convert = [f for f in listdir(d) if isfile(join(d, f))]

    #be careful here, will permanently delete files
    for f in files_to_convert:
        rawstring = re.search('(2019.{13})', splitext(f)[0])
        starttime = datetime.strptime(rawstring[1], "%Y-%m-%d_%H%M%S")
        if starttime.hour == 18 and starttime.minute > 10:
            delete_command = 'rm -Rf {}{}{}'.format(d, "/", f)
            try:
                print(starttime.hour)
                output = subprocess.check_output("".join(delete_command), stderr=subprocess.STDOUT, shell=True)
            except CalledProcessError as e:
                print('FAIL:\ncmd:{}\noutput:{}'.format(e.cmd, e.output))
