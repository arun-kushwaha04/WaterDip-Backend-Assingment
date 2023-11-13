import os
from flask import Flask
from dotenv import load_dotenv
from .extension import mongo
from .main.routes import main

load_dotenv();

def create_app():
    app = Flask(__name__)    
    app.config['MONGO_URI'] = os.environ.get('MONGO_URI')    
    app.register_blueprint(main)
    mongo.init_app(app)    
    return app
