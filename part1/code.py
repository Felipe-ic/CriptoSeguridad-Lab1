import sys

def cifrado_cesar(texto, desplazamiento):
    resultado = ""

    for caracter in texto:
        if caracter.isalpha():
            base = ord('A') if caracter.isupper() else ord('a')
            nuevo_codigo = (ord(caracter) - base + desplazamiento) % 26 + base
            resultado += chr(nuevo_codigo)
        else:
            resultado += caracter

    return resultado

def main():
    if len(sys.argv) != 3:
        print("Uso: python3 code.py \"<texto>\" <desplazamiento>")
        sys.exit(1)

    texto = sys.argv[1]
    try:
        desplazamiento = int(sys.argv[2])
    except ValueError:
        print("Error: El desplazamiento debe ser un número entero.")
        sys.exit(1)

    texto_cifrado = cifrado_cesar(texto, desplazamiento)
    print("Texto cifrado:", texto_cifrado)

if __name__ == "__main__":
    main()

