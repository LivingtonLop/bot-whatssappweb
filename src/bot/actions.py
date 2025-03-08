import pyautogui
import pyperclip
import re
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from app_web.WhatssapWebLabels import WhatssappWebLabels

# from src.exceptions import TimeoutError, RunError, ElementInteractionError, ScraperError
from src.bot.utils import wait_element_to_be_clickable, wait_element_to_be_clickable,actionschains_move_to_element,remove_emotes,str_to_bool
from src.bot.scraper import scrape_data,scrape_data_info_btn,scrape_element, scrape_data_info_list_txt,scrape_data_parent,scrape_data_size_list_member,scrape_elements
from src.data.data_json import DataJson
# from src.error_logger import ErrorLogger
from src.bot.decorators import handle_exceptions 
from collections import Counter

@handle_exceptions
def perform_login(driver: webdriver.Chrome, url: str):
    print(f"🌐 Intentando acceder a: {url}")
    driver.get(url=url)
    input("🔑 Presiona cualquier tecla después de escanear el código QR de WhatsApp...")
    print("\033[ok\033[0m ✅ Bot dentro de la aplicación web :)")

@handle_exceptions    
def open_group(driver:webdriver.Chrome, data : dict, selector : str):
    if not wait_element_to_be_clickable(driver=driver,selector=selector,timeout=data["time_wll"] ):
        print("Advertencia: No se pudo dar click en click_open_info_group. Terminando...")
        return
    
    print("✅ Elemento encontrado y clickeable. Abriendo grupo...")

@handle_exceptions    
def edit_on_input(element:WebElement, value : str | tuple, batch_input:int = 0):
        
    keys = None
    key = None
    
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

@handle_exceptions    
def read_chat_group(driver:webdriver.Chrome, data: dict, selector:str)->tuple[WebElement|None, list[WebElement]]:

    messages = scrape_data(driver=driver,selector=selector, timeout=data["time_wll"])
    return messages

@handle_exceptions    
def click_open_info_group(driver:webdriver.Chrome, data: dict, selector:str):

    if not wait_element_to_be_clickable(driver=driver, selector=selector, timeout=data["time_wll"]):
        print("Advertencia: No se pudo dar click en click_open_info_group. Terminando...")
        return
    print(f"✅ Elemento encontrado y clickeable. Abriendo Info del grupo :{data["group_name"]}...")
    return True
@handle_exceptions    
def click_see_all_members(driver:webdriver.Chrome, data: dict, selector:str):

    if not wait_element_to_be_clickable(driver=driver, selector=selector, timeout=data["time_wll"]):
        print("Advertencia: No se pudo dar click en click_see_all_members. Terminando...")
        return False
    print(f"✅ Elemento encontrado y clickeable. Abriendo Lista de miembros del grupo :{data["group_name"]}...")
    return True
@handle_exceptions
def close_modal(driver:webdriver.Chrome, data: dict, selector:str):
    
    if not wait_element_to_be_clickable(driver=driver, selector=selector, timeout=data["time_wll"]):
        print("Advertencia: No se pudo dar click en close_modal. Terminando...")
        return

@handle_exceptions
def back_modal(driver:webdriver.Chrome, data: dict, selector:str):
    if not wait_element_to_be_clickable(driver=driver, selector=selector, timeout=data["time_wll"]):
        print("Advertencia: No se pudo dar click en back_modal. Terminando...")
        return

