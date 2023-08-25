# Бизнес логика


from typing import List
from abc import ABC, abstractmethod

from .schemas import Contact
from .repositories import ContactsRepository



class ContactsService:
    def __init__(self) -> None:
        self.repo = ContactsRepository()


        # Const

        self.NUM_OF_CONTACTS_PER_PAGE = 3


    # Events
    
    def on_startup(self) -> None:
        """
        Единоразово вызывается перед началом работы с приложением.
        """
        self.repo.on_startup()

    def on_shutdown(self) -> None:
        """
        Единоразово вызвается в конце работы с приложением.
        """
        self.repo.on_shutdown()



    # Pagination

    def pagination(self, page_num:int, contacts:List[Contact]=None) -> (List[Contact], bool, bool):
        """
        @param
        first item - List of NUM_OF_CONTACTS_PER_PAGE contacts
        @param
        second item - Has prev page
        @param
        last item - Has next page
        """
        if contacts is None:
            contacts = self.repo.get_all()
        return (self.get_page(page_num, contacts), self.prev(page_num, contacts), self.next(page_num, contacts))

    def prev(self, page_num:int, contacts:List[Contact]=None) -> bool:
        if len(self.get_page(page_num-1, contacts)) != 0:
            return True
        return False
    
    def next(self, page_num:int, contacts:List[Contact]=None) -> bool:
        if len(self.get_page(page_num+1, contacts)) != 0:
            return True
        return False
    
    def get_page(self, page_num: int, contacts:List[Contact]=None) -> list:
        if contacts is None:
            contacts = self.repo.get_all()
        return contacts[self.NUM_OF_CONTACTS_PER_PAGE * page_num - self.NUM_OF_CONTACTS_PER_PAGE:self.NUM_OF_CONTACTS_PER_PAGE * page_num]
    

    def add(self, contact: Contact) -> None:
        self.repo.add(contact)

    def find(self, query:str) -> List[Contact]:
        return self.repo.find(query)

    def get_all(self) -> List[Contact]:
        return self.repo.get_all()
    
    def delete(self, contact: Contact) -> None:
        self.repo.delete(contact)