import glob
import math
import multiprocessing as mp
import os
import shutil
import subprocess

import cairo
import numpy as np
import tqdm

# Set `FFMPEG_PATH` to the local path of your installation of ffmpeg.
# I use the Homebrew version: https://formulae.brew.sh/formula/ffmpeg
FFMPEG_PATH = glob.glob('/usr/local/Cellar/ffmpeg/*/bin/ffmpeg')[-1]

WIDTH = 1920 * 2
HEIGHT = 1080 * 2

RADIUS = HEIGHT // 2
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

FPS = 60

MAX_NUM_DOTS = 32

CUR_DIR = os.path.join(os.path.dirname(__file__))
TMP_DIR = os.path.join(CUR_DIR, 'tmp')
FRAMES_PATTERN = os.path.join(TMP_DIR, 'frame_%d.png')
OUTPUT_PATH = os.path.join(CUR_DIR, 'movie.mov')


def main():
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    cr = cairo.Context(surface)

    # Paint the frame black.
    cr.save()
    cr.set_source_rgb(0, 0, 0)
    cr.set_operator(cairo.OPERATOR_SOURCE)
    cr.paint()
    cr.restore()

    # Set the line width and color.
    cr.set_line_width(1)

    # Calculate the dot positions.
    # dot_positions = [
    #     (
    #         CENTER_X + RADIUS * math.cos(-math.tau / 4 + i * math.tau / num_dots),
    #         CENTER_Y + RADIUS * math.sin(-math.tau / 4 + i * math.tau / num_dots),
    #     )
    #     for i in range(num_dots)
    # ]

    # Draw the dots.
    cr.set_source_rgb(1, 0, 0)
    cr.move_to(0, 0)
    cr.line_to(500, 500)
    surface.write_to_png('test.png')


if __name__ == '__main__':
    main()
