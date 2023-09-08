#!/usr/bin/python3
"""This is a Fabric script to distributes an archive to your web servers"""
from fabric.api import *
from datetime import datetime
from os import path

env.hosts = ['3.85.175.4', '100.26.175.217']
env.user = 'ubuntu'


def do_pack():
    """[generating archive the contents]"""
    local('mkdir -p versions')
    path_way = local("tar -czvf versions/web_static_{}.tgz web_static/".format((
        datetime.strftime(datetime.now(), "%Y%m%d%H%M%S"))), capture=True)

    if path_way.succeeded:
        return path_way
    return None


def do_deploy(archive_path):
    """This Distributes an archive to the web servers."""
    
    if not path.exists(archive_path):
        return False
    try:
        filename = archive_path.split("/")[-1]
        new = filename.split(".")[0]
        path_new = "/data/web_static/releases/{}/".format(new)
        s_link = "/data/web_static/current"
        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(path_new))
        run("tar -xzf /tmp/{} -C {}".format(filename, path_new))
        run("rm /tmp/{}".format(filename))
        run("mv {}web_static/* {}".format(path_new, path_new))
        run("rm -rf {}web_static".format(path_new))
        run("rm -rf {}".format(s_link))
        run("ln -s {} {}".format(path_no_ext, s_link))
        return True
    except Exception as e:
        return False


def deploy():
    """creates and distributes an archive to the web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
