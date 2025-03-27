import os
from selenium import webdriver
from pathlib import Path

# =======================
# 📌 CONFIGURACIONES GENERALES
# =======================
GROUP_NAME = "Artistas [ 2025 ]"
APP_WEB = "https://web.whatsapp.com"
BOT_ID="Tu nickname"
# =======================
# 📌 OPCIONES DE CHROME
# =======================
CHROME_OPTIONS = {
    "zoom": "--force-device-scale-factor=0.35",  # Zoom al 35%
    "maximize": "--start-maximized",
    "user_agent": "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "experimental_options": {
        "prefs": {"translate_whitelists": {}, "translate": {"enabled": False}},
        "excludeSwitches": ["enable-automation"],
        "useAutomationExtension": False
    }
}

# =======================
# 📌 TIEMPOS DE ESPERA
# =======================
WAIT_TIMES = {
    "load_labels": 3,   # Segundos hasta que carga
    "action_duration": 2000,  # Milisegundos de duración de acción
    "thread_timeout": 5,  # Tiempo máximo de espera de un hilo (segundos)
    "audio_limit": 600  # Límite de duración del audio (segundos)
}

# =======================
# 📌 DESCARGAS
# =======================
BASE_DIR = Path(os.getenv("BOT_BASE_DIR", "C:/Users/[Your account]/Documents/bot"))
DOWNLOAD_DIR = BASE_DIR / "downloads" / "sticker"

# =======================
# 📌 OTROS PARÁMETROS
# =======================
SPAM_THRESHOLD = 10
LIMIT_REPEAT = 10
ELEMENTO_EXECUTE_COMMAND = 50
ELEMENTO_MESSAGE = 40

# =======================
# 📌 CONFIGURAR CHROME OPTIONS
# =======================
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(CHROME_OPTIONS["zoom"])
chrome_options.add_argument(CHROME_OPTIONS["maximize"])
chrome_options.add_argument(CHROME_OPTIONS["user_agent"])

# Agregar opciones experimentales
for key, value in CHROME_OPTIONS["experimental_options"].items():
    chrome_options.add_experimental_option(key, value)

# =======================
# 📌 CONFIGURACIÓN FINAL
# =======================
CONFIG = {
    "webdriver_options": chrome_options,
    "url_app": APP_WEB,
    "group_name": GROUP_NAME,
    "wait_times": WAIT_TIMES,
    "download_paths": {
        "absolute": str(DOWNLOAD_DIR),
        "relative": "downloads/sticker"
    },
    "spam_settings": {
        "spam_threshold": SPAM_THRESHOLD,
        "limit_repeat": LIMIT_REPEAT
    },
    "execution_limits": {
        "element_execute_command": ELEMENTO_EXECUTE_COMMAND,
        "element_message": ELEMENTO_MESSAGE
    }
}
