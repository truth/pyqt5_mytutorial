import torch

# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5m, yolov5l, yolov5x, custom

# Images
img = './zidane.jpg'  # or file, Path, PIL, OpenCV, numpy, list
# Using cache found in C:\Users\truth/.cache\torch\hub\ultralytics_yolov5_master
# Inference
results = model(img)
results.show()
