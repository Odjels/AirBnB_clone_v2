#!/usr/bin/python3
"""Fabric script to distributes an archive to your web servers"""
from fabric.api import *
from datetime import datetime
from os import path

env.hosts = ['3.85.175.4', '100.26.175.217']
env.user = 'ubuntu'


def do_pack():
    """[summary]"""
    local('mkdir -p versions')
    output = local("tar -czvf versions/web_static_{}.tgz web_static/".format((
        datetime.strftime(datetime.now(), "%Y%m%d%H%M%S"))), capture=True)

    if output.succeeded:
        return output
    return None


def do_deploy(archive_path):
    """Distributes an archive to the web servers."""
    """
    Deploy archive to web server
    """
    if path.isfile(archive_path) is False:
        return False
    try:
        filename = archive_path.split("/")[-1]
        no_ext = filename.split(".")[0]
        path_no_ext = "/data/web_static/releases/{}/".format(no_ext)
        symlink = "/data/web_static/current"
        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(path_no_ext))
        run("tar -xzf /tmp/{} -C {}".format(filename, path_no_ext))
        run("rm /tmp/{}".format(filename))
        run("mv {}web_static/* {}".format(path_no_ext, path_no_ext))
        run("rm -rf {}web_static".format(path_no_ext))
        run("rm -rf {}".format(symlink))
        run("ln -s {} {}".format(path_no_ext, symlink))
        return True
    except Exception as e:
        return False


def deploy():
    """creates and distributes an archive to the web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
