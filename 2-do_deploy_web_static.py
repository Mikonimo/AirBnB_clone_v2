#!/usr/bin/python3
"""Distributes an archive to web servers using Fabric3"""
from fabric.api import env, put, run
import os

env.hosts = ['54.157.138.77', '100.26.155.31']
env.user = 'ubuntu'
env.key_filename = 'id_rsa'


def do_deploy(archive_path):
    """Deploys the archive to the web servers"""
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive
        print("Uploading Archive")
        put(archive_path, '/tmp/')

        # Extract the archive
        archive_name = os.path.basename(archive_path)
        name = archive_name.split(".")[0]
        path = f"/data/web_static/releases/{archive_folder}/"
        print("Creating Directory")
        run('mkdir -p {}'.format(path))
        print("Extracting the archive")
        run('tar -xzf /tmp/{} -C {}'.format(archive_name, path))
        print("Removing the /tmp/archive")
        run('rm /tmp/{}'.format(archive_name))

        # Create a symbolic link
        print("Removing the symbolic link")
        run('rm -f /data/web_static/current')
        print("Creating the new symbolic link")
        run('ln -s {} /data/web_static/current'.format(path))

        print("New version deployed!")
        return True
    except Exception as e:
        print("Deployment failed: ", str(e))
        return False
