import pygetwindow as gw
import win32gui
import win32con
from PIL import ImageGrab
import time
import os
import subprocess
import ctypes  # For getting screen dimensions
import cv2

# Get screen dimensions
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

# Create startupinfo to hide windows
startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
startupinfo.wShowWindow = subprocess.SW_HIDE

# Commands with full "
command = "./main.py"
http_server_cmd = "http-server"
output_folder = "./"
count = False
run = True

def is_window_focused(window_handle):
    return window_handle == win32gui.GetForegroundWindow()

# Start http-server hidden
subprocess.Popen(http_server_cmd, shell=True, startupinfo=startupinfo)

# Start the main loop
while (True):
    if (count == True and run == True):
        # Run emotion classifier hidden
        subprocess.Popen(f"python {command}", shell=True, startupinfo=startupinfo)
        time.sleep(5)  # Wait for processing to complete
    time.sleep(1)
    print("Searching for Zoom window...")
    
    # Find Zoom windows with more flexible title matching
    zoom_windows = [w for w in gw.getAllWindows() 
                   if w.title and ('zoom workplace' in w.title.lower() or 'zoom meeting' in w.title.lower())]
    
    print(f"Found {len(zoom_windows)} potential Zoom windows: {[w.title for w in zoom_windows]}")
    try:
        if not zoom_windows:
            print("No Zoom windows found.")
            continue  # Skip to next iteration if no windows found
            
        # Select the first matching window
        zoom_window = zoom_windows[0]
        zoom_window_handle = zoom_window._hWnd
        print(f"Working with window: '{zoom_window.title}'")
        
        # Force window to normal state first
        if (count == False):
            win32gui.ShowWindow(zoom_window_handle, win32con.SW_RESTORE)
            time.sleep(0.5)
            win32gui.SetForegroundWindow(zoom_window_handle)
            time.sleep(0.5)
            count = True
            
        
        # Check if Zoom is the active window
        if not is_window_focused(zoom_window_handle):
            print("Zoom is not the focused window, skipping screenshot")
            run = False
            continue
        
        # Calculate window size (16:9 aspect ratio) and position
        window_width = int(screen_width * 0.8)  # 80% of screen width
        window_height = int(window_width * 9/16)  # 16:9 aspect ratio
        window_x = screen_width - window_width
        window_y = screen_height - window_height
        

        # Bring to foreground
        time.sleep(0.5)
        
        # Get window position and dimensions
        left, top, right, bottom = win32gui.GetWindowRect(zoom_window_handle)
        
        # Add padding to exclude window borders and title bar
        padding_x = 8  # Adjust these values based on your system
        padding_y = 32  # Adjust these values based on your system
        bbox = (left + padding_x, top + padding_y, right - padding_x, bottom - padding_x)
        
        print(f"Capturing area: ({bbox[0]}, {bbox[1]}) to ({bbox[2]}, {bbox[3]})")
        
        # Take screenshot
        img = ImageGrab.grab(bbox)
        screenshot_path = os.path.join(output_folder, f"audience.png")
        img.save(screenshot_path)
        print(f"Screenshot saved as {screenshot_path}")
        run = True
    except Exception as e:
        print(f"Error interacting with Zoom window: {e}")
        run = False


