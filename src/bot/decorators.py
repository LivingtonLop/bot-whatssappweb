from src.exceptions import RunError, TimeoutError, ElementInteractionError
from src.error_logger import ErrorLogger
import functools


logger = ErrorLogger()

def handle_exceptions(func):
    """Decorador para manejar excepciones de manera uniforme en funciones del bot."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        
        except TimeoutError as e:
            error = RunError(f"⏳ Timeout en {func.__name__}", url=kwargs.get("url"))
            logger.log(error)
            # raise error
        
        except ElementInteractionError as e:
            error = RunError(f"🖱️ Fallo de interacción en {func.__name__}", url=kwargs.get("url"))
            logger.log(error)
            # raise error

        except Exception as e:
            error = RunError(f"❌ Error inesperado en {func.__name__}: {e}", url=kwargs.get("url"))
            logger.log(error)
            # raise error

    return wrapper

def handle_exceptions_list(func):
    "Decorator to case list"
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except (KeyError, IndexError) as e:
            error = RunError(f"Error in function '{func.__name__}': {e}")
            logger.log(error)
            return False

        except Exception as e:
            error = RunError(f"❌ Error inesperado en {func.__name__}: {e}", url=kwargs.get("url"))
            logger.log(error)
            return False
            # raise error

    return wrapper
