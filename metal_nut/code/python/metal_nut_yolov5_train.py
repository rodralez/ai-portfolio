#!/usr/bin/python3
#
# PROJECT
# ├── code
#     └── python
# └── data
#     └── PROJECT_bg
#     └── PROJECT_org
# └── model
#     └── yolov5
#         └── cv_00
#         └── cv_01

# SCREEN
# screen -S yolo_training -L -Logfile yolo_training_log_2022-01-31
# screen -ls
# screen -r # retach

# YOLOv5 DOCKER
# docker run --ipc=host -it --gpus all -v /home/rodralez/metal_nut:/usr/src/metal_nut ultralytics/yolov5:latest

# COPY TRAIN SCRIPT TO /usr/src/app
# cp ../metal_nut/code/python/metal_nut_yolov5_train.py . && python3 metal_nut_yolov5_train.py

import numpy as np
import os
import random
import shutil

# Train (1) or just test the previous code before training (0)
TRAIN = 1

# constants
PROJECT = 'metal_nut'
EXPERIMENT = 'yolov5'
IMG_FORMAT = '.png'
IMG_RESOLUTION = 704
NUMBER_OF_CV = 10
TRAIN_PERCENTAGE = float(0.80)
VAL_PERCENTAGE = float(0.20)

data_dir = '/usr/src/'+PROJECT+'/data/'
model_dir = '/usr/src/'+PROJECT+'/model/'
yolo_dir = '/usr/src/app'

# set origin image directory
data_org =  data_dir + PROJECT + '_org/'

# list all files in data_org that are an image
all_img = [f for f in os.listdir(data_org) if f.endswith(IMG_FORMAT)]

# divide the data_org for training and for validating
TRAIN_SAMPLES  = int(len(all_img) * TRAIN_PERCENTAGE)
VAL_SAMPLES  = int(len(all_img) * (1-TRAIN_PERCENTAGE))
# VAL_SAMPLES  = VAL_SAMPLES  = int(len(all_img) * VAL_PERCENTAGE)
# TEST_SAMPLES = VAL_SAMPLES

# change to model directory
os.chdir(model_dir)

# remove old experiment directory
exp_dir =  EXPERIMENT
shutil.rmtree(exp_dir, ignore_errors=True)

# Create new experiment directory
os.mkdir(exp_dir)

# start the CV training...
for i in range(NUMBER_OF_CV) :

    # change to model directory
    os.chdir(model_dir)

    # define new directories to train, validate and test
    train_dir = exp_dir + '/cv_' + str(i).zfill(2) 
    img_dir =   train_dir + '/images/' 
    img_train = train_dir + '/images/train/' 
    img_val =   train_dir + '/images/valid/' 
    img_test =  train_dir + '/images/test/'
    lbl_dir =   train_dir + '/labels/' 
    lbl_train = train_dir + '/labels/train/' 
    lbl_val =   train_dir + '/labels/valid/' 
    lbl_test =  train_dir + '/labels/test/' 

    # make directories
    os.mkdir(train_dir)
    os.mkdir(img_dir)
    os.mkdir(img_train)
    os.mkdir(img_val)
    os.mkdir(img_test)
    os.mkdir(lbl_dir)
    os.mkdir(lbl_train)
    os.mkdir(lbl_val)
    os.mkdir(lbl_test)

    # training images
    train_list = random.sample(all_img, TRAIN_SAMPLES)

    # validation images
    other_list = list(set(all_img) - set(train_list))
    val_list = random.sample(other_list, VAL_SAMPLES)

    # testing images
    # other_list = list(set(other_list) - set(val_list))
    # test_list = random.sample(other_list, TEST_SAMPLES)

    # change to model directory
    os.chdir(data_dir)

    # copy background images to train directory
    cmd = 'cp '+ PROJECT + '_bg/* ../model/' + img_train
    os.system(cmd)

    # images to train directory
    for train_file in train_list:
        file_org = data_org + train_file
        shutil.copy(file_org, '../model/' + img_train)
        continue

    # labels to train directory
    for train_file in train_list:
        file_org = data_org + (os.path.splitext(train_file)[0]+'.txt')
        shutil.copy(file_org , '../model/' + lbl_train)
        continue

    # images to val directory
    for val_file in val_list:
        file_org = data_org + val_file
        shutil.copy(file_org , '../model/' + img_val)
        continue

    # labels to val directory
    for val_file in val_list:
        file_org = data_org + (os.path.splitext(val_file)[0]+'.txt')
        shutil.copy(file_org , '../model/' + lbl_val)
        continue

    # images to test directory
    # for test_file in test_list:      
    #     file_org = data_org + test_file
    #     shutil.copy(file_org , '../model/' + img_test)
    #     continue

    # open and modify PROJECT.yaml
    file_yaml = PROJECT + '.yaml'

    # find 'path' in yaml file and replace accordingly	
    with open(file_yaml, "r") as input:
        with open("temp.txt", "w") as output:
	    # iterate all lines from file
            for line in input:
		# if substring contain in a line then don't write it
                if "path" not in line.strip("\n"):
                    output.write(line)
                else:
                    path_new = 'path: ' + model_dir + train_dir + "\n"
                    output.write(path_new)

    # replace file with original name
    os.replace('temp.txt', file_yaml)

    # change to yolo directory
    os.chdir(yolo_dir)

    # yolo command
    yolo_weights = "--weights '' "

    yolo_cmd = 'python3 train.py --img ' + str(IMG_RESOLUTION) + ' --batch 48 --epochs 1000 --cache ram --patience 50 --workers 10 '
    
    yolo_data = "--data '" + data_dir + PROJECT + ".yaml' "
    yolo_hyp = "--hyp '" + data_dir + "hyp.yaml' "
    yolo_cfg = "--cfg '" + data_dir + PROJECT + "_yolov5s.yaml' "
    yolo_project = "--project '" + model_dir + train_dir + "' "
    yolo_name = "--name 'train' "

    yolo_train =  yolo_cmd + yolo_data + yolo_weights + yolo_cfg + yolo_project + yolo_name + yolo_hyp
    print(yolo_train)

    if TRAIN :
        os.system(yolo_train)
