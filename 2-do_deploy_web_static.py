#!/usr/bin/python3
"""Fabric script to distributes an archive to your web servers"""
from fabric.api import *
from datetime import datetime
from os import path

env.hosts = ['3.85.175.4', '100.26.175.217']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """Distributes an archive to the web servers."""
    if path.exists(archive_path):
        put(archive_path, '/tmp/')
        # Split the archive_path using '/' delimiter to get the file name
        file_name = archive_path.split("/")[-1]
        # After getting the file name, split it again to remove the extension
        no_ext_file = file_name.split(".")[0]
        release_path = "/data/web_static/releases/"
        # Create the folder with the file name to keep uncompressed files
        run('mkdir -p {0}{1}/'.format(release_path, no_ext_file))
        # Decompress the archived files
        run('tar -xzf /tmp/{0} -C {1}{2}/'.format
            (file_name, release_path, no_ext_file)
            )
        # Delete the archive from the web server
        run('rm /tmp/{0}'.format(file_name))
        run('mv {0}{1}/web_static/* {0}{1}/'.format
            (release_path, no_ext_file)
            )
        run('rm -rf {0}{1}/web_static'.format(release_path, no_ext_file))
        run('rm -rf /data/web_static/current')
        run('ln -s {0}{1}/ /data/web_static/current'.format
            (release_path, no_ext_file)
            )
        return True
    else:
        return False
