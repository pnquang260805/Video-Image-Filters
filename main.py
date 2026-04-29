import cv2
import numpy as np
from services.video_service import video_processor
from services.PIL_service import convert_to_ascii, open_image, ascii_to_image
from services.ASCII_char import get_level

def image_mode(ascii_chars):
    path = input("Enter image path: ").strip()
    if not path:
        print("Invalid path!")
        return
        
    try:
        # Load image
        img_pil = open_image(path)
        img_np = cv2.imread(path) # For normal display
        
        print("\n1. Normal Display")
        print("2. Convert to ASCII")
        choice = input("Choice: ")
        
        if choice == '1':
            cv2.imshow("Normal Image", img_np)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        elif choice == '2':
            cols = int(input("Enter columns (default 100): ") or "100")
            res = convert_to_ascii(img_pil, ascii_chars, cols=cols)
            ascii_img = ascii_to_image(res)
            cv2.imshow("ASCII Image", ascii_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    except Exception as e:
        print(f"Error: {e}")

def video_mode(ascii_chars):
    path = input("Enter video path (or 0 for webcam): ").strip()
    if path == '0':
        path = 0
        
    print("\n1. Normal Display")
    print("2. Convert to ASCII")
    choice = input("Choice: ")
    
    if choice == '1':
        video_processor(path, func=None)
    elif choice == '2':
        cols = int(input("Enter columns (default 100): ") or "100")
        video_processor(path, convert_to_ascii, ascii_chars=ascii_chars, cols=cols)

if __name__ == "__main__":
    while True:
        try:
            ascii_chars = get_level(int(input("Enter level: ")))
            break
        except Exception:
            continue

    
    while True:
        print("\n=== ASCII ART GENERATOR ===")
        print("1. Image Mode")
        print("2. Video Mode")
        print("q. Quit")
        
        main_choice = input("Select mode: ").lower()
        
        if main_choice == '1':
            image_mode(ascii_chars)
        elif main_choice == '2':
            video_mode(ascii_chars)
        elif main_choice == 'q':
            break
        else:
            print("Invalid choice!")