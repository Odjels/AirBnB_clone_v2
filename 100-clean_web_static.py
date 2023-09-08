#!/usr/bin/python3
# This Fabfile is to delete out-of-date archives.
import os
from fabric.api import *

env.hosts = ["3.85.175.4", "100.26.175.217"]


def do_clean(number=0):
    """Deleting the out-of-date archives."""

    number = 1 if int(number) == 0 else int(number)

    archive_files = sorted(os.listdir("versions"))
    [archive_files.pop() for b in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(i)) for i in archives]

    with cd("/data/web_static/releases"):
        archive_files = run("ls -tr").split()
        archive_files = [i for i in archive_files if "web_static_" in i]
        [archive_files.pop() for b in range(number)]
        [run("rm -rf ./{}".format(i)) for i in archive_files]
