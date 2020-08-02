import os

CUR_DIR = os.path.join(os.path.dirname(__file__))
OUTPUT_DIR = os.path.join(CUR_DIR, 'output')


def main():
    num_frames = len(
        [path for path in os.listdir(OUTPUT_DIR) if os.path.isfile(os.path.join(OUTPUT_DIR, path))]
    )
    has_missing_frame = False
    for frame_num in range(num_frames):
        frame_path = os.path.join(OUTPUT_DIR, f'frame_{frame_num}.png')
        if not os.path.exists(frame_path):
            print('Missing frame: {frame_num}')
            has_missing_frame = True

    if not has_missing_frame:
        print(f'All {num_frames} were found.')


if __name__ == '__main__':
    main()
