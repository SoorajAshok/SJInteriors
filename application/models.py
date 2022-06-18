import flask
from application import db
from werkzeug.security import generate_password_hash, check_password_hash

#User Data
class User(db.Document):
    user_id     =   db.IntField( unique = True )
    user_name   =   db.StringField( max_length = 50 )
    password    =   db.StringField( max_length = 500 )

    def set_password(self,password):
        self.password   =   generate_password_hash(password)

    def get_password(self,password):
        return check_password_hash(self.password, password)

    def __str__(self):
        return "user_name: %s," \
         "password: %s" %(self.user_name, self.password)


#Recent project
class Projects(db.Document):
    #project_id     =   db.IntField(required=True, primary_key = True)
    project_name    =   db.StringField( max_length = 50, unique =   True )
    project_caption =   db.StringField()

    #def __str__(self):
    #    return "project_name: %s," \
    #    "project_Caption: %s" %(self.project_name, self.project_Caption)

#Project Images
class Gallery(db.Document):
    #image_id       =   db.IntField(required=True, primary_key = True)
    image_name      =   db.StringField()
    image_path      =   db.StringField()
    project_name    =   db.StringField()
    