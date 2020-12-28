# -*- coding: utf-8 -*-

from codes import *
import argparse
import socket
import sys
from struct import pack
from seed import *
from connection import *
from bytes import *

class Client(Connection):

    def greetting(self):
        """
        Mostrar mensaje de bienvenida que es enviado por el servidor.
        """
        reply = self.socket.recv(1)
        if bytes_to_int(reply) == codes['hello']:
            print("Hola, entrenador, ¿estas listo para ser el mejor entrenador pokemon?. ¡Comencemos!")

    def commence_protocol(self):
        """
        Iniciailiza la conexión con el prótocolo para iniciar la captura
        de pokemones.
        """
        reply = self.socket.recv(1)
        reply = bytes_to_int(reply)
        self.socket.sendall(pack('B', codes['yes']))
        self.receive_list()


    def receive_list(self):
        """
        Recibe la lista personas con las que se jugará.
        """
        reply = self.socket.recv(4096)
        if reply[0] == codes['timeout']:
            print("Ocurrió un timeout en la conexión")
            self.close_connection()
        if reply[0] == codes['trainers']:
            decision = 100
            first = True
            while not self.confirmed_id(decision, first):
                print(reply[1:].decode())
                decision = int(
                    input("Elige el ID de usuario que te corresponde: "))
                if first:
                    first = False

    def confirmed_id(self, decision, first):
        """
        Confirma identificador.
        Args:
        decision: Identificador de la decisión.
        first: Si el usuario ya corresponde a un entrenador.
        Returns:
        (bool) Su el identificador ya fue confirmado.
        """
        self.socket.sendall(pack('B', codes['id']) + pack('B', decision))
        print("Mandando ID...")
        reply = self.socket.recv(1)
        if reply[0] == codes['timeout']:
            print("Ocurrió un timeout en la conexión")
            self.close_connection()
        if bytes_to_int(reply) == codes['id_not_found']:
            if not first:
                print("No se encontró el ID .")
            return False
        elif bytes_to_int(reply) == codes['yes']:
            if not first:
                print("El ID fue encontrado en la base de datos.")
                self.input_password()
            return True
        elif bytes_to_int(reply) == codes['active_user']:
            if not first:
                print(
                    "El ID del usuario corresponde a un entrenador que ya está activo.")
            return False

    def verify_pokemon(self, id_p):
        """
        Verifica si el identificaor del pokemon es válido.
        Args:
        id_p: Identificador del pokemon.
        """
        if id_p > 9 or id_p < 1:
            self.close_connection()
            print("Ocurrió un error de transporte con el socket.")

    def verify_img_code(self, code):
        """
        Verifica si el código el código es de una imagen.
        Args:
        code: Código de la imágen.
        """
        if bytes_to_int(code) == -119:
            self.close_connection()
            print("Ocurrió un error de transporte con el socket.")

    def input_password(self):
        """
        Le pide al usuario su contraseña.
        """
        first = True
        password = ""
        while not self.password_confirmed(password, first):
            password = input("Contraseña: ")
            first = False

    def password_confirmed(self, password, first):
        """
        Verifica la contraseña para así permitir el acceso al juego.
        Args:
        password: Contraseña del usuario
        first: Si es la primera vez que estaba dentro
        Returns:
        (bool) Si pudo acceder a jugar.
        """
        self.socket.sendall(pack('B', codes['password']) + password.encode())
        reply = self.socket.recv(1)
        if reply[0] == codes['timeout']:
            print("Ocurrió un timeout en la conexión")
            self.close_connection()
        if bytes_to_int(reply) == codes['pass_no_match']:
            if not first:
                print("No coincide la contraseña.")
            return False
        elif bytes_to_int(reply) == codes['yes']:
            if not first:
                print("Estás dentro.")

                self.receive_captured_list()

                self.request_capturing()
            return True

    def request_capturing(self):
        """
        Pide que se pueda capturar un pokemon.
        """
        self.socket.sendall(pack('B', codes['request_pokemon']))
        self.receive_pokemon_suggestion()

    def receive_pokemon_suggestion(self):
        """
        Le pregunta al usuario si quiere capturar a ese pokemon.
        """
        reply = self.socket.recv(1024)
        if reply[0] == codes['timeout']:
            print("Ocurrió un timeout en la conexión")
            self.close_connection()
        if reply[0] == codes['capturing_verification']:
            answer = ""
            while answer != "y" and answer != "n":
                answer = input("Quieres capturar al pokemón " +
                               reply[2:].decode() + "? (y/n): ")
            self.send_capturing_answer(answer)
        else:
            raise Exception("Esperaba CAPTURING_VERIFICATION")

    def send_capturing_answer(self, answer):
        """
        Envía al servidor si sí fue capturado o no el pokemon.
        Args:
        answer: Respuesta de si se ha capturado.
        """
        if answer == "y":
            self.socket.sendall(pack('B', codes['yes']))
            self.receive_capturing_validation()
        elif answer == "n":
            self.socket.sendall(pack('B', codes['no']))
            self.receive_session_termination()

    def receive_capturing_validation(self):
        """
        Muestra las posibles opciones sobre la captura de los pokemones
        tales conmo que lo has capturado o no.
        """
        reply = self.socket.recv(1)
        if reply[0] == codes['timeout']:
            print("Ocurrió un timeout en la conexión")
            self.close_connection()
        if bytes_to_int(reply) == codes['already_have_all']:
            print("Ya tenías todos los pokémones. Has completado el juego.")
            self.receive_session_termination()

        elif bytes_to_int(reply) == codes['already_have_pokemon']:
            print("Ya tienes el pokémon sugerido. Intentaré encontrarte otro.")
            self.receive_pokemon_suggestion()

        elif bytes_to_int(reply) == codes['do_not_have_pokemon']:
            print("Tu pokédex no reconoce a este pokémon. Intenta capturarlo!")
            captured = False
            while not captured:
                captured = self.verify_capture()
                if captured:
                    break
                again = ""
                while again != "y" and again != "n":
                    again = input("Quieres tratar de nuevo? (y/n): ")
                if again == "n":
                    self.socket.sendall(pack('B', codes['no']))
                    self.receive_session_termination()
                elif again == "y":
                    self.socket.sendall(pack('B', codes['yes']))
            if captured:
                print("Lo capturaste")
                self.receive_image()
                self.receive_session_termination()


    def send_reception_image(self):
        """
        Muestra un mensaje de que ya envió la imagen.
        """

        self.socket.sendall(pack('B', codes['image_received']))

    def receive_image(self):
        """
        Recibe la imagen del pokemon que fue enviada por el servidor.
        """
        code = self.socket.recv(1)
        self.verify_img_code(code)
        if code[0] == codes['timeout']:
            print("Ocurrió un timeout en la conexión")
            self.close_connection()
        idpokemon = bytes_to_int(self.socket.recv(1))
        self.verify_pokemon(idpokemon)
        tam_image = bytes_to_int(self.socket.recv(4))
        f = open("../.." + str(idpokemon) + ".png", 'wb')
        l = 1
        while(l):
            l = self.socket.recv(1024)
            f.write(l)
        print("Se guardó una imagen del pokémon capturado en el archivo " +
              str(idpokemon) + ".png.")
        f.close()

        print("Sesión terminada.")
        reply = self.socket.recv(1)
        self.close_connection()

    def receive_captured_list(self):
        """
        Muestra los pokemones capturados del socket.
        """
        reply = self.socket.recv(4096)
        print("Pokemon capturados")
        print(reply[1:].decode())


    def verify_capture(self):
        """
        Verifica si se capturó un pokmeon.
        Returns:
        (bool) Si se capturó un pokmeon.
        """
        reply = self.socket.recv(3)
        if reply[0] == codes['timeout']:
            print("Ocurrió un timeout en la conexión")
            self.close_connection()
        if reply[0] == codes['attemps']:
            print("No lo capturaste. Te quedan " +
                  str(reply[-1]) + " intentos.")
            return False
        elif reply[0] == codes['captured']:
            return True
        elif reply[0] == codes['no_attemps']:
            print("Se acabaron los intentos.")
            reply = self.socket.recv(1)
            self.close_connection()

    def receive_session_termination(self):
        """
        Recibe por el socket el estado de que la sesión ya se ha terminado
        """
        reply = self.socket.recv(1)
        if bytes_to_int(reply) == codes['terminated_session'] or bytes_to_int(reply) == codes['timeout']:
            print("Sesión terminada: " +
                  ("timeout" if bytes_to_int(reply) == codes['timeout'] else ""))
            self.close_connection()
        else:
            raise Exception("Esperaba cerrar sesión")



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    print(parser)
    parser.add_argument('--host', type=str, help='Dirección del host')
    args = parser.parse_args()
    host_arg = args.host
    host = 'localhost' if host_arg is None else host_arg

    client = Client(host, 9999)
    client.connect()
    client.greetting()
    client.commence_protocol()
