---
transition: slide-left
theme: sirius-college
exportFilename: pdf/oop_lection_8
layout: cover
title: oop_8
mdc: true
---

# Объектно-ориентированное программирование<br>Лекция 8: Метаклассы, Дескрипторы и Фабрики классов

Дескрипторы (`__get__`, `__set__`, `__delete__`). Фабрики классов. Введение в метапрограммирование. Понятие метаклассов, `type()`. Создание пользовательских метаклассов.

---

# Дескрипторы

````md magic-move
```python
class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity
```

```python
class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError
        if value < 0:
            raise ValueError
        self._price = value
```

```python
class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    ...

    @property
    def quantity(self):
        return self._quatity

    @quantity.setter
    def quantity(self, value):
        if not isinstance(value, int):
            raise TypeError
        self._quatity = value
```
````

---

# Дескрипторы

**Дескриптор** — это класс, который реализует хотя бы один из методов протокола дескриптора: `__get__`, `__set__` или `__delete__`.
Экземпляр этого класса назначается как атрибут **другого** класса.

> Дескриптор — это «менеджер» конкретной переменной. Сам объект не хранит данные и не проверяет их, он делегирует эту работу менеджеру (Дескриптору).

---

# Протокол дескриптора (Методы)

::v-clicks

| Метод        | Сигнатура                         | Когда вызывается                          | Описание аргументов                                                                                                               |
| :----------- | :-------------------------------- | :---------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------- |
| **Get**      | `__get__(self, instance, owner)`  | При чтении атрибута:<br>`print(obj.attr)` | `self` — сам дескриптор.<br>`instance` — объект, у которого читают атрибут (Студент).<br>`owner` — класс объекта (class Student). |
| **Set**      | `__set__(self, instance, value)`  | При записи:<br>`obj.attr = 10`            | `value` — новое значение, которое пытаются присвоить.                                                                             |
| **Delete**   | `__delete__(self, instance)`      | При удалении:<br>`del obj.attr`           | `instance` — объект, у которого удаляют атрибут.                                                                                  |
| **Set Name** | `__set_name__(self, owner, name)` | При создании класса (Python 3.6+)         | Автоматически сообщает дескриптору имя переменной, к которой он привязан.                                                         |

    ::

---

# Где хранить данные?

::v-clicks

- **Ошибка:** Хранить значение в `self.value` внутри дескриптора. Значение станет общим для **всех** экземпляров класса (так как дескриптор создается один раз на уровне класса).
- **Правило:** Дескриптор должен хранить данные внутри `instance` (экземпляра объекта, который его использует), обычно в словаре `instance.__dict__`.

  ::

---

# Пример дескриптора

```python {*|1|2-3|5-8|6-7|8|10-17|12-15|17|19-25|20-21|24-25|28-29}{maxHeight: '420px'}
class Integer:
    def __set_name__(self, owner, name):
        self.name = "_" + name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.name, 0)

    def __set__(self, instance, value):
        print(f"Установка значения для {self.name}")
        if not isinstance(value, int):
            raise TypeError("Значение должно быть целым числом")
        if value < 0:
            raise ValueError("Значение не может быть отрицательным")

        setattr(instance, self.name, value)

class Point:
    x = Integer()
    y = Integer()

    def __init__(self, x, y):
        self.x = x
        self.y = y

p1 = Point(10, 20)
p1.x = 100  # Вызовет __set__ у дескриптора Integer
p1.y = "строка" # Вызовет TypeError
```

<!--
- Автоматически запоминаем имя атрибута (например, "score") 

- instance - это конкретный объект (например, student1)
  Если обращаемся через класс (Student.score), instance будет None
  Достаем значение из словаря самого объекта

- Сохраняем значение в сам объект, а не в дескриптор!
-->

---

# Виды дескрипторов (Data vs Non-Data)

::v-clicks{depth=2}

