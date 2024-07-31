import cv2
import numpy as np

# Load Yolo
cfg_path = "yolov3.cfg"
weights_path = "yolov3.weights"

net = cv2.dnn.readNet(weights_path, cfg_path)
classes = []

coco = "coco.names"
with open(coco, "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()

# Get the names of the output layers
try:
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
except TypeError:
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

print("YOLO model and class labels loaded successfully.")
print("Output layers:", output_layers)


colors = np.random.uniform(0, 255, size=(len(classes), 3))


# Loading image
#img_path = r"E:\Perception working\Opencv\yolo_object_detection\room_ser.jpg"
img_path = "sample4.jpg"
img = cv2.imread(img_path)

# Store original dimensions
original_height, original_width, _ = img.shape

# Resize image for detection
img = cv2.resize(img, (416, 416))
#img = cv2.resize(img, None, fx=0.4, fy=0.4)
height, width, channels = img.shape


# Detecting objects
blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

net.setInput(blob)
outs = net.forward(output_layers)

# Showing information on the screen
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
font = cv2.FONT_HERSHEY_PLAIN
for i in range(len(boxes)):
    if i in indexes:
        x, y, w, h = boxes[i]
        label = str(classes[class_ids[i]])
        color = colors[class_ids[i]]
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
        cv2.putText(img, label, (x, y + 30), font, 1, color, 2)


# Resize image back to original dimensions
img = cv2.resize(img, (original_width, original_height))

# Save the output image
output_path = "output_sample4.jpg"
cv2.imwrite(output_path, img)
print(f"Output image saved as {output_path}")

# Show image
cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
