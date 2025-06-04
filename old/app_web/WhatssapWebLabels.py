from app_web.config import GROUP_NAME

class WhatssappWebLabels:
    """
    Todos los labels o targets existentes dentro de la aplicacion, para si facilitar la actualizacion y solo instanciar y llamar los elementos
    En este caso solo contendra los selector (XPATH, CLASSNAME...) necesarios parasu busqueda e interaccion de eleemtos del DOM o de la pagina
    
    """
    #BTNS
    BTN_CLICK_TO_OPEN_GROUP : str = f"//span[@title='{GROUP_NAME}']" #btn para abrir el grupo
    BTN_INFO_GROUP = "//div[@title='Detalles del perfil' and @role='button']"
    BTN_SEE_OLD_MEMBERS = "//button[@class='xjb2p0i xk390pu x1heor9g x1ypdohk xjbqb8w x972fbf xcfux6l x1qhh985 xm0m39n xexx8yu x4uap5 x18d9i69 xkhd6sd xh8yej3 x5yr21d']"
    BTN_SEE_ALL_MEMBERS = "//div[@class='_alzb  xnnlda6 xh8yej3 x8x1vt3 x78zum5 x6s0dn4 x16cd2qt x1z0qo99' and @role = 'button']"
    BTN_TO_CLOSE = "//div[@aria-label='Cerrar' and @role='button']"
    BTN_TO_BACK = "//div[@aria-label='Atrás' and @role='button']"
    BTN_TO_CONFIG_GROUP = "//div[@role='button' and contains(@class, 'xkhd6sd') and .//div[contains(text(), 'Permisos del grupo')]]"
    BTN_BOTTOM_TO_DELETE_MULTIPLE = "//button[@title='Eliminar']"
    BTN_TO_DISPLAY_MENU_MENSSAGE = "//div[@aria-label='Menú contextual']"
    BTN_TO_DISPLAY_MENU_MEMBERS_1 = "//button[@aria-label='Abrir el menú contextual del chat']"
    BTN_TO_SEND_FILE = "//div[@aria-label='Enviar']"
    
    BTN_TO_DELETE = ".//button[.//div[contains(text(), 'Eliminar')]]"
    BTN_TO_DELETE_TO_ALL = "//button[.//div[contains(text(), 'Eliminar para todos')]]"
    BTN_TO_OK = "//button[.//div[contains(text(), 'OK')]]"
    BTN_TO_CONFIRM_CERRAR_SESSION = "//button[.//div[contains(text(), 'Cerrar sesión')]]"
    BTN_TO_CONFIRM_RESET_ENLACE_INVITACION = "//button[.//div[contains(text(), 'Restablecer enlace')]]"
    BTN_TO_CLOSE_2 = "//button[@title='Cerrar' and @aria-label='Cerrar']"
    # 
    BTN_RESET_ENLACE_INVITACION = "//div[@title='Restablecer enlace' and @aria-label='Restablecer enlace']"
    BTN_COPY_ENLACE_INVITACION = "//div[@title='Copiar enlace' and @aria-label='Copiar enlace']"
    
    BTN_TO_ASIGN_ADMIN = ".//button[.//div[contains(text(), 'Designar como admin. del grupo')]]"

    BTN_TO_ADJUNTAR_FILES = "//button[@title='Adjuntar']"
    BTN_TO_DOWNLOAD_IMG = "//button[@title='Descargar']"

    
    BTN_TO_APROVE = "//div[@aria-label='Aprobar']"
    BTN_TO_DENEGER = "//div[@aria-label='Rechazar']"
    
    BTN_SOLICITUD_PENDIENTES = "//div[contains(text(),'Solicitudes pendientes')]"
    BTN_ENLACE_INVITACION = "//div[contains(text(),'Enlace de invitación al grupo')]"

    BTN_AJUSTES = "//button[@aria-label='Ajustes']"
    BTN_CLOSE_SESSION = "//div[@role = 'button' and .//text()[contains(., 'Cerrar sesión')]]"
    
    #TEXTS
    TXT_CHAT_GROUP = "//div[@class='x1hx0egp x6ikm8r x1odjw0f x1k6rcq7 x6prxxf']"
    TXT_INFO_MEMBER = ".//span[@class = 'x1iyjqo2 x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1rg5ohu _ao3e']"
    TXT_SOURCE_MEMBERS = "//p[@class = 'selectable-text copyable-text x15bjb6t x1n2onr6']"
    OPTIONES_MIEMBROS_CHILDREN = ".//div[@class = 'x1c4vz4f xs83m0k xdl72j9 x1g77sc7 x78zum5 xozqiw3 x1oa3qoh x12fk4p8 xeuugli x2lwn1j x1nhvcw1 x1q0g3np x6s0dn4']"
    TXT_TARGET_MESSAGE = ".//div[@class='_akbu']"
    TXT_COPYABLE_TEXT_ARG = ".//div[contains(@class, 'copyable-text')]"
    
    TXT_SPAN_CASO_TAG_MEMBER_TO_COMMAND = ".//span[@class = 'x1ypdohk x1a06ls3 _ao3e selectable-text select-all copyable-text']" #data-jid(numero ------@c.us) or data-display
    TXT_RANGE_MEMBER_DISPLAY_INFO = ".//div[@class'_ak8i']"
    # copyable-text div data-pre-plain-text #formate [3:37 PM, 1/30/2025] +54 -----:  #autor

    #INPUTS
    INPUT_CONFIG_GROUP_CHAT = ".//div[@class='xdl72j9 x1g77sc7 x78zum5 xozqiw3 x1oa3qoh x12fk4p8 xeuugli x2lwn1j x13a6bvl x1q0g3np x6s0dn4 x1c4vz4f x2lah0s x14qfxbe']"
    CHILD_INPUT_CONFIG_CHAT = ".//div[@class = 'x3nfvp2 xl56j7k x6s0dn4 x1td3qas x1qx5ct2 x7r5mf7 xeyog9w xahult9 x1w4ip6v x1n2onr6 x1ypdohk']"    
    CHECK_INPUT_CONFIG_GROUP_CHAT = ".//div[@role='switch']"
    #modal/container/display/targets

    CONTAINER_CHAT = "div[class='x3psx0u xwib8y2 xkhd6sd xrmvbpv'][role='application']"

    CONTAINER_INFO_GROUP = "//div[@class = 'xdj266r xcr5guo xat24cr xd8oflk']"
    DISPLAY_INFO_GROUP = "//div[@class = 'x1n2onr6 xyw6214 x78zum5 xdt5ytf x1iyjqo2 x1odjw0f x150wa6m' and @id = 'pane-side']"
    CONTAINER_LIST_MEMBERS =  "//div[@class='x1n2onr6 x1n2onr6 xyw6214 x78zum5 x1r8uery x1iyjqo2 xdt5ytf x6ikm8r x1odjw0f x1hc1fzr']"
    TARGET_INFO_MEMBER = ".//div[@class = 'x10l6tqk xh8yej3 x1g42fcv']"
    CONTAINER_MESSAGES_GROUP = "//div[@class='_amjv _aotl']"
    CONTAINER_CONFIG_GROUP = "//div[@class='x13mwh8y x1q3qbx4 x1wg5k15 x1bnvlk4 x1n2onr6 x1c4vz4f x2lah0s xdl72j9 x13x2ugz xexx8yu x18d9i69 xyorhqc xkhd6sd x4uap5']"
    CONTAINER_MENU_OPTION_MESSAGE = "//div[@class='_ak4w' and @role = 'application']" #_ak4w xacj9c0 xfh8nwu xoqspk4 x12v9rci x138vmkv
    CONTAINER_MENU_OPTION_SEND_FILE = "//div[@class='_ak4w xacj9c0 xfh8nwu xoqspk4 x12v9rci x138vmkv' and @role = 'application']"
    CONTAINER_INFO_GROUP_ALL = "//div[@class = 'x1n2onr6 xyw6214 x78zum5 x1r8uery x1iyjqo2 xdt5ytf x6ikm8r x1odjw0f x1hc1fzr']"
    CONTAINER_ARIA_LABEL = "//div[contains(@class, 'focusable-list-item') and contains(@class, '_amjy') and contains(@class, '_amjw') and (contains(@class, 'message-in') or contains(@class, 'message-out'))]"

    CONTAINER_OPCIONES_MIEMBROS = "//div[@class = 'x1bnvlk4 x1n2onr6 x1c4vz4f x2lah0s xdl72j9 xyorhqc x13x2ugz']"
    MODAL_ROLE_DIALOG = "//div[@role='dialog']" #si existe mira sus btns y contenido de estos 
    #Revisa (solictud para unirse)
    CONTAINER_SOLICITUD_PENDIENTES = "//div[@title= 'Solicitudes pendientes']"
    CONTAINER_TARGET_SOLICITUDES = "//div[@class='x1n2onr6 x1c4vz4f x2lah0s xdl72j9 x13x2ugz xat24cr']"
    TARGET_SOLICITUD = ".//div[@class='x1c4vz4f xs83m0k xdl72j9 x1g77sc7 x78zum5 xozqiw3 x1oa3qoh x12fk4p8 xeuugli x2lwn1j x1nhvcw1 xdt5ytf x1cy8zhl']"
    SEE_DIALOG_BTN = "//div[@role='dialog'].//button[.//span[contains(text(),'Revisa')]]"
    LISTITEM = ".//div[@role='listitem']"
    LISTITEM_NAME_OR_ID = ".//div[@class='_ak8q']"
    #class="_ak8q" name o id
    #class="_ak8i" rango

    #class name
    CLASSNAME_AHKM = "_ahkm"

    #aria-label="Menú contextual"

    #LI
    ELEMENT_UL = ".//li[@role = 'button']" 

    #atributes
    DATA_PRE_PLAIN_TEXT = "data-pre-plain-text"
    DATA_PLAIN_TEXT_ETIQ = "data-plain-text" #la etiquetda
    # data-app-text-template   ---@c.us
    #data-jid ---@c.us

    # Expresión regular para capturar texto o número de teléfono + hora
    PATRON_HOUR = r"\b\d{1,2}:\d{2}\s?[APM]{2}\b" 
    PATRON_HORA_AUTOR = r"\[(\d{1,2}:\d{2}\s?[APM]{2}), .*?\] (.+?):"

    PATRON_NUMERO_TELEFONO = r"^\+?(\d{1,4})?\s?(\(?\d{2,5}\)?[-.\s]?)?\d{4}[-.\s]?\d{4}$"
 
    PATRON_LINK_YOUTUBE =  r'(https?://)?(www\.)?((youtube\.com/watch\?v=|youtu\.be/)[\w-]+)'

    PATRON_ARIA_LABEL = r'Quizá\s+([\w\W]+?)\s+(\+\d{2}\s\d{3}\s\d{6})'

    SIZE_LIMIT_AUDIO : float = 16.0


    BOT_ID = "Lllc"

    IMAGE_STICKER = ".//img[starts-with(@alt, 'Sticker')]"
    IMAGE_NORMAL = ".//div[@aria-label='Abrir foto']"
    VIDEO_NORMAL = ".//span[@data-icon='media-play']"
    GIF_NORMAL = ".//span[@data-icon='media-gif']"
    VOICE_RECORD = ".//span[@data-icon='audio-play']"


    # QUERY_SELECTOR_MULTIMEDIA = "img, span[data-icon='media-play'], span[data-icon='audio-play'], span[data-icon='media-gif']"
    QUERY_SELECTOR_MULTIMEDIA = "div[class = '_amk4 _amkt'], div[class = '_amk4 _amkv'], div[class = '_amk4 _amk9'], div[class = '_amk4 _amku']"


    def with_content(self,content : str)->str:
        """Return xpath"""
        if content:
            return f".//div[@class='_akbu' and contains(., '{content}')]"
