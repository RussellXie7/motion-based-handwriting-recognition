import numpy as np
from utils import dtw, l2
from .. import data
from data import data_utils, data_visualizer, data_augmentation, data_flatten

train_dirs = ["kevin_11_7", "russell_11_7"]
test_dirs = ["kelly_11_7"]

root = "./data/"

train_data, train_labels = [],[] # shape should roughly be (40*26, 100, 3)
test_data, test_labels = [],[]  # shape should roughly be (20*26, 100, 3)

for dir in train_dirs:
    loaded_dataset = load_data_dict_from_file(dir, calibrate=True)
    flattened_dataset = resample_dataset(loaded_dataset, is_flatten_ypr=True, feature_num=100)

    for label_name, data_sequences in flattened_dataset.items():
    	train_data.extend(data_sequences)
    	train_labels.extend([label_name]*len(data_sequences))

train_data = np.asarray(train_data)
train_labels = np.asarray(train_labels)

print("train_data", train_data.shape)
print("train_labels", train_labels.shape)


for dir in test_dirs:
    loaded_dataset = load_data_dict_from_file(dir, calibrate=True)
    flattened_dataset = resample_dataset(loaded_dataset, is_flatten_ypr=True, feature_num=100)

    for label_name, data_sequences in flattened_dataset.items():
    	train_data.extend(data_sequences)
    	train_labels.extend([label_name]*len(data_sequences))    	



