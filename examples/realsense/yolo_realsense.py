import torch
from pathlib import Path
import pyrealsense2 as rs
import cv2
import numpy as np

# load yolov5n model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5n.pt')
model.conf = 0.5  # confidence threshold

# start realsense stream
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
pipeline.start(config)

try:
    while True:
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue

        color_image = np.asanyarray(color_frame.get_data())

        # run yolo inference
        results = model(color_image)

        # parse results
        for *xyxy, conf, cls in results.xyxy[0]:
            x1, y1, x2, y2 = map(int, xyxy)
            label = f'{model.names[int(cls)]} {conf:.2f}'
            cv2.rectangle(color_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(color_image, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

        cv2.imshow("yolo detection", color_image)
        if cv2.waitKey(1) == 27:
            break

finally:
    pipeline.stop()
    cv2.destroyAllWindows()
