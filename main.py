from ultralytics import YOLO
import cv2
import numpy as np
from sort.sort import *
import util
from util import get_vehicle, read_license_plate, write_csv
import sys


results = {}
set_time = False
time_end = 1.0
time_start = 0.0
frame_start = 0

time_not_end = True

# print("set_time: {}".format(set_time))

if __name__ == "__main__":
    for i, arg in enumerate(sys.argv):
        # print(f"{i} argument: {arg}")
        if i == 1:
            set_time = bool(arg.lower() == 'true')
        elif i ==2:
            time_end = float(arg)
        elif i ==3:
            time_start = float(arg)

# print("set_time: {}",set_time)
# print(f"set_time: {time_end}")


mot_tracker = Sort()

# Load models
Vehicle_Detector = YOLO('/home/sare/Downloads/train4/weights/best.pt')
license_plate_detector = YOLO('/home/sare/Vehicle_Detection/best.pt')

# Load video
cap = cv2.VideoCapture(util.video_test)
# Check if the video was opened successfully
if not cap.isOpened():
    # print(f"Error: Could not open video {video_path}")
    exit()


fps = cap.get(cv2.CAP_PROP_FPS)

# Read frames
frame_start  = int(time_start * fps)

# print(f"frame number is {frame_start}")
cap.set(cv2.CAP_PROP_POS_FRAMES, int(frame_start))

frame_nmr = frame_start - 1
frame_counter = 0
ret = True

while (ret and time_not_end):
    frame_nmr += 1
    frame_counter += 1

    # print(f"Current frame of {cap.get(1)}")
    ret, frame = cap.read()
    if ret:
        results[frame_nmr] = {}
        current_time = frame_counter / fps
        # print("Time is {}",current_time)
        if set_time:
            if current_time > time_end:
                time_not_end=False

        # Detect vehicles
        detections = Vehicle_Detector(frame)[0]
        detections_ = []
        vehicle_scores = []
        vehicle_types = []
        for detection in detections.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = detection
            detections_.append([x1, y1, x2, y2, score])
            vehicle_scores.append(score)
            if class_id == 0:  # Assuming 0 is Car, 1 is Korope, 2 is Bus
                vehicle_types.append("Car")
            elif class_id == 1:
                vehicle_types.append("Korope")
            elif class_id == 2:
                vehicle_types.append("Bus")
            else:
                vehicle_types.append("Unknown")

        # Track vehicles
        track_ids = mot_tracker.update(np.asarray(detections_))

        # Detect license plates
        license_plates = license_plate_detector(frame)[0]
        for license_plate in license_plates.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = license_plate

            # Assign license plate to vehicle
            xvehicle1, yvehicle1, xvehicle2, yvehicle2, vehicle_id = get_vehicle(license_plate, track_ids)

            if vehicle_id != -1:
                # Crop license plate
                license_plate_crop = frame[int(y1):int(y2), int(x1): int(x2), :]

                # Process license plate
                license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
                # _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, 64, 255, cv2.THRESH_BINARY_INV)

                # Read license plate number
                format_type = 1
                license_plate_text, license_plate_text_score = read_license_plate(license_plate_crop_gray)

                if license_plate_text is not None:
                    vehicle_type = vehicle_types[track_ids[:, -1].tolist().index(vehicle_id)]
                    vehicle_score = vehicle_scores[track_ids[:, -1].tolist().index(vehicle_id)]
                    results[frame_nmr][vehicle_id] = {
                        'Vehicle_type': vehicle_type,
                        'Vehicle_score': vehicle_score,
                        'vehicle': {'bbox': [xvehicle1, yvehicle1, xvehicle2, yvehicle2]},
                        'current_time': current_time,
                        'license_plate': {
                            'bbox': [x1, y1, x2, y2],
                            'text': license_plate_text,
                            'bbox_score': score,
                            'text_score': license_plate_text_score
                        }
                    }

# Write results
write_csv(results, './sample.csv')
