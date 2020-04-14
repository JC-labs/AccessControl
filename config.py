import os
basedir = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.join(basedir, 'data')
os.makedirs(data_dir, exist_ok=True)

SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess898986980'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(data_dir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