@handle_exceptions
def find_members(dict_country_code:dict,driver:webdriver.Chrome,data: dict, app_web : WhatssappWebLabels)->tuple[list,list]:
    
    members = []
    admins = []

    country_codes = list(dict_country_code.values()) 

    click_open_info_group(driver=driver,data=data,selector=app_web.BTN_INFO_GROUP)
        
    if scrape_data_info_btn(driver=driver, selector=app_web.CONTAINER_INFO_GROUP,selector_btn=app_web.BTN_SEE_OLD_MEMBERS, timeout=data["time_wll"]):
        
        """Caso que sea verdad que solo se pueda ver miembros, viejos, solo obtendremos la info de app_web@DISPLAY_INFO_GROUP"""
        members.clear()
        time.sleep(10)
        members = scrape_data_info_list_txt(driver=driver,list_data = members, selector=app_web.DISPLAY_INFO_GROUP,selector_item=app_web.TXT_INFO_MEMBER, timeout=data["time_wll"])
        
    else:
        members.clear()

        """Buscaremos y daremo click a app_web@BTN_SEE_ALL_MEMBERS"""
        if not click_see_all_members(driver=driver,data=data,selector=app_web.BTN_SEE_ALL_MEMBERS):
            print("Problemas en click see all members @findmembers")
            return
        input_search = scrape_element(driver=driver, selector=app_web.TXT_SOURCE_MEMBERS, timeout=data["time_wll"])

        members = scrape_data_info_list_txt(driver=driver,list_data = members, selector=app_web.CONTAINER_LIST_MEMBERS,selector_item=app_web.TXT_INFO_MEMBER, timeout=data["time_wll"])

        for country_code in country_codes:
            
            edit_on_input(element=input_search, value=country_code)
            time.sleep(10)
            members = scrape_data_info_list_txt(driver=driver,list_data = members, selector=app_web.CONTAINER_LIST_MEMBERS,selector_item=app_web.TXT_INFO_MEMBER, timeout=data["time_wll"])

            range_code = len(country_code)
            for _ in range(range_code):
                edit_on_input(element=input_search, value="BACKSPACE")

        
        close_modal(driver=driver,data=data, selector=app_web.BTN_TO_CLOSE)

    admins = get_admins(admins=admins,driver=driver,data=data, app_web=app_web)

    return (members,admins)
    
@handle_exceptions
def get_member(data: dict, app_web : WhatssappWebLabels, driver:webdriver.Chrome)->tuple[list,list]:
    """Codigo experimental"""
    members= []
    admins = []
    estadistica_pos = 1.2
    scroll_prox = -1500
    stop_while = False
    data_set = set()


    click_open_info_group(driver=driver,data=data,selector=app_web.BTN_INFO_GROUP)

    if scrape_data_info_btn(driver=driver, selector=app_web.CONTAINER_INFO_GROUP,selector_btn=app_web.BTN_SEE_OLD_MEMBERS, timeout=data["time_wll"]):
        
        """Caso que sea verdad que solo se pueda ver miembros, viejos, solo obtendremos la info de app_web@DISPLAY_INFO_GROUP"""
        members.clear()
        time.sleep(10)
        members = scrape_data_info_list_txt(driver=driver,list_data = members, selector=app_web.DISPLAY_INFO_GROUP,selector_item=app_web.TXT_INFO_MEMBER, timeout=data["time_wll"])
        
    else:
        members.clear()

        """Buscaremos y daremo click a app_web@BTN_SEE_ALL_MEMBERS"""
        if not click_see_all_members(driver=driver,data=data,selector=app_web.BTN_SEE_ALL_MEMBERS):
            print("Problemas en click see all members @findmembers")
            return

        """"""
        
        container_member:WebElement = scrape_element(driver=driver,selector=app_web.CONTAINER_LIST_MEMBERS, timeout=data["time_wll"])

        if not container_member:
            return
        #iniciando observer/reconectando
        driver.execute_script("window.flagListMember(arguments[0]);",container_member)
        # Forzar el primer cambio
        if not driver.execute_script("return window.listMemberResponse;"): #se supone que sea false, para oblgarl aentra en el bucle, sino es true no se hace nada
            driver.execute_script("window.listMemberResponse = true;")

        #scrolling
        while not stop_while:
            if driver.execute_script("return window.listMemberResponse;"):
                print("Hubo un cambio")

                """Captacion de datos"""
                items = scrape_elements(driver=container_member,selector=app_web.LISTITEM,timeout=data["time_wll"])

                if not items:
                    break
                
                for i in items:
                    id_or_name = scrape_element(driver=i,selector=app_web.LISTITEM_NAME_OR_ID,timeout=data["time_wll"])
                    if not id_or_name:
                        continue
                    data_set.add(id_or_name.text)

                element_location = container_member.location
                element_x, element_y = element_location['x'], element_location['y']

                # Calcular las coordenadas absolutas en la pantalla
                absolute_x = element_x *0.37
                absolute_y = element_y * estadistica_pos

                driver.execute_script("window.listMemberResponse = false;")
                """scrolling o movimiento"""

                pyautogui.moveTo(absolute_x, absolute_y)

                pyautogui.scroll(scroll_prox)

                time.sleep(3)
            else:
                stop_while = True
        #desconctando observer
        driver.execute_script("window.desconectarObserverListMember();")

    members = list(data_set)
    admins = get_admins(admins=admins,driver=driver,data=data, app_web=app_web)
    
    return (members,admins)

