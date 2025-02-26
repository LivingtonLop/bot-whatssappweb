from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException,WebDriverException,JavascriptException
from src.bot.actions import perform_login, open_group,edit_on_input,restringe_chat,delete_message_chat, ban_member,approve_or_reject_user,close_session,download_image,get_size_listmember
from src.bot.scraper import scrape_element
from app_web.WhatssapWebLabels import WhatssappWebLabels
from download import Download
from src.data.data_json import DataJson
from src.bot.commands import Commands
from src.bot.utils import remove_emotes,get_author_in_data_id,get_type_in_target_message,normalize_number,find_number_position,get_datetime
from src.bot.scripts import to_ver_chat_masive,to_return_ver_chat, to_ver_chat, to_return_node
import re
import time
import threading

class Bot:
    def __init__(self, options:webdriver.ChromeOptions, data : dict, app_web : WhatssappWebLabels, list_black : list,list_grey : list,dict_country_codes : dict,list_link_spam : list, download: Download,data_json : DataJson):
        self.options = options
        self.data = data
        self.json = data_json
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.execute_script(script=data["script"])
        self.app_web = app_web
        self.download = download #class para descargar musica
        self.stop_events = threading.Event()
        self.pause_events = threading.Event() 
        self.pause_events.set() 
        # self.count_pause = 0
        self.commands = Commands(driver = self.driver, data=data,app_web=app_web, dict_country_codes=dict_country_codes, download=download,data_json= self.json,pause_events = self.pause_events,stop_events = self.stop_events)
        self.lock = threading.Lock()# Evita accesos concurrentes
        self.executed_commands : dict[str,set[tuple[str,str]]] = dict()
        self.restringe_chat = False
        self.__filtrer_list_black = list_black
        self.__filtrer_list_grey = list_grey
        self.__filtrer_list_link_spam = list_link_spam

        self.regex_ban = r"\b(?:{})\b".format("|".join(map(re.escape, self.__filtrer_list_black)))
        self.regex_kick = r"\b(?:{})\b".format("|".join(map(re.escape, self.__filtrer_list_grey)))
        self.regex_links_ban = r"\b(?:{})\b".format("|".join(map(re.escape, self.__filtrer_list_link_spam)))


        self.verify_requests_thread = threading.Thread(target=self.verify_requests, daemon=True)
        self.reset_variables_thread = threading.Thread(target=self.reset_variables,daemon=True)
        self.verifique_new_message_thread = threading.Thread(target=self.verifique_new_message, daemon=True)
        

    def run(self):

        try:
            self.init_run()
            time.sleep(3)
            
            self.driver.execute_script(to_ver_chat_masive, self.app_web.CONTAINER_CHAT,self.app_web.QUERY_SELECTOR_MULTIMEDIA,3000,4)
            self.driver.execute_script(to_ver_chat, self.app_web.CONTAINER_CHAT)

            while not self.stop_events.is_set():

                self.pause_events.wait()
                if not self.restringe_chat:
                    self.detector_spam_js()

                # self.detector_chat_pause()

                time.sleep(1)

            print("Finalizando Bot")  
            
        except WebDriverException as e:
            if "Unable to find url to connect to from capabilities" in str(e):
                print("⚠️ Error: No se puede encontrar la URL de conexión. Revisa la configuración del servidor.")
            else:
                print(f"Error de WebDriver: {e}")

        except Exception as e:
            print(f"Error Inesperado (base bot) : {e}")   
            close_session(driver=self.driver,data=self.data,app_web=self.app_web)  
        finally:
            self.driver.quit()

    def caso_chat_restringe(self, value : bool):

        self.commands.shh(value if value else None)
        self.status_chat()
        self.commands.admins()  

    def detector_spam_js(self):
        """Solo coje el retur del windws.spamDetected"""
        if self.driver.execute_script(script=to_return_ver_chat):  
            self.caso_chat_restringe(value=False)         
            input_text = scrape_element(driver=self.driver, selector=self.app_web.TXT_CHAT_GROUP, timeout=self.data["time_wll"])
            edit_on_input(element=input_text, value="Mucho spam de Stickers/Imagenes/Videos/Audio/Mensajes repeteido/Gifs/Roleo :)")
            edit_on_input(element=input_text, value="ENTER")
                
    # def detector_chat_pause(self):
    #     input_text = scrape_element(driver=self.driver, selector=self.app_web.TXT_CHAT_GROUP, timeout=self.data["time_wll"])
    #     if self.count_pause == 300: #si pasa de los 5 minutos, el bot descansa

    #         self.caso_chat_restringe(value=False)         
    #         self.pause_events.clear()
    #         tiempo = self.count_pause/60
    #         edit_on_input(element=input_text, value=f"Inactividad del chat, me voy a mimir, esperen sus {tiempo} minutos :)")
    #         edit_on_input(element=input_text, value="ENTER")

    #         time.sleep(self.count_pause)
    #         self.pause_events.set()

    #         self.caso_chat_restringe(value=True)         
    #         self.count_pause = 0
    #         edit_on_input(element=input_text, value="Reanudamos actvidad del bot :)")
    #         edit_on_input(element=input_text, value="ENTER")

    def init_run(self):
        perform_login(self.driver,self.data["url_app"])
            
        open_group(driver=self.driver, data=self.data, selector=self.app_web.BTN_CLICK_TO_OPEN_GROUP)
            
        value = self.commands.salute()
        input_text = scrape_element(driver=self.driver, selector=self.app_web.TXT_CHAT_GROUP, timeout=self.data["time_wll"])
        edit_on_input(element=input_text, value=value)
        edit_on_input(element=input_text, value="ENTER")
            
        # self.actualizar_miembros()
        if not self.json.load():
            self.commands.upmembers()

        if str(get_datetime().date()) == self.json.get_datetime():
            self.commands.r_link(3)

        self.init_threads()

        self.executed_commands_reset()
        #scripts


    def init_threads(self):
        #inicializamos los hilos
        """COmienco de los hiloes"""
        self.verify_requests_thread.start()
        self.reset_variables_thread.start()
        self.verifique_new_message_thread.start()

    def reset_variables(self):

        while True:
            self.pause_events.wait()
            
            with self.lock:

                if len(self.executed_commands) > self.data["elemento_execute_command"]:
                    self.executed_commands_reset()
        
            time.sleep(360) #limpa cada 6 minutos

    def verifique_new_message(self):
        """Verificamos el valor del mensaje """
        while True:
            
            self.pause_events.wait()

            try:

                target : WebElement = self.driver.execute_script(to_return_node)


                if target:
                    # print(f"Primer tiempo : {self.test_time()}")
                   
                    message = scrape_element(driver=target,selector=self.app_web.TXT_TARGET_MESSAGE,timeout=self.data["time_wll"])

                    if not self.detect_commando(message=message,target=target):
                        """No es comando es un mensaje o mutimedia"""
                        # print("No command")

                    if not self.verifique_ban_or_kick(message=message,target_message=target):
                        """Por que paso el filtro, o porque no es un mensaje/mensaje con imagen"""
                        # print("No paso los filtros")


                    # print("Nuevo Mensaje")

                    # print(f"Finalizando tiempo : {self.test_time()}")

            except StaleElementReferenceException as e:
                print(f"Error, problemas con message, posiblemente eliminado {e}")
                continue
            except JavascriptException as e:
                print(f"Error, problemas con scriptos : {e}")
                continue

    def verifique_ban_or_kick(self, message : WebElement, target_message : WebElement)->bool:
        try:
            
            if not message:
                return False

            parts_message = message.text.split(maxsplit=1)
            _seudo = parts_message[0] #/_seudo

            if _seudo.startswith("/"):
                return False

            if re.search(self.regex_ban, message.text.lower()):
                self.__algoritmo_ban(message=message,target_message=target_message)
                return True
                    
            if re.search(self.regex_links_ban, message.text):
                self.__algoritmo_ban(message=message,target_message=target_message)
                return True
                    
            if re.search(self.regex_kick, message.text.lower()):
                delete_message_chat(driver=self.driver,message_del=message,data=self.data, app_web=self.app_web)
                return True
            
            return False

        except StaleElementReferenceException as e:
            print(f"Error, problemas con message, posiblemente eliminado {e}")
            return False

    def verify_requests(self):
        while True:
            # print(f"verefique:{self.pause_events.is_set()}")
            self.pause_events.wait()
            if not approve_or_reject_user(driver=self.driver, data=self.data,app_web=self.app_web,json=self.json):
                print("No se encontro nuevas solicitudes")

            time.sleep(360)

    def __algoritmo_ban (self, message :WebElement, target_message : WebElement):
        self.pause_events.clear()

        author,_,_,_ = self.get_data_message(target_message=target_message)
        if not self.restringe_chat:
            restringe_chat(driver=self.driver,data=self.data, app_web=self.app_web)
        
        delete_message_chat(driver=self.driver,message_del=message,data=self.data, app_web=self.app_web)
        if author:
            ban_member(driver=self.driver, id_member=author,data=self.data,app_web=self.app_web,json=self.json)
        if self.restringe_chat:
            restringe_chat(driver=self.driver,data=self.data, app_web=self.app_web)
        self.pause_events.set()

    def get_data_message(self, target_message:WebElement, t_data : bool = False)->tuple[str,str,str,str]:

        
        """Type : (str, media-play, media-gif, img (alt= Abrir foto), sticker (alt=Sticker sin etiquetas))
        
        @str:
            class="copyable-text" data-pre-plain-text="[9:32 a. m., 16/2/2025] Lllc: "
            class="_ahy1 copyable-text" data-pre-plain-text="[10:19 p. m., 15/2/2025] Leohpy🍁: "
            [time, data], author
        
        @media-play, @media-gif, @img, @sticker

            x_paths : 
                @IMAGE_STICKER = ".//img[@alt='Sticker sin etiquetas']"
                @IMAGE_NORMAL = ".//div[@aria-label='Abrir foto']"
                @VIDEO_NORMAL = ".//span[@data-icon='media-play']"
                @GIF_NORMAL = ".//span[@data-icon='media-gif']"
        
            return -> 
                @author : str : [Juan|@+593 6 151 1615|None]
                @data_id : str : [true_120363277516704470@g.us_BDCA1D25B168F98F89317BDEAEB20E39_xxxxxxxxxxx@c.us-5|None]
                @type_ : str : [None(text)|sticker|image|video|gif]
                @hour : str [None|[10:31 a. m.]|[[10:31 p. m.]]


        """
        author= None
        data_id_target = None
        type_ = None
        hour = None
        data_target = None

        try:
            
            copy_text_arg = scrape_element(driver=target_message,selector=self.app_web.TXT_COPYABLE_TEXT_ARG,timeout=0.1)
            
            if copy_text_arg:
                data_target = copy_text_arg.get_attribute(self.app_web.DATA_PRE_PLAIN_TEXT)

            target_text = target_message.text
            lineas = target_text.split("\n")
            
            
            if t_data:
                is_sticker = scrape_element(driver=target_message,selector=self.app_web.IMAGE_STICKER,timeout=0.1)
                is_img = scrape_element(driver=target_message,selector=self.app_web.IMAGE_NORMAL,timeout=0.1)
                is_media_play = scrape_element(driver=target_message,selector=self.app_web.VIDEO_NORMAL,timeout=0.1)
                is_gif = scrape_element(driver=target_message,selector=self.app_web.GIF_NORMAL,timeout=0.1)
                is_voice_record = scrape_element(driver=target_message,selector=self.app_web.VOICE_RECORD,timeout=0.1)
                
                type_ = get_type_in_target_message(is_sticker=is_sticker,is_img=is_img,is_media_play=is_media_play,is_media_gif=is_gif,is_voice_record = is_voice_record)
                

            data_id_target = target_message.get_attribute("data-id")

            if data_target: #[2:04 PM, 2/16/2025] Lllc:
                coincidencia = re.search(self.app_web.PATRON_HORA_AUTOR,data_target)
                if coincidencia:
                    hour = coincidencia.group(1)
                    author = remove_emotes(coincidencia.group(2))
                else:
                    print("No se ha encontrado coincidencia data target,vamos a usar PATRON_HOUR, para asi encontrar la hora" )
                    for linea in reversed(lineas):
                        if re.search(self.app_web.PATRON_HOUR, linea):
                            hour = linea.strip()
        
            if not copy_text_arg:
                print("Por medio de no patron [:2]")
                #audio = none, sticker = none, images (sin txt) = none
                for linea in lineas[:2]:
                    if not re.search(self.app_web.PATRON_HOUR, linea):
                        if not self.json.find_member(remove_emotes(linea)) in ["not found","old","ban"]:
                            author = remove_emotes(linea)
                    else:
                        hour = linea.strip()

            if not author:
                author_ = get_author_in_data_id(data_id=data_id_target)
                members = self.json.structure[self.data["group_name"]]["members"]
                normalized_members = [normalize_number(m) for m in members] #todos los numeros deben de estar ahi, no se permiten nombres
                pos = find_number_position(number=author_,normalized_members=normalized_members)
                try:
                    author = self.json.structure[self.data["group_name"]]["members"][pos]
                except (IndexError,TypeError):
                    data_target = None
                        

            if not type_:
                #caso text
                type_ = "text"

            

            # print((author,data_id_target,type_,hour))
            return (author,data_id_target,type_,hour) 

        except StaleElementReferenceException:
            print("Elemento ya no es accesible, reintentando...")
            return (None,None,None,None)
        except IndexError as e:
            print(f"Error en el index {e}")
            return (None,None,None,None)
        except Exception as e:
            print(f"Error inesperado{e}" )
            return (None,None,None,None)

    def actualizar_miembros(self, label="members"):
        try:
            # Intentamos cargar el archivo JSON
            if self.json.load():
                # Obtenemos el tamaño de los miembros actuales y compararlos
                size_member = self.json.get_size_members(label)
                size_now_member = get_size_listmember(driver=self.driver, data=self.data, app_web=self.app_web)

                print(f"Tamano actual : {size_now_member}")
                print(f"Tamano antiguo : {size_member}")


                # Si los tamaños no coinciden, actualizamos los miembros
                if size_member != size_now_member:
                    self.commands.upmembers()
            else:
                # Si no se puede cargar el JSON o no existe, actualizamos los miembros
                self.commands.upmembers()

        except Exception as e:
            # Manejo de excepciones (en caso de que self.json.load() falle o cualquier otro error)
            print(f"Error al actualizar miembros: {e}")
            self.commands.upmembers()

    def executed_commands_reset(self):
        keys_to_keep = {"commands"}
        self.executed_commands = {key: set() for key in keys_to_keep}

    def register_data_commands(self,data_id : str,hour : str, key ="default"):
        
        if not data_id:
            data_id = "default"

        if key in self.executed_commands:
            self.executed_commands[key].add((data_id,hour))
        else:
            self.executed_commands[key] = {(data_id,hour)}

    def detect_commando(self, message :WebElement, target : WebElement)->bool:
        try:        
            if not message:
                print("383")
                return False
                
            parts_message = message.text.split(maxsplit=1)
            command = parts_message[0] #/command
            arg = parts_message[1:] if len(parts_message)>1 else [] #arg

            if not command.startswith("/"):
                print("391")
                return False

            author,data_id_target,type_,hour = self.get_data_message(target_message=target,t_data=True)

            if not self.json.find_member(author) == "admin":
                """Saltamos a otra iteracion porque no es admin"""
                print("398")
                return False

            is_command = command[1:]
            if is_command in self.executed_commands and any(data_id_target == data[0] for data in self.executed_commands[is_command]):
                """No ejecutamos el comando"""
                print("404")
                return False

            if command == "/sticker" and type_ == "images":
                self.pause_events.clear()

                if not download_image(driver=self.driver, target_message=target,data=self.data,app_web=self.app_web,command=command):
                    print(f"Este comando/imagen : {command}, no existe, usa /menu, para saber que comandos usar")            
                    
                self.pause_events.set()

            if hasattr(self.commands, is_command) and callable(getattr(self.commands, is_command)):
                metodo = getattr(self.commands, is_command)
                metodo(*arg)
                if command == "/shh":
                    self.status_chat()
                # self.restringe_chat = res if res is not None else False
            else:
                value = f"El comando '{is_command}' no existe. Usa /menu para ver los disponibles."
                input_text = scrape_element(driver=self.driver, selector=self.app_web.TXT_CHAT_GROUP, timeout=self.data["time_wll"])
                edit_on_input(element=input_text, value=value)
                edit_on_input(element=input_text, value="ENTER")
                
            self.register_data_commands(data_id=data_id_target,hour=hour, key=is_command)
            return True
        
        except StaleElementReferenceException as e:
            print(f"Error, problemas con message, posiblemente eliminado {e}")
            return
        
    def status_chat(self):
        if self.restringe_chat:
            """Ta restringido el chat"""
            self.restringe_chat = False
        else:
            """esta hbailitado el chat"""
            self.restringe_chat = True

    def test_time(self):
        return time.time()