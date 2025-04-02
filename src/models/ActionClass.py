from selenium import webdriver
from src.bot.decorators import handle_exceptions
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    WebDriverException,
)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

from src.utils import Utils

class ActionClass:

    def __init__(self,driver:webdriver.Chrome):
        self.driver = driver
        self.utils = Utils(driver=driver)

    @handle_exceptions(NoSuchElementException,StaleElementReferenceException, WebDriverException)
    def perform_login(self,url:str="https://web.whatsapp.com/"):
        """
        Ingresa a la direccion url y logeate para entrar en la otra fase
        Parameters:
            url (str): Link or url of web. Default is "https://web.whatsapp.com/".
        
        """
        print(f"🌐 Intentando acceder a: {url}")
        self.driver.get(url=url)
        input("🔑 Presiona cualquier tecla después de escanear el código QR de WhatsApp...")
        print("\033[ok\033[0m ✅ Bot dentro de la aplicación web :)")
    
    @handle_exceptions(NoSuchElementException,StaleElementReferenceException, WebDriverException)
    def click_in_selector(self, selector :str, timeout:int):
        
        """
        Abriendo grupo/chat de la url
        Parameters:
            selector (str): Xpath a buscar para darle click/interactuar/revisar 
            timeout (int): Tiempo de salida, o tiempo limite de espera a que el elemento sea interactuable        

        """
        if not self.utils.wait_to_element_to_be_clickable(selector = selector,timeout=timeout):
            print(f"Advertencia: No se pudo dar click en {selector} -. Terminando...")
            return
        print(f"✅ Elemento encontrado y clickeable. {selector} ...")
    

    @handle_exceptions(NoSuchElementException,StaleElementReferenceException, WebDriverException)
    def interaction_input(self, element : WebElement,value : str | tuple, batch_input:int = 0):
        """
        Interaccion con el input
        Parameters:
            element (WebElement): Elemento para interactuar/revisar".
            value (str|tuple) : name del xpath o valor que le quieres poner al input
            batch_input (int) : cuantas ordenes existen en el value
        
        """
        if isinstance(value, tuple):
                    
            keys = [getattr(Keys, key,None) for key in value]

            if keys:
                element.send_keys(*keys)

        else : 
            key = getattr(Keys, value,value)
            if key:
                if batch_input > 0:
                    element.send_keys(key*batch_input)
                else:
                    element.send_keys(key)



    