@handle_exceptions
def restringe_chat(driver:webdriver.Chrome,data:dict, app_web:WhatssappWebLabels)->bool:
    click_open_info_group(driver=driver,data=data,selector=app_web.BTN_INFO_GROUP)
    container_bloq_btn = scrape_element(driver=driver,selector=app_web.CONTAINER_CONFIG_GROUP,timeout=data["time_wll"])
    wait_element_to_be_clickable(driver=container_bloq_btn,selector=app_web.BTN_TO_CONFIG_GROUP,timeout=data["time_wll"])
        
    parent = scrape_element(driver=driver,selector=app_web.CONTAINER_OPCIONES_MIEMBROS,timeout=data["time_wll"])
    response = False   
    if parent:
        children = scrape_data_parent(parent=parent, child=app_web.OPTIONES_MIEMBROS_CHILDREN,timeout=data["time_wll"])
          
        if children:
            for child in children:
                #confirmar si ya tiene check o no div role="switch" aria-checked="false"
                if child.text == "Enviar mensajes":        
                    wait_element_to_be_clickable(driver=child,selector=app_web.INPUT_CONFIG_GROUP_CHAT,timeout=data["time_wll"])        
                    check = scrape_element(driver=driver,selector=app_web.CHECK_INPUT_CONFIG_GROUP_CHAT,timeout=data["time_wll"])
                    if check:
                        value = check.get_attribute("aria-checked")
                        print("Se encontro")
                        response = str_to_bool(value=value)
                        break

    back_modal(driver=driver,data=data,selector=app_web.BTN_TO_BACK)
    close_modal(driver=driver,data=data,selector=app_web.BTN_TO_CLOSE)
    return response

@handle_exceptions  
def delete_message_chat(driver: webdriver.Chrome, message_del: WebElement, data: dict, app_web: WhatssappWebLabels):

    if not message_del:
        print("El mensaje no existe, va vacio")
        return
    if not actionschains_move_to_element(driver=driver, element=message_del, timeout=data["time_ad"]):
        print("Advertencia: No se encontro el elemento al que se debe de eliminar. Terminando...")
        return
    if not wait_element_to_be_clickable(driver=driver, selector=app_web.BTN_TO_DISPLAY_MENU_MENSSAGE, timeout=data["time_wll"]):
        print("Advertencia: No se pudo abrir el menú de opciones. Terminando...")
        return
    menu = scrape_element(driver=driver, selector=app_web.CONTAINER_MENU_OPTION_MESSAGE, timeout=data["time_wll"])
    if not menu:
        print("Advertencia: No se encontró el menú. Terminando...")
        return

    li = scrape_data_parent(parent=menu, child=app_web.ELEMENT_UL, timeout=data["time_wll"])
    if not li:
        print("Advertencia: No se encontraron opciones en el menú. Terminando...")
        return

    for option in li:
        if option.text == "Eliminar":
            option.click()

            if not wait_element_to_be_clickable(driver=driver, selector=app_web.BTN_BOTTOM_TO_DELETE_MULTIPLE, timeout=data["time_wll"]):
                print("Advertencia: No se pudo presionar el botón para eliminar múltiples mensajes.")
                return
                
            if not wait_element_to_be_clickable(driver=driver,selector=app_web.BTN_TO_DELETE_TO_ALL,timeout=data["time_wll"]):
                print("Advertencia: No se pudo presionar el botón para eliminar para todos")
                return
            if not wait_element_to_be_clickable(driver=driver,selector=app_web.BTN_TO_DELETE_TO_ALL,timeout=data["time_wll"]):    
                print("Advertencia: No se pudo presionar el botón para eliminar para todos 2")
                    
            if not wait_element_to_be_clickable(driver=driver,selector=app_web.BTN_TO_OK,timeout=data["time_wll"]):
                print("Advertencia: No se pudo presionar el botón OK")    
                
            break  

