
import os
import random
import shutil

import numpy as np


def copy_nth_image(src_folder, dst_folder, interval=10):

    # Ensure destination folder exists
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)

    # List all files in the source folder
    files = os.listdir(src_folder)

    # Iterate over the image files and copy every nth one
    for idx, image_file in enumerate(files):
        if (idx + 1) % interval  == 0:
            src_path = os.path.join(src_folder, image_file)
            dst_path = os.path.join(dst_folder, image_file)
            shutil.copy(src_path, dst_path)
    
    print('Images copied!')


def train_test_split(src_folder, train_folder, val_folder, test_folder, 
                     split=[0.7, 0.2, 0.1]):
    
    # Create a list of image filenames in 'src_path'
    imgs_list = [filename for filename in os.listdir(src_folder)]

    # Sets the random seed 
    random.seed(42)
    # Shuffle the list of image filenames
    random.shuffle(imgs_list)
    
    # Determine the number of images for each set
    assert np.round(np.array(split).sum()) == 1.0
    train_size = int(len(imgs_list) * split[0])
    val_size = int(len(imgs_list) * split[1])
    test_size = int(len(imgs_list) * split[2])
    
    # Create destination folders if they don't exist
    for folder_path in [train_folder, val_folder, test_folder]:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    
    # Copy image files to destination folders
    for i, f in enumerate(imgs_list):
        if i < train_size:
            dest_folder = train_folder
        elif i < train_size + val_size:
            dest_folder = val_folder
        else:
            dest_folder = test_folder

        shutil.copy(os.path.join(src_folder, f), os.path.join(dest_folder, f))
    
    print('Dataset successfully split!')


src_folder = 'path/to/data/raw_videos'
train_folder = 'path/to/data/train'
val_folder = 'path/to/data/valid'
test_folder = 'path/to/data/test'


if __name__ == '__main__':
    #copy_nth_image(src_folder, dst_folder)
    train_test_split(src_folder, train_folder, val_folder, test_folder)