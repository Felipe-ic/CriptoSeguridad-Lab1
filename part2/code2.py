import subprocess
import sys
import time

IP_DESTINO = "8.8.8.8"
TAMANIO_TRAMA = 56  # Total bytes a enviar. 8 bytes son del header ICMP, 48 serán Data

def generar_payload_hex(caracter):
    # Primer byte: el carácter que queremos ocultar
    payload = [format(ord(caracter), '02x')]

    # ASCII imprimibles desde 0x21 hasta 0x7e (excluyendo 0x20 espacio)
    ascii_imprimibles = [i for i in range(0x21, 0x7f)]

    # Rellenar los siguientes 55 bytes con valores cíclicos del ASCII imprimible
    for i in range(1, TAMANIO_TRAMA):
        payload.append(format(ascii_imprimibles[(i - 1) % len(ascii_imprimibles)], '02x'))

    return ''.join(payload)

def enviar_ping_con_caracter(caracter):
    payload_hex = generar_payload_hex(caracter)
    comando = ['ping', '-c', '1', '-s', str(TAMANIO_TRAMA), '-p', payload_hex, IP_DESTINO]

    try:
        resultado = subprocess.run(comando, capture_output=True, text=True)
        if resultado.returncode == 0:
            print("Sent 1 packets.")
        else:
            print("Failed to send packet.")
    except Exception as e:
        print("Error:", e)

def main():
    if len(sys.argv) != 2:
        print("Uso: sudo python3 pingv4.py \"<mensaje>\"")
        sys.exit(1)

    mensaje = sys.argv[1]

    for caracter in mensaje:
        enviar_ping_con_caracter(caracter)
        time.sleep(0.2)

    enviar_ping_con_caracter('b')  # Delimitador final

if __name__ == "__main__":
    main()