1.  **Дескрипторы данных (Data Descriptors):** Реализуют `__set__` или `__delete__`.
    - Имеют приоритет над словарем объекта `__dict__`. Даже если в объекте есть атрибут с таким именем, Python все равно вызовет дескриптор.
2.  **Дескрипторы без данных (Non-Data Descriptors):** Реализуют только `__get__`.
    - Имеют приоритет **ниже**, чем `__dict__`.
    - _Пример:_ Обычные методы в Python — это дескрипторы без данных (они превращают функцию в связанный метод при доступе).

    ::

---

# Применение дескрипторов

1.  **`@property`**, **`@classmethod`**, **`@staticmethod`** — это всё дескрипторы "под капотом".
2.  **ORM (Django, SQLAlchemy):** Когда в Django пишут `name = models.CharField(...)`, `CharField` — это мощный дескриптор, который отвечает за валидацию, связь с базой данных и отслеживание изменений.

---

# Дескрипторы

````md magic-move
```python
class Order:
    @property
    def price(self): ...
    @price.setter
    def price(self, val): # проверка > 0

    @property
    def quantity(self): ...
    @quantity.setter
    def quantity(self, val): # та же проверка > 0!

    # И так много раз...
```

```python
class PositiveNumber:
    # Логика проверки 1 раз
    ...

class Order:
    price = PositiveNumber()
    quantity = PositiveNumber()
    discount = PositiveNumber()
```
````

---

# Фабрики классов (Class Factories)

**Фабрика классов** — это функция или метод, которые создают и возвращают **новый класс**.

В Python класс — это тоже объект (экземпляр метакласса `type`). Значит, мы можем:

1. Создать класс внутри функции.
2. Вернуть класс как результат работы функции.
3. Присвоить класс переменной.

---

# Реализация №1: Функция-обертка

Самый простой способ создать фабрику классов — определить класс внутри функции.

```python {*|1-2|4-14|1,9,11|16-17|19,22,25|20,23,26}{maxHeight: '370px'}
def create_robot_class(robot_type):
    """Фабрика, создающая классы роботов с разным приветствием."""

    class Robot:
        def __init__(self, name):
            self.name = name

        def say_hello(self):
            if robot_type == "war":
                return f"{self.name}: Готов уничтожать!"
            elif robot_type == "service":
                return f"{self.name}: Чем могу помочь?"
            else:
                return f"{self.name}: Бип-буп."

    # Возвращаем сам КЛАСС (не экземпляр!)
    return Robot

WarRobot = create_robot_class("war")         # WarRobot теперь — это класс
ServiceRobot = create_robot_class("service") # ServiceRobot — другой класс

terminator = WarRobot("T-800")
wall_e = ServiceRobot("Wall-E")

print(terminator.say_hello())  # T-800: Готов уничтожать!
print(wall_e.say_hello())      # Wall-E: Чем могу помочь?
```

---

# Реализация №2: Использование `type()`

Функция `type` имеет два применения:

1. `type(obj)` — возвращает тип объекта.
2. `type(name, bases, dict)` — **создает новый класс**.
   - `name` (`str`): Имя будущего класса (то, что будет в `__name__`).
   - `bases` (`tuple`): Кортеж родительских классов (наследование).
   - `dict` (`dict`): Пространство имен класса (атрибуты и методы).

---

# Реализация №2: Использование `type()`

```python {*|4-12|5|6|7-11|8|9|10,1-2|14-16}{maxHeight: '360px'}
def say_hello_func(self):
    return f"Привет, я {self.name}"

User = type(
    'User',              # Имя класса
    (),                  # Родители (пустой кортеж)
    {                    # Атрибуты и методы
        'category': 'person',
        '__init__': lambda self, name: setattr(self, 'name', name),
        'hello': say_hello_func
    }
)

u = User("Alice")
print(u.hello())      # Привет, я Alice
print(type(u))        # <class '__main__.User'>
```

::v-click

