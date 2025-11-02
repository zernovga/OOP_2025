from statistics import mean


class Car:
    def __init__(self, brand, year, price):
        self.brand = brand
        self.year = year
        self.price = price

    def __repr__(self):
        return f"{self.brand} ({self.year}): ${self.price}"


class CarDataset:
    def __init__(self, cars):
        self.cars = cars

    def filter_by_price(self, min_price):
        self.cars = [car for car in self.cars if car.price > min_price]
        return self

    def sort_by_year(self, reverse=True):
        self.cars.sort(key=lambda c: c.year, reverse=reverse)
        return self

    def average_price(self):
        return mean(car.price for car in self.cars)

    def show(self):
        for car in self.cars:
            print(car)


# Использование
cars = [
    Car("Toyota", 2020, 18000),
    Car("BMW", 2022, 35000),
    Car("Audi", 2021, 40000),
    Car("Ford", 2019, 22000),
    Car("Kia", 2023, 19500),
]

dataset = CarDataset(cars)
dataset.filter_by_price(20000).sort_by_year()

print("Отфильтрованные и отсортированные машины:")
dataset.show()

print(f"\nСредняя цена: ${dataset.average_price():.2f}")
