from src.bot.base_bot import Bot
from app_web.config import data
from diccionary_data import LIST_BLACK, LIST_GREY,COUNTRY_CODES,LIST_LINK_SPAM,COUNTRY_CODES_SPAM_OR_SCAM
from app_web.WhatssapWebLabels import WhatssappWebLabels
from src.exceptions import BotError, RunError, ScraperError
from src.error_logger import ErrorLogger
from download import Download
from src.data.data_json import DataJson


# Inicializamos el logger
logger = ErrorLogger()

try:
    app_web = WhatssappWebLabels()
    download = Download()  # Edit en el caso de enviarlo a un lugar específico
    data["list_country_code_spam_or_scam"] = COUNTRY_CODES_SPAM_OR_SCAM
    data_json = DataJson(group_name=data["group_name"])

    bot = Bot(
        options=data["options_webdriver_chrome"],
        data=data,
        app_web=app_web,
        list_black=LIST_BLACK,
        list_grey=LIST_GREY,
        dict_country_codes=COUNTRY_CODES,
        list_link_spam=LIST_LINK_SPAM,
        download=download,
        data_json= data_json
    )

    bot.run()
    print("\033[ok\033[0m Bot Corriendo :)")

except RunError as e:
    print(f"❌ Error en el run del bot: {e}")
    logger.log(e)  # Guardamos el error en logs

except ScraperError as e:
    print(f"⚠️ Error en scraping: {e}")
    logger.log(e)

except BotError as e:
    print(f"🚨 Error general del bot: {e}")
    logger.log(e)

except Exception as e:
    print(f"🔴 Error inesperado: {e}")
    logger.log(e)

finally:
    print("✅ Ejecución del bot finalizada.")
