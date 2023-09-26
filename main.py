import cv2
import os
import time
import pygetwindow as gw
import pyautogui
import subprocess


def register_base_face_width():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    base_face_width = None
    
    while True:
        ret, frame = cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
            if len(faces) > 0:  # If a user is detected
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    base_face_width = w

                cv2.imshow('frame', frame)
                cv2.waitKey(1000)
                break  # Exit the loop once user is detected

    cap.release()
    cv2.destroyAllWindows()
    
    return base_face_width

def reset_zoom():
    pyautogui.hotkey('ctrl', '0')
    time.sleep(0.5)
    print("Zoom Reset to 100%.")

def zoom_application(times=1, zoom_in=True):
    time.sleep(0.5) 

    for _ in range(times):
        if zoom_in:
            pyautogui.hotkey('ctrl', '+')
            print(f"Zoomed In: {_ + 1} times")
        else:
            pyautogui.hotkey('ctrl', '-')
            print(f"Zoomed Out: {_ + 1} times")
        time.sleep(0.1)

def determine_zoom_level(face_width, base_face_width, unit=50):
    """
    Determine the zoom level based on the face width.
    The greater the difference from the base_face_width, the more zooming action.
    """
    diff = face_width - base_face_width
    if diff > 0: # Person is close
        print('Person is close')
        unit=50
        zoom_level = abs(diff) // unit
    else: # Person is far
        print("Person is far")
        unit=25
        zoom_level = abs(diff) // unit
    print(face_width, base_face_width,  diff, zoom_level)
    return zoom_level

def capture_and_zoom(base_face_width=305, timeout=5): # Search for a face 5 times
    print(base_face_width)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    
    start_time = time.time()
    while True:
        ret, frame = cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
            if len(faces) > 0:  # If a user is detected
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

                    reset_zoom()  # Reset zoom to 100% before determining zoom actions.

                    zoom_level = determine_zoom_level(w, base_face_width)  # Pass the base_face_width

                    if w > base_face_width and zoom_level > 0:
                        zoom_application(times=zoom_level, zoom_in=True)
                        print(f"Detected face width: {w}. Zoomed In by {zoom_level} levels.")
                    elif w < base_face_width and zoom_level > 0:
                        zoom_application(times=zoom_level, zoom_in=True)
                        print(f"Detected face width: {w}. Zoomed Out by {zoom_level} levels.")

                cv2.imshow('frame', frame)
                cv2.waitKey(1000)
                break  # Exit the loop once user is detected

            if time.time() - start_time > timeout:  # If timeout is reached
                print("Timeout reached without detecting a face.")
                break  # Exit the loop

    cap.release()
    cv2.destroyAllWindows()

def set_brightness(brightness_level):
    script_path = "C:/Users/Rugved Chavan/Desktop/UVA-Course/HCI Project/set_brightness.ps1"
    subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path, str(brightness_level)])

def open_and_resize(app_path, app_title, width, height, x, y, args=None):
    if args:
        cmd = [app_path] + args
        subprocess.Popen(cmd)
    else:
        os.startfile(app_path)
    
    time.sleep(3)
    windows = [win for win in gw.getWindowsWithTitle('') if app_title in win.title]
    
    if not windows:
        print(f"{app_title} window not found!")
        return

    target_window = windows[0]
    
    if target_window.isMaximized:
        pyautogui.hotkey('alt', 'space')
        time.sleep(0.5)
        pyautogui.press('r')
        time.sleep(0.5)
    
    target_window.resizeTo(width, height)
    target_window.moveTo(x, y)

    capture_and_zoom()



# if __name__ == '__main__':
#     brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
#     vs_code_path = "C:/Users/Rugved Chavan/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Visual Studio Code/Visual Studio Code.lnk"
#     screen_width = pyautogui.size().width
#     screen_height = pyautogui.size().height


#     open_and_resize(brave_path, "Brave", screen_width // 2, screen_height // 2, screen_width // 2, 0, args=["--new-window", "https://www.google.com/"]) 
#     open_and_resize(brave_path, "Brave", screen_width // 2, screen_height // 2, screen_width // 2, screen_height // 2, args=["--new-window", "https://chat.openai.com/"])
#     open_and_resize(vs_code_path, "Visual Studio Code", screen_width // 2, screen_height, 0, 0)

#     set_brightness(100)
