#!/usr/bin/python3
'''
script that deletes out-of-date archives, using the function do_clean
'''
from fabric.api import local, run


def do_clean(number=0):
    '''
    Deletes out-of-date archives
    '''
    number = int(number)
    to_del = number + 1
    dirname = '/data/web_static/releases'
    if (number == 0 or number == 1):
        local('cd versions; ls -t | tail -n +2 | xargs rm -rf')
        run('cd ' + dirname + '; ls -t | tail -n +2 | xargs rm -rf')
    else:
        local('cd versions; ls -t | tail -n +{} | xargs rm -rf'.format(to_del))
        run('cd ' + dirname + '; ls -t | tail -n +{} | xargs rm -rf'.
            format(to_del))
