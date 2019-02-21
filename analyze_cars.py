#### Created by Shiva Patre ####

import cv2
import argparse
import importlib
import math

extractor = importlib.import_module('extractor')
detector = importlib.import_module('detector')
matcher = importlib.import_module('matcher')
importlib.invalidate_caches()

MIN_TIME = 8  # list length 8 corresponds to one minute
SECONDS = 60
park_map = {}


# Calculates time from the Unix timestamp in minutes (approx)
def get_time(start_time, end_time):

    time_parked = math.ceil((int(end_time) - int(start_time)) / SECONDS)
    return time_parked


# If the car is parked for more than 1 min (to eliminate false alarms by passing cars)
# It adds the start and end time stamp which contain the car to a dictionary
def add_to_map(car_time_stamps):

    if len(car_time_stamps) >= MIN_TIME:
        park_map[car_time_stamps[0]] = car_time_stamps[-1]


# Analyzes each image by running YOLO, checking for same car, and adding to a list
def analyze_image(start, end, idx_file):

    car_found = 0
    car_time_stamps = []
    yolo_net, out_layer = detector.load_net()

    for idx in idx_file[idx_file.index(start):idx_file.index(end) + 1:2]:

        img_num = idx.split('.')[0]
        img = img_num + '.jpg'
        classIDs = detector.detect(img, yolo_net, out_layer)

        if not classIDs:
            if car_found != 0 and len(car_time_stamps) > 1:
                add_to_map(car_time_stamps)
            car_found = 0
            car_time_stamps[:] = []
        else:
            car_found += 1
            if car_found == 1:
                car_time_stamps.append(img_num)
            elif matcher.check_similarity(car_time_stamps[car_found - 2], img_num):
                car_time_stamps.append(img_num)
            else:
                add_to_map(car_time_stamps)
                car_time_stamps[:] = []
                car_time_stamps.append(img_num)
                car_found = 1


# comparing start time img of first car with start and end time img of the second car and
# also end time img of first car with start and end time img of the second car
# This eliminates any false alarms by multiple cross validations
def check(start_time_1, end_time_1, start_time_2, end_time_2):

    if matcher.check_similarity(start_time_1, start_time_2) or matcher.check_similarity(start_time_1, end_time_2):
        return True
    if matcher.check_similarity(end_time_1, start_time_2) or matcher.check_similarity(end_time_1, end_time_2):
        return True
    return False


# This gives a dictionary with the final output timestamp ranges
# The key gives start time stamp of the car
# The corresponding value gives end time stamp of the car
# This basically replaces the value of one key with the value of other key, if it is the same car
# Thereby, accumulating the time stamps together for each different car
def cross_validate(park_map):

    flag = 1
    park_list = list(park_map.items())
    i = 0
    while flag:
        j = i + 1
        if j > len(park_list)-1:
            flag = 0
            continue

        if check(park_list[i][0], park_list[i][1], park_list[j][0], park_list[j][1]):
            park_map[park_list[i][0]] = park_map[park_list[j][0]]
            park_list[i] = (park_list[i][0], park_list[j][1])
            del park_map[park_list[j][0]], park_list[j]
            i = i - 1
        i = i + 1
    return park_map


# Prints the image of the car first detected along with the parking time details
def image_printer(park_map):

    img_location = '../extracted_images/'
    for start_time, end_time in park_map.items():

        parked_time = get_time(start_time, end_time)
        print("Found Car at " + str(start_time) + " parked until " + str(end_time) + " for " + str(parked_time) +
              " minutes")
        img_park = img_location + start_time + '.jpg'
        img_park_read = cv2.imread(img_park)
        output_image = '../output/' + start_time + '-' + str(parked_time) + 'min.jpg'

        #cv2.rectangle(img_park_read, (detector.top_left_x, detector.top_left_y),
         #             (detector.bottom_right_x, detector.bottom_right_y), (0, 255, 0), 2)
        #cv2.putText(img_park_read, 'Car Found', (detector.top_left_x, detector.top_left_y - 5),
         #           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.imwrite(output_image, img_park_read)
        print("... Wrote " + output_image)


# Main function starts executing from here by parsing the input from the Command Line
def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--index", required=True, help="Path to the index.txt file")
    parser.add_argument("-s", "--start", required=True, help="Starting .ts filename")
    parser.add_argument("-e", "--end", required=True, help="Ending .ts filename")
    args = vars(parser.parse_args())

    idx_file = open(args["index"]).read().strip().split("\n")

    start = args["start"] + '.ts'
    end = args["end"] + '.ts'

    if start not in idx_file or end not in idx_file:
        print("File not present")
    else:
        #extractor.download_extract(start,end,idx_file)
        print("Analyzing from " + args["start"] + ' to ' + args["end"])
        analyze_image(start, end, idx_file)
        if not park_map:
            print("No Cars Found")
        else:
            park_out = cross_validate(park_map)
            image_printer(park_out)
            print("No More Cars Found!")


if __name__ == '__main__':
    main()

# ****** END OF FILE ***** #