@handle_exceptions  
def ban_member(driver:webdriver.Chrome,id_member : str,data : dict, app_web : WhatssappWebLabels,json:DataJson):
    selector = f".//span[@title=\"{id_member}\" or contains(text(), \"{id_member}\")]"

    element = None
    parent = None

        
    click_open_info_group(driver=driver,data=data,selector=app_web.BTN_INFO_GROUP)

    if scrape_data_info_btn(driver=driver, selector=app_web.CONTAINER_INFO_GROUP,selector_btn=app_web.BTN_SEE_OLD_MEMBERS, timeout=data["time_wll"]):
        parent = scrape_element(driver=driver, selector=app_web.DISPLAY_INFO_GROUP,timeout=data["time_wll"])    
        if not parent:
            print("Advertencia|Problema: No se pudo acceder a parent en actions@ban_member ")
            return
            
        element = scrape_element(driver=parent, selector=selector,timeout=data["time_wll"])
            
    else:
        if not click_see_all_members(driver=driver,data=data,selector=app_web.BTN_SEE_ALL_MEMBERS):
            print("Problemas en click see all members @findmembers")
            return

        input_search = scrape_element(driver=driver, selector=app_web.TXT_SOURCE_MEMBERS, timeout=data["time_wll"])

        if not input_search:
            print("Advertencia|Problema: No se pudo acceder a input search en actions@ban_member ")
            return
            
        edit_on_input(element=input_search, value=f"{id_member}")
        edit_on_input(element=input_search, value="ENTER")

        parent = scrape_element(driver=driver, selector=app_web.CONTAINER_LIST_MEMBERS,timeout=data["time_wll"])
        if not parent:
            print("Advertencia|Problema: No se pudo acceder a parent en actions@ban_member ")
            return
        time.sleep(10)
        element = scrape_element(driver=parent, selector=selector,timeout=data["time_wll"])
            
    if not element:
        print("Advertencia|Problema: No se pudo acceder al element en actions@ban_member ")
        return


    if not actionschains_move_to_element(driver=driver, element=element, timeout=data["time_ad"]):
        print("Advertencia: No se pudo mover el puntero al elemento ")
        return
                
    # if not wait_element_to_be_clickable(driver=element, selector=app_web.BTN_TO_DISPLAY_MENU_MEMBERS_1, timeout=data["time_wll"]):
    #     print("Advertencia: No se pudo abrir el menú de opciones. Terminando...")
    #     if not wait_element_to_be_clickable(driver=element, selector=app_web.BTN_TO_DISPLAY_MENU_MENSSAGE, timeout=data["time_wll"]):
    #         print("Advertencia: No se pudo abrir el menú de opciones.251")
    #         if not wait_element_to_be_clickable(driver=driver, selector=app_web.BTN_TO_DISPLAY_MENU_MEMBERS_1, timeout=data["time_wll"]):
    #             print("Advertencia: No se pudo abrir el menú de opciones. 253...")
    #             if not wait_element_to_be_clickable(driver=driver, selector=app_web.BTN_TO_DISPLAY_MENU_MENSSAGE, timeout=data["time_wll"]):
    #                 print("Advertencia: No se pudo abrir el menú de opciones. Terminando...255")

    element.click()
        
    menu = scrape_element(driver=driver, selector=app_web.CONTAINER_MENU_OPTION_MESSAGE, timeout=data["time_wll"])
    if not menu:
        print("Advertencia: No se encontró el menú. Terminando...")
        return

    li = scrape_data_parent(parent=menu, child=app_web.ELEMENT_UL, timeout=data["time_wll"])
    if not li:
        print("Advertencia: No se encontraron opciones en el menú. Terminando...")
        return

    for option in li:
        if option.text == "Eliminar":
            option.click()
                
            if not wait_element_to_be_clickable(driver=driver, selector=app_web.BTN_TO_DELETE, timeout=data["time_wll"]):
                print("Advertencia: No se pudo confirmar la primera ventana modal.")
                break
                
                
            if not wait_element_to_be_clickable(driver=driver,selector=app_web.BTN_TO_OK,timeout=data["time_wll"]):
                print("Advertencia: No se pudo presionar OK")
                break    

            break

    close_modal(driver=driver,data=data, selector=app_web.BTN_TO_CLOSE)

    json.ban_member(name=remove_emotes(id_member))

