#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from web_sttic folder"""
from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """Creates a .tgz archive"""
    if not os.path.exists("version"):
        os.makedirs("versions")

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = "versions/web_static_{}.tgz".format(timestamp)

    # Create the archive
    result = local("tar -cvzf {} web_static".format(archive_name))

    # Check if the archive was created successfully
    if result.succeeded:
        return os.path.abspath(archive_name)
    else:
        return None
