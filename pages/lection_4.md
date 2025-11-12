---
transition: slide-left
theme: sirius-college
exportFilename: pdf/oop_lection_4
layout: cover
title: oop_4
mdc: true
---

# Объектно-ориентированное программирование<br>Лекция 4. Полиморфизм, Абстрактные классы и Исключения

Понятие полиморфизма, переопределение методов. Утиная типизация. Абстрактные классы и методы (модуль `abc`), интерфейсы. Обработка исключений: `try-except-finally`, пользовательские исключения.

---

# Принципы ООП

1. Абстракция
2. Инкапсуляция
3. Наследование
4. Полиморфизм

---

# Полиморфизм

**Полиморфизм** - это свойство объектов разных классов реагировать на одинаковые вызовы методов по-разному.

> Суть: один интерфейс — множество реализаций.

<br>

```python {*|2-3,6-7|10-11}{maxHeight: '280px'}
class Circle:
    def area(self):
        return 3.14 * self.r ** 2

class Rectangle:
    def area(self):
        return self.w * self.h

# Полиморфный вызов
for shape in [Circle(), Rectangle()]:
    print(shape.area())
```

---

# Переопределение методов

**Переопределение (overriding)** — это замещение метода базового класса в подклассе новой реализацией.

```python {*|2-3|5|6-7|9-13}{maxHeight: '340px'}
class Animal:
    def speak(self):
        print("Some sound")

class Dog(Animal):
    def speak(self):
        print("Bark")

animal = Animal()
dog = Dog()

animal.speak()  # Some sound
dog.speak()     # Bark
```

---

# Динамическая диспетчеризация

Python выбирает реализацию метода во время выполнения (runtime). Это обеспечивает гибкость, но требует осознанного проектирования интерфейсов.

Реализуется через поиск метода по цепочке наследования (**MRO — Method Resolution Order**).

---

# Динамическая диспетчеризация

```python {*|1-3|5-7|9-11|13-16|13|15|18-24}{maxHeight: '420px'}
class Animal:
    def speak(self):
        print("Неопределенный звук животного")

class Dog(Animal):
    def speak(self):
        print("Гав!")

class Cat(Animal):
    def speak(self):
        print("Мяу!")

def make_animal_speak(animal: Animal):
    print(f"Пришел объект типа {type(animal).__name__}. Он говорит:")
    animal.speak()
    print("-" * 20)

generic_animal = Animal()
my_dog = Dog()
my_cat = Cat()

make_animal_speak(generic_animal)
make_animal_speak(my_dog)
make_animal_speak(my_cat)
```

<!-- "Давайте посмотрим, как работает динамическая диспетчеризация на практике. У нас есть иерархия классов: Animal и его потомки Dog и Cat. Каждый из них по-своему реализует метод speak."
"Ключевой элемент здесь — функция make_animal_speak. Заметьте, она написана так, чтобы работать с базовым классом Animal. Она ничего не знает ни про собак, ни про кошек."
"Когда мы вызываем animal.speak() внутри этой функции, Python смотрит на реальный объект, который пришел в эту функцию в данный момент."
"Если пришел объект Dog, Python поднимается по его MRO, находит speak() в классе Dog и вызывает его. Если пришел Cat — вызовется реализация из Cat."
"Этот механизм принятия решения в момент выполнения программы, а не на этапе написания кода, и называется динамической диспетчеризацией. Это то, что делает полиморфизм таким мощным и гибким инструментом." -->

---

# Утиная типизация

В Python важна не принадлежность к классу, а наличие требуемых методов.

> “Если объект ходит как утка и крякает как утка, значит, это утка.”

<v-click>

::center
![alt text](/imgs/4/image2.png){width=420px lazy}
::

</v-click>

---

# Утиная типизация

```python
class Duck:
    def quack(self): print("Quack!")

class Person:
    def quack(self): print("I'm imitating a duck!")

def make_it_quack(obj):
    obj.quack()

make_it_quack(Duck())
make_it_quack(Person())
```

---

# Утиная типизация

```python {*|1-7|9-15|6-7|6-7,14-15|17-18|20-28}{maxHeight: '420px'}
class Book:
    def __init__(self, title, pages_content):
        self.title = title
        self.pages = pages_content

    def __len__(self):
        return len(self.pages)

class City:
    def __init__(self, name, streets_list):
        self.name = name
        self.streets = streets_list

    def __len__(self):
        return len(self.streets)

def print_object_length(obj):
    print(f"Длина объекта: {len(obj)}")

my_book = Book("Война и мир", ["страница 1", "страница 2", "...", "страница 1300"])
my_city = City("Москва", ["Тверская", "Арбат", "...", "Ленинский проспект"])
my_string = "Это просто строка"
my_list = [1, 2, 3, 4, 5]

print_object_length(my_book)
print_object_length(my_city)
print_object_length(my_string)
print_object_length(my_list)
```

