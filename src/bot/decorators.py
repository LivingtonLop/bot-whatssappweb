from src.exceptions import RunError
from src.error_logger import ErrorLogger
import functools
from typing import Any, Callable, Type

logger = ErrorLogger()

def handle_exceptions(*exception_types: Type[Exception]):
    """Decorador genérico para manejar excepciones de forma uniforme en el bot."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any | bool:
            try:
                return func(*args, **kwargs)
            
            except exception_types as e:
                error_msg = f"⚠️ {type(e).__name__} en {func.__name__}: {e}"
                logger.log(RunError(error_msg, url=kwargs.get("url")))
                return False  # No interrumpe el programa

            except Exception as e:
                error_msg = f"❌ Error inesperado en {func.__name__}: {e}"
                logger.log(RunError(error_msg, url=kwargs.get("url")))
                return False  # No interrumpe el programa

        return wrapper
    return decorator

# Decoradores específicos basados en el decorador genérico

# handle_exceptions_bot = handle_exceptions(
#     TimeoutError, 
#     ElementInteractionError, 
#     NoSuchElementException, 
#     StaleElementReferenceException, 
#     WebDriverException,
#     MoveTargetOutOfBoundsException,
#     ElementNotInteractableException,
#     InvalidElementStateException,
# )

# handle_exceptions_list = handle_exceptions(
#     KeyError, 
#     IndexError, 
#     TypeError, 
#     ValueError
# )

# handle_exceptions_utils = handle_exceptions(
#     TimeoutException, 
#     TimeoutError, 
#     FileNotFoundError, 
#     PermissionError, 
#     OSError, 
#     JSONDecodeError
    
# )
