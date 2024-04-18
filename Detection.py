from datetime import datetime
import cv2
import numpy as np
from HumanDetection import age_detect

net = cv2.dnn.readNet("training_model.weights", "config.cfg")
classes = ["Weapon"]

output_layer_names = net.getUnconnectedOutLayersNames()
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# Camera Selection
def value():
    val = input("Enter file name or press enter to start webcam : \n")
    if val == "":
        val = 0
    return val

cap = cv2.VideoCapture(value())

def current_time():
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    return 'record/CLIP_' + current_time + '.mp4'

# Video Recording
frames = []

def video_recording():
    if not frames:
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
 
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
    video_out = cv2.VideoWriter(current_time(), fourcc, 20.0, (width, height))

    for frame in frames:
        video_out.write(frame)
    
    print(frames)
    frames.clear()
    video_out.release()
    return

# Image Capturing
def image_capturing(img):
    name = 'weapon' + '.png'
    cv2.imwrite(name, img)
    print("Weapon detected in frame")

# Main functionalities...
def capture_detected():

    global video_name 
    while cap.isOpened():
        success, img = cap.read()
        if not success:
            print("Error: Failed to read a frame from the video source.")
            break

        height, width, channels = img.shape
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

        net.setInput(blob)
        outs = net.forward(output_layer_names)

        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        print(indexes)

        # Decided to detect
        if indexes == 0 or indexes == 1 or indexes == 2:
            # Image capture
            image_capturing(img)
            age_detect.set()

            # Video write
            frames.append(img)
        else:
            video_recording()

        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                color = colors[class_ids[i]]
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, label, (x, y + 30), font, 3, color, 3)

        # frame = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
        cv2.imshow("Image", img)
        cv2.waitKey(1)

    cap.release()  # Release the video writer
    cv2.destroyAllWindows()
