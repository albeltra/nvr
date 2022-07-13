import argparse
import glob
from subprocess import run
from pathlib import Path

parser = argparse.ArgumentParser(description='Merges any files that were missed due to down time / restarts')
parser.add_argument('-directory', help='Description for foo argument', required=True)
parser.add_argument('-name', help='Name of stream. Used to make folders and file names', required=True)
parser.add_argument('-extension', help='File extension for streams', required=True)

args = vars(parser.parse_args())

directory = Path(args['directory'])
extension = args['extension']
name = args['name']

cleanup = [x for x in glob.glob(str(directory / f'*/*{extension}')) if len(x) == len(f'{directory / name}{extension}')]
if f'{directory / name}{extension}' in cleanup:
    cleanup.remove(f'{directory / name}{extension}')

for file in cleanup:
    end = file[-(len(extension) + 1)]
    paths = sorted(glob.glob(file.replace(end + extension, end + '*' + extension)))
    if len(paths) > 1 and not run(["mv", f"{file}", f"{file.replace(end + extension, end + '0' + extension)}"]).returncode:
        join_paths = sorted(glob.glob(file.replace(end + extension, end + '*' + extension)))
        if not run(["ffmpeg", "-i",
                    f"concat:{'|'.join(join_paths)}",
                    "-c", "copy", f"{file}"]).returncode:
            run(["rm"] + [x for x in glob.glob(file.replace(end + extension, end + '*' + extension)) if x != file])
        else:
            run(["rm"] + join_paths)
