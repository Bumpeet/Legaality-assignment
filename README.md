# Legaality-assignment

## Dataset preparation
- Dataset used in this problem is from this [ink](https://www.kaggle.com/datasets/ishanikathuria/handwritten-signature-datasets).
- I've used setup.py to extract the data from zip file and also arrange it in the required format.
- Only 15 forged and 15 original from each person of all three datasets have been used for uniformity.
- Model used in this assignment is taken from this [ink](https://github.com/VinhLoiIT/signet-pytorch/).

  ## Commands to follow
  - `kaggle datasets download -d ishanikathuria/handwritten-signature-datasets`
  - `python setup.py` (to extract the downloaded zip file and setup the data in the requried format)
  - `python pre_process.py` (to split the data into train and validatio sets)
  - `python train.py` (to train the model and save the checkpoints)

## Metrics
- Accuracy: 0.742
- link for model [checkpoint](https://drive.google.com/file/d/1keLNeJjlfIIB-V-j4P2C2c5Fpl_bPVfv/view?usp=sharing).
