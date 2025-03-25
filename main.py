from src.error_logger import ErrorLogger
from config import CONFIG as config


logger = ErrorLogger()



try:
    """"""




except Exception as e:
    print(f"🔴 Error inesperado: {e}")
    logger.log(e)

finally:
    print("✅ Ejecución del bot finalizada.")
