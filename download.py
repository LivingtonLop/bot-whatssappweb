import yt_dlp
import os
import re

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

class Download:

    """
        Class para descargar audios de Youtube
    
    """

    def __init__(self, output_folder="downloads"):

        """
        
            self.output_folder = carpeta de destino de los audios de Youtube
        
        """
        self.output_folder = output_folder
        os.makedirs(self.output_folder, exist_ok=True)

    def download_audio(self, url)->tuple[str,float]:
        """Descargar el audio"""

        file_path:str = None
        size:float = None 
        
        options = {
            'format': 'bestaudio/best',
            'extract_audio': True,
            'audio_format': 'mp3',
            'outtmpl': f"{self.output_folder}/%(title)s.%(ext)s",
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=False)

            raw_title = info["title"]
            title = self.clean_filename(raw_title)
            # title = info.get('title', 'Unknown')
            artist = info.get('uploader', 'Unknown')

            new_options = options.copy()

            new_options['outtmpl'] = f"{self.output_folder}/{title}.%(ext)s"

            with yt_dlp.YoutubeDL(new_options) as ydl_new:
                ydl_new.download([url]) 

            file_path = f"{self.output_folder}/{title}.mp3"
            self.add_metadata(file_path, title, artist)
            size = self.get_file_size(file_path=file_path)
            print(f"✅ Descargado: {file_path}")

        return (file_path,size)

    def add_metadata(self, file_path, title, artist):
        """Agregar los metadatos"""
        try:
            audio = MP3(file_path, ID3=EasyID3)
            audio["title"] = title
            audio["artist"] = artist
            audio.save()
            print(f"📝 Metadatos añadidos: {title} - {artist}")
        except Exception as e:
            print(f"⚠️ No se pudieron agregar los metadatos: {e}")

    def get_file_size(self, file_path)->float:
        """Obtener el tamaño del archivo"""
        file_size = os.path.getsize(file_path)
        file_size_mb = file_size / (1024 * 1024)
        print(f"📏 Tamaño del archivo: {file_size_mb:.2f} MB")
        return round(file_size_mb, 2)
    

    def clean_filename(self,title):
        """Reemplazar caracteres especiales excepto letras, números y caracteres en japonés"""
        cleaned_title = re.sub(r"[^\wぁ-んァ-ン一-龥ー]+", "_", title)
        return cleaned_title.strip("_")  # Eliminar guiones bajos al inicio/final

