#!/usr/bin/python3
"""This Fabric script distributes an archive to my web servers"""
from fabric.api import *
from datetime import datetime
from os import path

env.hosts = ['3.85.175.4', '100.26.175.217']
env.user = 'ubuntu'
env.key_filename = '/root/.ssh/id_rsa'

def do_deploy(archive_path):
    """Distributing an archive to the web servers."""
    if path.exists(archive_path):
        put(archive_path, '/tmp/')
        # get the file name by spliting the archive_path using '/' delimiter
        fil_name = archive_path.split("/")[-1]
        # After getting the file name, split it again to remove the extension
        n_e_file = fil_name.split(".")[0]
        path_way = "/data/web_static/releases/"
        # Creainge the folder with the file name to keep uncompressed files
        run('mkdir -p {0}{1}/'.forma(path_way, n_e_file))
        # Decompressing the archived files
        run('tar -xzf /tmp/{0} -C {1}{2}/'.format
            (fil_name, path_way, n_e_file)
            )
        # Deleinge the archive from the web server
        run('rm /tmp/{0}'.format(fil_name))
        run('mv {0}{1}/web_static/* {0}{1}/'.format
            (path_way, n_e_file)
            )
        run('rm -rf {0}{1}/web_static'.format(path_way, n_e_file))
        run('rm -rf /data/web_static/current')
        run('ln -s {0}{1}/ /data/web_static/current'.format
            (path_way, n_e_file)
            )
        return True
    else:
        return False
