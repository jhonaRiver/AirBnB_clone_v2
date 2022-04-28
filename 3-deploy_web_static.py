#!/usr/bin/python3
'''
script that creates and distributes an archive to your web servers, using the
function deploy
'''
from datetime import datetime
from fabric.api import local, run, put, env
from os.path import isdir
from os import path
import os

env.hosts = ["35.196.111.72", "3.80.62.168"]


def do_pack():
    '''
    Generates a tgz archive from web_static
    '''
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            local("mkdir versions")
        name = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(name))
        return name
    except:
        return None


def do_deploy(archive_path):
    '''
    deploys archive to web server
    '''
    if path.exists(archive_path):
        try:
            put(archive_path, '/tmp/')
            filename = archive_path[9:]
            no_ext = filename[:4]
            dir_name = '/data/web_static/releases/' + no_ext + '/'
            run('mkdir -p ' + dir_name)
            run('tar -xzf /tmp/' + filename + ' -C ' + dir_name)
            run('rm -f /tmp/' + filename)
            run('mv ' + dir_name + '/web_static/* ' + dir_name)
            run('rm -rf /data/web_static/current')
            run('ln -s ' + dir_name + ' /data/web_static/current')
            print('New version deployed!')
            return True
        except:
            return False
    else:
        return False


def deploy():
    '''
    Creates and distributes an archive to your web servers
    '''
    name = do_pack()
    if name is None:
        return False
    return do_deploy(name)
