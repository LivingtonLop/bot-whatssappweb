from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.bot.decorators import handle_exceptions
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
    WebDriverException,
    MoveTargetOutOfBoundsException,
    ElementNotInteractableException,
    InvalidElementStateException,
)

class Utils:

    def __init__(self, driver:webdriver.Chrome):
        self.driver = driver

    @handle_exceptions(TimeoutException,NoSuchElementException,WebDriverException) 
    def wait_to_presence_of_element_located(self, selector:str,by = By.XPATH, timeout=10)->WebElement:

        """
        Espera a que se localize el elemento dentro WebDriver.

        :param selector: El selector que se utiliza para encontrar el elemento.
        :param by: El tipo de búsqueda (por defecto es By.XPATH).
        :param timeout: Tiempo de espera en segundos (por defecto es 10 segundos).
        
        :return: True si el elemento fue presenciado, de lo contrario False.
        """
        element = WebDriverWait(driver=self.driver,timeout=timeout).until(
            EC.presence_of_element_located((by,selector))
        )

        return element

    @handle_exceptions(TimeoutException,NoSuchElementException,WebDriverException) 
    def wait_to_presence_of_all_elements_located(self, selector:str,by = By.XPATH, timeout=10)->list[WebElement]:
        """
        Espera a que se localizen los elementos dentro WebDriver.

        :param selector: El selector que se utiliza para encontrar el elemento.
        :param by: El tipo de búsqueda (por defecto es By.XPATH).
        :param timeout: Tiempo de espera en segundos (por defecto es 10 segundos).
        
        :return: True si los elementos fue presenciados, de lo contrario False.
        """

        element = WebDriverWait(driver=self.driver,timeout=timeout).until(
            EC.presence_of_all_elements_located((by,selector))
        )

        return element

    @handle_exceptions(TimeoutException,NoSuchElementException,ElementNotInteractableException,WebDriverException) 
    def wait_to_element_to_be_clickable(self, selector:str,by = By.XPATH, timeout=10)->bool:
        """
        Espera a que un elemento sea clickeable en el WebDriver

        :param selector: El selector que se utiliza para encontrar el elemento.
        :param by: El tipo de búsqueda (por defecto es By.XPATH).
        :param timeout: Tiempo de espera en segundos (por defecto es 10 segundos).
        
        :return: True si el elemento es clickeable, de lo contrario False.
        """

        element = WebDriverWait(driver=self.driver,timeout=timeout).until(
            EC.element_to_be_clickable((by,selector))
        )

        element.click()

        return True

    @handle_exceptions(TimeoutException,NoSuchElementException,StaleElementReferenceException,MoveTargetOutOfBoundsException,InvalidElementStateException,WebDriverException) 
    def actionschains_move_to_element(self, element:WebElement, timeout = 2000)->bool:
        """
        Action de moverse al Web Element

        :param element: Elemento donde se va el puntero (accion).
        :param timeout: Tiempo de espera (por defecto es 2000 ).
        
        :return: True si el elemento fue tocado, de lo contrario False, si fallo al tocarlo.
        """
        action = ActionChains(driver=self.driver,duration=timeout)
        action.move_to_element(to_element=element).perform()
        return True
        