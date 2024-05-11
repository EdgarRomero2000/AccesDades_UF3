import os, yaml
import mysql.connector

#metode per obtindre la conexio amb la Base de Dades a partir del arxiu de configuració
def conexio():
    try:
        THIS_PATH = os.path.dirname(os.path.abspath(__file__))
        ruta_fitxer_configuracio = os.path.join(THIS_PATH, 'configuracio.yml')
        config = {}
        with open(ruta_fitxer_configuracio, 'r') as conf:
            config = yaml.safe_load(conf)

        credencials = {}
        
        credencials['host'] = config["base de dades"]["host"]
        credencials['user'] = config["base de dades"]["user"]
        credencials['port'] = config["base de dades"]["port"]
        credencials['password'] = config["base de dades"]["password"]
        credencials['database'] = config["base de dades"]["database"]

        return mysql.connector.connect(
                host=credencials["host"],
                port=credencials['port'],
                user=credencials['user'],
                password=credencials['password'],
                database=credencials['database']
            )
    except Exception as e:
        return{"status":-1,"message":f"Error de connexió:{e}"}