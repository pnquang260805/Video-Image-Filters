import cv2
import numpy as np
from services.PIL_service import ascii_to_image

def video_processor(video_source = 0, func=None, **kwargs):
        cap = cv2.VideoCapture(video_source)
        if not cap.isOpened():
            print("Error: Could not open video file.")
            exit()
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                if func:
                    result = func(frame, **kwargs)
                    
                    # If result is ASCII (list of strings), render to image
                    if isinstance(result, list) and len(result) > 0 and isinstance(result[0], str):
                        frame = ascii_to_image(result)
                    else:
                        # Otherwise, assume it's a modified frame
                        frame = result

                cv2.imshow('ASCII Video (Press Q to quit)', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            cap.release()
            cv2.destroyAllWindows()