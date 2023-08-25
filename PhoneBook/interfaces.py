# Здесь можно создать различные интерфейсы
# По ТЗ сделан только консольный интерфейс

import os
from typing import List, Callable
from abc import ABC, abstractmethod




from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.text import Text


from .db.strategies import DataBaseStrategy
from .services import ContactsService
from .schemas import Contact



class ContactsAbstractInterface(ABC):
    pass


class Status:
    def __init__(self) -> None:
        self.style = ""
        self.text = ""

    def update(self, text:str, danger:bool = False) -> None:
        self.text = "Status: "+text
        if danger:
            self.style = "red"
        else:
            self.style = "green"

    def reset(self) -> None:
        self.text = ""
        self.style = ""

class ContactsConsoleInterface(ContactsAbstractInterface):
    def __init__(self, contacts_per_page: int = None) -> None:
        """
        @param
        contacts_per_page - If not defined, it is calculated automatically.
        """
        self.service = ContactsService()
        self.on_startup()
        self.console = Console(force_interactive=True)

        self.console.print("PhoneBook | Your guide to the world of contacts")


        # buttons

        self.buttons = {
            'prev': {
                'sym':'p', 
                'text':'Prev page'
            },
            'next': {
                'sym':'n', 
                'text':'Next page'
            },
            'add_contact': {
                'sym':'a',
                'text':'Add contact'
            },
            'find_contact': {
                'sym':'f',
                'text':'Find contact'
            },
            'exit': {
                'sym':'x',
                'text':'Exit (or Ctrl+C)'
            },
            'search_panel': {
                'sym':'s',
                'text':'Exit search panel'
            }
        }

        self.prev_button = self.get_stylized_menu_button(button=self.buttons['prev'])
        self.prev_button__inactive = self.get_stylized_menu_button(button=self.buttons['prev'], inactive=True)
        
        self.next_button = self.get_stylized_menu_button(button=self.buttons['next'])
        self.next_button__inactive = self.get_stylized_menu_button(button=self.buttons['next'], inactive=True)

        self.add_contact_button = self.get_stylized_menu_button(button=self.buttons['add_contact'])

        self.search_panel_disable_button  = self.get_stylized_menu_button(button=self.buttons['search_panel'])

        self.find_contact_button = self.get_stylized_menu_button(button=self.buttons['find_contact'])
        self.find_contact_button__inactive = self.get_stylized_menu_button(button=self.buttons['find_contact'], inactive=True)

        self.exit_button = self.get_stylized_menu_button(button=self.buttons['exit'], danger=True)


        # vars

        self.page:List[Contact] = []
        self.page_num = 1
        self.next = False
        self.prev = False
        
        self.search_panel_enabled = False
        self.search_panel_page:List[Contact] = []
        self.search_panel_contacts:List[Contact] = []
        self.search_panel_next = False
        self.search_panel_prev = False
        self.search_panel_page_num = 1

        self.not_work = False
        self.status = Status()
        self.empty_contacts = self.are_the_contacts_empty()

        # adaptive
        
        self.columns, self.lines = self.get_terminal_size()
        if contacts_per_page is None:
            self.service.NUM_OF_CONTACTS_PER_PAGE = self.calc_num_contacts_per_page()
            self.contacts_per_page_calc_auto = True
        else:
            self.service.NUM_OF_CONTACTS_PER_PAGE = contacts_per_page
            self.contacts_per_page_calc_auto = False

        if self.columns <= 84 or self.lines <= 10:
            self.console.print(f"Error! With this resolution of the console, the program cannot run. Set console size. We highly recommend ({84}<,{30}<)", style='red')
            self.not_work = True




    # Events

    def loop(self) -> None:
        loop = True
        while loop and not self.not_work:
            try:
                ch = self.main_menu()

                if ch in [self.buttons['exit']['sym'],self.buttons['exit']['sym'].upper()]:
                    loop = False

                elif ch in [self.buttons['add_contact']['sym'],self.buttons['add_contact']['sym'].upper()]:
                    self.add_contact_menu()

                elif ch in [self.buttons['find_contact']['sym'],self.buttons['find_contact']['sym'].upper()] and not self.empty_contacts:
                    self.find_contact_menu()

                elif ch in [self.buttons['prev']['sym'],self.buttons['prev']['sym'].upper()]:
                    if self.search_panel_enabled:
                        if self.search_panel_prev:
                            self.search_panel_page_num -= 1
                    else:
                        if self.prev:
                            self.page_num -= 1

                elif ch in [self.buttons['next']['sym'],self.buttons['next']['sym'].upper()]:
                    if self.search_panel_enabled:
                        if self.search_panel_next:
                            self.search_panel_page_num += 1
                    else:
                        if self.next:
                            self.page_num += 1

                elif ch in [self.buttons['search_panel']['sym'],self.buttons['search_panel']['sym'].upper()]:
                    self.search_panel_enabled = False
                    self.search_pane_page_num = 1
                    self.search_panel_page = []
                    self.search_panel_contacts = []

                elif 'del' in ch  and not self.empty_contacts:
                    ch = ch.replace('del', '')
                    try:
                        ch = int(ch)
                    except ValueError:
                        continue
                    if ch in [int(i) for i in range(1, len(self.page)+1)]:
                        self.delete_contact_menu(ch)

                elif ch in [str(i) for i in range(1, len(self.page)+1)]  and not self.empty_contacts:
                    try:
                        ch = int(ch)
                    except ValueError:
                        continue
                    self.edit_contact_menu(ch)
            except KeyboardInterrupt:
                loop = False
        self.on_shutdown()

    def on_startup(self):
        self.service.on_startup()
    def on_shutdown(self):
        self.service.on_shutdown()


    
    # Menu

    def main_menu(self) -> str:
        self.clear_screen()
        # page:List[Contact] = []
        if self.search_panel_enabled:
            page, prev, next = self.service.pagination(self.search_panel_page_num, self.search_panel_contacts)
            self.search_panel_page = page
            self.search_panel_next = next
            self.search_panel_prev = prev
        else:
            page, prev, next = self.service.pagination(self.page_num)
            self.page = page
            self.next = next
            self.prev = prev
        self.print_page(page)

        divider = self.service.NUM_OF_CONTACTS_PER_PAGE - len(page) 
        for i in range(divider * 2):
            self.console.print()
        
        if not self.empty_contacts:
            self.console.print(f"Enter a contact number to [cyan]edit[/cyan] it (1-{len(page)}), when adding [red]'del'[/red] keyword removes it", markup=True)
            if self.search_panel_enabled:
                self.console.print(f"Or enter the symbol of the search panel menu item {self.search_panel_page_num}")
            else:
                self.console.print("Or enter the symbol of the menu item")
        else:
            self.console.print("Oops, no contacts yet :(")
            self.console.print("Create your first contact by entering the keyword [green]'a'[/green]", markup=True)
        self.console.print(self.status.text, style=self.status.style)
        self.status.reset()

        # menu

        if prev:
            self.console.print(self.prev_button)
        else:
            self.console.print(self.prev_button__inactive)

        if next:
            self.console.print(self.next_button)
        else:
            self.console.print(self.next_button__inactive)

        if  not self.empty_contacts:
            self.console.print(self.find_contact_button)
        else:
            self.console.print(self.find_contact_button__inactive)

        if self.search_panel_enabled:
            self.console.print(self.search_panel_disable_button)
        else:
            self.console.print(self.add_contact_button)

        self.console.print(self.exit_button)

        return input(" : ")
    
    def add_contact_menu(self, contact: Contact = None) -> None:
        self.clear_screen()
        self.console.print("# Add contact menu")
        confirm = Confirm.ask("Are you sure you want to create a contact?", default='y')
        if not confirm:
            return None
        if contact is not None:
            first_name = Prompt.ask("Enter first name", default=contact.first_name)
            middle_name = Prompt.ask("Enter middle name", default=contact.middle_name)
            last_name = Prompt.ask("Enter last name", default=contact.last_name)
            company = Prompt.ask("Enter company name", default=contact.company)
            work_phone = Prompt.ask("Enter work phone", default=contact.work_phone)
            personal_phone = Prompt.ask("Enter personal phone", default=contact.personal_phone)
        else:
            first_name = Prompt.ask("Enter first name")
            middle_name = Prompt.ask("Enter middle name")
            last_name = Prompt.ask("Enter last name")
            company = Prompt.ask("Enter company name")
            work_phone = Prompt.ask("Enter work phone")
            personal_phone = Prompt.ask("Enter personal phone")
        contact = Contact(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            company=company,
            work_phone=work_phone,
            personal_phone=personal_phone
        )
        self.console.print(contact)
        confirm = Confirm.ask("All OK? Save?")
        if not confirm:
            contact = self.add_contact_menu(contact)
            return None
        if contact is not None:
            self.service.add(contact)
            self.empty_contacts = self.are_the_contacts_empty()
            self.status.update("Contact added!")
            if self.contacts_per_page_calc_auto:
                self.service.NUM_OF_CONTACTS_PER_PAGE = self.calc_num_contacts_per_page()
        else:
            self.status.update("Contact not added!", danger=True)

    def edit_contact_menu(self, ch:int) -> None:
        self.clear_screen()
        if self.search_panel_enabled:
            contact = self.search_panel_page[ch-1]
        else:
            contact = self.page[ch-1]

        confirm = Confirm.ask("Are you sure you want to edit this contact?", default='y')
        if not confirm:
            self.status.update("Contact not edited!", danger=True)
            return None
        
        first_name = Prompt.ask("Enter first name", default=contact.first_name)
        middle_name = Prompt.ask("Enter middle name", default=contact.middle_name)
        last_name = Prompt.ask("Enter last name", default=contact.last_name)
        company = Prompt.ask("Enter company name", default=contact.company)
        work_phone = Prompt.ask("Enter work phone", default=contact.work_phone)
        personal_phone = Prompt.ask("Enter personal phone", default=contact.personal_phone)

        contact.first_name=first_name
        contact.middle_name=middle_name
        contact.last_name=last_name
        contact.company=company
        contact.work_phone=work_phone
        contact.personal_phone=personal_phone

        self.status.update("Contact edited!")

    def delete_contact_menu(self, nums : int | List[int]) -> None:
        self.clear_screen()
        if isinstance(nums, int):
            if self.search_panel_enabled:
                contact = self.search_panel_page[nums-1]
            else:
                contact = self.page[nums-1]
            self.console.print(contact)
            confirm = Confirm.ask(f"Are you sure you want to delete this contact?")
            if confirm:
                self.service.delete(contact)
                self.status.update("Contact deleted!", danger=True)
                self.empty_contacts = self.are_the_contacts_empty()
                if self.contacts_per_page_calc_auto:
                    self.service.NUM_OF_CONTACTS_PER_PAGE = self.calc_num_contacts_per_page()
        else:
            # TODO Сделать в будущем функцию для удаления множества контактов одной командой (Перечисление их номеров)
            confirm = Confirm.ask("Are you sure you  to delete this contacts?")


    def find_contact_menu(self):
        self.clear_screen()
        query = Prompt.ask("Enter name, company or phone number")
        contacts = self.service.find(query)
        self.console.print(contacts)
        if contacts:
            self.search_panel_contacts = contacts
            self.search_panel_enabled = True
            self.status.update("Here is what you found for your query!")
        else:
            self.status.update("Nothing found for your query!", danger=True)


    # Utils
    def are_the_contacts_empty(self):
        if len(self.service.get_all()) == 0:
            self.search_panel_enabled = False
            return True
        return False

    def clear_screen(self):
        os.system('cls')

    def get_terminal_size(self) -> tuple[int,int]:
        return os.get_terminal_size()

    def calc_num_contacts_per_page(self) -> int:
        lines = self.lines - 11 # Строки занимающие грани таблицы и пункты меню
        return min(lines // 2, len(self.service.get_all()))

    def get_stylized_menu_button(self, button: dict, inactive: bool = False, danger: bool = False) -> Text:
        stylized_button = Text()
        if inactive:
            sym_style = "bold #222222"
            text_style = "#222222"
        else:
            sym_style = "bold blue"
            text_style = ""
        if danger:
            sym_style = "bold red"
            text_style = "red"
        stylized_button.append('|'+button['sym']+'|', style=sym_style)
        stylized_button.append('  '+button['text'], style=text_style)
        return stylized_button

    def print_page(self, contacts_list:List[Contact]) -> None:
        table = Table(show_lines=True, expand=True)
        table.add_column("№", style="green", no_wrap=True, min_width=1)
        table.add_column("First name", style="cyan", no_wrap=True, max_width=12)
        table.add_column("Middle name", style="green", no_wrap=True, max_width=12)
        table.add_column("Last name", style="cyan", no_wrap=True, max_width=12)
        table.add_column("Company", style="green", no_wrap=True, max_width=12)
        table.add_column("Work phone", style="cyan", no_wrap=True, max_width=12)
        table.add_column("Personal phone", style="green", no_wrap=True, max_width=12)

        for n, i in enumerate(contacts_list):
            table.add_row(str(n+1), i.first_name, i.middle_name, i.last_name, i.company, i.work_phone, i.personal_phone)

        self.console.print(table)
