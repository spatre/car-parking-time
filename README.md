# car-parking-time
Calculating Car parking time at a parking spot using YOLOv3 and SIFT

* This application calculates the parking time of a car in a particular parking spot using YOLOv3. Just enter the website containing .ts video files in the extractor.py, and run the analyze_cars.py script as shown below and you get the output parking times of the cars in the particular time range.

* Please download YOLOv3 weights from this [link](https://pjreddie.com/media/files/yolov3.weights) as it is required for car detection.

* Instructions regarding Dependencies
-------------------------------------

Requirements: Python 3.7 and OpenCV 3.4.2 or 3.4.3 with Contrib

For Mac OS
----------

I have used Mac OS as my environment to do this assignment and I'll list the easiest way to download
the above requirements

* We need Command Line Tools for XCode installed from the App Store for the below

* Download Homebrew by running the below in the Terminal

/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

* Install Python 3.7 (if not already installed) with the following command in Terminal

brew install python

* Install numpy (if not already installed) with the following command in Terminal

brew install numpy

* Install OpenCV 3.4.3 (with Contrib) with the following command in Terminal

brew install opencv

Note:
-----
1) Contrib is required as I have used SIFT and all patented algorithms are present in OpenCV's Contrib

Once the above is installed, we are good to go!

-----------------------------------------------------------------------------------------------------------------------

* Instructions to run the code
------------------------------
* analyze-cars.py : Runs the python script that is used to analyze cars parked at the particular spot


* Run the following in the terminal accordingly

* Input the start and end time range as follows

Example 1:

> python3 analyze-cars.py 1538076003 1538078234

sample o/p:
-----------

Beginning files Download...

1538076003.ts

.
.
.
.

Downloading and Extracting images complete!

Analyzing from 1538076003 to 1538078234 using YOLO3

Found Car at 1538076227 parked until 1538077866 for 28 minutes

... Wrote ../output/1538076227-28min.jpg

Found Car at 1538077954 parked until 1538078194 for 4 minutes

... Wrote ../output/1538077954-4min.jpg

No More Cars Found!
