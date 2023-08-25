from PhoneBook.interfaces import ContactsConsoleInterface
from PhoneBook.db.strategies import JSONStrategy, SQLiteStrategy

interface = ContactsConsoleInterface()
interface.loop()