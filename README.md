# Телефонная книга

Данное приложение представляет собой консольную книгу для управления своими контактами

 Стек технологий: Python, Pydantic

## Для начала работы (Windows)
```
python -m venv venv

./venv/scripts/activate

pip install -r requirements.txt

python main.py
```


## Структура данных контакта
```python
class Contact(pydantic.BaseModel):
    first_name: str | None
    middle_name: str | None
    last_name: str | None
    company: str | None
    work_phone: str | None
    personal_phone: str | None
```

## Функционал

Контакты можно создавать, удалять, редактировать и искать по нужным вам параметрам.

## Архитектура

Архитектуре я выделил достаточное внимание, поэтому все внешние компоненты такие как способ хранения данных и интерфейс можно сменить не трогая бизнес логику.

### Стратегия хранения данных

Например для смены способа хранения данных нужно создать новый класс и сделать его наследником абстракного класса <code>DataBaseStrategy</code>, а в репозитории <code>ContactsRepository</code> переменную <code>strategy</code> изменить на созданный Вами класс.

В файле <code>strategies</code> для наглядной демонстрации простой смены стратегии хранения данных я начал создавать новую стратегию в которой хранение будет происходить с помощью sqlite3

### Интерфейс

Чтобы сменить интерфейс, и подключить например Flask или FastAPI. Нужно импортировать <code>ContactsService</code> и с помощью документации которая будет описана ниже интегрировать ее с эндпоинтами API. Позже планируется добавить пример такой реализации.

P.S.Так же в будущем планируется добавить возможность смены модели контакта. Пока что бизнес логика сильно связана с текущей структурой данных контакта

## Документация

### <code>ContactsService</code> 

#### function <code>on_startup</code>

В любой интерфейсе созданный вами нужно будет единоразово вызвать данный метод перед началом работы с приложением.

#### function <code>on_shutdown</code>

В любой интерфейсе созданный вами нужно будет единоразово вызвать данный метод в конце работы с приложением.

#### function <code>pagination</code>

Метод принимает два свойства.
- <code>page_num</code> - Integer. Страница которая нужна.
- <code>contacts</code> - Список объектов класса <code>Contact</code>. Если ничего не передается то данные загружаются из базы.

Метод возвращает три свойства.
1. Результат выполнения функции <code>get_page</code> (Будет описана ниже)
2. Результат выполнения функции <code>prev</code> (Будет описана ниже)
3. Результат выполнения функции <code>next</code> (Будет описана ниже)

Данный метод нужен. Для того чтобы не выполнять три функции. Т.е. снижает походы в базу данных с 3 до 1.

#### function <code>prev</code>

Принимает номер страницы и в ответ дает булево значени. Если истина то есть возможность загрузить предыдущую страницу

#### function <code>prev</code>

Принимает номер страницы и в ответ дает булево значени. Если истина то есть возможность загрузить следующую страницу

#### function <code>get_page</code>

Принимает номер страницы и в ответ дает список объектов класса <code>Contact</code>

#### function <code>add</code>

Принимает объект класса <code>Contact</code> и сохраняет его в базе данных

#### function <code>find</code>

Принимает строку и вызывает метод <code>find/code> с переданным аргументом

#### function <code>get_all</code>

Возвращает список объектов класса <code>Contact</code>

#### function <code>delete</code>

Принимает объект класса <code>Contact</code> и удаляет его из базы данных

### TODO

- #### Дописать документацию.