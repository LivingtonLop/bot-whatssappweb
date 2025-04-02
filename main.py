from src.error_logger import ErrorLogger
from config import CONFIG as config
from src.bot.base_bot import BaseBot


logger = ErrorLogger()


try:
    """"""
    bot = BaseBot(config=config)

    bot.run()

except Exception as e:
    print(f"🔴 Error inesperado: {e}")
    logger.log(e)

finally:
    print("✅ Ejecución del bot finalizada.")
    bot.driver.quit()
