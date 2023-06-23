class User(object):
    def __init__(self,name,age,gender='male'):
        self.name = name
        self.age = age
        self.gender = gender

    def __str__(self):
        return 'name: ' + self.name + ', age: ' + self.age + ', gender:' + self.gender