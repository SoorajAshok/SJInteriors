
from flask import Flask
from config import Config
from flask_mongoengine import MongoEngine
from flask_mail import Mail

UPLOAD_FOLDER = 'C:/Users/SRJ/SJInteriors/application/static/images/projects/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = MongoEngine() 
db.init_app(app)

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
