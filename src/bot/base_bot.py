from src.models.BotClass import BotClass
from selenium import webdriver
import time
class BaseBot(BotClass):
    
    def __init__(self, config):
        
        self.wait_times : dict = self.config["wait_times"]
        self.driver = webdriver.Chrome(options=self.config["webdriver_options"])
        super().__init__(driver=self.driver,bot_id=config["bot_id"],group_name=config["group_name"], config=config)

    def run(self):
        """Bucle principal Bot"""
        print("Starting bot...")

        self.init_run()
        self.init_threads()

        while not self.stop_run.is_set():
            try:
                """Ejecutamos las verificaciones o funciones"""
                self.process()

            except:
                """Caso de error al realizar las verificaciones o funciones"""
            finally:
                time.sleep(1)

    def init_threads(self):
        """Inicializacion de los hilos"""

    def process(self):
        """Procesos dentro dle bucle principal"""
        # time.sleep(15)

    def init_run(self):

        """Abrir el link, e iniciar session"""
        self.action.perform_login(url=self.config["url_app"])        
        """Buscamos el chat despues de scanear el QR"""
        selector_open = self.whatsappweb.get_xpath(category="buttons",key="open_group")
        
        if not selector_open:
            print("Algo Anda mal, init_run")
            return
        self.action.open_group(selector = selector_open,timeout=self.wait_times["load_labels"])
        """Iniciamos los scripts"""
