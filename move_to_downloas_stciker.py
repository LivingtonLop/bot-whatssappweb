import os
import shutil
import glob

"""Scripts to manipalucin de multimedia"""

def move_recent_whatsapp_image(downloads_destine :str,downloads_folder = r"~/Downloads")->bool:

    """

        move_recent_whatsapp_image : Funcion para mover la imagen descargada del navegador, en downloads/descargas, para asi overla dentro dle proyecto

        move_recent_whatsapp_image@downloads_destine : str [el path o destino para mover el archivo]

        move_recent_whatsapp_image@downloads_folder : str|r"~/Downloads" [el path o lugar de descarga del archivo de WhatsApp Image {fecha} at HH.MM.SS AM/PM.jpeg]

        return True = [Movida con exito]

        return False = [Fallo en mover]
    
    """

    downloads_folder = os.path.expanduser(downloads_folder)
 
    pattern = os.path.join(downloads_folder, "WhatsApp Image * at *.jpeg")
    images = glob.glob(pattern)

    if not images:
        return False
    
    images.sort(key=os.path.getmtime, reverse=True)
    src_path = images[0]  # Seleccionar la imagen más reciente

    filename = os.path.basename(src_path)  # Extraer el nombre del archivo
    dst_path = os.path.join(downloads_destine, filename)  # Ruta destino

    # Crear la carpeta destino si no existe
    os.makedirs(downloads_destine, exist_ok=True)

    # Evitar sobrescribir archivos
    counter = 1
    while os.path.exists(dst_path):
        name, ext = os.path.splitext(filename)
        dst_path = os.path.join(downloads_destine, f"{name} ({counter}){ext}")
        counter += 1

    # Mover el archivo
    try:
        shutil.move(src_path, dst_path)
        print(f"Imagen movida a: {dst_path}")
    except Exception as e:
        print(f"Error inesperado: {e}")
        return False
        
    return True
        

