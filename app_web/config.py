from selenium import webdriver

"""CONFIGURACION DEL BOT"""

#Variables Constantes (Editables, antes de la ejecucion)

#GROUP_NAME = "Pongamoslo a prueba"
GROUP_NAME = "Artistas [ 2025 ]"

APP_WEB = "https://web.whatsapp.com"
#options
ZOOM = "--force-device-scale-factor=0.35"
MAX = "--start-maximized"
USER_AGENT =  "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
#experimental
NO_TRANSLATE = ("prefs", {"translate_whitelists": {}, "translate": {"enabled": False}})
EXCLUSE_SWITCHES = ("excludeSwitches", ["enable-automation"])
USE_AUTAMTIC_EXTENSION = ("useAutomationExtension",False)
#
TIME_WAIT_TO_LOAD_LABELS = 3 #seconds hasta que carga
TIME_ACTION_DURACION = 2000 #miliseconds mantiene la seleccion

#DOWNLOAD
DOWNLOAD_STICKER = r"C:\Users\[Your Account]\Documents\bot\downloads\sticker"
DOWNLOAD_STICKER_RELATIVE = r"downloads\sticker"

SPAM_THRESHOLD = 10

options = webdriver.ChromeOptions()
options.add_argument(ZOOM)  # Zoom al 25%
options.add_argument(MAX)  # Opcional: inicia el navegador maximizado
# options.add_argument(USE_AUTAMTIC_EXTENSION)  # Opcional: inicia el navegador maximizado

#No autotranslate
options.add_experimental_option(
    NO_TRANSLATE[0],NO_TRANSLATE[1]
)
options.add_experimental_option(
    "excludeSwitches", ["enable-automation"]
)
options.add_experimental_option(
    "useAutomationExtension",False
)

DRIVER_SCRIPT = "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"

data = {
    "options_webdriver_chrome":options,
    "url_app" : APP_WEB,
    "group_name":GROUP_NAME,
    "time_wll" : TIME_WAIT_TO_LOAD_LABELS,
    "time_ad" : TIME_ACTION_DURACION,
    "script":DRIVER_SCRIPT,
    "relative_path_download_sticker" : DOWNLOAD_STICKER,
    "relative_download_sticker" : DOWNLOAD_STICKER_RELATIVE,
    "spam_message" : SPAM_THRESHOLD,
    "limite_repeat":10,
    "elemento_execute_command":50,
    "elemento_message":40,
    "tiempo_maximo_hilo":5,
    "duration_limit_audio":600

}

