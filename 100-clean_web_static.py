#!/usr/bin/python3
from fabric.api import *
import os

env.hosts = ['54.157.138.77', '100.26.155.31']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_clean(number=0):
    """Deletes out-of-date archives.

    Args:
        number (int): The number of archives to keep.
    """
    number = int(number)

    if number < 1:
        number = 1

    # Clean local archives
    local_archives = sorted(os.listdir("versions"))
    if len(local_archives) > number:
        archives_to_delete = local_archives[:-number]
        for archive in archives_to_delete:
            local("rm -f versions/{}".format(archive))

    # Clean remote archives
    with cd("/data/web_static/releases"):
        rem_archives = run("ls -1t").split()
        rem_archives = [arc for arc in rem_archives if "web_static_" in arc]
        if len(rem_archives) > number:
            archives_to_delete = rem_archives[:-number]
            for archive in archives_to_delete:
                run("rm -rf /data/web_static/releases/{}".format(archive))
