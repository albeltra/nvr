import argparse
import atexit
import glob
import os
from subprocess import run, Popen
import time
from datetime import datetime
from pathlib import Path
from difflib import ndiff
from math import floor
from utils import get_date

parser = argparse.ArgumentParser(description='Description of your program')
parser.add_argument('-url', help='Stream url rtsp', required=True)
parser.add_argument('-name', help='Name of stream. Used to make folders and file names', required=True)
parser.add_argument('-base', help='Base directory to store recordings', required=True)
parser.add_argument('-segment', help='Segment time for ffmpeg', required=True)
parser.add_argument('-extension', help='File extension for streams', required=True)
args = vars(parser.parse_args())

base = Path(args['base'])
url = args['url']
extension = args['extension']
directory = base / args['name']

segment = int(args['segment'])

now = datetime.now()

name = args['name'] + now.replace(minute=int(segment * floor(now.minute / segment)), second=0, microsecond=0).strftime(
    " %Y-%m-%d %H-%M")

run(["python3", "cleanup.py", '-directory', directory, '-name', name, '-extension', extension])

if not os.path.isdir(str(directory)):
    os.makedirs(str(directory))
now = datetime.now()
date = now.strftime("%Y-%m-%d")
directory = base / args['name']

name = args['name'] + now.replace(minute=int(segment * floor(now.minute / segment)), second=0, microsecond=0).strftime(
    " %Y-%m-%d %H-%M")

t = int(segment * (floor(now.minute / segment) + 1) * 60) - int((now.minute * 60) + now.second)

continuous = ["ffmpeg",
              "-i", f"{url}",
              "-vcodec", "copy",
              "-acodec", "copy",
              "-map", "0",
              "-f", "segment",
              "-strftime", "1",
              "-segment_time", f"{segment * 60}",
              "-segment_atclocktime", '1',
              str((directory / '%Y-%m-%d' / args['name'])) + f' %Y-%m-%d %H-%M{extension}'
              ]

date = get_date()
directory = directory / date
os.makedirs(str(directory), exist_ok=True)

if os.path.exists(f"{directory / name}.mkv"):
    file = sorted(glob.glob(str(directory / name) + '*' + extension))[-1]
    end = '1' if file == f"{directory / name}.mkv" else str(int(file[-(len(extension) + 1)]) + 1)
    if not run(["ffmpeg",
                "-t", f"{t}",
                "-i", f"{url}",
                "-vcodec", "copy",
                "-acodec", "copy",
                f"{directory / (name + end + extension)}"]).returncode:
        proc = Popen(continuous)
        if not run(["mv", f"{directory / name}{extension}", f"{directory / name}0{extension}"]).returncode:
            if not run(["ffmpeg",
                        "-i", f"concat:{'|'.join(sorted(glob.glob(str(directory / name) + '*' + extension)))}",
                        "-c", "copy",
                        f"{directory / name}{extension}"]).returncode:
                rm_files = [x for x in glob.glob(str(directory / name) + '*' + extension) if
                            x != f'{directory / name}{extension}']
                run(["rm"] + rm_files)
else:
    if not run(["ffmpeg",
                "-t", f"{t}",
                "-i", f"{url}",
                "-vcodec", "copy",
                "-acodec", "copy",
                f"{directory / (name + extension)}"]).returncode:
        proc = Popen(continuous)

while True:
    if proc.poll() is not None:
        p.kill()
    else:
        time.sleep(5)
