---
transition: slide-left
theme: sirius-college
exportFilename: pdf/oop_lection_5
layout: cover
title: oop_5
mdc: true
---

# Объектно-ориентированное программирование<br>Лекция 5: `dataclass`, `mixin` и декорирование классов

`dataclass`: упрощение создания классов данных. `mixin`-классы для повторного использования поведения. Декорирование классов: применение декораторов к классам.

---

# Dataclasses


````md magic-move
```python {*}{maxHeight: '420px'}
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


p = Point(0, 0)
print(p)
# <__main__.Point object at 0x7f45e98f4590>
```

```python {*}{maxHeight: '420px'}
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"point({self.x}, {self.y})"

        
p = Point(0, 0)
print(p)
# point(0, 0)
```

```python {*}{maxHeight: '420px'}
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"point({self.x}, {self.y})"

    
    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented()
        return self.x == other.x and self.y == other.y
```
````

---

# Dataclasses

**Dataclasses** призваны автоматизировать генерацию кода классов, которые используются для хранения данных. Не смотря на то, что они используют другие механизмы работы, их можно сравнить с "изменяемыми именованными кортежами со значениями по умолчанию".

<v-click>

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

p1 = Point(1.0, 2.0)
p2 = Point(1.0, 2.0)
print(p1) # Point(x=1.0, y=2.0)
print(p1 == p2) # True
```

</v-click>

---

# Dataclasses: Добавляем возможность сравнения

По умолчанию `dataclass` не знает, как сравнивать объекты. Мы можем включить эту возможность с помощью параметра `order=True`.

> `order=True` автоматически генерирует методы `__lt__`, `__le__`, `__gt__`, `__ge__`. Сравнение происходит поэлементно, как у кортежей.

```python {*|8-10|12|14-15|17-19}{maxHeight: '260px'}
from dataclasses import dataclass

@dataclass(order=True)
class Student:
    gpa: float  # Сортировка будет в первую очередь по среднему баллу
    name: str

s1 = Student(4.5, "Анна")
s2 = Student(4.9, "Иван")
s3 = Student(4.5, "Борис")

print(s1 < s2)  # True

# Если gpa одинаковый, сравнение идет по второму полю (name)
print(s3 < s1)  # False

students = [s1, s2, s3]
print(sorted(students))
# [Student(gpa=4.5, name='Анна'), Student(gpa=4.5, name='Борис'), Student(gpa=4.9, name='Иван')]
```

---

# Dataclasses: Создание неизменяемых объектов

Иногда важно гарантировать, что данные в объекте не будут случайно изменены после его создания. Параметр `frozen=True` делает объект **иммутабельным (неизменяемым)**.

> `frozen=True` запрещает присваивание значений атрибутам после инициализации. При попытке изменения будет вызвана ошибка `FrozenInstanceError`.

---

# Dataclasses: Создание неизменяемых объектов

> Это делает объекты-конфигурации или ключи словарей более безопасными и предсказуемыми.

```python {*|1|3|3-7|9|11|13-19|}{maxHeight: '350px'}
from dataclasses import dataclass, FrozenInstanceError

@dataclass(frozen=True)
class Config:
    host: str
    port: int
    user: str

db_config = Config("localhost", 5432, "admin")

print(db_config.host)  # 'localhost'

try:
    # Попытка изменить атрибут "замороженного" объекта
    db_config.host = "127.0.0.1"
except FrozenInstanceError as e:
    print(f"Ошибка: {e}")

# Ошибка: cannot assign to field 'host'
```

---

# Dataclasses: Настройка полей с помощью `field`

Функция `field` из модуля `dataclasses` позволяет тонко настраивать каждое поле класса.

::v-clicks

**Основные параметры `field`:**
- `default`: Задает простое значение по умолчанию.
- `default_factory`: Задает **функцию**, которая будет вызвана для создания значения по умолчанию (например, `list` для пустого списка).
- `repr=False`: Исключает поле из метода `__repr__`.
- `init=False`: Исключает поле из метода `__init__`. Полезно для вычисляемых полей.
  ::

---

# Dataclasses: Настройка полей с помощью `field`


```python {*|1-2|6-9|11-12|14-15|17-19|21-24}{maxHeight: '420px'}
from dataclasses import dataclass, field
import uuid

