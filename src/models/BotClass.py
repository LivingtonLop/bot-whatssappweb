import threading as th
import queue
from src.models.CommandClass import CommandClass
from src.models.ActionClass import ActionClass
from src.models.WhatsappWebClass import WhatsAppWebClass
from src.bot.commands import Commands as ListCommands
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException,WebDriverException,JavascriptException

from selenium import webdriver
import time


class BotClass:

    def __init__(self, bot_id,group_name,config):
        
        self.driver = webdriver.Chrome(options=config["webdriver_options"])
        self.wait_times : dict = config["wait_times"]
        
        self.pause_event = th.Event()
        self.pause_event.set()
        self.stop_run = th.Event()
        self.lock = th.Lock()
        
        self.config = config

        #Cola de espera comando
        self.command_queue = queue.Queue()
        self.action =ActionClass(driver=self.driver)
        self.whatsappweb = WhatsAppWebClass(bot_id=bot_id,group_name=group_name,utils=self.action.utils)
        self.commands = CommandClass(driver = self.driver,actions = self.action,entity=self.whatsappweb,config=config)
        self.list_commands = ListCommands(commands=self.commands) #con este se inractua paratrabajar las acciones

        self.create_theards()

    def read_chat(self):
        while not self.stop_run.is_set():
            # self.pause_event.wait()
            """
            Siempre va a leer el chat del grupo, cuando el script de js, tenga un node que pasara el filtro, y si es comando se anotara en una cola
            Para asi, si ya exsiten varias peticiones estas se ejecuten de poco a poco

            """ 
            try:

                target : WebElement = self.driver.execute_script("return window.obtenerYVaciarMensaje();")

                if target:
                    text = target.text
                    if self.detected_author(text = text):
                        self.detected_command(text=text)



            except StaleElementReferenceException as e:
                print(f"Error, problemas con message, posiblemente eliminado {e}")
                continue
            except JavascriptException as e:
                print(f"Error, problemas con scriptos : {e}")
                continue

            time.sleep(1)

    def detected_spam(self):
        while not self.stop_run.is_set():
            """Siempre estara viendo si spamDetected es true o false, un hilo que puede detener todo y ejecutar el comando shh, para restringir el chat """
            spamDetected = self.driver.execute_script("return window.getSpamDetected();")
            if spamDetected:
                """Caso de spam"""
                self.pause_event.clear()

                self.list_commands.shh()
            
                self.pause_event.set()
            time.sleep(1)

    def detected_command(self,text: str):
        """Detectamos el comando en un cadena de string"""
        list_str = text.split("\n")

        if list_str:
            txt_command = next((texto for texto in list_str if texto.startswith("/")), None)

            if txt_command:
                line_command = txt_command[1:]
                is_command, _, arguments = line_command.partition(" ")

                """Verficamos si es comando"""
                if hasattr(self.list_commands, is_command) and callable(getattr(self.list_commands, is_command)):
                    """Agregamos a la cola de espera"""
                    command = getattr(self.list_commands, is_command)
                    self.command_queue.put(lambda args = arguments : command(*args) )

    def detected_author(self,text:str):
        """Detecta el autor con la cadena de string, retornara lo que es ejemplo True para admins y False para miembros"""

    def filtrer_words(self,text:str):
        """Filtra las palabras, si encunetra una dentro de los filtros, procedera a elimianr el mensaje o banear al usuario"""

    def execute_command_chat(self):
        while not self.stop_run.is_set():
            """
            Ejecutará los comandos de la lista
            """
            self.pause_event.wait()
            try:
                command = self.command_queue.get(timeout=1)  # Evita bloqueo indefinido
                """Ejecución del comando"""
                command()
                self.command_queue.task_done()
            except queue.Empty:
                pass  # Evita que el hilo se bloquee si la cola está vacía

    def create_theards(self):
        self.th_read_chat = th.Thread(target=self.read_chat, daemon=True)
        self.th_execute_command_chat = th.Thread(target=self.execute_command_chat, daemon=True)
