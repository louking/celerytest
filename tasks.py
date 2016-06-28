from __future__ import absolute_import

from proj.celerytest import app

from longtask import long_task

@app.task
def add(x, y):
    return x + y

@app.task
def mul(x, y):
    return x * y

@app.task
def xsum(numbers):
    return sum(numbers)

