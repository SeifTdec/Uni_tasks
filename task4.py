class Animal:
    def __init__(self, name):
        self.name = name
        self.age = 0

    def eat(self):
        print(f"{self.name} is eating.")

    def sleep(self):
        print(f"{self.name} is sleeping.")

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed
    def bark(self):
        print(f"{self.name} is barking.")

dog = Dog("Princess", "Pitbull")

print(f"Name: {dog.name}")
print(f"Breed: {dog.breed}")
print(f"Age: {dog.age}")

dog.eat()
dog.sleep()
dog.bark()
