import threading as th
import queue
from src.models.CommandClass import CommandClass
from src.models.ActionClass import ActionClass
from src.models.WhatsappWebClass import WhatsAppWebClass

from selenium import webdriver



class BotClass:

    def __init__(self, driver:webdriver.Chrome, bot_id,group_name,config):
        
        self.pause_event = th.Event()
        self.stop_run = th.Event()
        self.lock = th.Lock()
        
        self.config = config

        #Cola de espera comando
        self.command_queue = queue.Queue()
        self.action =ActionClass(driver=driver)
        self.whatsappweb = WhatsAppWebClass(bot_id=bot_id,group_name=group_name)
        self.command = CommandClass(driver = driver,actions = self.action,entity=self.whatsappweb,config=config)

    def read_chat(self):
        while not self.stop_run.is_set():
            # self.pause_event.wait()
            """
            Siempre va a leer el chat del grupo, cuando el script de js, tenga un node que pasara el filtro, y si es comando se anotara en una cola
            Para asi, si ya exsiten varias peticiones estas se ejecuten de poco a poco

            """

    def execute_command_chat(self):
        while not self.stop_run.is_set():
            """
            Ejecutara los comandos de la lista

            """
            if not self.command_queue.empty():
                command = self.command_queue.get()

                """Ejecuacion del comando"""


                self.command_queue.task_done()
                self.command_queue.join()


    def create_theards(self):
        self.th_read_chat = th.Thread(target=self.read_chat, daemon=True)
        self.th_execute_command_chat = th.Thread(target=self.execute_command_chat, daemon=True)
