# Defects detection in metal nuts by using vision IA multi-label object detection

## Autor: Rodrigo Gonzalez

## Introduction

The primary objective of this project is to utilize a YOLOv5 convolutional neural network to identify flaws in metal nuts. Given that convolutional neural networks require a significant amount of data to train effectively, this project aims to investigate whether 40 images per class are sufficient to train a YOLOv5 network and achieve satisfactory results.

### Dataset

The dataset used for training and evaluation purposes is the [The MVTec Anomaly Detection Dataset (MVTec AD)](https://www.mvtec.com/company/research/datasets/mvtec-ad). This dataset comprises 206 images of metal nuts, with five defect labels and approximately 40 images per defect category. The five defect labels are: 

1. bent
2. color
3. flip
4. metal-nut
5. scratch

However, it's important to note that the metal-nut label is not a defect but a way to identify that a complete nut is being observed.

To train a YOLOv5 network, the metal nut images should be labeled accordingly. The images were labeled using [Label Studio](https://labelstud.io/).  Both the labeled images and their respective labels are available in the `data/metal_nut_org` folder.

### YOLOv5 Docker

A Docker image is used to deploy the YOLOv5 network. It can be downloaded from: 

[https://hub.docker.com/r/ultralytics/yolov5](https://hub.docker.com/r/ultralytics/yolov5).

A YOLOv5 container is run with the following command:

```
$ docker run --ipc=host -it --gpus all -v /home/rodralez/metal_nut:/usr/src/metal_nut ultralytics/yolov5:latest
```

## Training


The training step is controlled by the Python script `code/python/metal_nut_yolov5_train.py`. A cross-validation approach is implemented to train the system. Several training and validation datasets are created randomly sampling images from the  `data/metal_nut_org` folder.

Once the YOLOv5 container is running, the  Python script has to be copied to the Docker container and run:

```
/usr/src/app# cp ../metal_nut/code/python/metal_nut_yolov5_train.py . && python3 metal_nut_yolov5_train.py
```

## Validation

The validation step is implemented with:

```
/usr/src/app# cp ../metal_nut/code/python/metal_nut_yolov5_train.py . && python3 metal_nut_yolov5_train.py
```

### Infered defects

Next, images of metal nuts from the validation step of one cross-validation experiment are compared. It's worth noting that the inferred labels were not used to train the model and can be considered as unseen data.


True labels            |  Infered labels 
:-------------------------:|:-------------------------:
![True images](./val_batch0_labels.jpg)  |  ![Predicted images](./val_batch0_pred.jpg)


## Conclusion
 
The YOLOv5 system's average mAP50 score for detecting defects in metal nuts is 0.374 across 10 cross-validation experiments. However, in some particular experiments, the system achieved an mAP50 of 0.75. Based on these results, it can be concluded that using 40 images per label to make predictions is a threshold for the vision AI system to function optimally.


