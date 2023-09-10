#!/usr/bin/python3
""" Based on '1-pack_web_static.py'. It distributes an archive to my web
    servers using the function 'do_deploy'.
"""
from fabric.api import env, put, run, sudo
from os.path import exists
env.hosts = ['54.210.88.216', '100.25.104.112']
env.user = 'ubuntu'


def do_deploy(file_path):
    """ It distributes an archive to my web servers."""
    if not exists(file_path):
        print('file doesnt exist')
        return False
    try:
        filename = file_path.split('/')[-1]
        file = filename.split('.')[0]
        put(file_path, '/tmp/')
        sudo('mkdir -p /data/web_static/releases/{}'.format(file))
        sudo('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'
             .format(filename, file))
        run('rm -f /tmp/{}'.format(filename))
        run('rm -f /data/web_static/current')
        run("ln -sf /data/web_static/releases/{}/web_static/ \
                /data/web_static/current".format(file))

        return True
    except Exception as e:
        print(e)
        return False
    