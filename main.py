"""Лабораторная работа №1. Вариант 15: Система учета домашних животных"""

import json
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime


class AnimalError(Exception):
    pass


class AnimalNotFoundError(AnimalError):
    pass


class InvalidAnimalDataError(AnimalError):
    pass


class FileOperationError(AnimalError):
    pass


class Animal(ABC):
    def __init__(self, animal_id: int, name: str, age: int, breed: str, owner: str, health_status: str = "Здоров"):
        self._validate_positive_int(animal_id, "ID")
        self._validate_positive_int(age, "Возраст")
        self._validate_string(name, "Имя")
        self._validate_string(breed, "Порода")
        self._validate_string(owner, "Владелец")

        self.animal_id = animal_id
        self.name = name
        self.age = age
        self.breed = breed
        self.owner = owner
        self.health_status = health_status

    def _validate_positive_int(self, value: int, field_name: str):
        if not isinstance(value, int) or value <= 0:
            raise InvalidAnimalDataError(f"{field_name} должен быть положительным целым числом")

    def _validate_string(self, value: str, field_name: str):
        if not isinstance(value, str) or not value.strip():
            raise InvalidAnimalDataError(f"{field_name} не может быть пустым")

    def display_info(self) -> str:
        return (f"ID: {self.animal_id}, Имя: {self.name}, Возраст: {self.age}, "
                f"Порода: {self.breed}, Владелец: {self.owner}, "
                f"Состояние здоровья: {self.health_status}")

    @abstractmethod
    def make_sound(self) -> str:
        pass

    def to_dict(self) -> dict:
        return {
            'type': self.__class__.__name__,
            'animal_id': self.animal_id,
            'name': self.name,
            'age': self.age,
            'breed': self.breed,
            'owner': self.owner,
            'health_status': self.health_status,
            **self._specific_attributes()
        }

    @abstractmethod
    def _specific_attributes(self) -> dict:
        pass

    @classmethod
    def from_dict(cls, data: dict) -> 'Animal':
        animal_type = data.get('type')
        if animal_type == 'Dog':
            return Dog.from_dict(data)
        elif animal_type == 'Cat':
            return Cat.from_dict(data)
        elif animal_type == 'Bird':
            return Bird.from_dict(data)
        else:
            raise InvalidAnimalDataError(f"Неизвестный тип животного: {animal_type}")


class Dog(Animal):
    def __init__(self, animal_id: int, name: str, age: int, breed: str, owner: str,
                 health_status: str = "Здоров", dog_size: str = "Средний"):
        super().__init__(animal_id, name, age, breed, owner, health_status)
        self._validate_dog_size(dog_size)
        self.dog_size = dog_size

    def _validate_dog_size(self, size: str):
        valid_sizes = ["Маленький", "Средний", "Большой"]
        if size not in valid_sizes:
            raise InvalidAnimalDataError(f"Размер собаки должен быть одним из: {valid_sizes}")

    def make_sound(self) -> str:
        return "Гав! Гав!"

    def _specific_attributes(self) -> dict:
        return {'dog_size': self.dog_size}

    @classmethod
    def from_dict(cls, data: dict) -> 'Dog':
        return cls(
            animal_id=data['animal_id'],
            name=data['name'],
            age=data['age'],
            breed=data['breed'],
            owner=data['owner'],
            health_status=data.get('health_status', 'Здоров'),
            dog_size=data.get('dog_size', 'Средний')
        )


class Cat(Animal):
    def __init__(self, animal_id: int, name: str, age: int, breed: str, owner: str,
                 health_status: str = "Здоров", is_indoor: bool = True):
        super().__init__(animal_id, name, age, breed, owner, health_status)
        self.is_indoor = bool(is_indoor)

    def make_sound(self) -> str:
        return "Мяу! Мяу!"

    def _specific_attributes(self) -> dict:
        return {'is_indoor': self.is_indoor}

    @classmethod
    def from_dict(cls, data: dict) -> 'Cat':
        return cls(
            animal_id=data['animal_id'],
            name=data['name'],
            age=data['age'],
            breed=data['breed'],
            owner=data['owner'],
            health_status=data.get('health_status', 'Здоров'),
            is_indoor=data.get('is_indoor', True)
        )


