# Структуры данных


import pydantic

class Contact(pydantic.BaseModel):
    first_name: str | None
    middle_name: str | None
    last_name: str | None
    company: str | None
    work_phone: str | None
    personal_phone: str | None