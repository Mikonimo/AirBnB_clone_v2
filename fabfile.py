#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from web_static folder"""
from fabric import task, Config
from datetime import datetime
import os

# Importing local command from Fabric API
from fabric.api import local

@task
def do_pack(c):
    """Creates a .tgz archive"""
    if not os.path.exists("versions"):
        os.makedirs("versions")

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = "versions/web_static_{}.tgz".format(timestamp)

    # Create the archive
    result = c.local("tar -cvzf {} web_static".format(archive_name))

    # Check if the archive was created successfully
    if result.ok:
        return os.path.abspath(archive_name)
    else:
        return None
