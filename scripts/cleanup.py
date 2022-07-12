import argparse
import glob
from subprocess import run
from pathlib import Path

parser = argparse.ArgumentParser(description='Merges any files that were missed due to down time / restarts')
parser.add_argument('-directory', help='Description for foo argument', required=True)
parser.add_argument('-extension', help='Description for bar argument', required=True)
parser.add_argument('-name', help='Description for bar argument', required=True)

args = vars(parser.parse_args())

directory = Path(args['directory'])
extension = args['extension']
name = args['name']

cleanup = glob.glob(str(directory / f'*-0{extension}'))
if f'{directory / name}{extension}' in cleanup:
    cleanup.remove(f'{directory / name}{extension}')

for file in cleanup:
    paths = sorted(glob.glob(file.replace('-0.', '-0*.')))
    if len(paths) > 1 and not run(["mv", f"{file}", f"{file.replace('-0.', '-00.')}"]).returncode:
        join_paths = sorted(glob.glob(file.replace('-0.', '-0*.')))
        if not run(["ffmpeg", "-i", f"concat:{'|'.join(join_paths)}", "-c", "copy", f"{file}"]).returncode:
            run(["rm"] +  [x for x in glob.glob(file.replace('-0.', '-0*.')) if x != file])
        else:
            run(["rm"] + join_paths)
