import random
import string
import json
import base64
import hashlib
from cryptography.fernet import Fernet, InvalidToken


def generar_contraseña(long: int) -> str:
    caracteres = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choices(caracteres, k=long))


def generar_clave_desde_password(password: str) -> bytes:
    hash_password = hashlib.sha256(password.encode()).digest()
    clave = base64.urlsafe_b64encode(hash_password[:32])
    return clave


def cifrar_datos(datos: str, clave: bytes) -> bytes:
    fernet = Fernet(clave)
    return fernet.encrypt(datos.encode())


def descifrar_datos(datos_cifrados: bytes, clave: bytes) -> str:
    try:
        fernet = Fernet(clave)
        return fernet.decrypt(datos_cifrados).decode()
    except InvalidToken:
        return None  # Indica que la clave es incorrecta


def cargar_contraseñas(clave: bytes):
    try:
        with open("contraseñas.json", "rb") as file:
            datos_cifrados = file.read()
        datos_descifrados = descifrar_datos(datos_cifrados, clave)
        return json.loads(datos_descifrados) if datos_descifrados else None
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def guardar_contraseñas(clave: bytes):
    datos_cifrados = cifrar_datos(json.dumps(passwords, indent=4), clave)
    with open("contraseñas.json", "wb") as file:
        file.write(datos_cifrados)


# Solicitar clave al usuario con 3 intentos
intentos = 3
clave_fernet = None
while intentos > 0:
    clave_maestra = input("Introduce tu clave maestra: ")
    clave_fernet = generar_clave_desde_password(clave_maestra)
    passwords = cargar_contraseñas(clave_fernet)

    if passwords is not None:
        break
    else:
        intentos -= 1
        print(f"Clave incorrecta. Intentos restantes: {intentos}")

if intentos == 0:
    print("Has superado el número de intentos. Saliendo...")
    exit()

while True:
    print("--------- Generador de Contraseñas ---------")
    print(
        "Este generador de contraseñas funciona con un menú numérico. Selecciona siempre las opciones por su número."
    )
    print("1- Crear nueva contraseña")
    print("2- Ver una contraseña guardada")
    print("3- Salir")

    while True:
        try:
            opcion = int(input("Selecciona tu opción (1/2/3): "))
            if 1 <= opcion <= 3:
                break
            else:
                print("Opción inválida, elige entre 1, 2 o 3.")
        except ValueError:
            print("Error: Ingresa un número válido.")

    if opcion == 1:
        print(
            "A completar: Título - Usuario - Contraseña Nueva (Sí/No) - Cantidad de dígitos - Calidad de contraseña"
        )
        nombre = input("Título de la contraseña: ")
        usuario = input("Nombre de usuario: ")
        print("1- Generar nueva contraseña")
        print("2- Guardar contraseña existente")
        print("3- Volver al menú principal")

        while True:
            try:
                optionPassword = int(input("Selecciona tu opción (1/2/3): "))
                if 1 <= optionPassword <= 3:
                    break
                else:
                    print("Opción inválida, selecciona entre 1, 2 o 3.")
            except ValueError:
                print("Error: Ingresa un número válido.")

        if optionPassword == 1:
            print("Seleccionaste 1- Generar nueva contraseña")
            while True:
                try:
                    carAm = int(
                        input("Selecciona la cantidad de caracteres (entre 4 y 128): ")
                    )
                    if 4 <= carAm <= 128:
                        break
                    else:
                        print("El valor debe estar entre 4 y 128.")
                except ValueError:
                    print("Error: Ingresa un número válido.")
            nuevaPassword = generar_contraseña(carAm)
            print(f"Contraseña generada: {nuevaPassword}")
        elif optionPassword == 2:
            nuevaPassword = input("Introduce tu contraseña: ")
        elif optionPassword == 3:
            continue  # Volver al menú principal

        passwords.append(
            {"titulo": nombre, "usuario": usuario, "password": nuevaPassword}
        )
        guardar_contraseñas(clave_fernet)
        print("Contraseña guardada con éxito.")

    elif opcion == 2:
        if passwords:
            print("\nLista de contraseñas guardadas:")
            for idx, cred in enumerate(passwords, start=1):
                print(f"{idx}. Título: {cred['titulo']}, Usuario: {cred['usuario']}")

            try:
                seleccion = int(
                    input(
                        "Ingresa el número de la contraseña que quieres ver (0 para volver): "
                    )
                )
                if seleccion == 0:
                    continue
                elif 1 <= seleccion <= len(passwords):
                    print(f"Contraseña: {passwords[seleccion - 1]['password']}")
                else:
                    print("Número inválido.")
            except ValueError:
                print("Error: Ingresa un número válido.")
        else:
            print("No hay contraseñas guardadas aún.")
    elif opcion == 3:
        print("Saliendo...")
        break
