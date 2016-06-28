# standard
import os.path

# pypi
from flask import Flask
from celery import Celery

# homegrown
from loutilities.configparser import getitems

app = Flask(__name__)

# pull in app and celery configuration, configuration file in parent dir from this file
configpath = os.path.join(os.path.sep.join(os.path.dirname(__file__).split(os.path.sep)[:-1]), 'celerytest.cfg')
appconfig = getitems(configpath, 'app')
app.config.update(appconfig)

celeryconfig = getitems(configpath, 'celery')
celery = Celery('proj')
celery.conf.update(celeryconfig)

# import views after configuration
import longtask
import debug

