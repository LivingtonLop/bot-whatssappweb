import json
import os
from typing import List, Optional
from datetime import datetime


class DataJson:
    def __init__(self, group_name: str, admins: Optional[List[str]] = None, members: Optional[List[str]] = None,old_members: Optional[dict[str,int]] = None,ban_members: Optional[List[str]] = None, path_folder = "src/data"):
        self.group_name = group_name
        self.directory = path_folder  # Carpeta donde se guardarán los archivos JSON
        self.file_path = os.path.join(self.directory, f"{group_name}.json")
        # Crear estructura inicial
        self.structure = {
            group_name: {
                "admins": admins if admins else [],
                "members": members if members else [],
                "old_members": old_members if old_members else {},
                "ban_members": ban_members if ban_members else [],
                "auto":"2025-02-19"
            }
        }

        # Asegurar que la carpeta exista
        os.makedirs(self.directory, exist_ok=True)

    def save(self) -> bool:
        """Guarda la estructura en un archivo JSON dentro del directorio 'data/'."""
        try:
            with open(self.file_path, "w") as file:
                json.dump(self.structure, file, indent=4)
            return True
        except Exception as e:
            print(f"Error al guardar el archivo JSON: {e}")
            return False

    def load(self) -> bool:
        """Carga los datos desde el archivo JSON si existe."""
        try:
            if not os.path.exists(self.file_path):
                return False  # No hay archivo, se mantiene la estructura inicial

            with open(self.file_path, "r") as file:
                self.structure = json.load(file)
            return True
        except Exception as e:
            print(f"Error al cargar el archivo JSON: {e}")
            return False

    def find_member(self, name: str) -> str:
        """Busca un miembro en admins o members y devuelve su rol."""
        if name in self.structure[self.group_name]["admins"]:
            return "admin"
        elif name in self.structure[self.group_name]["members"]:
            return "member"
        elif name in self.structure[self.group_name]["old_members"]:
            return "old"
        elif name in self.structure[self.group_name]["ban_members"]:
            return "ban"
        return "not found"

    def add_member(self, name: str) -> bool:
        """Agrega un nuevo miembro si no existe."""
        if self.find_member(name) == "not found":
            self.structure[self.group_name]["members"].append(name)
            return self.save()
        return False

    def add_admin(self, name: str) -> bool:
        """Agrega un nuevo miembro si no existe."""
        if self.find_member(name) == "not found":
            self.structure[self.group_name]["admins"].append(name)
            return self.save()
        return False
        

    def add_multiples(self, members: list, label: str, replace = False):
        if label not in ["admins", "members"]:
            raise ValueError("Label debe ser 'admins' o 'members'")

        group_data = self.structure[self.group_name]

        if "old_members" not in group_data:
            group_data["old_members"] = {}  # Inicializar si no existe

        if "ban_members" not in group_data:
            group_data["ban_members"] = []  

        existing_members = set(group_data[label])
        new_members = set(members)

        # Identificar miembros que salieron
        removed_members = existing_members - new_members  

        # Agregar a old_members con un conteo de salidas
        for member in removed_members:
            if member in group_data["old_members"]:
                group_data["old_members"][member] += 1
            else:
                group_data["old_members"][member] = 1

            # Limitar a 3 veces máximo
            if group_data["old_members"][member] > 3:
                group_data["ban_members"].append(member)
                del group_data["old_members"][member]  # Se borra si supera el límite

        # Actualizar la lista con los nuevos miembros
        if replace:
            group_data[label].extend(list(new_members))
        else:
            group_data[label] = list(new_members)

        self.save()
        return True

    def ban_member(self, name: str) -> bool:
        """Elimina un usuario de la lista de miembros o admins."""
        role = self.find_member(name)
        if role == "admin":
            self.structure[self.group_name]["ban_members"].append(name)
            self.structure[self.group_name]["admins"].remove(name)
            self.structure[self.group_name]["members"].remove(name)
        elif role == "member":
            self.structure[self.group_name]["ban_members"].append(name)    
            self.structure[self.group_name]["members"].remove(name)
        else:
            return False
        return self.save()

    def promote_member(self, name: str) -> bool:
        """Promueve un miembro a admin si está en la lista de miembros."""
        if self.find_member(name) == "member":
            # self.structure[self.group_name]["members"].remove(name)
            if name not in self.structure[self.group_name]["admins"]:  # Evitar duplicados
                self.structure[self.group_name]["admins"].append(name)
            return self.save()
        return False

    def demote_admin(self, name: str) -> bool:
        """Degrada un admin a miembro si está en la lista de admins."""
        if self.find_member(name) == "admin":
            self.structure[self.group_name]["admins"].remove(name)
            if name not in self.structure[self.group_name]["members"]:  # Evitar duplicados
                self.structure[self.group_name]["members"].append(name)
            return self.save()
        return False

    def get_members(self, label : str)->list:
        if label not in ["admins", "members"]:
            raise ValueError("Label debe ser 'admins' o 'members'")
        return self.structure[self.group_name].get(label, [])    
    
    def get_size_members(self, label:str)->int:
        if label not in ["admins", "members"]:
            raise ValueError("Label debe ser 'admins' o 'members'")
        return len(self.structure[self.group_name].get(label, []))    
        
    def get_old_member_number (self,target : str)->int:
        
        value = 0
        dict_:dict = self.structure[self.group_name].get("old_members", {})
        if dict_:
            value = dict_.get(target,0)

        return value
    
    def get_datetime(self):
        return self.structure[self.group_name].get("auto", False)
        
    def add_date_time(self,date : datetime):
        group_data = self.structure[self.group_name]

        if "auto" not in group_data:
            group_data["auto"] = str(date) 
            return self.save()

        group_data["auto"]=str(date)
        
        return self.save()
