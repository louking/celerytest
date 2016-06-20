###########################################################################################
# fabfile  -- deployment using Fabric
#
#   Copyright 2014 Lou King
###########################################################################################
'''
fabfile  -- deployment using Fabric
=================================================================

'''

from fabric.api import env, run, cd

USERNAME = 'scoretility'
APP_NAME = 'celerytest'
WSGI_SCRIPT = 'celerytest.wsgi'

server = 'celerytest.scoretility.com'
project_dir = '/var/www/{}/{}'.format(server, APP_NAME)
env.hosts = ["{}@{}".format(USERNAME, server)]
env.forward_agent = True

def deploy(branchname='master'):
    with cd(project_dir):
        run('git pull')
        run('git checkout {}'.format(branchname))
        run('source bin/activate; pip install -r requirements.txt')
        # run('touch {}'.format(WSGI_SCRIPT))
