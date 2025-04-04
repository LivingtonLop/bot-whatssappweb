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
import pyautogui
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

    @handle_exceptions(NoSuchElementException,StaleElementReferenceException, WebDriverException)
    def scrolling_to_scrape_data(self,container_member:WebElement,xpath_items:str,xpath_id_name:str)->list:
        """
        Se le pasa valores, para el scrolleo

        """    
        estadistica_pos = 1.2
        scroll_prox = -1500
        stop_while = False
        coor_porcentaje = 0.37
        data_set = set() #este contendra dos cosas, miembros -> list, admisn -> list

        #iniciando observer/reconectando
        self.driver.execute_script("window.flagListMember(arguments[0]);",container_member)
        # Forzar el primer cambio
        if not self.driver.execute_script("return window.listMemberResponse;"): #se supone que sea false, para oblgarl aentra en el bucle, sino es true no se hace nada
            self.driver.execute_script("window.listMemberResponse = true;")

        #scrolling
        while not stop_while:
            if self.driver.execute_script("return window.listMemberResponse;"):

                items = self.utils.wait_to_presence_of_all_elements_located(selector= xpath_items)

                if not items:
                    break
                
                for i in items:
                    
                    id_or_name :WebElement = self.utils.wait_to_presence_of_element_located(selector=xpath_id_name) #Obtenemos los datos id o nickname 

                    if not id_or_name:
                        continue

                    data_set.add(id_or_name.text)

                element_location = container_member.location
                element_x, element_y = element_location['x'], element_location['y']

                # Calcular las coordenadas absolutas en la pantalla
                absolute_x = element_x *coor_porcentaje
                absolute_y = element_y * estadistica_pos

                self.driver.execute_script("window.listMemberResponse = false;")
                """scrolling o movimiento"""

                pyautogui.moveTo(absolute_x, absolute_y)

                pyautogui.scroll(scroll_prox)

            else:
                stop_while = True
        #desconctando observer
        self.driver.execute_script("window.desconectarObserverListMember();")

        return list(data_set)
    