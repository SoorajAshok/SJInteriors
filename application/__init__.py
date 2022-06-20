
from flask import Flask
from config import Config
from flask_mongoengine import MongoEngine
from flask_mail import Mail

#from mongoengine import connect

UPLOAD_FOLDER = 'C:/Users/SRJ/SJInteriors/application/static/images/projects/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#db = MongoEngine() 


#DB_URI = "mongodb+srv://Sooraj:"+ quote("Pa55w0rd@0")+"@sjinteriors.o8zfgtm.mongodb.net/?retryWrites=true&w=majority"
#app.config["MONGODB_HOST"] = DB_URI
#connect(host=DB_URI)
db = MongoEngine(app)

#db.init_app(app)




mail = Mail(app) # instantiate the mail class
   
# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'sales.sjlifespacesinteriors@gmail.com'
app.config['MAIL_PASSWORD'] = "9539789121"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

from application import routes, models
