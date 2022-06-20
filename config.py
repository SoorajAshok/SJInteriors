import os
from urllib.parse import quote

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "SJSOORAJ"

    MONGODB_SETTINGS = { 'db' : 'SJInteriors', 'host': 'mongodb+srv://Sooraj:'+ quote("Pa55w0rd@0")+ '@sjinteriors.o8zfgtm.mongodb.net/?retryWrites=true&w=majority' }
    

    

    
    