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
            raise error
        
        except ElementInteractionError as e:
            error = RunError(f"🖱️ Fallo de interacción en {func.__name__}", url=kwargs.get("url"))
            logger.log(error)
            raise error

        except Exception as e:
            error = RunError(f"❌ Error inesperado en {func.__name__}: {e}", url=kwargs.get("url"))
            logger.log(error)
            raise error

    return wrapper


# def with_pause_handling(event_name):
#     def decorator(func):
#         @functools.wraps(func)  # Mantiene el nombre y propiedades originales
#         def wrapper(self, *args, **kwargs):
#             event = getattr(self, event_name, None)
#             if event and hasattr(event, "clear") and hasattr(event, "set"):
#                 event.clear()
#                 result = func(self, *args, **kwargs)
#                 event.set()
#                 return result
#             return func(self, *args, **kwargs)
#         return wrapper
#     return decorator