@handle_exceptions  
def promove_member(driver:webdriver.Chrome,id_member : str,data : dict, app_web : WhatssappWebLabels,json:DataJson):    
    selector = f".//span[@title=\"{id_member}\" or contains(text(), \"{id_member}\")]"

    element = None
    parent = None

    click_open_info_group(driver=driver,data=data,selector=app_web.BTN_INFO_GROUP)

    if scrape_data_info_btn(driver=driver, selector=app_web.CONTAINER_INFO_GROUP,selector_btn=app_web.BTN_SEE_OLD_MEMBERS, timeout=data["time_wll"]):
        
        parent = scrape_element(driver=driver, selector=app_web.DISPLAY_INFO_GROUP,timeout=data["time_wll"])
            
        if not parent:
            print("Advertencia|Problema: No se pudo acceder a parent en actions@ban_member ")
            return
        
        time.sleep(10)
        element = scrape_element(driver=parent, selector=selector,timeout=data["time_wll"])
            
    else:
        if not click_see_all_members(driver=driver,data=data,selector=app_web.BTN_SEE_ALL_MEMBERS):
            print("Advertencia: No se pudo dar click en all_members actions@ban_member ")
            return
        input_search = scrape_element(driver=driver, selector=app_web.TXT_SOURCE_MEMBERS, timeout=data["time_wll"])

        if not input_search:
            print("Advertencia|Problema: No se pudo acceder a parent en actions@ban_member ")
            return
            
        edit_on_input(element=input_search, value=f"{id_member}")
        edit_on_input(element=input_search, value="ENTER")

        parent = scrape_element(driver=driver, selector=app_web.CONTAINER_LIST_MEMBERS,timeout=data["time_wll"])
        if not parent:
            print("Advertencia|Problema: No se pudo acceder a parent en actions@ban_member ")
            return
        time.sleep(10)
            
        element = scrape_element(driver=parent, selector=selector,timeout=data["time_wll"])
            
    if not element:
        print("Advertencia|Problema: No se pudo acceder al element en actions@ban_member ")
        return
    time.sleep(1)
    if not actionschains_move_to_element(driver=driver, element=element, timeout=data["time_ad"]):
        print("Advertencia: No se pudo mover el puntero al elemento ")
        return

    if not wait_element_to_be_clickable(driver=driver, selector=app_web.BTN_TO_DISPLAY_MENU_MEMBERS_1, timeout=data["time_wll"]):
        print("Advertencia: No se pudo abrir el menú de opciones. Terminando...")
        element.click()

    menu = scrape_element(driver=driver, selector=app_web.CONTAINER_MENU_OPTION_MESSAGE, timeout=data["time_wll"])
    if not menu:
        print("Advertencia: No se encontró el menú. Terminando...")
        return

    li = scrape_data_parent(parent=menu, child=app_web.ELEMENT_UL, timeout=data["time_wll"])
    if not li:
        print("Advertencia: No se encontraron opciones en el menú. Terminando...")
        return

    for option in li:
        if option.text == "Designar como admin. del grupo":
            option.click()

            if not wait_element_to_be_clickable(driver=driver, selector=app_web.BTN_TO_ASIGN_ADMIN, timeout=data["time_wll"]):
                print("Advertencia: No se pudo confirmar la primera ventana modal.")
                return

            if not wait_element_to_be_clickable(driver=driver,selector=app_web.BTN_TO_OK,timeout=data["time_wll"]):
                print("Advertencia: No se pudo presionar OK")
                break    

    
    close_modal(driver=driver,data=data, selector=app_web.BTN_TO_CLOSE)
    json.promote_member(name=remove_emotes(id_member))

