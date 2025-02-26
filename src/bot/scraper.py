from src.bot.utils import wait_for_element_located, wait_for_elements_located,get_number
from src.exceptions import ScraperError, ElementInteractionError
from selenium.webdriver.remote.webelement import WebElement

import re

def scrape_data(driver, selector : str, timeout:int)->tuple[WebElement, list[WebElement]]:
    
    try:
        messages = wait_for_elements_located(parent=driver, selector=selector, timeout=timeout)

    except TimeoutError as e:

        raise ScraperError (f"Error (scraper) en el tiempo de ejecucion : {e}")

    except ElementInteractionError as e:

        raise ScraperError (f"Error (scraper) en la interaccion del elemento: {e}")

    except Exception as e:

        raise ScraperError (f"Error (scraper) inesperado en scrape : {e}")

    finally:
        return (messages[-1],messages) if messages else (None,None)
    
def scrape_data_info_btn(driver, selector : str,selector_btn : str, timeout:int)->bool:
    try:
        container_btns = wait_for_element_located(driver=driver, selector=selector, timeout=timeout)
        btns = wait_for_elements_located(parent=container_btns,selector=selector_btn,timeout=timeout)

    except TimeoutError as e:

        raise ScraperError (f"Error (scraper) en el tiempo de ejecucion : {e}")

    except ElementInteractionError as e:

        raise ScraperError (f"Error (scraper) en la interaccion del elemento: {e}")

    except Exception as e:

        raise ScraperError (f"Error (scraper) inesperado en scrape : {e}")

    finally:
        return True if btns else False

def scrape_data_parent(parent,child : str, timeout:int)->list[WebElement]:
    children = []

    try:
        children = wait_for_elements_located(parent=parent,selector=child,timeout=timeout)

    except TimeoutError as e:

        raise ScraperError (f"Error (scraper) en el tiempo de ejecucion : {e}")

    except ElementInteractionError as e:

        raise ScraperError (f"Error (scraper) en la interaccion del elemento: {e}")

    except Exception as e:

        raise ScraperError (f"Error (scraper) inesperado en scrape : {e}")

    finally:
        return children

def scrape_data_info_list_txt (driver,list_data: list, selector : str,selector_item : str, timeout:int, filter_regex = r'^\+?\d{1,3}[\s-]?\d+([\s-]?\d+)+$')->list:
    
    try:
        parent = wait_for_element_located(driver=driver, selector=selector, timeout=timeout)
        children = wait_for_elements_located(parent=parent,selector=selector_item,timeout=timeout)
    
        if children:
            for child in children:
                txt = child.text.strip()
                #mejorar el filrado
                if txt:
                    if re.match(filter_regex,txt):
                        list_data.append(txt)
                    else:
                        list_data.append(txt)
        else:
            raise ScraperError (f"En {parent.tag_name} no se encontro a {selector_item}")

    except TimeoutError as e:

        raise ScraperError (f"Error (scraper@scrape_data_info_list_txt) en el tiempo de ejecucion : {e}")

    except ElementInteractionError as e:

        raise ScraperError (f"Error (scraper@scrape_data_info_list_txt) en la interaccion del elemento: {e}")

    except Exception as e:

        raise ScraperError (f"Error (scraper@scrape_data_info_list_txt) inesperado en scrape : {e}")

    finally:
        return list_data
    
def scrape_element(driver, selector : str, timeout:int):
    try:
        
        element = wait_for_element_located(driver=driver,selector=selector, timeout=timeout)

    except TimeoutError as e:

        raise ScraperError (f"Error (scraper) en el tiempo de ejecucion : {e}")

    except ElementInteractionError as e:

        raise ScraperError (f"Error (scraper) en la interaccion del elemento: {e}")

    except Exception as e:

        raise ScraperError (f"Error (scraper) inesperado en scrape : {e}")

    finally:

        return element
   
def scrape_elements(driver, selector : str, timeout:int)->list[WebElement]:
    elements = []

    try:
        
        elements = wait_for_elements_located(parent=driver,selector=selector, timeout=timeout)

    except TimeoutError as e:

        raise ScraperError (f"Error (scraper) en el tiempo de ejecucion : {e}")

    except ElementInteractionError as e:

        raise ScraperError (f"Error (scraper) en la interaccion del elemento: {e}")

    except Exception as e:

        raise ScraperError (f"Error (scraper) inesperado en scrape : {e}")

    finally:

        return elements
    
def scrape_data_size_list_member(driver, selector:str,timeout:int)->int:
    
    element = scrape_element(driver=driver,selector=selector,timeout=timeout)

    if not element:
        print(f"No se encontro {selector}")
        return 0
    
    text = element.text
    return get_number(texto=text)