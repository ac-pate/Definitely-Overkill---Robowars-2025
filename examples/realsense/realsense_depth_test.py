import cv2
import pyrealsense2 as rs
import numpy as np

# initialize realsense pipeline
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

pipeline.start(config)

try:
    while True:
        # wait for a coherent pair of frames
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue

        # convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # ---- boundary detection ----
        # convert to hsv
        hsv = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)
        # define white boundary color range (adjust if needed)
        lower_white = np.array([0, 0, 180])
        upper_white = np.array([255, 30, 255])
        boundary_mask = cv2.inRange(hsv, lower_white, upper_white)

        # ---- enemy detection ----
        # threshold depth to find close objects
        depth_thresh = 1500  # in mm, adjust as needed
        enemy_mask = cv2.inRange(depth_image, 300, depth_thresh)  # exclude floor
        enemy_mask = cv2.medianBlur(enemy_mask, 5)

        # find contours in enemy mask
        contours, _ = cv2.findContours(enemy_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            area = cv2.contourArea(c)
            if area > 500:  # filter small noise
                x, y, w, h = cv2.boundingRect(c)
                cv2.rectangle(color_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(color_image, 'enemy', (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # check for boundary near bottom of image
        bottom_line = boundary_mask[440:480, :]
        if np.count_nonzero(bottom_line) > 3000:
            cv2.putText(color_image, 'boundary ahead!', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            # stop or reverse

        # display images
        cv2.imshow('color', color_image)
        cv2.imshow('boundary mask', boundary_mask)
        cv2.imshow('enemy mask', enemy_mask)

        key = cv2.waitKey(1)
        if key == 27:  # esc to quit
            break

finally:
    pipeline.stop()
    cv2.destroyAllWindows()
