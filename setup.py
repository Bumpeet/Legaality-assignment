from pathlib import Path
import shutil
import regex


def delete_create_dirs(src_path, dest_path):
    # removing the dest_path and creating it again
    shutil.rmtree(dest_path, ignore_errors=True)
    Path.mkdir(dest_path, exist_ok=True)
    assert Path.exists(src_path)

    #
    raw_data_path = Path(dest_path.joinpath('raw'))
    raw2_data_path = Path(dest_path.joinpath('raw2'))
    Path.mkdir(raw2_data_path)

    #unzipping the downloaded zip file
    shutil.unpack_archive(src_path, raw_data_path, format="zip")

    return raw_data_path, raw2_data_path


def main(src_path: Path, dest_path: Path):
    raw_data_path, raw2_data_path = delete_create_dirs(src_path, dest_path)
    print("---- successfully deleted and created the raw data path ----")

    #iterating over all the person folders from different datasets into a
    #single place and renaming all the persons
    for i, fldr_path in enumerate(raw_data_path.glob('*/*/*')):
      dest_fldr_path = raw2_data_path.joinpath(f'{i+1}')


      if fldr_path.parents[0].stem=='CEDAR':
        shutil.move(fldr_path,dest_fldr_path)
        for j, img_path in enumerate(dest_fldr_path.glob('*.png')):
          stem = img_path.stem
          split = stem.split('_')
          num = int(split[2])
          if split[0]=='forgeries':
            if num<=10:
              img_path.rename(img_path.parent.joinpath(f'{i+1}-F-{num:02d}.tif'))
            else:
              img_path.unlink()

          else:
            if num<=10:
              img_path.rename(img_path.parent.joinpath(f'{i+1}-G-{num:02d}.tif'))
            else:
              img_path.unlink()


      elif fldr_path.parents[0].stem[:8]=='BHSig260':
        shutil.move(fldr_path,dest_fldr_path)
        for j, img_path in enumerate(dest_fldr_path.glob('*.tif')):
          stem = img_path.stem
          split = stem.split('-')
          num = int(split[4])
          if split[3]=='F':
            if int(split[4])<=10:
              img_path.rename(img_path.parent.joinpath(f'{i+1}-F-{num:02d}.tif'))
            else:
              img_path.unlink()
          else:
            if int(split[4])<=10:
              img_path.rename(img_path.parent.joinpath(f'{i+1}-G-{num:02d}.tif'))
            else:
              img_path.unlink()

      print(f'--- renamed and moved the {fldr_path} --')

    print("--- successfully moved and renamed all the folders---")


if __name__=='__main__':

  main(Path('handwritten-signature-datasets.zip'),
      Path('dataset'))