@handle_exceptions  
def depromove_member(driver:webdriver.Chrome,id_member : str,data : dict, app_web : WhatssappWebLabels,json:DataJson):
    
    selector = f".//span[@title=\"{id_member}\" or contains(text(), \"{id_member}\")]"
    element = None
    parent = None

    click_open_info_group(driver=driver,data=data,selector=app_web.BTN_INFO_GROUP)

    if scrape_data_info_btn(driver=driver, selector=app_web.CONTAINER_INFO_GROUP,selector_btn=app_web.BTN_SEE_OLD_MEMBERS, timeout=data["time_wll"]):

        parent = scrape_element(driver=driver, selector=app_web.DISPLAY_INFO_GROUP,timeout=data["time_wll"])

        if not parent:
            print("Advertencia|Problema: No se pudo acceder a parent en actions@ban_member ")
            return

        element = scrape_element(driver=parent, selector=selector,timeout=data["time_wll"])

    else:
        if not click_see_all_members(driver=driver,data=data,selector=app_web.BTN_SEE_ALL_MEMBERS):
            print("Advertencia: No se pudo dar click en all_members actions@ban_member ")
            return
        input_search = scrape_element(driver=driver, selector=app_web.TXT_SOURCE_MEMBERS, timeout=data["time_wll"])

        if not input_search:
            print("Advertencia|Problema: No se pudo acceder a parent en actions@ban_member ")
            return

        edit_on_input(element=input_search, value=f"{id_member}")
        edit_on_input(element=input_search, value="ENTER")


        parent = scrape_element(driver=driver, selector=app_web.CONTAINER_LIST_MEMBERS,timeout=data["time_wll"])
        if not parent:
            print("Advertencia|Problema: No se pudo acceder a parent en actions@ban_member ")
            return
        time.sleep(10)

        element = scrape_element(driver=parent, selector=selector,timeout=data["time_wll"])

    if not element:
        print("Advertencia|Problema: No se pudo acceder al element en actions@ban_member ")
        return

    if not actionschains_move_to_element(driver=driver, element=element, timeout=data["time_ad"]):
        print("Advertencia: No se pudo mover el puntero al elemento ")
        return

    if not wait_element_to_be_clickable(driver=driver, selector=app_web.BTN_TO_DISPLAY_MENU_MEMBERS_1, timeout=data["time_wll"]):
        print("Advertencia: No se pudo abrir el menú de opciones. Terminando...")
        element.click()

    menu = scrape_element(driver=driver, selector=app_web.CONTAINER_MENU_OPTION_MESSAGE, timeout=data["time_wll"])
    if not menu:
        print("Advertencia: No se encontró el menú. Terminando...")
        return

    li = scrape_data_parent(parent=menu, child=app_web.ELEMENT_UL, timeout=data["time_wll"])
    if not li:
        print("Advertencia: No se encontraron opciones en el menú. Terminando...")
        return

    for option in li:
        if option.text == "Descartar como admin.":
            option.click()
    
    close_modal(driver=driver,data=data, selector=app_web.BTN_TO_CLOSE)
    json.demote_admin(name=remove_emotes(id_member))

@handle_exceptions  
def send_mp3(driver:webdriver.Chrome,path : str,data : dict, app_web : WhatssappWebLabels):
    
    pyperclip.copy(path)
    input_search = scrape_element(driver=driver, selector=app_web.TXT_CHAT_GROUP, timeout=data["time_wll"])

    if not wait_element_to_be_clickable(driver=driver,selector=app_web.BTN_TO_ADJUNTAR_FILES,timeout=data["time_wll"]):
        print("Problemas en dar click en el btn de adjuntar")
        return
        
    menu = scrape_element(driver=driver,selector=app_web.CONTAINER_MENU_OPTION_SEND_FILE,timeout=data["time_wll"])

    if not menu:
        print("No existe el menu para adjuntar archivos")
        return
        
    li = scrape_data_parent(parent=menu, child=app_web.ELEMENT_UL, timeout=data["time_wll"])
    if not li:
        print("Advertencia: No se encontraron opciones en el menú. Terminando...")
        return

    for option in li:
        if option.text == "Documento":
            option.click()
            break

    time.sleep(2) 

    pyautogui.hotkey("ctrl", "v")

    time.sleep(1)

    pyautogui.press("enter")

    if not wait_element_to_be_clickable(driver=driver,selector=app_web.BTN_TO_SEND_FILE,timeout=data["time_wll"]):
        print("Advertencia no se pudo dar click, pasamos a dar enter")
        edit_on_input(element=input_search, value="ENTER")
        return
        
    # print(type(path))
    # partes = path.split("\\")
    # if partes:
    #     edit_on_input(element=input_search, value=f"Ya tenemos tu archivo mp3 y ya ha sido enviado con exito uwu : {partes[-1]}")
    #     edit_on_input(element=input_search, value="ENTER")

@handle_exceptions              
def close_session(driver:webdriver.Chrome,data : dict, app_web : WhatssappWebLabels):
    if not wait_element_to_be_clickable(driver=driver, selector=app_web.BTN_AJUSTES,timeout=data["time_wll"]):
        print("No existe o no se puede dar click en el elemento clickleable ajustes")
        return
        
    if not wait_element_to_be_clickable(driver=driver, selector=app_web.BTN_CLOSE_SESSION,timeout=data["time_wll"]):
        print("No existe o no se puede dar click en el elemento clickleable CERRAR cession")
        return
        
    if not wait_element_to_be_clickable(driver=driver, selector=app_web.BTN_TO_CONFIRM_CERRAR_SESSION,timeout=data["time_wll"]):
        print("No existe o no se puede dar click en el elemento modal clickleable CERRAR cession")
        return
        
