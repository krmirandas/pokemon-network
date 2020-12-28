
import socket
import os
import sys
from codes import *
from seed import *
from bytes import *
from _thread import *
from struct import pack
from random import randint
from socket import timeout

def transmit(conn, message):
    """
    Envía un mensaje.
    Args:
    conn: Socket utilizado.
    message: Mensaje o codigo de envío.
    """
    conn.sendall(message)


def say_hello(conn):
    """
    Envía mensaje de bienvenida.
    Args:
    conn: Socket utilizado.
    """
    transmit(conn, pack('B', codes['hello']))


def send_pregunta_juego(conn):
    """
    Envía un pregunta para inicializar juego.
    Args:
    conn: Socket utilizado.
    """
    transmit(conn, pack('B', codes['question']))


def get_bool_answer(conn):
    """
    Obtiene la la respuesta del usuario.
    Args:
    conn: Socket utilizado.
    Returns:
    (bool) Respuesta.
    """
    return bytes_to_int(conn.recv(1))


def terminate_session(conn):
    """
    Finaliza la sesión con el cliente.
    Args:
    conn: Socket utilizado.
    """
    transmit(conn, pack('B', codes['terminated_session']))


def send_trainers(conn):
    """
    Enviá los entrenadores.
    Args:
    conn: Socket utilizado.
    """
    transmit(conn, pack('B', codes['trainers']) + get_trainers().encode())


def get_user_id(conn):
    """
    Obtiene el identificador del usuario.
    Args:
    conn: Socket utilizado.
    Returns:
    ID elegido.
    """
    user_id = conn.recv(2)
    if user_id[0] == codes['id']:
        return user_id[1]
    raise Exception("Esperaba id")


def get_user_pwd(conn):
    """
    Obtiene la contraseña del usuario.
    Args:
    conn: Socket utilizado.
    Returns:
    La contraseña del usuario.
    """
    user_pwd = conn.recv(1024)
    if user_pwd[0] == codes['password']:
        return user_pwd[1:].decode()
    raise Exception("Esperaba contraseña")


def send_id_no_encontrado(conn):
    """
    Envía mensaje de ID no encontrado.
    Args:
    conn: Socket utilizado.
    """
    transmit(conn, pack('B', codes['id_not_found']))


def send_active_user(conn):
    """
    Envía mesaje de usuario activo.
    Args:
    conn: Socket utilizado.
    """
    transmit(conn, pack('B', codes['active_user']))


def send_confirmation(conn):
    """
    Envía confirmación del servidor.
    Args:
    conn: Socket utilizado.
    """
    transmit(conn, pack('B', codes['yes']))


def send_pass_no_match(conn):
    """
    Envía mesaje de contraseña incorrecta.
    Args:
    conn: Socket utilizado.
    """
    transmit(conn, pack('B', codes['pass_no_match']))


def get_request(conn):
    """
    Obtiene por el socket la solicitud.
    Args:
    conn: Socket utilizado.
    Returns:
    (int) Número de la solicitud.
    """
    solicitud = conn.recv(1)
    return bytes_to_int(solicitud)


def choose_random_pokemon():
    """
    Reegresa un número aleatorio entre [1, len(db_pokemons)].
    Returns:
    (int) Numero positivo entre [1, len(db_pokemons)].
    """
    return randint(1, len(db_pokemons))


def send_pokemon_info(conn, pokemon_row):
    """
    Envía por el socket la fila de los pokemones.
    Args:
    conn: Socket utilizado.
    pokemon_row: Fila de los pokemones.
    """
    info = pack('B', codes['capturing_verification']) + \
        pack('B', pokemon_row) + db_pokemons[pokemon_row][0].encode()
    transmit(conn, info)


def send_all_catched(conn):
    """
    Envía pokemones capturados.
    Args:
    conn: Socket utilizado.
    """
    transmit(conn, pack('B', codes['already_have_all']))


def send_already_have(conn):
    """
    Envía mesaje de pokemon ya capturado.
    Args:
    conn: Socket utilizado.
    """
    transmit(conn, pack('B', codes['already_have_pokemon']))


def send_not_have(conn):
    """
    Envía mensaje de pokemón disponible.
    Args:
    conn: Socket utilizado.
    """
    transmit(conn, pack('B', codes['do_not_have_pokemon']))


def terminate(conn):
    """
    Termina la conexión con el socket.
    Args:
    conn: Socket utilizado.
    """
    terminate_session(conn)
    conn.close()


def send_attempts(conn, n, pokemon_id):
    """
    Envía el número de intentos con el id del pokemon.
    Args:
    conn: Socket utilizado.
    pokemon_id: ID del pokenon.
    n: Número de intentos.
    """
    package = pack('B', codes['attemps']) + \
        pack('B', pokemon_id) + pack('B', n)
    transmit(conn, package)


