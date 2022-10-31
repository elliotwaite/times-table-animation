import glob
from pathlib import Path
import subprocess

FRAMES_DIR = Path(__file__).parent / 'frames'
OUTPUT_PATH = Path(__file__).parent / 'video.mov'
FPS = 60

# Set `FFMPEG_PATH` to the local path of your installation of ffmpeg.
# I use the Homebrew version: https://formulae.brew.sh/formula/ffmpeg
FFMPEG_PATH = glob.glob('/usr/local/Cellar/ffmpeg/*/bin/ffmpeg')[-1]


def main():
    frames_pattern = FRAMES_DIR / 'frame_%d.png'
    args = [
        FFMPEG_PATH,
        '-y',
        '-f',
        'image2',
        '-framerate',
        str(FPS),
        '-i',
        frames_pattern,
        '-c:v',
        'prores_ks',
        '-profile:v',
        '3',
        OUTPUT_PATH,
    ]

    print(f'Writing video...')
    subprocess.run(args)


if __name__ == '__main__':
    main()
