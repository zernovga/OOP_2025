from statistics import mean

cars = [
    {"brand": "Toyota", "year": 2020, "price": 18000},
    {"brand": "BMW", "year": 2022, "price": 35000},
    {"brand": "Audi", "year": 2021, "price": 40000},
    {"brand": "Ford", "year": 2019, "price": 22000},
    {"brand": "Kia", "year": 2023, "price": 19500},
]

# 1. Фильтрация (только машины дороже 20 000)
filtered = filter(lambda c: c["price"] > 20000, cars)

# 2. Сортировка по году (от новых к старым)
sorted_cars = sorted(filtered, key=lambda c: c["year"], reverse=True)

# 3. Средняя цена
average_price = mean(map(lambda c: c["price"], sorted_cars))

print("Отфильтрованные и отсортированные машины:")
for c in sorted_cars:
    print(f"{c['brand']} ({c['year']}): ${c['price']}")

print(f"\nСредняя цена: ${average_price:.2f}")
