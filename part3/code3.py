#!/usr/bin/env python3
import subprocess
import sys

def extraer_mensaje_icmp(archivo):
    # Usamos data.data en lugar de icmp.payload
    comando = ["tshark", "-r", archivo, "-T", "fields", "-e", "data.data"]
    try:
        resultado = subprocess.run(comando, capture_output=True, text=True)
    except FileNotFoundError:
        print("Error al ejecutar tshark. Asegúrate de tener tshark instalado y en PATH.")
        sys.exit(1)

    if resultado.returncode != 0:
        print("Error al leer el archivo pcapng con tshark.")
        print(resultado.stderr)
        sys.exit(1)

    chars = []
    for linea in resultado.stdout.splitlines():
        linea = linea.strip()
        if not linea:
            continue
        # Tomamos solo el primer byte de cada payload
        try:
            primer_byte = int(linea[:2], 16)
            if 32 <= primer_byte <= 126:  # solo ASCII imprimibles
                c = chr(primer_byte)
                if c != 'b':  # ignoramos el delimitador final
                    chars.append(c)
        except ValueError:
            continue

    return "".join(chars)

def descifrar_cesar(texto, corrimiento):
    resultado = ""
    for c in texto:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            resultado += chr((ord(c) - base - corrimiento) % 26 + base)
        else:
            resultado += c
    return resultado

def main():
    if len(sys.argv) != 2:
        print(f"Uso: sudo python3 {sys.argv[0]} <archivo_pcapng>")
        sys.exit(1)

    archivo = sys.argv[1]
    mensaje_cifrado = extraer_mensaje_icmp(archivo)

    if not mensaje_cifrado:
        print("No se pudo extraer ningún carácter válido del archivo.")
        sys.exit(1)

    for corrimiento in range(26):
        descifrado = descifrar_cesar(mensaje_cifrado, corrimiento)
        # Resaltamos en verde si encontramos una palabra clave
        if "criptografia" in descifrado.lower():
            print(f"{corrimiento}\n\033[92m{descifrado}\033[0m")
        else:
            print(f"{corrimiento}\n{descifrado}")

if __name__ == "__main__":
    main()