> **Пример из жизни:** `collections.namedtuple` — это классическая фабрика классов в стандартной библиотеке.

::

---

# Метапрограммирование

**Метапрограммирование** — это написание программ, которые управляют другими программами (или самими собой). В контексте Python это означает **перехват и изменение процесса создания классов**.

:::v-clicks{depth=2}

**Аналогия "Печенье и Формочка"**:

1.  **Объект** (instance) — это **Печенье**.
2.  **Класс** (class) — это **Формочка** для печенья (инструкция, как делать объекты).
3.  **Метакласс** (metaclass) — это **Завод по производству формочек**.

> Метакласс создает классы. Классы создают объекты.

:::

---

# Роль `type`

`type` — это встроенный метакласс по умолчанию. Все классы в Python являются экземплярами `type`.

```python
class A: pass

print(type(A())) # <class '__main__.A'> (Объект создан классом A)
print(type(A))   # <class 'type'>       (Класс A создан метаклассом type)
```

---

# Создание своего метакласса

Чтобы изменить поведение создания класса, нужно наследоваться от `type`.

**Основные методы метакласса:**

1.  `__new__(mcs, name, bases, attrs)`:
    - Вызывается **до** создания класса.
    - Именно здесь мы можем изменить атрибуты, добавить методы или проверить имя класса.
2.  `__init__(cls, name, bases, attrs)`:
    - Вызывается **после** создания класса (для инициализации).

---

# Пример<br>Метакласс для валидации (Naming Convention)

```python {*|1|2-11|2-4|8-9|11|13-15|17-19}{maxHeight: '420px'}
class CamelCaseMeta(type):
    def __new__(mcs, name, bases, attrs):
        # mcs - это сам метакласс
        # name - имя создаваемого класса (например, "my_class")

        print(f"Метакласс: Проверяю имя класса '{name}'...")

        if not name[0].isupper():
            raise TypeError(f"Класс {name} должен начинаться с большой буквы!")

        return super().__new__(mcs, name, bases, attrs)

class GoodClass(metaclass=CamelCaseMeta):
    pass
# Вывод: Метакласс: Проверяю имя класса 'GoodClass'... (Успех)

class bad_class(metaclass=CamelCaseMeta):
    pass
# Ошибка: TypeError: Класс bad_class должен начинаться с большой буквы!
```

---

# Практический пример<br>Автоматическая регистрация (Registry)

```python {*|1-9|1|2|4-9|4|5|7-9|9|11-13|15-16|18-19|22-23}{maxHeight: '420px'}
class PluginMeta(type):
    plugins = []

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)

        if name != "Plugin":
            print(f"Регистрация плагина: {name}")
            PluginMeta.plugins.append(cls)

class Plugin(metaclass=PluginMeta):
    """Базовый класс для всех плагинов"""
    def action(self): pass

class AudioPlugin(Plugin):
    def action(self): print("Playing Audio")

class VideoPlugin(Plugin):
    def action(self): print("Playing Video")


print("\nСписок плагинов:", PluginMeta.plugins)
# [AudioPlugin, VideoPlugin]
```

<!--
Это самый популярный паттерн использования метаклассов (используется в Django Models, плагинах).
Вместо того чтобы вручную добавлять классы в список плагинов, метакласс делает это сам при объявлении класса.
-->

---

# Заключение и предостережение

> _"Метаклассы — это магия на 99%. Если вы думаете, нужны ли они вам, то они вам не нужны. Те, кому они действительно нужны, точно знают зачем, и им не нужно объяснять почему."_ **Тим Питерс (автор Zen of Python)**

::v-clicks{depth=2}

**Когда использовать метапрограммирование?**

1. При написании фреймворков и библиотек (ORM, API).
2. Когда нужно гарантировать строгое соблюдение правил в большом количестве классов.
3. Для автоматической регистрации и уменьшения boilerplate-кода.

В обычном прикладном коде лучше использовать более простые инструменты (декораторы, наследование).
::
