import zmq, threading, time
from decouple import config

from ..models import SesionCompra

class DatabaseHandling: 
    def saveSessionProduct(product):
        
        return

class ZMQConnection:
    def __init__(self):
        """
        Inicializa la conexión ZMQ utilizando las variables de entorno definidas.
        """
        # Configuración para recepción de mensajes
        # Almacén de mensajes recibidos
        self.received_messages = []

        # Hilo para escuchar mensajes
        self.listener_thread = None
        

    def send_message(self, message):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)  # Socket REQ para enviar mensajes y recibir respuesta
        socket.connect(f"tcp://127.0.0.1:5555")
        """
        Envía un mensaje a través del socket de envío.
        :param message: Mensaje a enviar (string o bytes).
        :return: Respuesta recibida (si aplica).
        """
        try:
            print(f"Enviando mensaje al cliente: {message}")
            socket.send_string(message)  # Enviar mensaje al cliente

            # Esperar respuesta del cliente
            response = socket.recv_string()
            self.received_messages.append(response)
            print(f"Respuesta del cliente: {response}")
            return response
        except Exception as e:
            print(f"Error al comunicarse con el cliente: {e}")
            return None
        finally:
            socket.close()
            context.term()

    

    def _listen_for_messages(self, m):
        """
        Método interno para recibir mensajes continuamente.
        """
        while True:
            try:
                message = self.recv_string(flags=zmq.NOBLOCK)
                print(f"Mensaje recibido: {message}")
                self.received_messages.append(message)
            except zmq.Again:
                # No hay mensajes disponibles, continuar
                continue

    def get_received_messages(self):
        """
        Devuelve los mensajes recibidos hasta el momento.
        """
        return self.received_messages

    def close_connection(self):
        """
        Cierra ambos sockets y el contexto ZMQ.
        """
        self.send_socket.close()
        self.receive_socket.close()
        self.context.term()
        print("Conexión ZMQ cerrada.")



###################################################################################################
############################################ VERSION 2 ############################################
###################################################################################################

from .message_codec import MessageCodec

# Dejo este modulo por aqui, funciona para enviar y recibir mensajes de ambas partes
# Lo unico el primero que envia el mensaje siempre es el backend. 
class ZMQClient:
    def __init__(self):
        """
        Inicializa las conexiones ZMQ leyendo las configuraciones desde las variables de entorno.
        """
        print("[INFO] Iniciando cliente ZMQ...")

        # Leer configuraciones desde las variables de entorno
        self.ZMQ_IP = config("ZMQ_IP", default="100.78.173.23")
        self.ZMQ_PORT_PUSH = config("ZMQ_PORT_PUSH", cast=int, default=5555)  # Donde envía mensajes
        self.ZMQ_PORT_PULL = config("ZMQ_PORT_PULL", cast=int, default=5556)  # Donde recibe mensajes
        self.ZMQ_TIMEOUT = config("ZMQ_TIMEOUT", cast=int, default=5000)
        print(f"[INFO] Configuración cargada: ZMQ_IP={self.ZMQ_IP}, "
              f"ZMQ_PORT_PUSH={self.ZMQ_PORT_PUSH}, ZMQ_PORT_PULL={self.ZMQ_PORT_PULL}, ZMQ_TIMEOUT={self.ZMQ_TIMEOUT}")

        # Crear contexto de ZMQ
        self.context = zmq.Context()

        print("[INFO] Contexto ZMQ creado.")
        sender = self.context.socket(zmq.PUSH)
        sender.connect("tcp://100.78.173.23:5555")

        # Configurar socket PUSH para enviar mensajes
        #self.push_socket = self.context.socket(zmq.PUSH)
        
        #self.push_socket.connect("tcp://192.168.1.115:5555")
        print(f"[INFO] Socket PUSH conectado a tcp://{self.ZMQ_IP}:{self.ZMQ_PORT_PUSH}")

        # Configurar socket PULL para recibir mensajes
        self.pull_socket = self.context.socket(zmq.PULL)
        self.pull_socket.bind("tcp://*:5556")
        print(f"[INFO] Socket PULL conectado a tcp://{self.ZMQ_IP}:{self.ZMQ_PORT_PULL}")

        # # Iniciar hilo de recepción de mensajes
        # self.running = True
        # self.receive_thread = threading.Thread(target=self._receive_messages, daemon=True)
        # self.receive_thread.start()
        # print("[INFO] Hilo de recepción de mensajes iniciado.")

        # Configuramos el decodificador
        self.codec = MessageCodec()

    def send_message(self, message):
        """
        envia un mensaje a traves del socket push.
        """
        sender = self.context.socket(zmq.PUSH)
        sender.connect("tcp://100.78.173.23:5555")
        try:
            print(f"[INFO] Enviando mensaje: {message}")
            sender.send_string(message)  
            print(f"[INFO] Mensaje enviado correctamente: {message}")
        except zmq.ZMQError as e:
            print(f"[ERROR] Error al enviar mensaje: {e}")
            time.sleep(1)

    def wait_for_message(self):
        """
        Espera un mensaje bloqueando el flujo de ejecución.
        """
        print("[INFO] Esperando mensaje...")
        try:
            message = self.pull_socket.recv_string()
            print(f"[INFO] Mensaje recibido: {message}")
            return message
        except zmq.ZMQError as e:
            print(f"[ERROR] Error al recibir mensaje: {e}")
            return None
        
    # def _receive_messages(self):
    #     """
    #     Hilo dedicado a la recepcin de mensajes de manera no bloqueante.
    #     """
    #     print("[INFO] Iniciando recepcion de mensajes en segundo plano...")
    #     while self.running:
    #         try:
    #             message = self.pull_socket.recv_string(flags=zmq.NOBLOCK)
    #             print(f"[INFO] Mensaje recibido: {message}")

    #         except zmq.Again:
    #             pass

    def close(self):
        """
        Cierra los sockets y el contexto de ZMQ.
        """
        print("[INFO] Cerrando cliente ZMQ...")
        self.running = False
        self.receive_thread.join()
        self.push_socket.close()
        self.pull_socket.close()
        self.context.term()
        print("[INFO] Cliente ZMQ cerrado correctamente.")