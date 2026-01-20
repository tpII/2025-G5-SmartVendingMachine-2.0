import cv2
from ultralytics import YOLO


# CONFIGURACIÓN

MODEL_PATH = "C:/Users/josep/OneDrive/Desktop/Pruebamodel/nuevobestsm_ir11.onnx"
CONF_THRESHOLD = 0.7  # confianza mínima
IOU_THRESHOLD = 0.5   # para NMS
CLASS_NAMES = ["lays", "oreo", "pepsi"]
COLORS = [(0, 255, 0), (0, 0, 255), (255, 0, 0)]


# CARGAR MODELO

model = YOLO(MODEL_PATH)


# CÁMARA

cap = cv2.VideoCapture(1)
if not cap.isOpened():
    print("No se pudo acceder a la cámara.")
    exit()
print("Cámara encendida. Presiona 'q' para salir.")

# Definir tamaño de salida de la ventana
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error al leer el fotograma.")
        break

    # Redimensionar el frame capturado para que se ajuste a la ventana
    frame_resized = cv2.resize(frame, (WINDOW_WIDTH, WINDOW_HEIGHT))

    # Inferencia y dibujar cajas sobre frame_resized
    results = model.predict(frame_resized, conf=CONF_THRESHOLD, verbose=False)

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


# BUCLE PRINCIPAL

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error al leer el fotograma.")
        break

    # Inferencia
    results = model.predict(frame, conf=CONF_THRESHOLD, iou=IOU_THRESHOLD, verbose=False)

    # Dibujar detecciones
    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()
        scores = result.boxes.conf.cpu().numpy()
        classes = result.boxes.cls.cpu().numpy()

        for box, score, cls in zip(boxes, scores, classes):
            x1, y1, x2, y2 = map(int, box)
            cls = int(cls)
            color = COLORS[cls % len(COLORS)]
            label = f"{CLASS_NAMES[cls]} {score:.2f}"
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    cv2.imshow("Detección YOLO (ONNX)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# LIMPIEZA

cap.release()
cv2.destroyAllWindows()
print("Finalizado.")
