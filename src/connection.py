# -*- coding: utf-8 -*-
import socket
import os
import sys
from codes import *
from _thread import *
from struct import pack
from random import randint
from socket import timeout
import pickle

class Connection:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def bind_socket(self):
        """
        Enlace entre el socket y la dirección
        """
        self.socket.bind((self.host, self.port))


    def _create_socket(self):
        """
        Crear un socket para la comunicación con el servidor.
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return s

    def connect(self):
        """
        El socket se conecta al host y al puerto.
        """
        self.socket.connect((self.host, self.port))
        print("Conectado a " + self.host + " con el puerto "+str(self.port)+"\n")

    def listen_socket(self):
        """
        Escucha conexiones al socket.
        """
        self.socket.listen(5)

    def close_connection(self):
        """
        Cierra la conexión con el socket.
        """
        self.socket.close()
        print("Conexión cerrada.")
        exit()
