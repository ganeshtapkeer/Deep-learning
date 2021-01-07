# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 10:44:40 2020

@author: user
"""
import cv2
import numpy as np

net = cv2.dnn.readNet('F:/FINAL YEAR BTECH/DATA MINING/yolo (1)\yolo/wt/yolov3.weights','F:/FINAL YEAR BTECH/DATA MINING/yolo (1)/yolo/darknet-master/cfg/yolov3.cfg')

classes = []
with open('F:/FINAL YEAR BTECH/DATA MINING/yolo (1)/yolo/darknet-master/data/coco.names','r') as f:
    classes = f.read().splitlines()

################print(classes) #read file

#cap=cv2.VideoCapture(0)

img = cv2.imread('F:/DMDW Project/computer_vision/Model/models-master/models-master/research/object_detection/test_images/image2.jpg')


height, width, _ = img.shape

blob = cv2.dnn.blobFromImage(img,1/255,(416,416),(0,0,0), swapRB=True, crop=False)

net.setInput(blob)
output_layers_names = net.getUnconnectedOutLayersNames()
layerOutputs = net.forward(output_layers_names)

boxes = []
confidences = []
class_ids = []

for output in layerOutputs:
    for detection in output:
        scores = detection[5:] #starting from 6th element
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.5:
            center_x = int(detection[0]*width)
            center_y = int(detection[1]*height)
            w = int(detection[2]*width)
            h = int(detection[3]*height)

            x = int(center_x - w/2)
            y = int(center_y - h/2) #position of corner

            boxes.append([x,y,w,h])
            confidences.append((float(confidence)))
            class_ids.append(class_id)

print(len(boxes))
indexes = cv2.dnn.NMSBoxes(boxes,confidences, 0.5, 0.4)

font = cv2.FONT_HERSHEY_PLAIN
colors = np.random.uniform(0,255, size=(len(boxes),3))

for i in indexes.flatten():
    x,y,w,h = boxes[i]
    label =  str(classes[class_ids[i]])
    confidence = str(round(confidences[i],2))
    color = colors[i]
    cv2.rectangle(img,(x,y),(x+w, y+h),color,2)
    cv2.putText(img, label + " " + confidence,(x,y+20), font, 2, (255,255,255),2)

    #####print(indexes.flatten())-->print size of boxes


cv2.imshow('img',img)
cv2.waitKey()


cv2.destroyAllWindows()
