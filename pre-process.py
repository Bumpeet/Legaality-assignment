from pathlib import Path
import shutil
from argparse import ArgumentParser

def make_label_dirs(dest_path):
    labels = ['forgery', 'genuine']
    list(map(lambda x: Path.mkdir(dest_path.joinpath(x), exist_ok=True), labels))


def main(src_path: Path, dest_path: Path):
    Path.mkdir(dest_path, exist_ok=True)
    assert Path.exists(src_path)
    # shutil.unpack_archive(src_path,'./dataset/raw',format="zip")
    raw_data_path = Path(dest_path.joinpath('raw'))
    make_label_dirs(dest_path)

    for i, img_path in enumerate(raw_data_path.glob('*/*/*/*.tif')):
        if 'F' in img_path.stem:
            shutil.move(img_path,dest_path.joinpath('forgery'))
        elif 'G' in img_path.stem:
            shutil.move(img_path, dest_path.joinpath('genuine'))

    shutil.rmtree(raw_data_path)


def args():
    parser = ArgumentParser()
    parser.add_argument('--src_path', default='./handwritten-signature-datasets.zip', type=str)
    parser.add_argument('--dest_path', default='./dataset', type=str)
    return parser.parse_args()


if __name__ == '__main__':
    arguments = args()
    main(Path(arguments.src_path), Path(arguments.dest_path))