<!-- "Давайте посмотрим, как утиная типизация работает в реальном коде Python. Возьмем, например, встроенную функцию `len()`."
"Мы создали два совершенно разных класса: Book, длина которого — это количество страниц, и City, длина которого — количество улиц. Обратите внимание, у них нет общего родителя!"
"Но у обоих классов мы реализовали магический метод `__len__`. Это и есть наш "утиный" интерфейс. Реализуя этот метод, класс как бы говорит: 'Я знаю, как отвечать на вопрос о моей длине'."
"Теперь посмотрите на функцию print_object_length. Она вызывает len(obj). Ей абсолютно все равно, что такое obj — книга, город, строка или список. Для нее важно только одно: можно ли к этому объекту применить операцию `len()`."
"Когда мы передаем в эту функцию объекты совершенно разных, не связанных наследованием типов, она корректно работает с каждым из них. Она не смотрит на "паспорт" (тип класса), а смотрит на "поведение" (наличие метода `__len__`)."
"Это и есть мощь утиной типизации в Python. Она позволяет писать очень гибкий и универсальный код." -->

---

# Утиная типизация и интерфейсы

- Не требует наследования от общего базового класса.
- Поддерживает структурную типизацию — поведение определяет тип.
- Позже формализовано в typing.Protocol (PEP 544).

Сравнение:

| Подход                | Требует наследования | Проверка          |
| --------------------- | -------------------- | ----------------- |
| Номинальная типизация | Да                   | По имени класса   |
| Утиная типизация      | Нет                  | По набору методов |

---

# Абстрактные классы

Абстрактный класс имеет некоторые особенности, а именно:

- Абстрактный класс не содержит всех реализаций методов, необходимых для полной работы, это означает, что он содержит один или несколько абстрактных методов. Абстрактный метод - это только объявление метода, без его подробной реализации.
- Абстрактный класс предоставляет интерфейс для подклассов, чтобы избежать дублирования кода. Нет смысла создавать экземпляр абстрактного класса.
- Производный подкласс должен реализовать абстрактные методы для создания конкретного класса, который соответствует интерфейсу, определенному абстрактным классом. Следовательно, экземпляр не может быть создан, пока не будут переопределены все его абстрактные методы.

---
layout: statement
---

Абстрактный класс определяет общий интерфейс для набора подклассов. Он предоставляет общие атрибуты и методы для всех подклассов, чтобы уменьшить дублирование кода. Он также заставляет подклассы реализовывать абстрактные методы, чтобы избежать каких-либо несоответствий.

---

# Определение абстрактного класса

````md magic-move
```python {*|*}
class Animal:
    def move(self): pass

a = Animal()
```

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def move(self): pass

a = Animal()
# TypeError: Can't instantiate abstract class Animal with abstract methods move
```
````

<div v-click="[1, 2]">

> Класс Animal не является в полной мере абстрактным, так как может быть инициализирован.

</div>

---

# Реализация абстрактного метода

```python {*|3-6|7-13|15-19|21-24}{maxHeight: '420px'}
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def move(self): pass

class Cat(Animal):
    def move(self): 
        print('Кошка грациозно крадется')

class Fish(Animal):
    def move(self): 
        print('Рыба плывет')

cat = Cat()
cat.move() # Работает

fish = Fish()
fish.move() # Работает

# А если не реализовать, будет ошибка:
class Bird(Animal): pass
    
bird = Bird() # TypeError: Can't instantiate...
```

---

# Обработка исключений

```python
try:
    num = int(input("Введите число: "))
    result = 10 / num
    print(f"Результат: {result}")
except ValueError:
    print("Ошибка: Введено не число!")
except ZeroDivisionError:
    print("Ошибка: Деление на ноль!")
finally:
    print("Блок finally выполнен.")
```

---

# Пользовательские исключения

::center
![alt text](/imgs/4/image.png){width=850px lazy}
::

---

# Пользовательские исключения

```python {*|1|3-6|5|8-12|11}
class BalanceTooLowError(Exception): pass

def withdraw(balance, amount):
    if amount > balance:
        raise BalanceTooLowError("Недостаточно средств на счете")
    return balance - amount

my_balance = 100
try:
    my_balance = withdraw(my_balance, 150)
except BalanceTooLowError as e:
    print(f"Ошибка операции: {e}")
```
