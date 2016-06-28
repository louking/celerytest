# standard
import random
import time
import sys

# pypi
from flask.views import MethodView
from flask import Flask, request, render_template, session, flash, redirect, \
    url_for, jsonify
from celery import Celery

# home grown
from app import app, celery

class StartLongTask(MethodView):
    def post(self):
        task = long_task.apply_async()
        return jsonify({}), 202, {'Location': url_for('longtaskstatus',
                                                      task_id=task.id)}
app.add_url_rule('/longtask',view_func=StartLongTask.as_view('longtask'),methods=['POST',])

class LongTaskStatus(MethodView):
    def get(self, task_id):
        task = long_task.AsyncResult(task_id)
        if task.state == 'PENDING':
            # job did not start yet
            response = {
                'state': task.state,
                'current': 0,
                'total': 1,
                'status': 'Pending...'
            }
        elif task.state != 'FAILURE':
            response = {
                'state': task.state,
                'current': task.info.get('current', 0),
                'total': task.info.get('total', 1),
                'status': task.info.get('status', '')
            }
            if 'result' in task.info:
                response['result'] = task.info['result']
        else:
            # something went wrong in the background job
            response = {
                'state': task.state,
                'current': 1,
                'total': 1,
                'status': str(task.info),  # this is the exception raised
            }
        return jsonify(response)
app.add_url_rule('/longtaskstatus/<task_id>',view_func=LongTaskStatus.as_view('longtaskstatus'), methods=['GET',])

@celery.task(bind=True)
def long_task(self):
    """Background task that runs a long function with progress reports."""
    verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking']
    adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast']
    noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit']
    message = ''
    total = random.randint(10, 50)
    for i in range(total):
        if not message or random.random() < 0.25:
            message = '{0} {1} {2}...'.format(random.choice(verb),
                                              random.choice(adjective),
                                              random.choice(noun))
        self.update_state(state='PROGRESS',
                          meta={'current': i, 'total': total,
                                'status': message})
        time.sleep(1)
    return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': 42}


