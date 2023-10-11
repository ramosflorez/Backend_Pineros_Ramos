from flask_bcrypt import Bcrypt

hash = Bcrypt.generate_password_hash(self=Bcrypt ,password='123')

password = hash
print(password)
