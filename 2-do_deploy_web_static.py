#!/usr/bin/python3
'''
script that distributes an archive to your web servers, using the function
do_deploy
'''
from fabric.api import run, put, env
from os import path
import os

env.hosts = ["35.196.111.72", "3.80.62.168"]


def do_deploy(archive_path):
    '''
    Distributes an archive to your web servers
    '''
    if path.exists(archive_path):
        try:
            put(archive_path, '/tmp/')
            filename = archive_path[9:]
            no_ext = filename[:-4]
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
