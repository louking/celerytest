from __future__ import absolute_import

from celery import Celery

# note doe not config backend here else state does not come back
# see https://stackoverflow.com/questions/25495613/celery-getting-started-not-able-to-retrieve-results-always-pending
app = Celery('celerytest',
             include=['celerytest.tasks'])

# Optional configuration, see the application user guide.
app.config_from_object('celerytest.celeryconfig')

if __name__ == '__main__':
    app.start()
