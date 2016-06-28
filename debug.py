# standard
import json
import csv
import os.path
import time
import tempfile
import os
from datetime import timedelta
import traceback

# pypi
import flask
from flask import make_response,request
from flask.views import MethodView

# home grown
from app import app, celery

#######################################################################
class ViewDebug(MethodView):
#######################################################################
    
    #----------------------------------------------------------------------
    def get(self):
    #----------------------------------------------------------------------
        try:
            appconfigpath = getattr(app,'configpath','<not set>')
            appconfigtime = getattr(app,'configtime','<not set>')

            # collect groups of system variables                        
            sysvars = []
            
            # collect app.config variables
            configkeys = app.config.keys()
            configkeys.sort()
            appconfig = []
            for key in configkeys:
                value = app.config[key]
                if key in ['SQLALCHEMY_DATABASE_URI','SECRET_KEY']:
                    value = '<obscured>'
                appconfig.append({'label':key, 'value':value})
            sysvars.append(['app.config',appconfig])
            
            # collect flask.session variables
            sessionkeys = flask.session.keys()
            sessionkeys.sort()
            sessionconfig = []
            for key in sessionkeys:
                value = flask.session[key]
                sessionconfig.append({'label':key, 'value':value})
            sysvars.append(['flask.session',sessionconfig])
            
            # collect celery variables
            celerytable = celery.conf.table()
            celeryconfig = [{'label':key, 'value':celerytable[key]} for key in celerytable]
            sysvars.append(['celery', celeryconfig])

            # render page
            return flask.render_template('debug.html',pagename='Debug',
                                         configpath=appconfigpath,
                                         configtime=appconfigtime,
                                         sysvars=sysvars)
        
        except:
            raise
#----------------------------------------------------------------------
app.add_url_rule('/_debuginfo',view_func=ViewDebug.as_view('debug'),methods=['GET'])
#----------------------------------------------------------------------