class Bird(Animal):
    def __init__(self, animal_id: int, name: str, age: int, breed: str, owner: str,
                 health_status: str = "Здоров", wingspan: float = 0.0):
        super().__init__(animal_id, name, age, breed, owner, health_status)
        self._validate_wingspan(wingspan)
        self.wingspan = wingspan

    def _validate_wingspan(self, wingspan: float):
        if not isinstance(wingspan, (int, float)) or wingspan < 0:
            raise InvalidAnimalDataError("Размах крыльев должен быть неотрицательным числом")

    def make_sound(self) -> str:
        return "Чик-чирик!"

    def _specific_attributes(self) -> dict:
        return {'wingspan': self.wingspan}

    @classmethod
    def from_dict(cls, data: dict) -> 'Bird':
        return cls(
            animal_id=data['animal_id'],
            name=data['name'],
            age=data['age'],
            breed=data['breed'],
            owner=data['owner'],
            health_status=data.get('health_status', 'Здоров'),
            wingspan=data.get('wingspan', 0.0)
        )


class PetClinic:
    def __init__(self):
        self.animals: List[Animal] = []
        self._next_id = 1

    def _get_next_id(self) -> int:
        current_id = self._next_id
        self._next_id += 1
        return current_id

    def add_animal(self, animal: Animal) -> None:
        try:
            for existing_animal in self.animals:
                if existing_animal.animal_id == animal.animal_id:
                    raise InvalidAnimalDataError(f"Животное с ID {animal.animal_id} уже существует")

            self.animals.append(animal)
            print(f"Животное {animal.name} успешно добавлено!")

        except Exception as e:
            raise AnimalError(f"Ошибка при добавлении животного: {str(e)}")

    def remove_animal(self, animal_id: int) -> bool:
        try:
            for i, animal in enumerate(self.animals):
                if animal.animal_id == animal_id:
                    removed_animal = self.animals.pop(i)
                    print(f"Животное {removed_animal.name} удалено!")
                    return True

            raise AnimalNotFoundError(f"Животное с ID {animal_id} не найдено")

        except AnimalNotFoundError:
            raise
        except Exception as e:
            raise AnimalError(f"Ошибка при удалении животного: {str(e)}")

    def find_animal_by_id(self, animal_id: int) -> Optional[Animal]:
        try:
            for animal in self.animals:
                if animal.animal_id == animal_id:
                    return animal
            return None
        except Exception as e:
            raise AnimalError(f"Ошибка при поиске животного: {str(e)}")

    def find_animals_by_owner(self, owner: str) -> List[Animal]:
        try:
            return [animal for animal in self.animals if animal.owner.lower() == owner.lower()]
        except Exception as e:
            raise AnimalError(f"Ошибка при поиске животных по владельцу: {str(e)}")

    def display_all_animals(self) -> None:
        if not self.animals:
            print("В клинике нет животных.")
            return

        print("\n--- Все животные в клинике ---")
        for animal in self.animals:
            print(animal.display_info())
            print(f"Звук: {animal.make_sound()}")
            print("-" * 50)

    def save_to_json(self, filename: str) -> None:
        try:
            data = {
                'animals': [animal.to_dict() for animal in self.animals],
                'metadata': {
                    'saved_at': datetime.now().isoformat(),
                    'total_animals': len(self.animals)
                }
            }

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            print(f"Данные успешно сохранены в {filename}")

        except Exception as e:
            raise FileOperationError(f"Ошибка при сохранении в JSON: {str(e)}")

    def load_from_json(self, filename: str) -> None:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.animals.clear()
            for animal_data in data.get('animals', []):
                animal = Animal.from_dict(animal_data)
                self.animals.append(animal)

            if self.animals:
                max_id = max(animal.animal_id for animal in self.animals)
                self._next_id = max_id + 1

            print(f"Данные успешно загружены из {filename}")

        except FileNotFoundError:
            raise FileOperationError(f"Файл {filename} не найден")
        except Exception as e:
            raise FileOperationError(f"Ошибка при загрузке из JSON: {str(e)}")

    def save_to_xml(self, filename: str) -> None:
        try:
            root = ET.Element('pet_clinic')
            metadata = ET.SubElement(root, 'metadata')
            ET.SubElement(metadata, 'saved_at').text = datetime.now().isoformat()
            ET.SubElement(metadata, 'total_animals').text = str(len(self.animals))

            animals_elem = ET.SubElement(root, 'animals')
            for animal in self.animals:
                animal_elem = ET.SubElement(animals_elem, 'animal')
                animal_elem.set('type', animal.__class__.__name__)

                ET.SubElement(animal_elem, 'animal_id').text = str(animal.animal_id)
                ET.SubElement(animal_elem, 'name').text = animal.name
                ET.SubElement(animal_elem, 'age').text = str(animal.age)
                ET.SubElement(animal_elem, 'breed').text = animal.breed
                ET.SubElement(animal_elem, 'owner').text = animal.owner
                ET.SubElement(animal_elem, 'health_status').text = animal.health_status

                if isinstance(animal, Dog):
                    ET.SubElement(animal_elem, 'dog_size').text = animal.dog_size
                elif isinstance(animal, Cat):
                    ET.SubElement(animal_elem, 'is_indoor').text = str(animal.is_indoor)
                elif isinstance(animal, Bird):
                    ET.SubElement(animal_elem, 'wingspan').text = str(animal.wingspan)

            tree = ET.ElementTree(root)
            tree.write(filename, encoding='utf-8', xml_declaration=True)

            print(f"Данные успешно сохранены в {filename}")

        except Exception as e:
            raise FileOperationError(f"Ошибка при сохранении в XML: {str(e)}")

    def load_from_xml(self, filename: str) -> None:
        try:
            tree = ET.parse(filename)
            root = tree.getroot()

            self.animals.clear()

            for animal_elem in root.find('animals'):
                animal_type = animal_elem.get('type')
                animal_data = {
                    'type': animal_type,
                    'animal_id': int(animal_elem.find('animal_id').text),
                    'name': animal_elem.find('name').text,
                    'age': int(animal_elem.find('age').text),
                    'breed': animal_elem.find('breed').text,
                    'owner': animal_elem.find('owner').text,
                    'health_status': animal_elem.find('health_status').text
                }

                if animal_type == 'Dog':
                    animal_data['dog_size'] = animal_elem.find('dog_size').text
                elif animal_type == 'Cat':
                    animal_data['is_indoor'] = animal_elem.find('is_indoor').text.lower() == 'true'
                elif animal_type == 'Bird':
                    animal_data['wingspan'] = float(animal_elem.find('wingspan').text)

                animal = Animal.from_dict(animal_data)
                self.animals.append(animal)

            if self.animals:
                max_id = max(animal.animal_id for animal in self.animals)
                self._next_id = max_id + 1

            print(f"Данные успешно загружены из {filename}")

        except FileNotFoundError:
            raise FileOperationError(f"Файл {filename} не найден")
        except Exception as e:
            raise FileOperationError(f"Ошибка при загрузке из XML: {str(e)}")


