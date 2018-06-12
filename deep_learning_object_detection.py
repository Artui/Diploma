# python deep_learning_object_detection.py --image images/example_01.jpg \
#	--prototxt MobileNetSSD_deploy.prototxt.txt --model MobileNetSSD_deploy.caffemodel

import argparse

import cv2
import numpy as np
from PIL import Image

def detect_object():
    predictions = []
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--confidence", type=float, default=0.2,
                    help="minimum probability to filter weak detections")
    args = vars(ap.parse_args())

    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
               "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
               "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
               "sofa", "train", "tvmonitor"]

    net = cv2.dnn.readNetFromCaffe(
        '/Users/arturveres/Projects/Diploma/object-detection-deep-learning/MobileNetSSD_deploy.prototxt.txt',
        '/Users/arturveres/Projects/Diploma/object-detection-deep-learning/MobileNetSSD_deploy.caffemodel'
    )

    image = cv2.imread("/Users/arturveres/image.png")
    pil_image = Image.open("/Users/arturveres/image.png")
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)

    net.setInput(blob)
    detections = net.forward()

    for i in np.arange(0, detections.shape[2]):

        confidence = detections[0, 0, i, 2]

        if confidence > args["confidence"]:

            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            label = "{}".format(CLASSES[idx])
            lanel_conf = "{:.2f}".format(confidence * 100)
            object_detected = {
                "name": label,
                "confidence": float(lanel_conf),
                "start_x": int(startX),
                "start_y": int(startY),
                "end_x": int(endX),
                "end_y": int(endY),
                "image_width": pil_image.size[0],
                "image_height": pil_image.size[1]
            }
            predictions.append(object_detected)
    return predictions
