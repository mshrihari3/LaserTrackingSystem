from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import serial
import math

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.flush()
ser.write(b"X0:Y0")
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str,
	help="path to input video file")
ap.add_argument("-t", "--tracker", type=str, default="csrt",
	help="OpenCV object tracker type")
args = vars(ap.parse_args())

OPENCV_OBJECT_TRACKERS = {
	"csrt": cv2.TrackerCSRT_create,
	"kcf": cv2.TrackerKCF_create,
	"boosting": cv2.TrackerBoosting_create,
	"mil": cv2.TrackerMIL_create,
	"tld": cv2.TrackerTLD_create,
	"medianflow": cv2.TrackerMedianFlow_create,
	"mosse": cv2.TrackerMOSSE_create
}
trackers = cv2.MultiTracker_create()

if not args.get("video", False):
	print("[INFO] starting video stream...")
	vs = VideoStream(src=0).start()
	time.sleep(1.0)
else:
	vs = cv2.VideoCapture(args["video"])

while True:
	frame = vs.read()
	frame = frame[1] if args.get("video", False) else frame
	if frame is None:
		break
	frame = imutils.resize(frame, width=600, height=600)
	frame = cv2.resize(frame, (600, 600))
	(success, boxes) = trackers.update(frame)
	for box in boxes:
		(x, y, w, h) = [int(v) for v in box]
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		print(x+(w/2), y+(h/2))
		Xval = str(180-math.ceil(x+(w/2))/(600/120))
		Yval = str(math.ceil(y+(h/2))/(600/180))
		strs = "X{0}:Y{1}".format(Xval, Yval)
		bstrs = bytes(strs, encoding="utf-8")
		ser.write(bstrs)
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("s"):
		box = cv2.selectROI("Frame", frame, fromCenter=False,
			showCrosshair=True)
		tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()
		trackers.add(tracker, frame, box)
	elif key == ord("q"):
		break
if not args.get("video", False):
	vs.stop()
else:
	vs.release()
cv2.destroyAllWindows()
