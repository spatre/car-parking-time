#### Created by Shiva Patre  ####

import cv2
import importlib
detector = importlib.import_module('detector')
importlib.invalidate_caches()

# Defining the parameters as constants
THRESHOLD = 6
LOWE_NUM = 0.7
FLANN_INDEX_KDTREE = 0
TREES = 3
CHECKS = 100
KNN = 2


# Compares two cars and returns true if they are same, else returns false
def check_similarity(image1, image2):

    # Image Location
    img_1 = '../extracted_images/' + image1 + '.jpg'
    img_2 = '../extracted_images/' + image2 + '.jpg'

    # Reading the image
    car_1 = cv2.imread(img_1)
    car_2 = cv2.imread(img_2)

    # Slicing the ROI to be fed into SIFT
    car_1_spot = car_1[detector.top_left_y:detector.bottom_right_y, detector.top_left_x:detector.bottom_right_x]
    car_2_spot = car_2[detector.top_left_y:detector.bottom_right_y, detector.top_left_x:detector.bottom_right_x]

    # Initializing the SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()

    # Getting the keypoints and Descriptors using SIFT
    keypoints_1, descriptors_1 = sift.detectAndCompute(car_1_spot, None)
    keypoints_2, descriptors_2 = sift.detectAndCompute(car_2_spot, None)

    # Using Fast Library for Approximate Nearest Neighbors (FLANN) for image matching
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=TREES)
    search_params = dict(checks=CHECKS)

    # Invoking the Flann Matcher
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    # Getting the total number of matches between car_1 and car_2
    matches = flann.knnMatch(descriptors_1, descriptors_2, k=KNN)

    # Need to get only good matches
    # This is based on Lowe's ratio test
    good_matches = []
    for m, n in matches:

        if m.distance < LOWE_NUM * n.distance:
            good_matches.append(m)

    # Total number of good matches. Should be high for similar cars
    num_good_matches = len(good_matches)

    # Finally, making a decision, if the matches exceed the threshold, it is the same car, else not.
    if num_good_matches >= THRESHOLD:
        return True
    else:
        return False
