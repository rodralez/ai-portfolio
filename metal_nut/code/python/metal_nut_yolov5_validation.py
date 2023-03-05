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

# COPY VALIDATION SCRIPT TO /usr/src/app
# cp ../metal_nut/code/python/metal_nut_yolov5_validation.py . && python3 metal_nut_yolov5_validation.py

import numpy as np
import os
import random
import shutil

# Validate (1) or just test the previous code before validating (0)
VAL = 1

# constants
PROJECT = 'metal_nut'
EXPERIMENT = 'yolov5'
IMG_FORMAT = '.png'
IMG_RESOLUTION = 704
NUMBER_OF_CV = 10
TRAIN_PERCENTAGE = float(0.80)
VAL_PERCENTAGE = float(0.20)

data_dir  = '/usr/src/'+PROJECT+'/data/'
model_dir = '/usr/src/'+PROJECT+'/model/'
yolo_dir = '/usr/src/app'
exp_dir =  EXPERIMENT

# Remove old directories
for i in range(NUMBER_OF_CV) :

    # change to data directory
    os.chdir(model_dir)

    # set others directories
    dir_train = exp_dir + '/cv_' + str(i).zfill(2)
    dir_val =  dir_train + '/val'
    shutil.rmtree(dir_val, ignore_errors=True)

for i in range(NUMBER_OF_CV) :

    # # change to model directory
    # os.chdir(model_dir)

    # # change to experiment directory
    dir_train = exp_dir + '/cv_' + str(i).zfill(2)

    # change to data directory
    os.chdir(data_dir)

    # os.system("pwd")

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
                    path_new = 'path: ' + model_dir + dir_train + "\n"
                    output.write(path_new)

    # replace file with original name
    os.replace('temp.txt', file_yaml)

    # change to yolo directory
    os.chdir(yolo_dir)
 
# yolo valid

    yolo_cmd = 'python3 val.py --img ' + str(IMG_RESOLUTION) + ' --name val --workers 10 ' # --save-txt --save-conf --save-hybrid
    yolo_project = "--project '" + model_dir + dir_train + "' "
    yolo_data = "--data '" + data_dir + PROJECT + ".yaml' "
    yolo_weights = "--weights '" + model_dir + dir_train + "/train/weights/best.pt' "

    yolo_val =  yolo_cmd + yolo_weights + yolo_data + yolo_project

    print(yolo_val)

    if VAL :
        os.system(yolo_val)     

# yolo test
# python detect.py --source '../datasets/metal-nut_cv_000/images/test/' 
# --weights '../datasets/metal-nut_cv_000/train_001/weights/best.pt' 
# --conf 0.6 --iou 0.45 --augment  --project '../datasets/metal-nut_cv_000/' --name 'test_001'

    # yolo_cmd = 'python3 detect.py '
    # yolo_opt = '--conf 0.6 --iou 0.45 --augment '
    # yolo_src = "--source  '../datasets/" + dir_dest + "/images/test' "
    # yolo_name =" --name 'test_001' "
    # # dir_dest =  PROJECT+'_'+'cv_00'+str(i+2)
    # yolo_weights = "--weights '../datasets/" + dir_dest + "/train_001/weights/best.pt' "

    # yolo_test = yolo_cmd+yolo_src+yolo_data+yolo_weights+yolo_opt+yolo_project+yolo_name 

    # print(yolo_test)
    
    #if SERVER :
    #    os.system(yolo_test)
