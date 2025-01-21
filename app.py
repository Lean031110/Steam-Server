import os
import shutil
import subprocess
import re
import json # Use this if the settings are in JSON.
#import configparser # Use this if the settings are in INI.

def get_steam_path():
    """Intenta encontrar la ruta de instalación de Steam."""
    steam_path = os.path.expandvars(r'%ProgramFiles(x86)%\Steam')
    if os.path.exists(steam_path):
        return steam_path
    steam_path = os.path.expandvars(r'%ProgramFiles%\Steam')
    if os.path.exists(steam_path):
        return steam_path
    # Agrega más posibles rutas si es necesario
    print("Steam no encontrada, por favor especifica la ruta")
    return input("Ruta de steam:")


def get_steam_config_file():
    """Busca el archivo de configuración de Steam."""
    steam_path = get_steam_path()
    config_file = os.path.join(steam_path, "config", "config.vdf")  # Reemplaza esto por la ruta real del archivo
    if os.path.exists(config_file):
         return config_file
    config_file = os.path.join(steam_path, "config","loginusers.vdf")
    if os.path.exists(config_file):
        return config_file
    config_file = os.path.join(steam_path,"steamapps","common","steamclient.config") # Reemplaza esto por la ruta real del archivo
    if os.path.exists(config_file):
         return config_file
    # Agrega más opciones
    print("Archivo de configuración no encontrado. Especifica la ruta manualmente")
    return input("Ruta de archivo de configuración:")


def modify_steam_config(config_file, new_server_address):
    """Modifica la configuración de Steam para usar el servidor local."""
    try:
        # Implementa la lógica especifica para analizar y modificar el archivo de configuracion
        # Esto depende del formato del archivo de configuracion

        with open(config_file, 'r') as f:
            config_content = f.read()

        # Ejemplo con una modificacion simple usando re, necesitaras conocer el formato del archivo para hacerlo correctamente.
        modified_content = re.sub(r'"last_server"\s+"[^"]+"', f'"last_server" "{new_server_address}"', config_content)

        with open(config_file, 'w') as f:
             f.write(modified_content)

        print("Configuración modificada correctamente")

    except Exception as e:
        print(f"Error al modificar la configuración: {e}")

def launch_steam():
    """Lanza el cliente de Steam."""
    try:
        steam_path = get_steam_path()
        steam_exe_path = os.path.join(steam_path, "steam.exe") # Reemplaza esto si el ejecutable esta en otra ruta
        subprocess.Popen(steam_exe_path)
        print("Cliente de Steam lanzado correctamente")
    except Exception as e:
        print(f"Error al lanzar Steam: {e}")

def main():
    new_server_address = "127.0.0.1:5000" #Reemplaza esto por la address de tu servidor local
    config_file = get_steam_config_file()
    if config_file:
      modify_steam_config(config_file, new_server_address)
      launch_steam()

if __name__ == '__main__':
    main()
