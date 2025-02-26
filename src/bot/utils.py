from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from src.exceptions import TimeoutError
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
import emoji
import re
from datetime import datetime,timedelta

def wait_for_element_located(driver : WebElement, selector,by = By.XPATH, timeout=10):
    element = None

    try:

        element = WebDriverWait(driver=driver,timeout=timeout).until(
            EC.presence_of_element_located((by,selector))
        )

    except TimeoutException:
        e = TimeoutError(selector=selector, timeout= timeout)
        # print(e)
    else:
        # print(f"\033[1mOK\033[0m Elemento encontrado:){selector}")
        pass
    finally:
        # print("Finalizando la funcion  wait_for_element")   

        return element

def wait_for_elements_located(parent:WebElement, selector,by = By.XPATH, timeout=10):

    elements = []

    try:
        
        elements = WebDriverWait(driver=parent,timeout=timeout).until(
            lambda p : p.find_elements(by=by, value=selector)
        )

    except TimeoutException:
        raise TimeoutError(selector=selector, timeout= timeout)
    
    else:
        # print(f"\033[1mOK\033[0m Elemento encontrado:) {selector}")
        pass
    finally:
        # print("Finalizando la funcion  wait_for_elements")   

        return elements

def wait_element_to_be_clickable(driver, selector,by = By.XPATH, timeout=10)->bool:

    element = None

    try:
        element = WebDriverWait(driver,timeout).until(
            EC.element_to_be_clickable((by,selector))
        )        
        element.click()
        return True
    except TimeoutError as e:
        # print (f"TimeOut : No se ha encontrado el elemento clickleado : {selector}")
        return False
    except Exception as e:
        # raise ElementInteractionError(selector=selector, action="click")
        return False
    finally:
        # print(f"Finalizando la funcion  wait_element_to_be_clickable para : {selector}")
        pass
    
def actionschains_move_to_element(driver, element:WebElement, timeout = 2000)->bool:
    action = None
    try:
        action = ActionChains(driver=driver,duration=timeout)
        action.move_to_element(to_element=element).perform()
        return True
    except TimeoutError as e:
        print (f"TimeOut : No se ha encontrado el elemento para interactuar {e}")
        return False
    finally:
        print("Finalizamos el movimiento o action uwuw")

def is_element_still_valid(element: WebElement) -> bool:
    """Verifica si el elemento aún existe y es válido en el DOM."""
    try:
        return element.is_displayed()  # Si no lanza excepción, el elemento sigue en el DOM
    except (StaleElementReferenceException, NoSuchElementException):
        return False

def remove_emotes(texto):
    texto_sin_emojis = emoji.replace_emoji(texto, "")
    return " ".join(texto_sin_emojis.split()) 

def get_number(texto: str) -> int:
    numeros = re.findall(r'\d+', texto)  # Busca todos los números en el texto
    print(numeros)

    return int(numeros[1]) if len(numeros)>1 else 0  # Convierte el primer número encontrado

def get_author_in_data_id(data_id:str)->str|None:
    try:
        parts = data_id.split("_")

        author_ = parts[-1] if len(parts) > 1 else None
        author_.split("@c.us")[0]
        return author_
    
    except Exception:
        return None
    
def get_type_in_target_message(is_sticker:WebElement|None,is_img:WebElement|None, is_media_play:WebElement|None,is_media_gif:WebElement|None,is_voice_record:WebElement|None)->str|None:

    if is_sticker:
        return "stickers"
    elif is_img:
        return "images"
    elif is_media_play:
        return "videos"
    elif is_media_gif:
        return "gifs"
    elif is_voice_record:
        return "audios"
    else:
        return None

def normalize_number(phone):
    phone = re.sub(r"\D", "", phone)  # Elimina todo lo que no sea dígito
    return phone if phone else None

def find_number_position(number, normalized_members : list):
    normalized_number = normalize_number(number)
    try:
        return normalized_members.index(normalized_number)
    except ValueError:
        return -1
    
def str_to_bool(value:str):
    if value.lower() == "true":
        return True
    elif value.lower() == "false":
        return False
    else:
        return False
    
def get_datetime():
    return datetime.today()

def get_datetime_to_three_days(date:datetime,days = 3):
    return (date + timedelta(days=days)).date()

