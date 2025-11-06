---
transition: slide-left
theme: sirius-college
exportFilename: pdf/oop_lection_2
layout: cover
title: oop_2
mdc: true
---

# Объектно-ориентированное программирование<br>Лекция 2. Принципы проектирования чистого кода

Принципы SOLID (SRP, OCP, LSP, ISP, DIP). Принципы DRY (Don't Repeat Yourself) и KISS (Keep It Simple, Stupid).

---
layout: two-cols
---

# Zen of Python

- Beautiful is better than ugly.
- Explicit is better than implicit.
- Simple is better than complex.
- Complex is better than complicated.

::right::

- Красивое лучше уродливого.
- Явное лучше неявного.
- Простое лучше сложного.
- Сложное лучше запутанного.

---
layout: fact
---

# DRY

## [Don't Repeat Yourself]{v-click}

## [Не повторяйся]{v-click=1}

---

# DRY - Don't Repeat Yourself<br>Не повторяйся

Принцип гласит, что каждая часть знания в системе должна иметь единственное, однозначное и авторитетное представление. Проще говоря: **избегайте дублирования кода**.

<v-switch>

<template #0-5>

```python {*|1-8|4-6|10-16|4-6,12-14}{maxHeight: '340px', at: 1}
def process_user_data(data):
    # Валидация email
    email = data.get('email', '')
    if '@' not in email or '.' not in email:
        print("Ошибка: Некорректный email")
        return
    # ... какая-то обработка ...
    print(f"Обработка данных для {email}")

def register_new_user(email, password):
    # Повторная валидация email
    if '@' not in email or '.' not in email:
        print("Ошибка: Некорректный email для регистрации")
        return
    # ... логика регистрации ...
    print(f"Регистрация пользователя с email: {email}")

```

</template>
<template #5-10>

```python {*|1-3|8-10|16-18|all}{maxHeight: '340px', at: 6}
def is_valid_email(email: str) -> bool:
    """Проверяет, является ли строка похожей на email."""
    return '@' in email and '.' in email


def process_user_data(data):
    email = data.get('email', '')
    if not is_valid_email(email):
        print("Ошибка: Некорректный email")
        return
    # ... какая-то обработка ...
    print(f"Обработка данных для {email}")


def register_new_user(email, password):
    if not is_valid_email(email):
        print("Ошибка: Некорректный email для регистрации")
        return
    # ... логика регистрации ...
    print(f"Регистрация пользователя с email: {email}")
```

</template>
</v-switch>

<!--
1.  **Показываем первый слайд (нарушение DRY):**
    *   "Посмотрите на этот код. У нас есть две функции: одна обрабатывает данные, другая регистрирует пользователя. И в обеих функциях мы видим **одинаковый блок кода** для проверки email."
    *   "Это и есть нарушение принципа DRY. В чем здесь проблема? Если завтра мы захотим усложнить проверку email (например, добавить проверку на длину или специальные символы), нам придется **менять код в двух местах**. Мы можем забыть изменить его где-то, что приведет к ошибкам."

2.  **Переключаемся на второй слайд (соблюдение DRY):**
    *   "Правильное решение — вынести повторяющуюся логику в отдельную, переиспользуемую функцию, в нашем случае — `is_valid_email`."
    *   "Теперь обе наши основные функции вызывают эту маленькую вспомогательную функцию. Код стал чище, короче, и, что самое главное, — **легче в поддержке**."
    *   "Если нам понадобится изменить логику валидации, мы сделаем это **только в одном месте** — внутри функции `is_valid_email`. Это и есть суть принципа 'Не повторяйся'."
-->

---
layout: fact
---

# KISS

## [Keep it stupid simple]{v-click}

## [Пусть оно будет простым до безобразия]{v-click=1}

## [(Keep it simple, stupid)]{v-click=2}

---

# KISS - Keep It Simple, Stupid<br>Пусть оно будет простым

Принцип призывает выбирать самые простые решения, которые работают. Не нужно усложнять код без необходимости, даже если сложное решение кажется "умнее" или "гибче". Простота облегчает чтение, понимание и поддержку кода.

<v-switch>
<template #0-4>

```python {*|3-4|5-6|17-20}{maxHeight: '310px', at: 1}
def get_day_of_week(day_number: int) -> str:
    """Возвращает название дня недели по его номеру."""
    if day_number == 1:
        return "Понедельник"
    elif day_number == 2:
        return "Вторник"
    elif day_number == 3:
        return "Среда"
    elif day_number == 4:
        return "Четверг"
    elif day_number == 5:
        return "Пятница"
    elif day_number == 6:
        return "Суббота"
    elif day_number == 7:
        return "Воскресенье"
    else:
        class InvalidDayError(Exception):
            pass
        raise InvalidDayError("Неверный номер дня")

```

</template>
<template #4-7>

```python {*|3-11|12}{maxHeight: '310px', at: 5}
def get_day_of_week(day_number: int) -> str:
    """Возвращает название дня недели по его номеру."""
    days = {
        1: "Понедельник",
        2: "Вторник",
        3: "Среда",
        4: "Четверг",
        5: "Пятница",
        6: "Суббота",
        7: "Воскресенье"
    }
    return days.get(day_number, "Неверный номер дня")

```

</template>
</v-switch>

<!--
1.  **Показываем первый слайд (нарушение KISS):**
    *   "Рассмотрим задачу: получить название дня недели по его номеру. Вот одно из решений. Оно работает? Да, работает."
    *   "Но посмотрите на эту длинную конструкцию из `if-elif-else`. Она громоздкая. А для обработки ошибки мы даже создаем свой собственный класс исключения, что в данном случае является избыточным усложнением."
    *   "Код выполняет простую задачу, но выглядит сложно. Это нарушение принципа KISS."

2.  **Переключаемся на второй слайд (соблюдение KISS):**
    *   "А вот более простое и элегантное решение той же задачи. Мы используем структуру данных, которая идеально подходит для сопоставления "ключ-значение" — словарь."
    *   "Весь наш длинный `if-elif-else` заменяется словарем. Код стал короче и, что важнее, — **нагляднее**. Мы сразу видим все сопоставления."
    *   "Обработка ошибки тоже упростилась. Вместо создания исключения мы используем встроенный метод словаря `.get()`, который позволяет указать значение по умолчанию, если ключ не найден."
    *   "Оба решения работают, но второе — проще, понятнее и легче в поддержке. Это и есть следование принципу KISS."
-->

---
layout: fact
---

# SOLID

<v-clicks>

### **S**ingle responsibility principle (принцип единственной ответственности)

### **O**pen-closed principle (принцип открытости/закрытости)

### **L**iskov substitution principle (принцип подстановки Лисков)

### **I**nterface segregation principle (принцип разделения интерфейса)

### **D**ependency inversion principle (принцип инверсии зависимостей)

</v-clicks>

---

# S - Single responsibility principle<br>Принцип единственной ответственности

Каждый блок вашего кода должен выполнять одну задачу

````md magic-move
```python
class TicketAndCardChecker:
    def check_ticket(self, ticket: str):
        if ticket.isdigit() and len(ticket) == 10:
            ...
        return False

    def check_card (self, card: str):
        card = card. replace(' ', '')
        if card.isdigit() and len(card) <= 17:
            ...
        return False

```

```python
class TicketChecker:
    def check(self, ticket: str):
        if ticket. isdigit() and len(ticket) == 10:
            ...
        return False

class CardChecker:
    def check(self, card: str):
        card = card. replace(' ', '')
        if card.isdigit() and len(card) <= 17:
            ...
        return False

```
````

---

# O - Open-closed principle<br>Принцип открытости/закрытости

Ваши модули или библиотеки должны быть открыты для расширения, но закрыты для модификации.

<v-switch>
<template #0-2>

```python {*|4-7}{at: 1}
class DiscountCalculator:
    """Класс для расчета скидки в зависимости от типа клиента."""
    def get_discount(self, customer_type: str, price: float) -> float:
        if customer_type == 'standard':
            return price * 0.05  # 5% скидка
        elif customer_type == 'premium':
            return price * 0.1   # 10% скидка

        return 0.0

```

</template>
<template #2-8>

```python {*|1-6|8-10|12-14|16-18|20-22}{maxHeight: '340px', at: 3}
from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
    @abstractmethod
    def apply_discount(self, price: float) -> float:
        pass

class StandardDiscount(DiscountStrategy):
    def apply_discount(self, price: float) -> float:
        return price * 0.05

class PremiumDiscount(DiscountStrategy):
    def apply_discount(self, price: float) -> float:
        return price * 0.1

class VipDiscount(DiscountStrategy):
    def apply_discount(self, price: float) -> float:
        return price * 0.2

class DiscountCalculator:
    def get_discount(self, strategy: DiscountStrategy, price: float) -> float:
        return strategy.apply_discount(price)

```

</template>
</v-switch>

---

# L - Liskov substitution principle<br>Принцип подстановки Лисков

- Функции (и классы), которые используют указатели или ссылки на базовые классы, должны иметь возможность использовать подтипы базового типа, ничего не зная об их существовании.
- Подкласс не должен создавать новых мутаторов свойств базового класса.

---

# L - Liskov substitution principle<br>Принцип подстановки Лисков

<div v-mark.red.cross>

```py
class Email:
    def __init__(self, username: str, host: str):
        self.email = '{0}@{1}'. format(username, host)

    def isvalid(self):
        known_hosts = ['yandex.ru', 'gmail.com']
        for host in known_hosts:
            if self.email.endswith(host):
                return True
        return False

class SiriusEmail(Email):
    def __init__(self, username: str) :
        super().__init__(username, 'talantiuspeh.ru')
```

</div>

---

# I - Interface segregation principle<br>Принцип разделения интерфейса

Программные сущности не должны зависеть от методов, которые они не используют.

Отделяйте и разделяйте методы, не заставляйте пользователей (вашего кода) использовать ненужные или навязанные методы.

---

# I - Interface segregation principle<br>Принцип разделения интерфейса

<v-switch>
<template #0-7>

```python {*|3-14|16-24|16|17-18|20-21|23-24}{at: 1, maxHeight: '420px'}
from abc import ABC, abstractmethod

class IMultiFunctionDevice(ABC):
    @abstractmethod
    def print_document(self, document):
        pass

    @abstractmethod
    def scan_document(self, document):
        pass

    @abstractmethod
    def fax_document(self, document):
        pass

class SimplePrinter(IMultiFunctionDevice):
    def print_document(self, document):
        print(f"Печатаю документ: {document}")

    def scan_document(self, document):
        pass  # Нечего делать

    def fax_document(self, document):
        raise NotImplementedError("Этот принтер не поддерживает факс")
```

</template>
<template #7-14>

```python {*|3-11|3-6|8-11|13-15|17-23|17}{at: 8, maxHeight: '420px'}
from abc import ABC, abstractmethod

class IPrinter(ABC):
    @abstractmethod
    def print_document(self, document):
        pass

class IScanner(ABC):
    @abstractmethod
    def scan_document(self, document):
        pass

class SimplePrinter(IPrinter):
    def print_document(self, document):
        print(f"Печатаю документ: {document}")

class MultiFunctionDevice(IPrinter, IScanner):
    def print_document(self, document):
        print(f"МФУ печатает: {document}")

    def scan_document(self, document):
        print(f"МФУ сканирует: {document}")
```

</template>
</v-switch>

<!--
Показываем первый слайд (нарушение ISP):
"Представим, что мы проектируем систему для работы с оргтехникой. Мы создали общий интерфейс IMultiFunctionDevice, в котором описали все возможные действия: печать, сканирование, отправка факса."
"Теперь мы хотим описать простой принтер SimplePrinter. Он, конечно же, реализует наш интерфейс. Но в чем проблема?"
"Проблема в том, что SimplePrinter умеет только печатать. Но из-за "толстого" интерфейса он вынужден иметь у себя методы scan_document и fax_document. Ему приходится либо оставлять их пустыми, либо вызывать ошибку. Это плохой дизайн. Класс зависит от методов, которые он не использует."

Переключаемся на второй слайд (соблюдение ISP):
"Правильный подход — разделить "толстый" интерфейс на несколько маленьких и сфокусированных."
"Шаг 1: Мы создаем отдельные интерфейсы для каждого действия: IPrinter, IScanner. Каждый из них отвечает только за одну вещь."
"Шаг 2: Теперь наш SimplePrinter реализует только тот интерфейс, который ему нужен — IPrinter. В нем нет лишних, неиспользуемых методов. Код стал чище и логичнее."
"А если нам нужен настоящий МФУ, он просто реализует несколько маленьких интерфейсов (IPrinter и IScanner). Таким образом, мы даем классам возможность выбирать только ту функциональность, которая им действительно необходима. Принцип разделения интерфейса соблюден."
-->

---

# D - Dependency inversion principle<br>Принцип инверсии зависимостей

- Модули верхних уровней не должны импортировать сущности из модулей нижних уровней. Оба типа модулей должны зависеть от абстракций.
- Абстракции не должны зависеть от деталей. Детали должны зависеть от абстракций.

> Проще говоря: ваш основной код ("бизнес-логика") не должен знать о конкретных "деталях" реализации (как именно что-то пишется в базу данных или отправляется по email). Он должен работать с "контрактом" (абстракцией).

---

# D - Dependency inversion principle<br>Принцип инверсии зависимостей

<v-switch>
<template #0-5>

```python {*|1-4|6-13|9|13}{at: 1, maxHeight: '420px'}
class EmailNotifier:
    """Модуль нижнего уровня (деталь)."""
    def send_email(self, message: str):
        print(f"Отправка email: {message}")

class OrderProcessor:
    """Модуль верхнего уровня (бизнес-логика)."""
    def __init__(self):
        self.notifier = EmailNotifier()

    def process_order(self, order_id: int):
        print(f"Обработка заказа #{order_id}...")
        self.notifier.send_email(f"Ваш заказ #{order_id} обработан.")

```

</template>
<template #5-11>

```python {*|3-6|8-10|12-18|13-14|18}{at: 6, maxHeight: '420px'}
from abc import ABC, abstractmethod

class INotifier(ABC):
    @abstractmethod
    def notify(self, message: str):
        pass

class EmailNotifier(INotifier):
    def notify(self, message: str):
        print(f"Отправка email: {message}")

class OrderProcessor:
    def __init__(self, notifier: INotifier):
        self.notifier = notifier

    def process_order(self, order_id: int):
        print(f"Обработка заказа #{order_id}...")
        self.notifier.notify(f"Ваш заказ #{order_id} обработан.")
```

</template>
<template #11-12>

```python {12-14}{maxHeight: '420px'}
from abc import ABC, abstractmethod

class INotifier(ABC):
    @abstractmethod
    def notify(self, message: str):
        pass

class EmailNotifier(INotifier):
    def notify(self, message: str):
        print(f"Отправка email: {message}")

class SmsNotifier(INotifier):
    def notify(self, message: str):
        print(f"Отправка SMS: {message}")

class OrderProcessor:
    def __init__(self, notifier: INotifier):
        self.notifier = notifier

    def process_order(self, order_id: int):
        print(f"Обработка заказа #{order_id}...")
        self.notifier.notify(f"Ваш заказ #{order_id} обработан.")
```

</template>
</v-switch>
