class Person():

    def __init__(self, name = 'Mark', last_name = 'Lopez', age = 25, nationality = "Mexican"):
        self.name = name
        self.last_name = last_name
        self.age = age
        self.nationality = nationality

    def introduce_yourself(self):
        print('Hi! My name is {} {}. I am {} and I am {} years old. Nice to meet you!'.format(self.name, self.last_name, self.age, self.nationality))

    def get_data(self):
        return [self.name, self.last_name, self.age, self.nationality]

class Student(Person):

    def __init__(self, name = 'Luis', last_name = 'James', age = 20, nationality = "Argentinian", school = "Minerva"):
        super().__init__(name,last_name,age,nationality)
        self.school = school

me = Person("Juan","Castro",22)
print(me.nationality)
info = me.get_data()
print(info)
me.introduce_yourself()
