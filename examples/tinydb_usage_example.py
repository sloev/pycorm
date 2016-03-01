from tinydb import TinyDB

from pycorm import BaseModel, StringField, NumberField

class User(BaseModel):
    name = StringField()
    age = NumberField()

    def get_name(self):
        return self.name

class Computer(BaseModel):
    model_name = StringField()
    user = User()

# init tinydb
db = TinyDB("test.json")
db.purge()

# create a dict repr of a computer
computer_dict = {"model_name":"ibm","user": {"name": "foobar", "age": 42}}
# insert into db
db.insert(computer_dict)

# get from db
computer_dict_from_db = db.all()[-1]
# construct and validate a Computer with dict from db
computer1 = Computer.with_validation(computer_dict_from_db)

# delete db beforehand to show nothing is there.
db.purge()
# insert computer model into db
db.insert(computer1)
computer2 = Computer(db.all()[-1])

# assert a lot
print "asserting"
assert(computer1 == computer_dict)
assert("foobar" == computer1.user.get_name())
assert(computer1 == computer2)
print "jep it works :-)"
