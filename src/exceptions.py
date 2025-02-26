class BotError(Exception):
    """
    Excepción base para todos los errores relacionados con el bot.
    """
    def __init__(self, message="Ha ocurrido un error en el Bot", **context):
        self.context = context  # Diccionario con detalles adicionales
        super().__init__(self.format_message(message))

    def format_message(self, message):
        """Formatea el mensaje con información adicional si existe."""
        if self.context:
            context_info = " | ".join(f"{k}: {v}" for k, v in self.context.items())
            return f"{message} ({context_info})"
        return message

    
class RunError(BotError):
    """
    Excepción para errores al iniciar el bot o cliente de Chrome.
    """
    def __init__(self, message="Error al iniciar el bot", **context):
        super().__init__(message, **context)


class ScraperError(BotError):
    """
    Excepción para errores de scraping o interacción con la web.
    """
    def __init__(self, message="Error en scraping", **context):
        super().__init__(message, **context)


class TimeoutError(ScraperError):
    """
    Excepción específica para errores de tiempo de espera al buscar un elemento.
    """
    def __init__(self, selector, timeout, url=None):
        message = f"Tiempo de espera agotado al buscar '{selector}' después de {timeout} segundos."
        super().__init__(message, selector=selector, timeout=timeout, url=url)


class ElementInteractionError(ScraperError):
    """
    Excepción para errores al interactuar con un elemento en la página.
    """
    def __init__(self, selector, action, url=None):
        message = f"Error al realizar '{action}' en el elemento '{selector}'."
        super().__init__(message, selector=selector, action=action, url=url)
