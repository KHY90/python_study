class Dog:

    def __init__(self, name, breed, age):
        self.name = name
        self.breed = breed
        self.age = age

class GuardDog(Dog): 

    def __init__(self, name, breed):
        super().__init__(name, breed, 5)

    def rrr(self):
        print("Stay away!")

class Puppy(Dog):

    def __init__(self, name, breed):
        super().__init__(name, breed, 0.1)

    def __str__(self):
        return f"{self.name}, {self.breed}"

    def woof_woof(self):
        print("woof")

    def introduce(self):
        self.woof_woof()
        print(f"My name is {self.name} and i am a {self.breed}")

ruffus = Puppy(
    name = "Ruffus",
    breed = "Beagel"
    )

bibi = Puppy(
    name = "bibi",
    breed = "dalmatian"
    )

ruffus.introduce()