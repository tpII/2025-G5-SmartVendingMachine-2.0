from util_inf_cam4 import setup as model_setup
from servo_control import setup, open_door, close_door, cleanup
from zmq_communication import setup_communication, send_message, receive_message
from proc_messages import decode_message, encode_difference_message
def start_session(detection_model, detection_counts):
    print("Iniciando nueva sesión...")
    open_door()
    detection_model.capture_and_infer(detection_counts)
    print("Sesión completada.")

def stop_session(detection_model, detection_counts_2):
    print("Realizando la segunda inferencia...")
    detection_model.capture_and_infer(detection_counts_2)
    print("Resultados de la segunda inferencia:", detection_counts_2)

def calculate_difference(detection_counts_1, detection_counts_2):
    difference = {
        key: detection_counts_1.get(key, 0) - detection_counts_2.get(key, 0)
        for key in set(detection_counts_1) | set(detection_counts_2)
    }
    print("Diferencia calculada entre inferencias:", difference)
    return difference



def reset_dictionaries(detection_counts_1, detection_counts_2):
    """
    Reinicia los valores de ambos diccionarios de conteo a cero.

    Args:
        detection_counts_1 (dict): Primer diccionario de detecciones.
        detection_counts_2 (dict): Segundo diccionario de detecciones.
    """
    for key in detection_counts_1.keys():
        detection_counts_1[key] = 0
    for key in detection_counts_2.keys():
        detection_counts_2[key] = 0
    print("Diccionarios de detección reiniciados.")


def decode(command):
    return command.strip().lower()

def main():
    print("Inicializando el sistema...")
    setup()
    detection_model = model_setup(
        onnx_model="nuevobestsm_ir11.onnx", 
        confidence_thres=0.5, 
        iou_thres=0.5, 
        print_thres=0.1
    )
    sockets = setup_communication()
    print("Sistema inicializado correctamente.")

    detection_counts_1 = {"pepsi": 0, "lays": 0, "oreo": 0}
    detection_counts_2 = {"pepsi": 0, "lays": 0, "oreo": 0}

    print("Entrando en modo de escucha.")

    action = "loop"
    while True:
        message = receive_message(sockets["receiver"])
        try:
            action = decode_message(message) if message != "loop" else "loop"
        except ValueError as e:
            print(f"Error al decodificar mensaje: {e}")
            action = "loop"

        if action == "exit":
            print("Saliendo del programa...")
            cleanup()
            break
        elif action == "start":
            try:
                reset_dictionaries(detection_counts_1,detection_counts_2)
                start_session(detection_model, detection_counts_1)
                print("Resultados de la sesión actual:", detection_counts_1)
            except Exception as e:
                print(f"Error al iniciar la sesión: {e}")
            action = "loop"
        elif action == "stop":
            try:
                stop_session(detection_model, detection_counts_2)
                close_door()
                print("Puerta cerrada.")
                difference = calculate_difference(detection_counts_1, detection_counts_2)
                encoded_message = encode_difference_message(difference)
                send_message(sockets["sender"], encoded_message)
                reset_dictionaries(detection_counts_1,detection_counts_2)
            except Exception as e:
                print(f"Error al detener la sesión: {e}")
            action = "loop"


if __name__ == "__main__":
    main()
