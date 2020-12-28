import sys

def bytes_to_int(byte_repr):
    """
    Convierte un flujo de bytes a un entero
    Args:
    byte_repr: Arreglo de bytes
    Returns:
    (int) Regresa la conversion de bytes a entero.
    """
    return int.from_bytes(byte_repr, byteorder='little', signed=True)
