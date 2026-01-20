import cv2
from ultralytics import YOLO


# CONFIGURACIÓN
MODEL_PATH = r "C:/Users/OneDrive/Desktop/Pruebamodel/nuevobestsm_ir11.onnx"
CONF_THRESHOLD = 0.5
IOU_THRESHOLD = 0.5
CLASS_NAMES = ["lays", "oreo", "pepsi"]
COLORS = [(0, 255, 0), (0, 0, 255), (255, 0, 0)]

# CARGAR MODELO
model = YOLO(MODEL_PATH)

# CÁMARA (USB)
cap = cv2.VideoCapture(1)   # si no funciona, prueba con 1,2,3...
if not cap.isOpened():
    print("No se pudo acceder a la cámara.")
    exit()
print("Cámara encendida. Presiona 'q' para salir.")

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# BUCLE PRINCIPAL (solo uno)
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error al leer el fotograma.")
        break

    # Redimensionar para mostrar
    frame_resized = cv2.resize(frame, (WINDOW_WIDTH, WINDOW_HEIGHT))

    # Inferencia YOLO
    results = model.predict(frame_resized, conf=CONF_THRESHOLD, iou=IOU_THRESHOLD, verbose=False)

    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()
        scores = result.boxes.conf.cpu().numpy()
        classes = result.boxes.cls.cpu().numpy()

        for box, score, cls in zip(boxes, scores, classes):
            x1, y1, x2, y2 = map(int, box)
            cls = int(cls)

            color = COLORS[cls % len(COLORS)]
            label = f"{CLASS_NAMES[cls]} {score:.2f}"

            cv2.rectangle(frame_resized, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame_resized, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    cv2.imshow("Detección YOLO (ONNX)", frame_resized)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# LIMPIEZA
cap.release()
cv2.destroyAllWindows()
print("Finalizado.")
