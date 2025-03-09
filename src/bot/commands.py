from selenium import webdriver
from app_web.WhatssapWebLabels import WhatssappWebLabels
from download import Download
from src.data.data_json import DataJson
from move_to_downloas_stciker import move_recent_whatsapp_image
from src.bot.actions import edit_on_input,restringe_chat,ban_member, promove_member, depromove_member,send_mp3,close_session,create_sticker, find_members,reset_link_invitation,get_member
from src.bot.scraper import scrape_element
from src.bot.utils import get_datetime_to_three_days,get_datetime
from src.bot.scripts import to_script_to_reinciar_observer,to_return_ver_chat
from pathlib import Path
import time
import re
import os
import glob
import pyperclip
import pyautogui
import threading




class Commands:
    def __init__(self,driver:webdriver.Chrome, data:dict, app_web:WhatssappWebLabels,dict_country_codes : dict, download: Download, data_json:DataJson,stop_events:threading.Event):
        self.driver = driver
        self.data = data
        self.app_web = app_web
        self.dict_country_code = dict_country_codes
        self.telefono_regex = r"^\+?\d{1,4}?[\s-]?\(?\d{1,4}?\)?[\s-]?\d{1,4}[\s-]?\d{1,4}$"
        self.download_instance = download #class para descargar musica
        self.json = data_json
        self.stop_events = stop_events
        
    def bye(self,*arg):
        input_box = scrape_element(driver=self.driver, selector=self.app_web.TXT_CHAT_GROUP, timeout=self.data["time_wll"])
        edit_on_input(element=input_box, value="Gracias chicos!!!, Bueno hasta pronto ;)")
        edit_on_input(element=input_box, value="ENTER")

        close_session(driver=self.driver,data=self.data,app_web=self.app_web)
        self.stop_events.set()

    def __innable(self):
        input_box = scrape_element(driver=self.driver, selector=self.app_web.TXT_CHAT_GROUP, timeout=self.data["time_wll"])
        edit_on_input(element=input_box, value="Funcion Inahilitada, por testing de otras funciones")
        edit_on_input(element=input_box, value="ENTER")
        time.sleep(5)

    def menu(self,*arg):
        input_box = scrape_element(driver=self.driver, selector=self.app_web.TXT_CHAT_GROUP, timeout=self.data["time_wll"])
        pyperclip.copy(
            """

                ⚠️Bot solo para admins⚠️ 

                Comandos:

                /menu 

                🖇️Administer/Accion grup🖇️ 


                /all [asunto]: Etiqueta a todos los miembros del grupo (excepto el bot) para su atención, puedes indicar el asunto, por defecto sera "Chicos de {self.data["group_name"]},vengan:".

                /ban [member] : Banea al usuario especificado del grupo. (campo obligatorio)

                /shh [true]: Restringe el chat del grupo (si ya está restringido, vuelve a ejecutar este comando, junto al true, para asi activar el detector de spam).

                /promove [member]: Promueve al miembro como administrador del grupo. (campo obligatorio)

                /despromove [member] : Revoca los privilegios de administrador de un miembro. (campo obligatorio)

                /r_link [days]: Restablecer/Resetear el enlace de invitacion del grupo, si pones los dias, seran los dias para hacerlo autamicamente, sinolopones conservara los dias, configurados anteriormente

                /enlace : Manda el link de invitacion del grupo 
                🪩Multimedia🪩 

                /audio [link youtube]: Descarga y envía el audio desde YouTube en formato mp3 (máximo 16MB). (campo obligatorio)

                /sticker : Crea un sticker a partir de una imagen o archivo


                🧯Apagado del bot🧯

                /bye : apaga el bot

            """
        )

        # Dar un pequeño tiempo para asegurar que el foco esté en el cuadro de texto
        input_box.click()
        time.sleep(2)
        # Usar pyautogui para pegar desde el portapapeles
        pyautogui.hotkey("ctrl", "v")
        time.sleep(3)
        edit_on_input(element=input_box, value=("ENTER"))

        
    def salute(self)->str:
        return f"Hola gente del grupo de {self.data["group_name"]}, En unos minutos estare disponibles, etsoy cargando los miembros uwu"
    
    def all(self,*args)->None:
        asunto = None
        if args:
            asunto = args[0]

        # self.__innable()
        members = self.json.get_members(label="members")

        input_box = scrape_element(driver=self.driver, selector=self.app_web.TXT_CHAT_GROUP, timeout=self.data["time_wll"])
        
        if members:
            members_set = set(members)
            members_set -= {"Tú", None}

            edit_on_input(element=input_box, value=f"Asunto : {asunto}" if asunto else f"Chicos de {self.data["group_name"]},vengan: ")
            edit_on_input(element=input_box, value=("SHIFT","ENTER"))
            
            for push,_ in enumerate(members_set):
                edit_on_input(element=input_box, value="@")
                """Confirmamos que eixtsan CONTACTOS"""
                
                """Secuencia de etiquetado"""
                if push > 0:
                    edit_on_input(element=input_box, value="ARROW_DOWN",batch_input=push)
                    time.sleep(0.2)

                edit_on_input(element=input_box, value="TAB")

                edit_on_input(element=input_box, value=("SHIFT","ENTER"))

            edit_on_input(element=input_box, value="ENTER")

        else: 
            raise print("Error la lista de miembros esta vacia :(")
        
        edit_on_input(element=input_box, value="Finalizamos la funcion de etiquetar todos :)")
        edit_on_input(element=input_box, value="ENTER")

    def admins(self,*args)->None:
        # self.__innable()
        members = self.json.get_members(label="admins")

        input_box = scrape_element(driver=self.driver, selector=self.app_web.TXT_CHAT_GROUP, timeout=self.data["time_wll"])
        
        if members:
            members_set = set(members)
            members_set -= {"Tú", None}

            print(len(members_set))

            # member_order = sorted(members_set,key=self.__extract_country_code)

            for member in members_set:
                
                #mejorar el formateado del value, oara captar todos
                member_value = f"@{member[:-3]}"
                if "\u202f" in member_value:
                    value = member_value.replace("\u202f"," ")
                else:
                    value = member_value
                edit_on_input(element=input_box, value=value)
                edit_on_input(element=input_box, value="TAB")

                if re.match(self.telefono_regex, member[:-3]):
                     rango = len(member_value)
                     for _ in range(rango): #error whweb cuando eliminas se elimina la etiqueta (rango+1)       
                         edit_on_input(element=input_box, value="BACKSPACE")
                
                edit_on_input(element=input_box, value=("SHIFT","ENTER"))

                

            edit_on_input(element=input_box, value="ENTER")

        else: 
            raise print("Error la lista de miembros esta vacia :(")

    def ban(self,*args)->None:
        members = self.json.get_members(label="members")
        member_ :str = None
        member:str = None
        
        if len(args) == 1:  # Si solo hay un argumento
            
            print(args[0])

            member_ = args[0]

            member = member_.lstrip("@").strip()

            if  member in members:

                ban_member(driver=self.driver,id_member=member,data=self.data, app_web=self.app_web,json=self.json)
        
            else:
                value = f"El argumento/miembro '{args[0]}' no existe. Use este comando mas tarde"
                input_text = scrape_element(driver=self.driver, selector=self.app_web.TXT_CHAT_GROUP, timeout=self.data["time_wll"])
                edit_on_input(element=input_text, value=value)
                edit_on_input(element=input_text, value="ENTER")
            
        else:
            print(f"Varios valores: {args}")
            self.__innable()

    def promove(self,*args)->None:
        
        members = self.json.get_members(label="members")
        member_ :str = None
        member:str = None
        if len(args) == 1:  # Si solo hay un argumento
            member_ = args[0]

            member = member_.lstrip("@").strip()

            if  member in members:
                
                promove_member(driver=self.driver,id_member=member,data=self.data, app_web=self.app_web,json=self.json)
        
            else:
                value = f"El argumento/miembro '{args[0]}' no existe. Use este comando mas tarde"
                input_text = scrape_element(driver=self.driver, selector=self.app_web.TXT_CHAT_GROUP, timeout=self.data["time_wll"])
                edit_on_input(element=input_text, value=value)
                edit_on_input(element=input_text, value="ENTER")
            
        else:
            self.__innable()

    def despromove(self,*args)->None:
        members = self.json.get_members(label="admins")
        member_ :str = None
        member:str = None
        if len(args) == 1:  # Si solo hay un argumento
            member_ = args[0]

            member = member_.lstrip("@").strip()

            if  member in members:

                depromove_member(driver=self.driver,id_member=member,data=self.data, app_web=self.app_web,json=self.json)
        
            else:
                value = f"El argumento/miembro '{args[0]}' no existe. Use este comando mas tarde"
                input_text = scrape_element(driver=self.driver, selector=self.app_web.TXT_CHAT_GROUP, timeout=self.data["time_wll"])
                edit_on_input(element=input_text, value=value)
                edit_on_input(element=input_text, value="ENTER")
            
        else:
            self.__innable()

    def shh(self,*args)->bool:
        """
            Si check = true (chat habilidado)
            Si check = false (chat inhabilidado)

            is_restringre_chat = False (esta habilitado)
            is_restringre_chat = True (esta inhabilitado)

        """
        if len(args) == 1:  # Si solo hay un argumento
            reboot_monitor :str = args[0] if args[0] is not None else "false"
            if reboot_monitor.lower() == "true":
                reboot_monitor = True
            elif reboot_monitor.lower() == "false":
                reboot_monitor = False

            if reboot_monitor:
                if self.driver.execute_script(script=to_return_ver_chat):
                    self.driver.execute_script(to_script_to_reinciar_observer,self.app_web.CONTAINER_CHAT)

        return True if not restringe_chat(driver=self.driver,data=self.data, app_web=self.app_web) else False
        
    def audio(self,*args)->None:
        if len(args) == 1:  # Si solo hay un argumento
            url = args[0]
            input_box = scrape_element(driver=self.driver, selector=self.app_web.TXT_CHAT_GROUP, timeout=self.data["time_wll"])
            
            edit_on_input(element=input_box, value="Descargando audio de Youtube... espere un momento")
            edit_on_input(element=input_box, value="ENTER")


            if re.match(self.app_web.PATRON_LINK_YOUTUBE, url):

                path, size = self.download_instance.download_audio(url=url,duration=self.data["duration_limit_audio"])

                #verificar si es stream o audios de mas de 10 minutos
                if path == "is_live":
                    message = "Este video/audio de youtube es un stream, y esta actualmente en transmicion, use otro audio/video, para su descargar, gracias uwu"
                    edit_on_input(element=input_box, value=message)
                    edit_on_input(element=input_box, value="ENTER")
                    return
                
                #caso de audios de mas de 10 minutos
                if path == "duration":
                    audio = time.strftime("%H:%M:%S", time.gmtime(size))
                    limite = time.strftime("%H:%M:%S", time.gmtime(self.data["duration_limit_audio"]))
                    message = f"Este video/audio de youtube es muy pesado/duracion muy larga, el limite es de {limite}, y este tiene :{audio}, use otro audio/video, para su descargar, gracias uwu"
                    edit_on_input(element=input_box, value=message)
                    edit_on_input(element=input_box, value="ENTER")
                                    
                    return
                
                try:
                    if size < self.app_web.SIZE_LIMIT_AUDIO:
                        
                        path_relative = Path(path)
                        print(path_relative.resolve())

                        send_mp3(driver=self.driver,path=path_relative.resolve(),data=self.data,app_web=self.app_web)
                    else:

                        edit_on_input(element=input_box, value=f"No se puede enviar este archivo, encontrado en: {path}, ya que pesa : {size} MB, esta por encima del limite")
                        edit_on_input(element=input_box, value="ENTER")
                except Exception as e:
                    print(f"Error en obtener la ruta por medio de Path: {e}")
                    return

            else:
                print(f"El link : {url}, no es accesible/no es un link o url de youtube")
                return
            edit_on_input(element=input_box, value="Ya esta su audio listo :), disfrutelo uwu")
            edit_on_input(element=input_box, value="ENTER")

    def upmembers(self,*args)->None:
        # members, admins = find_members(dict_country_code=self.dict_country_code, driver=self.driver,data=self.data, app_web=self.app_web)
        members, admins = get_member(data=self.data, app_web=self.app_web, driver=self.driver)
        self.json.add_multiples(members=members,label="members")
        self.json.add_multiples(members=admins,label="admins")
    
    def sticker(self,*args)->None:

        input_box = scrape_element(driver=self.driver, selector=self.app_web.TXT_CHAT_GROUP, timeout=self.data["time_wll"])

        edit_on_input(element=input_box, value="Descargando imagen para hacerla sticker... espere un momento")
        edit_on_input(element=input_box, value="ENTER")

        time.sleep(2)
        # Moveremos la imagen a la carpeta 
        if not move_recent_whatsapp_image(downloads_destine=self.data["relative_path_download_sticker"]):
            print("No se pudo mover la imagen recientemente descargada, no existe o no fue descargada")
            return 
        
         # Filtrar imágenes con extensiones comunes (puedes agregar más si es necesario)
        image_pattern = os.path.join(self.data["relative_download_sticker"], "*.jpeg")  # O también puedes usar "*.png", "*.jpg", etc.
        images = glob.glob(image_pattern)
        
        if not images:
            print("No se encontró ninguna imagen en la carpeta.")
            return None
        
        # Ordenar por fecha de modificación para obtener la más reciente
        images.sort(key=os.path.getmtime, reverse=True)
        path_img_sticker = images[0]  # Obtener la imagen más reciente
        
        path_relative = Path(path_img_sticker)
        print(path_relative.resolve())
        
        create_sticker(driver=self.driver,path=path_relative.resolve(),data=self.data,app_web=self.app_web)

        edit_on_input(element=input_box, value="Tu stciker ya esta hecho uwu, disfrutalo ")
        edit_on_input(element=input_box, value="ENTER")

    def r_link(self,*args)->None:
        days = None
        if len(args) == 1:  # Si solo hay un argumento
            days = args[0]

        input_box = scrape_element(driver=self.driver, selector=self.app_web.TXT_CHAT_GROUP, timeout=self.data["time_wll"])

        edit_on_input(element=input_box, value="Reseteando link de invitacion")
        edit_on_input(element=input_box, value="ENTER")

        res = reset_link_invitation(driver=self.driver,data=self.data, app_web=self.app_web)

        if days:
            #nuevo reseteo
            date = get_datetime()
            if self.json.add_date_time(date=get_datetime_to_three_days(days=int(days),date=date)):
                edit_on_input(element=input_box, value=f"El link de invitacion, se reseteara el {self.json.get_datetime()}, en {days} dias uwu")
                edit_on_input(element=input_box, value="ENTER")
            
            if res:
                edit_on_input(element=input_box, value=f"Nuevo Enlace de invitacion: \n {res}")
                edit_on_input(element=input_box, value="ENTER")
                self.json.add_new_link(link=res)
                edit_on_input(element=input_box, value=f"/admins Ha sido Reseteado el enlace")
                edit_on_input(element=input_box, value="ENTER")
                

    def enlace(self,*args)->None:
    
        res = self.json.get_link()
        if res:
            input_box = scrape_element(driver=self.driver, selector=self.app_web.TXT_CHAT_GROUP, timeout=self.data["time_wll"])
            edit_on_input(element=input_box, value=f"Enlace de invitacion: \n {res}")
            edit_on_input(element=input_box, value="ENTER")
        