#### Created by Shiva Patre  ####

import cv2
import numpy as np

# Defining the parameters as constants
SCALE_FACTOR = 255.0
INPUT_DIM = 90
CAR_CONF = 0.20
TRUCK_CONF = 0.35
CAR = 2
TRUCK = 7

# Defining Region Of Interest (ROI) for the particular parking spot
top_left_x = 184
top_left_y = 186
bottom_right_x = 274
bottom_right_y = 266


# Load the YOLOv3 net
def load_net():

	weights_path = '../files/yolo_coco/yolov3.weights'
	config_path = '../files/yolo_coco/yolov3.cfg'

	yolo_net = cv2.dnn.readNetFromDarknet(config_path, weights_path)
	out_layer = yolo_net.getLayerNames()
	out_layer = [out_layer[i[0] - 1] for i in yolo_net.getUnconnectedOutLayers()]
	return yolo_net,out_layer


# Detects the car or truck and outputs the classIDs
def detect(image_no, yolo_net, out_layer):

	# Location of the extracted image
	img_location = '../extracted_images/' + image_no
	image = cv2.imread(img_location)
	parking_spot = image[top_left_y:bottom_right_y, top_left_x:bottom_right_x]
	blob = cv2.dnn.blobFromImage(parking_spot, 1 / SCALE_FACTOR, (INPUT_DIM, INPUT_DIM), swapRB=True, crop=False)
	yolo_net.setInput(blob)
	layer_outputs = yolo_net.forward(out_layer)
	classIDs = []

	for output in layer_outputs:
		# loop over every detection
		for detection in output:
			# Get the class ID and probability of the current object detection
			scores = detection[5:]
			classID = np.argmax(scores)
			confidence = scores[classID]
			# This can be tweaked and tuned to get optimum results
			if (confidence > CAR_CONF and classID == CAR) or (confidence > TRUCK_CONF and classID == TRUCK):
				classIDs.append(classID)
	return classIDs



