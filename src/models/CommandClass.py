from selenium import webdriver
from src.models.ActionClass import ActionClass
from src.models.WhatsappWebClass import WhatsAppWebClass
# from selenium.webdriver.remote.webelement import WebElement
import pyperclip
import pyautogui

class CommandClass:

    def __init__(self, driver:webdriver.Chrome,actions:ActionClass,entity:WhatsAppWebClass,config):
        self.driver = driver
        self.actions = actions
        self.entity = entity
        self.config = config
        self.wait_times = config["wait_times"]

    def print_menu_in_chat(self,menu_texto : str):
        """
        Commando para pegar el texto de menu en un elemento input o caja de texto, para su envio al chat
        
        Params:
            menu_texto (str) : El menu del bot
        Return :
            None
        """
        input = self.entity.get_element(selector = self.entity.get_xpath("containers","text_chat"))

        pyperclip.copy(menu_texto)
        """Buscamos el elemnto para escribir el mensaje(caso pegarlo)"""

        input.click()

        pyautogui.hotkey("ctrl", "v")
        """Lo mandamos"""

        self.actions.interaction_input(element = input, value = "ENTER")

    def restringe_chat(self):
        """
        
        Comando para restringir el chat del grupo
            
            Usa el entity, para saber si esta restringido o no

            Y asi reactivar los obervadores (ay que quedan bloqueados o inactivo al detectar spam)

        """

        xpath_info = self.entity.get_xpath(category="buttons",key="open_info_group")
        xpath_group_permission = self.entity.get_xpath(category="buttons",key="group_permission")
        xpath_check = self.entity.get_xpath( category="containers",key="check_input")
        xpath_back = self.entity.get_xpath(category="buttons",key="back")
        xpath_close = self.entity.get_xpath(category="buttons",key="close")
        
        if (xpath_check,xpath_group_permission,xpath_info,xpath_back,xpath_close):
            self.actions.click_in_selector(selector= xpath_info,timeout=self.wait_times["load_labels"])
            self.actions.click_in_selector(selector= xpath_group_permission,timeout=self.wait_times["load_labels"])
            self.actions.click_in_selector(selector= xpath_check,timeout=self.wait_times["load_labels"])
            
            status = self.entity.getValueInputRestringeChat(case=False)
            chatSelector = self.entity.get_xpath("containers","chat")
            if status: #Si es true significa que todos los miembros pueden escribir en el chat.
                """Activar el observer"""
                self.driver.execute_script("window.reiniciarObserver(arguments[0])",chatSelector)

        self.actions.click_in_selector(selector= xpath_back,timeout=self.wait_times["load_labels"])
        self.actions.click_in_selector(selector= xpath_close,timeout=self.wait_times["load_labels"])

    def close_session(self):
        """Algoritmo para cerrar la session de la pagina web"""

        selector_open = self.entity.get_xpath(category="buttons",key="settings")
        selector_close_session = self.entity.get_xpath(category="buttons",key="close_session")
        selector_confirm = self.entity.get_xpath(category="buttons",key="confirm_close_session")
        if (selector_close_session,selector_confirm, selector_open):
            self.actions.click_in_selector(selector= selector_open,timeout=self.wait_times["load_labels"])
            self.actions.click_in_selector(selector= selector_close_session,timeout=self.wait_times["load_labels"])
            self.actions.click_in_selector(selector= selector_confirm,timeout=self.wait_times["load_labels"])

    