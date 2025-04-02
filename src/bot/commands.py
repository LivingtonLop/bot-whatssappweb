from src.models.CommandClass import CommandClass

class Commands():
    """
    List Commands (Modifique this files, with new commands to webapp)
    
    """

    MENU : str = """

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
    def __init__(self, commands : CommandClass):
        """"""
        self.commands = commands

    @classmethod
    def getMenu(cls)->str:
        return cls.MENU
    
    def menu(self,*args):
        """Despliege del menu [ok] revision 01/04/2025"""
        self.commands.print_menu_in_chat(menu_texto=self.getMenu())

    def all(self,*args):
        """"""

    def promover(self,*args):
        """"""

    def despromover(self,*args):
        """"""

    def ban(self,*args):
        """"""

    def shh(self,*args):
        """Restringir el chat [ok] revision 02/04/2025"""
        self.commands.restringe_chat()

    def r_link(self,*args):
        """"""

    def audio(self,*args):
        """"""

    def sticker(self,*args):
        """"""

    def enlace(self,*args):
        """"""

    def admins(self,*args):
        """"""

    def bye(self,*args):
        """Salida de session [ok] revision 01/04/2025"""
        self.commands.close_session()
        self.commands.driver.quit()