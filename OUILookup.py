import getopt
import sys
from subprocess import Popen, PIPE
import os.path
import re

path = "./arp"
check_file = os.path.isfile(path)
if check_file == False:
    arp = open("arp", "x", encoding='utf-8')

arp = open("arp", "a", encoding="utf-8")

data = open("manuf", "r", encoding='utf-8')

fabricantes = data.readlines()
# Función para obtener los datos de fabricación de una tarjeta de red por IP
def obtener_datos_por_ip(ip):
    mac = None
    fabricante_mac = None
    search = Popen(["arp","-a",ip],stdout = PIPE, stderr= PIPE)
    var = ((search.communicate()[0].decode('latin-1').split('Tipo\r\n'))[1]).split('     ')
    MAC = var[2].strip(" ")
    IP = var[0].strip(" ")
    print(MAC)
    print(IP)
    # Implementa la lógica para obtener los datos por IP aquí
    print("Aqui su codigo para obtener los datos por ip")
    pass

# Función para obtener los datos de fabricación de una tarjeta de red por MAC
def obtener_datos_por_mac(mac):
    datos_mac = None
    for fabricante in fabricantes:
        linea = fabricante.split()
        if mac in linea:
            datos_mac = fabricante
    if datos_mac == None:
        print("No se ha encontrado el fabricante")
        sys.exit(2)
    else:
        print("Aqui su codigo para obtener los datos por mac", datos_mac)
        arp.write(datos_mac)
# Función para obtener la tabla ARP
def obtener_tabla_arp():
        # Implementa la lógica para procesar la tabla ARP aquí
        # Imprime la tabla ARP
    pass


def main(argv):
    ip = None
    mac = None
    try:
        opts, args = getopt.getopt(argv, "i:m:a:h:", ["ip=", "mac=", "arp=", "help"])

    except getopt.GetoptError:
        #Modificar para coincidir con tarea
        print("Use: python OUILookup.py --ip <IP> | --mac <MAC> | --arp | [--help] \n --ip : IP del host a consultar. \n --Arg2:  \n --Atg3: \n --help:")
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-i", "--ip"):
            ip = arg
        elif opt in ("-m", "--mac"):
            mac = arg
        elif opt in ("-a", "--arp"):
            arp = arg
        elif opt in ("-h", "--help"):
            print("--ip: IP del host a consultar\n--mac: MAC a consultar. P.e. aa:bb:cc:00:00:00.\n--arp: muestra los fabricantes de los host disponibles en la tabla arp\n--help: muestra este mensaje y termina")
            sys.exit(2)
    if ip:
        obtener_datos_por_ip(ip)
    elif mac:
        obtener_datos_por_mac(mac)
    #elif arp:
        #obtener_tabla_arp()
    else:
        print("Debe proporcionar una opción válida (-i, -m o -a).")

if __name__ == "__main__":
    main(sys.argv[1:])