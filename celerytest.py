from __future__ import absolute_import

# standard
import os.path

# pypi
from celery import Celery

# homegrown
from loutilities.configparser import getitems

# note doe not config backend here else state does not come back
# see https://stackoverflow.com/questions/25495613/celery-getting-started-not-able-to-retrieve-results-always-pending
app = Celery('proj', include=['proj.tasks'])

# pull in configuration, configuration file in parent dir from this file
configpath = os.path.join(os.path.sep.join(os.path.dirname(__file__).split(os.path.sep)[:-1]), 'celerytest.cfg')
config = getitems(configpath, 'celery')

# Optional configuration, see the application user guide.
app.config_from_object(config)

if __name__ == '__main__':
    app.start()