@handle_exceptions  
def approve_or_reject_user(driver:webdriver.Chrome,data : dict, app_web : WhatssappWebLabels,json:DataJson)->bool:
    
    id_solicitud = None
    status_solicitante = None
    list_solicitud = []
    country_code_spam_or_scam :dict = data["list_country_code_spam_or_scam"]
    patron = re.compile(r"^\+(\d{1,4})")

    if not wait_element_to_be_clickable(driver=driver,selector=app_web.SEE_DIALOG_BTN,timeout=data["time_wll"]):
        print("No se ha encontrado el cuadro de dialogo")
        click_open_info_group(driver=driver,data=data,selector=app_web.BTN_INFO_GROUP)    
    
        if not wait_element_to_be_clickable(driver=driver,selector=app_web.BTN_SOLICITUD_PENDIENTES,timeout=data["time_wll"]):
            print("No se ha encontrado nuevas solicitudes")
            close_modal(driver=driver,data=data, selector=app_web.BTN_TO_CLOSE)
            return False        
    
    header = scrape_element(driver=driver,selector=app_web.CONTAINER_SOLICITUD_PENDIENTES, timeout=data["time_wll"])
    if header:
        parent = scrape_element(driver=driver,selector=app_web.CONTAINER_TARGET_SOLICITUDES,timeout=data["time_wll"])
        childrens = scrape_data_parent(parent=parent, child=app_web.TARGET_SOLICITUD,timeout=data["time_wll"])

        if childrens:
            for child in childrens:
                partes = child.text.split("\n")

                print(len(childrens))

                id_solicitud = partes[0]

                status_solicitante = json.get_old_member_number(target=id_solicitud)

                match = patron.match(id_solicitud.replace(" ", "").replace("-", ""))
                if match:
                    code = match.group(1)

                    if code in country_code_spam_or_scam.values():
                        if not wait_element_to_be_clickable(driver=driver,selector=app_web.BTN_TO_DENEGER,timeout=data["time_wll"]):
                            print("No se puedo dar click en denegar")
                        continue
                    
                    if json.find_member(name=id_solicitud) == "ban":
                        if not wait_element_to_be_clickable(driver=driver,selector=app_web.BTN_TO_DENEGER,timeout=data["time_wll"]):
                            print("No se puedo dar click en denegar")
                        continue 

                    if status_solicitante == 3:
                        if not wait_element_to_be_clickable(driver=driver,selector=app_web.BTN_TO_DENEGER,timeout=data["time_wll"]):
                            print("No se puedo dar click en denegar")
                        continue 

                    if not wait_element_to_be_clickable(driver=driver,selector=app_web.BTN_TO_APROVE,timeout=data["time_wll"]):
                        print("No se puedo dar click en Aprobar")

                    if len(childrens) > 1:
                        list_solicitud.append(id_solicitud)

                    # print(id_solicitud)

    print(f"Imprimimos la lista : {list_solicitud}")     
    close_modal(driver=driver,data=data, selector=app_web.BTN_TO_BACK)
    close_modal(driver=driver,data=data, selector=app_web.BTN_TO_CLOSE)
    
    json.add_multiples(members=list_solicitud,label="members",replace=True)
    
    return True

@handle_exceptions  
def download_image(driver:webdriver.Chrome,target_message: WebElement,data :dict, app_web:WhatssappWebLabels,command:str)->bool: #Ruta defaul config@DOWNLOAD_STICKER or config@DOWNLOAD_STICKER_RELATIVE
    if not command:
        return False

    selector = f'.//div[@aria-label="Abrir foto" and @role="button"][.//img[@alt="{command}"]]'

    if not wait_element_to_be_clickable(driver=target_message,selector=selector,timeout=data["time_wll"]):
        print(f"No hay imagen con el comando {command}")
        return False

    if not wait_element_to_be_clickable(driver=driver,selector=app_web.BTN_TO_DOWNLOAD_IMG, timeout=data["time_wll"]):
        print("No hay btn para descargar")
        return False
        
        
    close_modal(driver=driver,data=data, selector=app_web.BTN_TO_CLOSE_2)
    return True
    
