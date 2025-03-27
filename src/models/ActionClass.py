from selenium import webdriver
from src.bot.decorators import handle_exceptions
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    WebDriverException,
)

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
    def open_group(self, selector :str, timeout:int):
        
        """
        Abriendo grupo/chat de la url
        Parameters:
            selector (str): Elemento a buscar, o encontrar e interactuar/revisar".
            timeout (int): Tiempo de salida, o tiempo limite de espera a que el elemento sea interactuable        

        """
        if not self.utils.wait_to_element_to_be_clickable(selector = selector,timeout=timeout):
            print(f"Advertencia: No se pudo dar click en {selector} -. Terminando...")
            return
        print("✅ Elemento encontrado y clickeable. Abriendo grupo/chat...")

    
    @handle_exceptions(NoSuchElementException,StaleElementReferenceException, WebDriverException)
    def open_settings(self, selector :str, timeout:int):
        
        """
        Abriendo settings de la url
        Parameters:
            selector (str): Elemento a buscar, o encontrar e interactuar/revisar".
            timeout (int): Tiempo de salida, o tiempo limite de espera a que el elemento sea interactuable        

        """
        if not self.utils.wait_to_element_to_be_clickable(selector = selector,timeout=timeout):
            print(f"Advertencia: No se pudo dar click en {selector} -. Terminando...")
            return
        print("✅ Elemento encontrado y clickeable. Abriendo Settings")

    
    @handle_exceptions(NoSuchElementException,StaleElementReferenceException, WebDriverException)
    def confirm_close_session(self, selector :str, timeout:int):
        
        """
        Confimar
        Parameters:
            selector (str): Elemento a buscar, o encontrar e interactuar/revisar".
            timeout (int): Tiempo de salida, o tiempo limite de espera a que el elemento sea interactuable        

        """
        if not self.utils.wait_to_element_to_be_clickable(selector = selector,timeout=timeout):
            print(f"Advertencia: No se pudo dar click en {selector} . Terminando...")
            return
        print("✅ Elemento encontrado y clickeable. Confirmando el modal...")


    @handle_exceptions(NoSuchElementException,StaleElementReferenceException, WebDriverException)
    def close_session(self, selector :str, timeout:int):
        
        """
        cerrando session
        Parameters:
            selector (str): Elemento a buscar, o encontrar e interactuar/revisar".
            timeout (int): Tiempo de salida, o tiempo limite de espera a que el elemento sea interactuable        

        """
        if not self.utils.wait_to_element_to_be_clickable(selector = selector,timeout=timeout):
            print(f"Advertencia: No se pudo dar click en {selector} . Terminando...")
            return
        print("✅ Elemento encontrado y clickeable. cerrando session...")

    