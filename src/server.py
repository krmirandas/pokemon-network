# -*- coding: utf-8 -*-

import socket
import os
import sys
from codes import *
from seed import *
from bytes import *
from seed import *
from _thread import *
from struct import pack
from random import randint
from socket import timeout
import pickle
from connection import *
from pokemons import *

class Server(Connection):
    """
    Clase que representa al servidor
    """

    def __init__(self,host='127.0.0.1',port=9999):
        """
        Parámetros:
        host: string
                Dirección en la que se realizarán las conexiones (default localhost)
        port: int
                Puerto en el que se realizarán las conexiones (default 9999)
        """
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def serve(self):
        """
        Empezar la comunicación.
        """
        self.socket.bind((self.host,self.port)) #enlaza el socket con la dirección
        self.socket.listen(5)                   #escucha las conexiones hechas al socket
        while True:
            conn, addr = self.socket.accept()
            conn.settimeout(15)
            print("Host: " + addr[0] + "\nPuerto:" + str(addr[1]))
            start_new_thread(clientthread, (conn,))


if __name__ == '__main__':

    server = Server()
    server.serve()
