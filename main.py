import json
from abc import ABC, abstractmethod
from datetime import datetime


class Animal(ABC):
    def __init__(self, animal_id, name, age, breed, owner, health_status="Здоров"):
        self.animal_id = animal_id
        self.name = name
        self.age = age
        self.breed = breed
        self.owner = owner
        self.health_status = health_status

    def display_info(self):
        return f"ID: {self.animal_id}, Имя: {self.name}, Возраст: {self.age}, Порода: {self.breed}"

    @abstractmethod
    def make_sound(self):
        pass


class Dog(Animal):
    def make_sound(self):
        return "Гав! Гав!"


class Cat(Animal):
    def make_sound(self):
        return "Мяу! Мяу!"


class Bird(Animal):
    def make_sound(self):
        return "Чик-чирик!"


class PetClinic:
    def __init__(self):
        self.animals = []

    def add_animal(self, animal):
        self.animals.append(animal)
        print(f"✅ Добавлено: {animal.name}")

    def show_all(self):
        print("\n🐾 Все животные:")
        for animal in self.animals:
            print(f"{animal.display_info()} - {animal.make_sound()}")


def main():
    clinic = PetClinic()

    # Тестовые данные
    clinic.add_animal(Dog(1, "Бобик", 3, "Лабрадор", "Иван"))
    clinic.add_animal(Cat(2, "Мурка", 2, "Сиамская", "Мария"))

    while True:
        print("\n" + "=" * 30)
        print("1. Показать животных")
        print("2. Добавить собаку")
        print("0. Выход")

        choice = input("Выберите: ")

        if choice == '1':
            clinic.show_all()
        elif choice == '2':
            name = input("Имя собаки: ")
            clinic.add_animal(Dog(len(clinic.animals) + 1, name, 1, "Дворняга", "Хозяин"))
        elif choice == '0':
            break


if __name__ == "__main__":
    main()