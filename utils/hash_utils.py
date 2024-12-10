# utils/hash_utils.py
import hashlib


def generate_unique_id(name, organizationName):
    # Crear una cadena a partir de los datos y generar el hash
    unique_str = f"{name}-{organizationName}"
    # Hash MD5 como identificador único
    return hashlib.md5(unique_str.encode()).hexdigest()
