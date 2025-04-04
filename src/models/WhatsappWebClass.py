from selenium.webdriver.remote.webelement import WebElement
from src.utils import Utils

class WhatsAppWebClass:
    """
    Class to interact with WhatsApp Web on Windows 10 using ChromeDriver.

    Attributes:
        bot_id (str): Unique bot identifier.
        group_name (str): Name of the WhatsApp group.
    Methods:
        get_xpath: Returns the XPath for a given button.
    Regular Expression:
        PATRON_HOUR : 24:00|00:00
        PATRON_HOUR_AUTOR : 24:00|00:00 name or phone number
        PATRON_LINK_YOUTUBE: links youtube
    
    QUERYS:
        QUERY_SELECTOR_MULTIMEDIA: para seleccionar el contenido media del chat con js
        
    """

    PATRON_HOUR = r"\b\d{1,2}:\d{2}\s?[APM]{2}\b" 
    PATRON_HORA_AUTOR = r"\[(\d{1,2}:\d{2}\s?[APM]{2}), .*?\] (.+?):"
    PATRON_LINK_YOUTUBE =  r'(https?://)?(www\.)?((youtube\.com/watch\?v=|youtu\.be/)[\w-]+)'
    QUERY_SELECTOR_MULTIMEDIA = "div[class = '_amk4 _amkt'], div[class = '_amk4 _amkv'], div[class = '_amk4 _amk9'], div[class = '_amk4 _amku']"

    input_restringe_chat :bool = False 
    bot_to_admins : bool = True
    admins : list[str] = []

    def __init__(self,utils :Utils, bot_id: str = "000 00 0000 0000", group_name: str = "WhatsApp Group"):
        """
        Initializes an instance of WhatsAppWebClass.

        Parameters:
            bot_id (str): Bot identifier. Default is "000 00 0000 0000".
            group_name (str): Name of the WhatsApp group. Default is "WhatsApp Group".
        """
        self._bot_id: str = bot_id
        self._group_name: str = group_name
        self.utils =utils
        

    @property
    def bot_id(self) -> str:
        """Returns the bot ID (read-only)."""
        return self._bot_id

    @property
    def group_name(self) -> str:
        """Returns the group name (read-only)."""
        return self._group_name

    @property
    def buttons(self) -> dict[str, str]:
        """Returns a dictionary of XPath buttons."""
        return {
            "open_group": f"//span[@title='{self._group_name}']",
            "open_info_group": "//div[(@title='Detalles del perfil' or @title='Profile details') and @role='button']",
            "see_all_members": "//div[contains(., 'Ver todos')]",
            "see_old_members":"//button[text()='Ver miembros anteriores']",
            "close":"//div[@aria-label='Cerrar' and @role='button']",
            "close2":"//button[@title='Cerrar' and @aria-label='Cerrar']",
            "back":"//div[@aria-label='Atrás' and @role='button']",
            "confirm":"//button[.//div[contains(text(), 'OK')]]",
            "aprovee":"//div[@aria-label='Aprobar']",
            "deneger":"//div[@aria-label='Rechazar']",
            "group_permission":"//div[@role='button' and contains(@class, 'xkhd6sd') and .//div[contains(text(), 'Permisos del grupo')]]",
            "delete":"//button[@title='Eliminar']",
            "delete2":"//button[.//div[contains(text(), 'Eliminar')]]",
            "delete_all":"//button[.//div[contains(text(), 'Eliminar para todos')]]",
            "menu_contextual":"//div[@aria-label='Menú contextual']",
            "menu_contextual_member":"//button[@aria-label='Abrir el menú contextual del chat']",
            "send_file":"//div[@aria-label='Enviar']",
            "add_file":"//button[@title='Adjuntar']",
            "download_file":"//button[@title='Descargar']",
            "settings":"//button[@aria-label='Ajustes']",
            "confirm_close_session":"//button[.//div[contains(text(), 'Cerrar sesión')]]",
            "close_session":"//div[@role = 'button' and .//text()[contains(., 'Cerrar sesión')]]",
            "link_invited":"//div[contains(text(),'Enlace de invitación al grupo')]",
            "confirm_reset_link":"//button[.//div[contains(text(), 'Restablecer enlace')]]",
            "reset_link_invited":"//div[@title='Restablecer enlace' and @aria-label='Restablecer enlace']",
            "copy_link_invited":"//div[@title='Copiar enlace' and @aria-label='Copiar enlace']",
            "asign_admin":"//button[.//div[contains(text(), 'Designar como admin. del grupo')]]",
            "solicitud_pendientes":"//div[contains(text(),'Solicitudes pendientes')]",
            "see_solicutud":"//div[@role='dialog'].//button[.//span[contains(text(),'Revisa')]]",
            "search_members" : "//div[contains(@class, 'x13mwh8y')]//div[@role='button' and contains(@class, 'x1ypdohk')][.//span[contains(text(), ' miembros')]]"
        }

    @property
    def containers(self) -> dict[str, str]:
        """Returns a dictionary of container elements."""
        return {
            "chat":"div[class='x3psx0u xwib8y2 xkhd6sd xrmvbpv'][role='application']",
            "info_group":"//div[@class = 'xdj266r xcr5guo xat24cr xd8oflk']",
            "info_group_all":"//div[@class = 'x1n2onr6 xyw6214 x78zum5 x1r8uery x1iyjqo2 xdt5ytf x6ikm8r x1odjw0f x1hc1fzr']",
            "display_info_group":"//div[@class = 'x1n2onr6 xyw6214 x78zum5 xdt5ytf x1iyjqo2 x1odjw0f x150wa6m' and @id = 'pane-side']",
            "list_member":"//div[@class='x1n2onr6 x1n2onr6 xyw6214 x78zum5 x1r8uery x1iyjqo2 xdt5ytf x6ikm8r x1odjw0f x1hc1fzr']",
            "message_group":"//div[@class='_amjv _aotl']",
            "config_group":"//div[@class='x13mwh8y x1q3qbx4 x1wg5k15 x1bnvlk4 x1n2onr6 x1c4vz4f x2lah0s xdl72j9 x13x2ugz xexx8yu x18d9i69 xyorhqc xkhd6sd x4uap5']",
            "text_chat":"//div[@class='x1hx0egp x6ikm8r x1odjw0f x1k6rcq7 x6prxxf']",
            "text_info_member":"//span[@class = 'x1iyjqo2 x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1rg5ohu _ao3e']",
            "p_search":"//p[@class = 'selectable-text copyable-text x15bjb6t x1n2onr6']",
            "opciones_mimebors_children":"//div[@class = 'x1c4vz4f xs83m0k xdl72j9 x1g77sc7 x78zum5 xozqiw3 x1oa3qoh x12fk4p8 xeuugli x2lwn1j x1nhvcw1 x1q0g3np x6s0dn4']",
            "target_mensaje":"//div[@class='_akbu']",
            "target_info_member":"//div[@class = 'x10l6tqk xh8yej3 x1g42fcv']",
            "copyable_text_arg":"//div[contains(@class, 'copyable-text')]",
            "tag_member_to_command":"//span[@class = 'x1ypdohk x1a06ls3 _ao3e selectable-text select-all copyable-text']",
            "input_config_chat":"//div[@class='xdl72j9 x1g77sc7 x78zum5 xozqiw3 x1oa3qoh x12fk4p8 xeuugli x2lwn1j x13a6bvl x1q0g3np x6s0dn4 x1c4vz4f x2lah0s x14qfxbe']",
            "child_input_config_chat":"//div[@class= 'x3nfvp2 xl56j7k x6s0dn4 x1td3qas x1qx5ct2 x7r5mf7 xeyog9w xahult9 x1w4ip6v x1n2onr6 x1ypdohk']",            
            "check_input":"//div[input[@aria-label='Enviar mensajes'] and div[@role='switch']]/div[@role='switch']",
            "menu_opciones_message":"//div[@class='_ak4w' and @role = 'application']",
            "menu_option_file":"//div[@class='_ak4w xacj9c0 xfh8nwu xoqspk4 x12v9rci x138vmkv' and @role = 'application']",
            "option_member":"//div[@class = 'x1bnvlk4 x1n2onr6 x1c4vz4f x2lah0s xdl72j9 xyorhqc x13x2ugz']",
            "modal_dialog": "//div[@role='dialog']",
            "solicitud_pendientes":"//div[@title= 'Solicitudes pendientes']",
            "target_solictudes_pendientes":"//div[@class='x1n2onr6 x1c4vz4f x2lah0s xdl72j9 x13x2ugz xat24cr']",
            "target_solicitud":"//div[@class='x1c4vz4f xs83m0k xdl72j9 x1g77sc7 x78zum5 xozqiw3 x1oa3qoh x12fk4p8 xeuugli x2lwn1j x1nhvcw1 xdt5ytf x1cy8zhl']",
            "listitem":"//div[@role='listitem']",
            "listitem2":"//div[@class='_ak8q']",
            "li":"//li[@role = 'button']",
            "sticker": "//img[starts-with(@alt, 'Sticker')]",
            "img" : "//div[@aria-label='Abrir foto']",
            "video" : "//span[@data-icon='media-play']",
            "gif" : "//span[@data-icon='media-gif']",
            "voice_record":"//span[@data-icon='audio-play']",
        }


    @property
    def attributes(self) -> dict[str, str]:
        """Returns a dictionary of attribute values."""
        return {
            "ahkm":"_ahkm",
            "data_pre_plain_text":"data-pre-plain-text",
            "aria_checked_restringe_chat" : "aria-checked"
        }

    @property
    def limits(self) -> dict[str, int]:
        """Returns a dictionary of file and multimedia limits."""
        return {
            "max_video_size_mb": 16,
            "max_audio_size_mb": 16
        }
    
    def get_xpath(self,category: str,key: str) -> str|bool:
        """
        Returns the XPath from a specific category.

        Parameters:
            category (str): The category name ("buttons", "containers", "attributes", "limits").
            key (str): The button name (e.g., "open_group").

        Returns:
            str: The XPath string.
            bool: False if the XPath is not found.

        Buttons:
            • open_group •
            • open_info_group •
            • see_all_members •
            • see_old_members •
            • close •
            • close2 •
            • back •
            • confirm •
            • aprovee •
            • deneger •
            • group_permission •
            • delete •
            • delete2 •
            • delete_all •
            • menu_contextual •
            • menu_contextual_member •
            • send_file •
            • add_file •
            • download_file •
            • settings •
            • confirm_close_session •
            • close_session •
            • link_invited •
            • confirm_reset_link •
            • reset_link_invited •
            • copy_link_invited •
            • asign_admin •
            • solicitud_pendientes •
            • see_solicutud •
            • search_members •

        Containers:
            • chat •
            • info_group •
            • info_group_all •
            • display_info_group •
            • list_member •
            • message_group •
            • config_group •
            • text_chat •
            • text_info_member •
            • p_search •
            • opciones_mimebors_children •
            • target_mensaje •
            • target_info_member •
            • copyable_text_arg •
            • tag_member_to_command •
            • input_config_chat •
            • child_input_config_chat •
            • check_input •
            • menu_opciones_message •
            • menu_option_file •
            • option_member •
            • modal_dialog •
            • solicitud_pendientes •
            • target_solictudes_pendientes •
            • target_solicitud •
            • listitem •
            • listitem2 •
            • li •
            • sticker •
            • img •
            • video •
            • gif •
            • voice_record •

        Attributes:
            • "ahkm" •
            • "data_pre_plain_text" •
            •"aria_checked_restringe_chat"•
        
        Limites:
            • "max_video_size_mb" •
            • "max_audio_size_mb" •
        """
        categories = {
            "buttons": self.buttons,
            "containers": self.containers,
            "attributes": self.attributes,
            "limites":self.limits
        }

        cate:dict = categories.get(category,{})

        return cate.get(key, False)

    
    def get_element(self, selector : str) -> WebElement:
        """
        Get element del Entity: 

        Params:
            selector (str) : Xpath del elemento
        Returns:
            Web Element to interactions

        """
        return self.utils.wait_to_presence_of_element_located(selector = selector)

    def get_elements(self, selector : str) -> list[WebElement]:
        """
        Get elements del Entity: 

        Params:
            selector (str) : Xpath del elemento
        Returns:
            List [Web Element] to interactions

        """
        return self.utils.wait_to_presence_of_all_elements_located(selector = selector)

    def getValueInputRestringeChat(self,case:True)->bool:
        """Retorna el valor del input de restringe chat"""
        xpath = self.get_xpath(category="containers",key="check_input")
        attr = self.get_xpath(category="attributes",key="aria_checked_restringe_chat")
        """Algoritmo de ingreso a la parte de configuracion de whatssap"""
        if case:
            xpath_info = self.get_xpath(category="buttons",key="open_info_group")
            xpath_group_permission = self.get_xpath( category="buttons",key="group_permission")

            self.utils.wait_to_element_to_be_clickable(selector = xpath_info)
            self.utils.wait_to_element_to_be_clickable(selector = xpath_group_permission)
        
        check : WebElement = self.get_element(selector=xpath)

        value_input = check.get_attribute(name=attr)

        value_input_bool = self.utils.strtoBool(value_input)

        status = "Habilitado" if not value_input_bool else "Inhabilitado"
        print(f"Hubo un cambio en el restringe chat, ahora esta: {status}")

        self.input_restringe_chat = value_input_bool

        return value_input_bool
    
    def getAdminsGroup(self,case : True)->list:
        """
        Dara los numeros o nickname de los administradores, para asi confirmar si el autor es admin o no
        Retornara una lista y cambiara la variable d ela clase self.admins

        Params : 
            care (boo) : en el caso para evitar unos pasos        
        
            ej:
                Si queremos obtener los miembros, este ya no realizara uno o dos pasos para ver los usuarios
        """

        
