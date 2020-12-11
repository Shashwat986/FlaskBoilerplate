from app.models.user import User

if not User.find(1):
    u = User(id=1, name="Asdf")
    u.save()
    print ("User Created")
else:
    u = User.find(1)
    u.name = "Asdf"
    u.save()
    print ("User already exists")


print (User.where(name="Asdf").all())
