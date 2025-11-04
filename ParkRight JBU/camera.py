import cv2
import os
from datetime import datetime
from ultralytics import YOLO

# Cargar el modelo YOLOv8
model = YOLO("yolov8n.pt")

# Clases de COCO que nos interesan
COCO_CATEGORIES = {
    2: "car",
    3: "motorcycle"
}

# Crear carpeta 'fotos' si no existe
if not os.path.exists("fotos"):
    os.makedirs("fotos")

def detect_vehicles():
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, verbose=False)

        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                if class_id in COCO_CATEGORIES:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    label = f"{COCO_CATEGORIES[class_id]}"

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow("Detección en tiempo real", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def capture_and_save_photo(carID):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    
    if ret:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"fotos/{carID}_{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Foto guardada: {filename}")

    cap.release()
