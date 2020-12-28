import pickle

db_Trainers = {
 1: {
    'name': 'Kevin',
    'lastName': 'Miranda',
    'password': 'password',
    'Active': False,
    'Catched': []
 },
 2: {
    'name': 'Victor',
    'lastName': 'Molina',
    'password': 'password',
    'Active': False,
    'Catched': []
 },
 3: {
    'name': 'Francisco',
    'lastName': 'Licon',
    'password': 'password',
    'Active': False,
    'Catched': []
 },
 4: {
    'name': 'Paulo',
    'lastName': 'Contreras',
    'password': 'password',
    'Active': False,
    'Catched': []
 }
}

db_pokemons = {
    1: ("Pikachu", "../assets/Pikachu.png"),
    2: ("Charizard", "../assets/Charizard.png"),
    3: ("Beedrill", "../assets/Beedrill.png"),
    4: ("Blastoise", "../assets/Blastoise.png"),
    5: ("Cacnea", "../assets/Cacnea.png"),
    6: ("Cyndaquil", "../assets/Cyndaquil.png"),
    7: ("Diglett", "../assets/Diglett.png"),
    8: ("Ekans", "../assets/Ekans.png"),
    9: ("Gastly", "../assets/Gastly.png"),
    10: ("Gengar", "../assets/Gengar.png"),
    11: ("Golem", "../assets/Golem.png"),
    12: ("Ivysaur", "../assets/Ivysaur.png"),
    13: ("Jigglypuff", "../assets/Jigglypuff.png"),
    14: ("Kadabra", "../assets/Kadabra.png"),
    15: ("Magneton", "../assets/Magneton.png"),
    16: ("Meowth", "../assets/Meowth.png"),
    17: ("Pidgey", "../assets/Pidgey.png"),
    18: ("Poliwrath", "../assets/Poliwrath.png"),
    19: ("Primeape", "../assets/Primeape.png"),
    20: ("Psyduck", "../assets/Psyduck.png"),
    21: ("Scizor", "../assets/Scizor.png"),
    22: ("Scyther", "../assets/Scyther.png"),
    23: ("Snorlax", "../assets/Snorlax.png"),
    24: ("Squirtle", "../assets/Squirtle.png"),
    25: ("Chikorita", "../assets/Chikorita.png"),
}

def save_registers(object, name):
    """
    Guarda los registros en un archivo
    Args:
    name: Nombre del archivo
    """
    with open('db/' + name + '.pkl', 'wb') as f:
        pickle.dump(object, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    """
    Carga la base de datos que es un diccionario.
    Args:
    name: Nombre de la base de datos
    Returns:
    El objeto que se serializo.
    """
    with open('DB/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def get_trainers():
    """
    Obtiene la lista de usuarios
    Returns:
    Un (str) con los entrenadores de la base de datos.
    """
    return "\n".join([str(k) + " : " + v["name"] + ' ' + v["lastName"]  for k, v in db_Trainers.items()])

if __name__ == '__main__':
    save_registers(db_Trainers, 'trainers')
    save_registers(db_pokemons, 'pokemon')
