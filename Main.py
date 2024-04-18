import signal
import sys
from EmailSending import send_mail
from Detection import capture_detected, video_recording
from HumanDetection import age_detection
import threading

# Function to handle the signal (Ctrl+C)
def signal_handler(sig, frame):
    video_recording()
    print("Stopping threads...")
    sys.exit(0)

# Register the signal handler for Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

# Create threads for capturing the image and sending the email
capture_thread = threading.Thread(target=capture_detected)
age_thread = threading.Thread(target=age_detection)
send_thread = threading.Thread(target=send_mail)

# Start the threads
capture_thread.start()
age_thread.start()
send_thread.start()