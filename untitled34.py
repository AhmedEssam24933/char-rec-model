# -*- coding: utf-8 -*-
"""Untitled34.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eZ37Giji8ry3qgucjYscqDkL0t_F8xJb
"""

# Commented out IPython magic to ensure Python compatibility.
#clone YOLOv5 and
!git clone https://github.com/ultralytics/yolov5  # clone repo
# %cd yolov5
# %pip install -qr requirements.txt # install dependencies
# %pip install -q roboflow

import torch
import os
from IPython.display import Image, clear_output  # to display images

print(f"Setup complete. Using torch {torch.__version__} ({torch.cuda.get_device_properties(0).name if torch.cuda.is_available() else 'CPU'})")

!pip install roboflow

from roboflow import Roboflow
rf = Roboflow(api_key="XRcZB4HVUZw2RzVGB0EV")
project = rf.workspace("ahmad-essam-gvgib").project("car-plate-recognition-ts2bk")
dataset = project.version(1).download("yolov5")

os.environ["DATASET_DIRECTORY"] = "/content/dataset"

!python train.py --img 416 --batch 16 --epochs 500 --data {dataset.location}/data.yaml --weights yolov5s.pt --cache

# Load the YOLOv5 model
model = torch.hub.load('.', 'custom', path='/content/yolov5/runs/train/exp/weights/best.pt', source='local')

# Specify the path to your input image
image_path = '/content/images/test11.jpg'

# Perform object detection on the image
results = model(image_path)

# Get the predicted labels and bounding box coordinates
labels = results.xyxyn[0][:, -1].cpu().numpy()
boxes = results.xyxyn[0][:, :-1].cpu().numpy()

# Get the class names associated with the model
class_names = model.module.names if hasattr(model, 'module') else model.names

# Reverse the order of labels and bounding boxes
reversed_labels = labels[::-1]
reversed_boxes = boxes[::-1]

# Iterate over the reversed bounding box coordinates and labels
for label, box in zip(reversed_labels, reversed_boxes):
    # Get the label name using the model's class names
    label_name = class_names[int(label)]

    # Print the label name and reversed bounding box
    print("Label: {}, Bounding Box: {}".format(label_name, box))