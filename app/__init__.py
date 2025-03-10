from flask import Flask
from config import Config
from app.celery_app import celery
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db = SQLAlchemy(app)

# Import views and tasks
from app import views, tasks
