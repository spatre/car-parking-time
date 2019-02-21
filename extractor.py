#### Created by Shiva Patre  ####

import urllib.request
import cv2


# Downloads the video clips and extracts the first frame as a JPG image
def download_extract(start, end, idx_file):

    url = 'https://example.com/video/'
    file_location = '../video_clips/'
    img_location = '../extracted_images/'
    print("Beginning files Download...")
    for idx in idx_file[idx_file.index(start):idx_file.index(end)+1:2]:
        try:
            urllib.request.urlretrieve(url + idx, file_location + idx)
            print(idx)
            cap = cv2.VideoCapture(file_location + idx)
            ret, frame = cap.read()
            img_file = idx.split('.')[0] + '.jpg'
            cv2.imwrite(img_location + img_file, frame)
        except:
            print("Error: Couldn't Download the file")
    print("Downloading and Extracting images complete!")
