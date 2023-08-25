# Репозитории для работы с базами данных


from typing import List
from abc import ABC, abstractmethod


from .db.strategies import JSONStrategy
from .schemas import Contact


class AbstractRepository(ABC):
    strategy = None

    @abstractmethod
    def on_startup():
        raise NotImplementedError
    
    @abstractmethod
    def on_shutdown():
        raise NotImplementedError
    
    @abstractmethod
    def add():
        raise NotImplementedError
    
    @abstractmethod
    def find():
        raise NotImplementedError

    @abstractmethod
    def get_all():
        raise NotImplementedError

    @abstractmethod
    def delete():
        raise NotImplementedError

# JSONStrategy('db.json')

class ContactsRepository:
    def __init__(self) -> None:
        self.strategy = JSONStrategy('db.json')

    def on_startup(self):
        self.strategy.connect()

    def on_shutdown(self):
        self.strategy.disconnect()

    def add(self, contact: Contact) -> None:
        self.strategy.add(contact)

    def find(self, query: str) -> List[Contact]:
        contacts:List[Contact] = []
        for contact in self.get_all():
            add = False
            try:
                if query.upper() in contact.first_name.upper():
                    add = True
            except AttributeError:
                pass
            try:
                if query.upper() in contact.middle_name.upper():
                    add = True
            except AttributeError:
                pass
            try:
                if query.upper() in contact.last_name.upper():
                    add = True
            except AttributeError:
                pass
            try:
                if query.upper() in contact.company.upper():
                    contacts.append(contact)
            except AttributeError:
                pass
            try:
                if query.upper() in contact.work_phone.upper():
                    add = True
            except AttributeError:
                pass
            try:
                if query.upper() in contact.personal_phone.upper():
                    add = True
            except AttributeError:
                pass
            if add:
                contacts.append(contact)
        return contacts

    def get_all(self) -> List[Contact]:
        return self.strategy.get_all()
    
    def delete(self, contact: Contact) -> None:
        self.strategy.delete(contact)
