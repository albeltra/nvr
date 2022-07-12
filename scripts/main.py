import atexit
import glob
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path
from os import environ

from utils import convert_size

now = datetime.now()

max_size = float(environ.get('MAX_SIZE', 1))
housekeep_enabled = environ.get('T', True)
segment = int(environ.get('VIDEO_SEGMENT_TIME', 30))
extension = '.' + environ.get('VIDEO_FORMAT', 'mkv')
base = environ.get("RECORDING_DIR", '/recordings')

print(os.path.dirname(os.path.realpath(__file__)))

with open('streams.txt') as file:
    lines = file.readlines()
    lines = [line.rstrip().split(';') for line in lines]
folders = [str(Path(base) / line[1]) for line in lines]

procs = [subprocess.Popen(["python3", "record.py", '-url', str(line[0]), '-name', str(line[1]), '-base', str(base),  '-segment', str(segment), '-extension', extension]) for line in lines]
def exit_handler(P=procs):
    for p in P:
        p.kill()
atexit.register(exit_handler)

while True:
    for i, p in enumerate(procs):
        if p.poll() is None:
            continue
        else:
            subprocess.Popen(["python3", "record.py", '-url', str(lines[i][0]), '-name', str(lines[0][1]), '-base', str(base), '-segment', str(segment), '-extension', extension])
    time.sleep(int(60 * segment) + 10) 
    if housekeep_enabled:
        files = [glob.glob(folder + '/*') for folder in folders]
        oldest = [min(cur_files, key=os.path.getctime) for cur_files in files]
        total_file = convert_size(sum([sum([os.path.getsize(f) for f in cur_files]) for cur_files in files]))
        if total_file > max_size:
            for file in oldest:
                os.remove(file)