def display_menu():
    print("\n" + "=" * 50)
    print("         ВЕТЕРИНАРНАЯ КЛИНИКА 'ДОМАШНИЕ ПИТОМЦЫ'")
    print("=" * 50)
    print("1. Добавить животное")
    print("2. Удалить животное")
    print("3. Найти животное по ID")
    print("4. Найти животных по владельцу")
    print("5. Показать всех животных")
    print("6. Сохранить в JSON")
    print("7. Загрузить из JSON")
    print("8. Сохранить в XML")
    print("9. Загрузить из XML")
    print("0. Выход")
    print("=" * 50)


def get_animal_input(clinic: PetClinic) -> Animal:
    print("\nВыберите тип животного:")
    print("1. Собака")
    print("2. Кошка")
    print("3. Птица")

    while True:
        try:
            choice = input("Ваш выбор (1-3): ").strip()
            if choice not in ['1', '2', '3']:
                print("Пожалуйста, выберите 1, 2 или 3")
                continue

            animal_id = 1000 + len(clinic.animals)
            name = input("Имя животного: ").strip()
            age = int(input("Возраст: "))
            breed = input("Порода: ").strip()
            owner = input("Владелец: ").strip()
            health_status = input("Состояние здоровья (по умолчанию 'Здоров'): ").strip() or "Здоров"

            if choice == '1':
                print("Размер собаки:")
                print("1. Маленький")
                print("2. Средний")
                print("3. Большой")
                size_choice = input("Ваш выбор (1-3): ").strip()
                sizes = {"1": "Маленький", "2": "Средний", "3": "Большой"}
                dog_size = sizes.get(size_choice, "Средний")

                return Dog(animal_id, name, age, breed, owner, health_status, dog_size)

            elif choice == '2':
                indoor = input("Домашняя кошка? (да/нет): ").strip().lower()
                is_indoor = indoor in ['да', 'д', 'yes', 'y']
                return Cat(animal_id, name, age, breed, owner, health_status, is_indoor)

            elif choice == '3':
                wingspan = float(input("Размах крыльев (см): "))
                return Bird(animal_id, name, age, breed, owner, health_status, wingspan)

        except ValueError as e:
            print(f"Ошибка ввода: {e}. Пожалуйста, попробуйте снова.")
        except InvalidAnimalDataError as e:
            print(f"Ошибка данных: {e}. Пожалуйста, попробуйте снова.")


