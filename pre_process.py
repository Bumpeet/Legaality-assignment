import glob
import random
import itertools
from sklearn.model_selection import train_test_split
from typing import List, Tuple
import csv
import os

def make_partition(
    signers: List[int],
    pair_genuine_genuine: List[Tuple[int, int]],
    pair_genuine_forged: List[Tuple[int, int]],
):
    samples = []
    for signer_id in signers:
        sub_pair_genuine_forged = random.sample(pair_genuine_forged, len(pair_genuine_genuine))
        genuine_genuine = list(itertools.zip_longest(pair_genuine_genuine, [], fillvalue=1)) # y = 1
        genuine_genuine = list(map(lambda sample: (signer_id, *sample[0], sample[1]), genuine_genuine))
        samples.extend(genuine_genuine)
        genuine_forged = list(itertools.zip_longest(sub_pair_genuine_forged, [], fillvalue=0)) # y = 0
        genuine_forged = list(map(lambda sample: (signer_id, *sample[0], sample[1]), genuine_forged))
        samples.extend(genuine_forged)
    return samples

def write_csv(file_path, samples):
    with open(file_path, 'wt') as f:
        writer = csv.writer(f)
        writer.writerows(samples)


def prepare_dataset(M: int, K: int, random_state=0, data_dir='data/BHSig260/Bengali'):
    def get_path(row):
        writer_id, x1, x2, y = row
        if y == 1:
            x1 = os.path.join(data_dir, f'{writer_id}', f'{writer_id}-G-{x1:02d}.tif')
            x2 = os.path.join(data_dir, f'{writer_id}', f'{writer_id}-G-{x2:02d}.tif')
        else:
            x1 = os.path.join(data_dir, f'{writer_id}', f'{writer_id}-G-{x1:02d}.tif')
            x2 = os.path.join(data_dir, f'{writer_id}', f'{writer_id}-F-{x2:02d}.tif')
        return x1, x2, y # drop writer_id

    random.seed(random_state)
    signers = list(range(1, K+1))
    num_genuine_sign = 15
    num_forged_sign = 15

    train_signers, test_signers = train_test_split(signers, test_size=K-M)
    pair_genuine_genuine = list(itertools.combinations(range(1, num_genuine_sign+1), 2))
    pair_genuine_forged = list(itertools.product(range(1, num_genuine_sign+1), range(1, num_forged_sign+1)))

    train_samples = make_partition(train_signers, pair_genuine_genuine, pair_genuine_forged)
    train_samples = list(map(get_path, train_samples))
    write_csv(os.path.join(data_dir, 'train.csv'), train_samples)
    test_samples = make_partition(test_signers, pair_genuine_genuine, pair_genuine_forged)
    test_samples = list(map(get_path, test_samples))
    write_csv(os.path.join(data_dir, 'test.csv'), test_samples)


print('Preparing dataset..')
prepare_dataset(M=250, K=315, data_dir='dataset/raw2')
print('Done')