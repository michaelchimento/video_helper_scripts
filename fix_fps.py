import subprocess
from os import listdir
from os.path import isfile, isdir, join, splitext
from subprocess import CalledProcessError

#open 'smb://mchimento:Ice18cream!@r-zfssvr01.top.orn.mpg.de' run this in terminal first to mount smb


basepath = "/Volumes/grpLucy/"
dirs = ["Videos_GRETI/WormptVideo/Wormpt_P4_C7_2019-02-11_18",
        "Videos_GRETI/WormptVideo/Wormpt_P5_C9_2019-02-14_13",
        "Videos_GRETI/WormptVideo/Wormpt_P6_D1_2019-02-12_14"]

'''
        "Videos_GRETI/WormptVideo/Wormpt_P3_C5_2019-02-12_15"
        "Videos_GRETI/WormptVideo/Wormpt_P4_C7_2019-02-11_18",
        "Videos_GRETI/WormptVideo/Wormpt_P5_C9_2019-02-14_13",
        "Videos_GRETI/WormptVideo/Wormpt_P6_D1_2019-02-12_14"]
'''


directories_to_convert = [join(basepath,d) for d in dirs]
directories_to_convert = sorted(directories_to_convert, key=str.lower, reverse=True)

for d in directories_to_convert:
    files_to_convert = [f for f in listdir(d) if isfile(join(d, f))]

    for f in files_to_convert:
        command1 = 'MP4Box -single 1 -raw 1 {}{}{}'.format(d, "/", f)
        print(command1)
        try:
            output = subprocess.check_output("".join(command1), stderr=subprocess.STDOUT, shell=True)
        except CalledProcessError as e:
            print('FAIL:\ncmd:{}\noutput:{}'.format(e.cmd, e.output))

        command2 = 'MP4Box -add {}{}{}{}.h264:fps=36 -new {}{}{}.mp4'.format(d, "/", splitext(f)[0], "_track1", d, "/", splitext(f)[0])
        print(command2)
        try:
            output = subprocess.check_output("".join(command2), stderr=subprocess.STDOUT, shell=True)
        except CalledProcessError as e:
            print('FAIL:\ncmd:{}\noutput:{}'.format(e.cmd, e.output))

    files_to_convert = [f for f in listdir(d) if isfile(join(d, f))]
    #be careful here, will permanently delete files
    for f in files_to_convert:

        if splitext(f)[0][-6:] == "track1":
            print(splitext(f)[0][-6:])
            delete_command = 'rm -Rf {}{}{}'.format(d, "/", f)
            try:
                print(delete_command)
                output = subprocess.check_output("".join(delete_command), stderr=subprocess.STDOUT, shell=True)
            except CalledProcessError as e:
                print('FAIL:\ncmd:{}\noutput:{}'.format(e.cmd, e.output))