@handle_exceptions  
def create_sticker(driver:webdriver.Chrome,path : str,data : dict, app_web : WhatssappWebLabels):

    pyperclip.copy(path)
    input_search = scrape_element(driver=driver, selector=app_web.TXT_CHAT_GROUP, timeout=data["time_wll"])

    if not wait_element_to_be_clickable(driver=driver,selector=app_web.BTN_TO_ADJUNTAR_FILES,timeout=data["time_wll"]):
        print("Problemas en dar click en el btn de adjuntar")
        return

    menu = scrape_element(driver=driver,selector=app_web.CONTAINER_MENU_OPTION_SEND_FILE,timeout=data["time_wll"])

    if not menu:
        print("No existe el menu para adjuntar archivos")
        return

    li = scrape_data_parent(parent=menu, child=app_web.ELEMENT_UL, timeout=data["time_wll"])
    if not li:
        print("Advertencia: No se encontraron opciones en el menú. Terminando...")
        return

    for option in li:
        if option.text == "Nuevo sticker":
            option.click()
            break

    #intercatuandon con la ventana de windows
    time.sleep(2) 

    pyautogui.hotkey("ctrl", "v")

    time.sleep(1)

    pyautogui.press("enter")

    if not wait_element_to_be_clickable(driver=driver,selector=app_web.BTN_TO_SEND_FILE,timeout=data["time_wll"]):
        print("Advertencia no se pudo dar click, pasamos a dar enter")

        edit_on_input(element=input_search, value="ENTER")

        return

@handle_exceptions
def get_admins(admins:list,driver:webdriver.Chrome,data: dict, app_web : WhatssappWebLabels)->list:
    parent = scrape_element(driver=driver,selector=app_web.DISPLAY_INFO_GROUP,timeout=data["time_wll"])

    if parent:
        time.sleep(10)
        items = scrape_data_parent(parent=parent,child=app_web.TARGET_INFO_MEMBER,timeout=data["time_wll"])
        for i in items:

            # print(i.text)
            partes = i.text.split('\n')
            if "Admin. del grupo" in partes:
                admins.append(partes[0]) #tagname/numberphone/id

        if "Tú" in admins:
            admins.remove("Tú")
            admins.append(app_web.BOT_ID)

    close_modal(driver=driver,data=data, selector=app_web.BTN_TO_CLOSE)
    return admins

@handle_exceptions
def get_size_listmember(driver:webdriver.Chrome,data:dict,app_web:WhatssappWebLabels)->int:

    if not wait_element_to_be_clickable(driver=driver,selector=app_web.BTN_INFO_GROUP,timeout=data["time_wll"]):
        print("No se pudo abrir info")
        return
    time.sleep(3)
    
    return scrape_data_size_list_member(driver=driver,selector=app_web.TXT_NUMERO_MIEMBROS,timeout=data["time_wll"])

@handle_exceptions
def reset_link_invitation(driver:webdriver.Chrome,data:dict,app_web:WhatssappWebLabels)->str|None:
    
    nuevo_enlace = None

    if not click_open_info_group(driver=driver,data=data,selector=app_web.BTN_INFO_GROUP):   
        print("Error En abrir el info grupo")
        return
    
    if not wait_element_to_be_clickable(driver=driver,selector=app_web.BTN_ENLACE_INVITACION,timeout=data["time_wll"]):
        print("Error En abrir el enlace de invitacion")
        return
    
    if not wait_element_to_be_clickable(driver=driver,selector=app_web.BTN_RESET_ENLACE_INVITACION,timeout=data["time_wll"]):
        print("Error En resetear el enlace de invitacion")
        return
    
    if not wait_element_to_be_clickable(driver=driver,selector=app_web.BTN_TO_CONFIRM_RESET_ENLACE_INVITACION,timeout=data["time_wll"]):
        print("Error En confirmar resetear el enlace de invitacion")
        return
    
    time.sleep(2)

    if not wait_element_to_be_clickable(driver=driver,selector=app_web.BTN_COPY_ENLACE_INVITACION,timeout=data["time_wll"]):
        print("Error En resetear el enlace de invitacion")
        return

    #Tras dar click en copiar enlace, en teoria debe de estar en el portapapeles, lo obtenemos
    nuevo_enlace = pyperclip.paste() 

    close_modal(driver=driver,data=data, selector=app_web.BTN_TO_BACK)
    close_modal(driver=driver,data=data, selector=app_web.BTN_TO_CLOSE)
    
    return nuevo_enlace