def main():
    clinic = PetClinic()

    try:
        clinic.add_animal(Dog(1, "Бобик", 3, "Лабрадор", "Иван Иванов", "Здоров", "Большой"))
        clinic.add_animal(Cat(2, "Мурка", 2, "Сиамская", "Мария Петрова", "Здорова", True))
        clinic.add_animal(Bird(3, "Кеша", 1, "Попугай", "Алексей Сидоров", "Здоров", 15.5))
    except AnimalError as e:
        print(f"Ошибка при добавлении тестовых данных: {e}")

    while True:
        try:
            display_menu()
            choice = input("Выберите действие: ").strip()

            if choice == '1':
                try:
                    animal = get_animal_input(clinic)
                    clinic.add_animal(animal)
                except AnimalError as e:
                    print(f"Ошибка: {e}")

            elif choice == '2':
                try:
                    animal_id = int(input("Введите ID животного для удаления: "))
                    clinic.remove_animal(animal_id)
                except (ValueError, AnimalError) as e:
                    print(f"Ошибка: {e}")

            elif choice == '3':
                try:
                    animal_id = int(input("Введите ID животного: "))
                    animal = clinic.find_animal_by_id(animal_id)
                    if animal:
                        print("\nНайдено животное:")
                        print(animal.display_info())
                        print(f"Звук: {animal.make_sound()}")
                    else:
                        print("Животное с таким ID не найдено.")
                except ValueError:
                    print("Ошибка: ID должен быть числом")
                except AnimalError as e:
                    print(f"Ошибка: {e}")

            elif choice == '4':
                try:
                    owner = input("Введите имя владельца: ").strip()
                    animals = clinic.find_animals_by_owner(owner)
                    if animals:
                        print(f"\nНайдено животных у владельца {owner}: {len(animals)}")
                        for animal in animals:
                            print(animal.display_info())
                    else:
                        print(f"Животных у владельца {owner} не найдено.")
                except AnimalError as e:
                    print(f"Ошибка: {e}")

            elif choice == '5':
                clinic.display_all_animals()

            elif choice == '6':
                try:
                    filename = input("Введите имя файла (по умолчанию animals.json): ").strip() or "animals.json"
                    clinic.save_to_json(filename)
                except FileOperationError as e:
                    print(f"Ошибка: {e}")

            elif choice == '7':
                try:
                    filename = input("Введите имя файла (по умолчанию animals.json): ").strip() or "animals.json"
                    clinic.load_from_json(filename)
                except FileOperationError as e:
                    print(f"Ошибка: {e}")

            elif choice == '8':
                try:
                    filename = input("Введите имя файла (по умолчанию animals.xml): ").strip() or "animals.xml"
                    clinic.save_to_xml(filename)
                except FileOperationError as e:
                    print(f"Ошибка: {e}")

            elif choice == '9':
                try:
                    filename = input("Введите имя файла (по умолчанию animals.xml): ").strip() or "animals.xml"
                    clinic.load_from_xml(filename)
                except FileOperationError as e:
                    print(f"Ошибка: {e}")

            elif choice == '0':
                print("До свидания!")
                break

            else:
                print("Неверный выбор. Пожалуйста, выберите действие из меню.")

        except KeyboardInterrupt:
            print("\n\nПрограмма прервана пользователем. До свидания!")
            break
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")


if __name__ == "__main__":
    main()