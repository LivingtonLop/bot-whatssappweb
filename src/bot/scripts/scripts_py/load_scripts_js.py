import os
from src.error_logger import ErrorLogger

logger = ErrorLogger()

def load_scripts_js(folder: str = "src/bot/scripts/scripts_js", filename: str = "function_script.js") -> str | None:
    # Verificar que el archivo tenga la extensión correcta
    if not filename.endswith(".js"):
        e = ValueError("Solo se pueden cargar archivos con extensión .js")
        logger.log(exception=e)
        return None  # O podrías hacer `raise e` si prefieres detener la ejecución
    
    # Construir la ruta completa del archivo
    path = os.path.join(folder, filename)

    # Verificar si el archivo existe antes de leerlo
    if not os.path.exists(path):
        e = FileNotFoundError(f"No se encontró el archivo: {path}")
        logger.log(exception=e)
        return None  # O `raise e` si prefieres detener la ejecución

    # Leer y devolver el contenido del archivo
    with open(path, "r", encoding="utf-8") as file:
        return file.read()
