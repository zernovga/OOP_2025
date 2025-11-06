from statistics import mean


class Car:
    def __init__(self, brand, year, price):
        self.brand = brand
        self.year = year
        self.price = price

    def __repr__(self):
        return f"{self.brand} ({self.year}): {self.price} Руб."


class CarDatabase:
    def __init__(self, cars: list[Car]):
        self.cars = cars

    def filter_by_price(self, min_price: int):
        self.cars = [car for car in self.cars if car.price > min_price]
        return self

    def sorted_by_year(self, reverse=True):
        self.cars.sort(key=lambda x: x.year, reverse=reverse)
        return self

    def average_price(self):
        return mean(car.price for car in self.cars)

    def show(self):
        for car in self.cars:
            print(car)


db = CarDatabase(
    [
        Car("Toyota", 2020, 18000),
        Car("BMW", 2022, 35000),
        Car("Audi", 2021, 40000),
        Car("Ford", 2019, 22000),
        Car("Kia", 2023, 19500),
    ]
)

# 1. Фильтрация (только машины дороже 20 000)
# 2. Сортировка по году (от новых к старым)
db.filter_by_price(20_000).sorted_by_year()


print("Отфильтрованные и отсортированные машины:")
db.show()

print(f"\nСредняя цена: ${db.average_price():.2f}")
