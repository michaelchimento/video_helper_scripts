Python scripts that help with automating tasks related to video analysis of aviary data.
Individual scripts should be edited to contain proper paths to videos
WARNING: some scripts will delete files without prompting. Please check file paths before running any script, and backup if necessary.
Install ffmpeg before using these.

1. add_timestamp: to process videos without a timestamp. adds timestamp based on values in filename. ensure timestamp is readable and in the correct position before use. uses moviepy and PIL
2. add_timestamp_threaded: same as above, but uses multithreading to speed up processing.
3. convert2mp4: uses ffmpeg to convert .h264 files to mp4. check quality of files before use.
4. delete_night_videos: remove videos between set hours of the day. set hours before use.
5. fix_fps: probably the most idiosyncratic, but can be used to alter the frames per second of mp4 files which were incorrectly rendered at the wrong fps from .h264 files.
