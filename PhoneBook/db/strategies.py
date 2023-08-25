import json
import sqlite3
from typing import List
from abc import ABC, abstractmethod
from ..schemas import Contact



class DataBaseStrategy(ABC):
    @abstractmethod
    def connect():
        raise NotImplementedError

    @abstractmethod
    def disconnect():
        raise NotImplementedError

    @abstractmethod
    def add():
        raise NotImplementedError

    @abstractmethod
    def get():
        raise NotImplementedError

    @abstractmethod
    def get_all():
        raise NotImplementedError

    @abstractmethod
    def delete():
        raise NotImplementedError


class JSONStrategy(DataBaseStrategy):
    def __init__(self, path_to_file:str) -> None:
        self.path_to_file = path_to_file
        self.contacts:List[Contact] = []

        try:
            with open(self.path_to_file, 'x') as f:
                pass
        except FileExistsError:
            pass
        
    def connect(self):
        f = open(self.path_to_file, 'r', encoding='utf8')
        try:
            data = json.loads(f.read())
        except json.decoder.JSONDecodeError:
            f = open(self.path_to_file, 'w')
            json.dump([], f, ensure_ascii=False)
        f.close()
        
        for i in data:
            self.contacts.append(Contact.model_validate(i))

    def disconnect(self):
        contacts = []
        for i in self.contacts:
            contacts.append(i.model_dump())

        f = open(self.path_to_file, 'w', encoding='utf8')
        json.dump(contacts, f, ensure_ascii=False)
        f.close()


    # CRUD

    def add(self, contact: Contact) -> None:
        self.contacts.append(contact)

    def get(self, id: int) -> Contact:
        return self.contacts[id]

    def get_all(self) -> List[Contact]:
        return self.contacts
    
    def delete(self, contact: Contact) -> None:
        del self.contacts[self.contacts.index(contact)]


# Незаконченный пример реализации с другой базой данных

class SQLiteStrategy(DataBaseStrategy):
    def __init__(self, path_to_sqlite_file: str) -> None:
        self.path_to_sqlite_file = path_to_sqlite_file
        self.con = None

    def connect(self):
        self.con = sqlite3.connect(self.path_to_sqlite_file)
        cur = self.con.cursor()
        cur.execute("CREATE TABLE contacts(first_name, middle_name, last_name, company, work_phone, personal_phone)")
        self.con.commit()

    def disconnect():
        pass

    # CRUD

    def add(self, data:dict) -> None:
        cur = self.con.cursor()
        cur.execute("INSERT INTO contacts VALUES ('')")

    def get(self):
        pass

    def get_all(self):
        pass

    def delete(self):
        pass