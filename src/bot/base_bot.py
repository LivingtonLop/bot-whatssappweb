from src.models.BotClass import BotClass
# from selenium import webdriver
import time

from src.error_logger import ErrorLogger
from src.bot.scripts.scripts_py.load_scripts_js import load_scripts_js  
logger = ErrorLogger()

class BaseBot(BotClass):
    
    def __init__(self, config):
        super().__init__(bot_id=config["bot_id"],group_name=config["group_name"], config=config)
        
    def run(self):
        """Bucle principal Bot"""
        print("Starting bot...")

        self.init_run()
        self.init_threads()

        while not self.stop_run.is_set():
            try:
                """Ejecutamos las verificaciones o funciones"""
                self.pause_event.wait()

            except Exception as e:
                """Caso de error al realizar las verificaciones o funciones"""
                self.case_exception_inwait(e=e)
            finally:
                time.sleep(1)

    def init_threads(self):
        """Inicializacion de los hilos"""

        try:

            self.th_read_chat.start()
            self.th_execute_command_chat.start()

        except Exception as e: 
            print("Error")
            self.case_exception_inwait(e=e)
            self.stop_run.set()

    def case_exception_inwait(self,e):
        """Caso cuando hay una exception inesperada"""
        logger.log(exception=e)
        self.list_commands.bye()
        
    def init_run(self):

        """Abrir el link, e iniciar session"""
        self.action.perform_login(url=self.config["url_app"])        
        """Buscamos el chat despues de scanear el QR"""
        selector_open = self.whatsappweb.get_xpath(category="buttons",key="open_group")
        
        if not selector_open:
            print("Algo Anda mal, init_run")
            return
        self.action.click_in_selector(selector = selector_open,timeout=self.wait_times["load_labels"])
        """Iniciamos los scripts"""
        self.load_scripts()
        self.execute_scripts()

    def load_scripts(self):
        self.driver.execute_script(load_scripts_js(filename="driver_script.js"))
        self.driver.execute_script(load_scripts_js())

    def execute_scripts(self):
        chatSelector = self.whatsappweb.get_xpath(category="containers", key="chat")  # Asegurar que sea un string
        querySelectorMedia = self.whatsappweb.QUERY_SELECTOR_MULTIMEDIA  # Corrección de nombre
        tiempoReset = 3000
        limiteSpam = 10

        execute = """
            if (window.initObserver) { 
                window.initObserver(...arguments); 
            } else { 
                console.warn("initObserver no está definido en window"); 
            }
        """
        self.driver.execute_script(execute, chatSelector, querySelectorMedia, tiempoReset, limiteSpam)
