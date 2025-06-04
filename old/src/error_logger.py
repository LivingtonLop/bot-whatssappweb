import os
import datetime
import traceback

class ErrorLogger:

    """Class para anotar los errores en la ejecucion y asi resolverlos"""

    def __init__(self, log_dir="logs", log_file="errors.log"):
        self.log_dir = log_dir
        self.log_file = os.path.join(log_dir, log_file)

        # Crear el directorio de logs si no existe
        os.makedirs(self.log_dir, exist_ok=True)

    def log(self, exception: Exception):
        """Guarda la excepción en un archivo y muestra en consola."""
        timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        error_type = type(exception).__name__
        error_message = str(exception)
        stack_trace = traceback.format_exc()

        log_entry = f"{timestamp} ERROR: {error_type} - {error_message}\n{stack_trace}\n"

        # Guardar en el archivo de logs
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)

        # Mostrar en consola que el error se registró
        print(f"{timestamp} ERROR registrado en {self.log_file}: {error_type} - {error_message}")
