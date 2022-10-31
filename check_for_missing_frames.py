from pathlib import Path

FRAMES_DIR = Path(__file__).parent / 'frames'


def main():
    if not FRAMES_DIR.exists():
        print(f'The frames directory does not exists: {FRAMES_DIR}')
        return

    num_frames = len([None for path in FRAMES_DIR.iterdir() if path.is_file()])
    has_missing_frame = False
    for frame_num in range(num_frames):
        frame_path = FRAMES_DIR / f'frame_{frame_num}.png'
        if not frame_path.exists():
            print('Missing frame: {frame_num}')
            has_missing_frame = True

    if not has_missing_frame:
        print(f'All {num_frames} frames were found.')


if __name__ == '__main__':
    main()
