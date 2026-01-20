import zmq

def run_client(backend_ip="127.0.0.1", backend_port=5555):
    """
    Cliente ZeroMQ que escucha mensajes del backend y responde con un ACK.

    :param backend_ip: Dirección IP del backend.
    :param backend_port: Puerto del backend.
    """
    context = zmq.Context()
    socket = context.socket(zmq.REP)  # Socket REP para recibir mensajes y responder
    socket.bind(f"tcp://{backend_ip}:{backend_port}")

    print(f"Cliente ZeroMQ escuchando en tcp://{backend_ip}:{backend_port}...")

    try:
        while True:
            # Esperar mensaje del backend
            message = socket.recv_string()
            print(f"Mensaje recibido del backend: {message}")

            # Procesar el mensaje recibido
            response = f"ACK: ACK"
            socket.send_string(response)  # Enviar respuesta al backend
            print(f"Respuesta enviada al backend: {response}")

    except KeyboardInterrupt:
        print("\nCliente detenido manualmente.")
    except Exception as e:
        print(f"Error en el cliente: {e}")
    finally:
        socket.close()
        context.term()
        print("Conexión ZeroMQ cerrada.")

if __name__ == "__main__":
    run_client()