@dataclass
class User:
    username: str
    # default_factory нужен для изменяемых типов, чтобы избежать
    # использования одного и того же списка для всех объектов
    friends: list[str] = field(default_factory=list)
    
    # Исключаем пароль из вывода для безопасности
    password_hash: str = field(repr=False)
    
    # Это поле не будет в __init__, оно вычисляется позже
    user_id: str = field(init=False)

    def __post_init__(self):
        # Специальный метод, вызывается после __init__
        self.user_id = str(uuid.uuid4())

user = User("Alice", password_hash="a1b2c3d4")
print(user)
# User(username='Alice', friends=[])
# (password_hash и user_id не попали в repr)
```

---

# Dataclasses

```python
@dataclasses.dataclass(*, init=True, repr=True, eq=True, order=False, 
unsafe_hash=False, frozen=False, match_args=True, kw_only=False, 
slots=False, weakref_slot=False)
```

::v-clicks

- `unsafe_hash` — создаёт `__hash__`, даже если объект изменяемый (использовать с осторожностью).
- `frozen` — делает экземпляры неизменяемыми (аналог immutable).
- `match_args` — позволяет использовать позиционное сопоставление в `match`.
- `kw_only` — делает поля только именованными аргументами в конструкторе.
- `slots` — создаёт класс с `__slots__`, экономит память и запрещает новые атрибуты.
- `weakref_slot` — добавляет слот для поддержки weak references.

::

---

# Mixins

**Mixin-классы (примеси)** - это классы у которых нет данных, но есть методы. Mixin используются для добавления одних и тех же методов в разные классы.

- **Наследование** — это отношение "is-a" (Dog is an Animal). 
- **Композиция** — это "has-a" (Car has an Engine). 
- **Миксин** — это "provides-a" (Person provides a JsonExport capability).

<br>

::v-clicks

> Миксины не предназначены для создания экземпляров. Это просто "примесь" функциональности.

::

---

```python {*|3-6|6|8-11|8|13-16|18-21}{maxHeight: '420px'}
import json

class JsonMixin:
    def to_json(self):
        """Преобразуем атрибуты объекта в словарь"""
        return json.dumps(self.__dict__, indent=4, ensure_ascii=False)

class Person(JsonMixin):
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Book(JsonMixin):
    def __init__(self, title, author):
        self.title = title
        self.author = author

p = Person("Иван", 30)
b = Book("Война и мир", "Л.Н. Толстой")
print(p.to_json())
print(b.to_json())
```

---

# Декорирование классов

```python
def add_str_dunder(class_):
    def wrapper(self):
        attrs = [f'{k}={v}' for k, v in self.__dict__.items()]
        return ", ".join(attrs)
    setattr(class_, "__str__", wrapper)
    return class_

@add_str_dunder
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

print(Person('Petya', 20))
# name=Petya, age=20
```

---

```python {*|3-7|4-6|9-11|13-15|18-21}{maxHeight: '420px'}
PLUGINS = {}

def register_plugin(name):
    def decorator(cls):
        PLUGINS[name] = cls
        return cls
    return decorator

@register_plugin("video")
class VideoPlugin:
    def play(self): print("Playing video")

@register_plugin("audio")
class AudioPlugin:
    def play(self): print("Playing audio")


plugin_name = "video"
plugin_class = PLUGINS[plugin_name]
plugin_instance = plugin_class()
plugin_instance.play()
```

---

```python {*|1-7|3-6|4-5|6|9-12|14-16}{maxHeight: '420px'}
def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class DatabaseConnection:
    def __init__(self):
        print("Создано новое подключение к БД")

conn1 = DatabaseConnection()
conn2 = DatabaseConnection()
print(conn1 is conn2) # True
```