def send_successful_capture(conn):
    """
    Envía mensaje de captura exitosa.
    Args:
    conn: Socket utilizado.
    """
    transmit(conn, pack('B', codes['captured']))


def send_ran_out_of_attempts(conn):
    """
    Envía mesaje de número que no hay más intentos.
    Args:
    conn: Socket utilizado.
    """
    transmit(conn, pack('B', codes['no_attemps']))


def send_image(conn, pokemon_row):
    """
    Envía a imagen del pomekemon.
    Args:
    conn: Socket utilizado.
    pokemon_row: La fila del pokemon.
    """
    f = open(db_pokemons[pokemon_row][1], "rb")
    tam_image = os.stat(db_pokemons[pokemon_row][1]).st_size
    pack_tam = pack("<L", tam_image)
    l = f.read(1024)
    image = l
    while (l):
        l = f.read(1024)
        image += l
    package = pack('B', codes['captured']) + \
        pack('B', pokemon_row) + pack_tam + image
    transmit(conn, package)
    f.close()


def send_captured_pokemons(conn, id_user):
    """
    Envía los pokemones capturados.
    Args:
    conn: Socket utilizado.
    id_user: Identificador del usuario.
    """
    transmit(conn, pack('B', codes['pokemon_list']) +
             ' '.join(db_Trainers[id_user]['Catched']).encode())


def capture_pokemon(conn, user_id):
    """
    Captura de un pokemón.
    Args:
    conn: Socket utilizado.
    user_id: Identificador del usuario.
    """
    pokemon_row = choose_random_pokemon()
    send_pokemon_info(conn, pokemon_row)
    answer = get_bool_answer(conn)
    if answer == codes['yes']:
        if len(db_Trainers[user_id]["Catched"]) == len(db_pokemons):
            send_all_catched(conn)
            terminate(conn)
        elif pokemon_row in db_Trainers[user_id]["Catched"]:
            send_already_have(conn)
            capture_pokemon(conn, user_id)
        else:
            send_not_have(conn)
            captured = False
            max_attempts = randint(4, 20)
            while not captured and max_attempts > 1:
                captured = randint(0, 10) == 1
                max_attempts -= 1
                if not captured:
                    send_attempts(conn, max_attempts, pokemon_row)
                    try_again = get_bool_answer(conn)
                    if try_again == codes['no']:
                        break
                else:
                    send_successful_capture(conn)
            if not captured and try_again == codes['yes']:
                send_ran_out_of_attempts(conn)
                terminate(conn)
            elif not captured:
                terminate(conn)
            else:
                db_Trainers[user_id]["Catched"].append(db_pokemons[pokemon_row][0])
                save_registers(db_Trainers, "db")
                send_image(conn, pokemon_row)
                transmit(conn, pack('B', codes['terminated_session']))
                conn.close()
                pass

    elif answer == codes['no']:
        conn.sendall(pack('B', codes['terminated_session']))
        conn.close()


def clientthread(conn):
    """
    Función para manejar la conexión de cada cliente.
    Args:
    conn: Socket utilizado.
    """
    try:
        say_hello(conn)
        send_pregunta_juego(conn)
        to_play = get_bool_answer(conn)
        user_id = -1
        if to_play == codes['yes']:
            send_trainers(conn)
            user_id = get_user_id(conn)
            while user_id not in db_Trainers.keys() or db_Trainers[user_id]["Active"]:
                if user_id not in db_Trainers.keys():
                    send_id_no_encontrado(conn)
                elif db_Trainers[user_id]["Active"]:
                    send_active_user(conn)
                user_id = get_user_id(conn)
            db_Trainers[user_id]["Active"] = True
            save_registers(db_Trainers, "db")
            send_confirmation(conn)
            user_pwd = get_user_pwd(conn)
            while not db_Trainers[user_id]["password"] == user_pwd:
                send_pass_no_match(conn)
                user_pwd = get_user_pwd(conn)
            send_confirmation(conn)
            send_captured_pokemons(conn, user_id)
            solicitud = get_request(conn)
            if solicitud == codes['request_pokemon']:
                capture_pokemon(conn, user_id)
            db_Trainers[user_id]["Active"] = False
            save_registers(db_Trainers, "db")
        elif to_play == codes['no']:
            pac = pack('B', 32)
            conn.sendall(pack('B', 32))
            conn.close()
            print("se cerró la conexión")
    except timeout:
        transmit(conn, pack('B', codes['timeout']))
        conn.close()
        print("timeout")
