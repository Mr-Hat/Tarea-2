import getopt
import sys
import subprocess
import os.path

path = "./arp"
check_file = os.path.isfile(path)
if check_file == False:
    arp = open("arp", "x", encoding='utf-8')
    arp = open("arp", "a", encoding='utf-8')
    arp.write("ip:\t\t\t\tmac:")

arp = open("arp", "a", encoding="utf-8")

data = open("manuf", "r", encoding='utf-8')

fabricantes = data.readlines()
def cerrar_el_programa():
    data.close()
    arp.close()
    sys.exit(2)
# Función para obtener los datos de fabricación de una tarjeta de red por IP
def obtener_datos_por_ip(ip):
    try:
        search = subprocess.Popen(["arp","-a",ip],stdout = subprocess.PIPE, stderr= subprocess.PIPE)
        var = ((search.communicate()[0].decode('latin-1').split('Tipo\r\n'))[1]).split('     ')
    except:
        print("Error: ip is outside the host network")
    else:
        MAC = var[1].strip(" ")
        print(MAC)
        IP = var[0].strip(" ")
        flag = True
        obtener_datos_por_mac(MAC, ip = IP, flag = flag)
        
    cerrar_el_programa()

def escribir_tabla_arp(ip, mac):
    out = ip + " " + mac
    arp.write(out)

def obtener_datos_por_mac(mac, *args, **kwargs):
    ip = kwargs.get('ip', None)
    flag = kwargs.get('check', False)
    datos_mac = None
    for fabricante in fabricantes:
        linea = fabricante.split()
        if mac in linea:
            datos_mac = fabricante
    if datos_mac == None:
        print("MAC address :", mac)
        print("Fabricante\t: Not Found")
        cerrar_el_programa()
    else:
        print("MAC address :", datos_mac)
        print("Fabricante\t :", datos_mac)
        if flag:
            out = "\n" +ip + " " + mac
            arp.write(out)

# Función para obtener la tabla ARP
def obtener_tabla_arp():
        try:
            resultado = subprocess.check_output(["arp", "-a"], text=True)
            print(resultado) 
        except subprocess.CalledProcessError as e:
            print(f"Error al obtener la tabla ARP: {e}")
        finally:
            cerrar_el_programa()

def main(argv):
    ip = None
    mac = None
    try:
        opts, args = getopt.getopt(argv, "i:m:a:h:", ["ip=", "mac=", "arp", "help"])

    except getopt.GetoptError:
        #Modificar para coincidir con tarea
        print("Use: python OUILookup.py --ip <IP> | --mac <MAC> | --arp | [--help] \n --ip : IP del host a consultar. \n --Arg2:  \n --Atg3: \n --help:")
        cerrar_el_programa()

    for opt, arg in opts:
        if opt in ("-i", "--ip"):
            ip = arg
        elif opt in ("-m", "--mac"):
            mac = arg
        elif opt in ("-a", "--arp"):
            obtener_tabla_arp()
        elif opt in ("-h", "--help"):
            print("--ip: IP del host a consultar\n--mac: MAC a consultar. P.e. aa:bb:cc:00:00:00.\n--arp: muestra los fabricantes de los host disponibles en la tabla arp\n--help: muestra este mensaje y termina")
            cerrar_el_programa()
    if ip:
        obtener_datos_por_ip(ip)
    elif mac:
        obtener_datos_por_mac(mac)
    else:
        print("Debe proporcionar una opción válida (-i, -m o -a).")

if __name__ == "__main__":
    main(sys.argv[1:])