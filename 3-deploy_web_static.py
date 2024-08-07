#!/usr/bin/python3
"""Distributes an archive to web servers using Fabric3"""
from fabric.api import env, put, run, local
import os
from datetime import datetime

env.hosts = ['54.157.138.77', '100.26.155.31']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder"""
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = f"versions/web_static_{now}.tgz"

    if not os.path.exists("versions"):
        os.makedirs("versions")

    local(f"tar -cvzf {archive_name} web_static")

    if os.path.exists(archive_name):
        return archive_name
    return None


def do_deploy(archive_path):
    """Distributes an archive to the web servers."""
    if not os.path.exists(archive_path):
        return False

    try:
        # Local deployment
        archive_name = os.path.basename(archive_path)
        archive_folder = archive_name.split(".")[0]
        local_release_path = f"/data/web_static/releases/{archive_folder}"

        local(f"mkdir -p {local_release_path}")
        local(f"tar -xzf {archive_path} -C {local_release_path}")

        local(f"mv {local_release_path}/web_static/* {local_release_path}")
        local(f"rm -rf {local_release_path}/web_static")

        local("rm -rf /data/web_static/current")
        local(f"ln -s {local_release_path} /data/web_static/current")

        # Server deployment
        release_path = f"/data/web_static/releases/{archive_folder}"
        put(archive_path, "/tmp/")

        run(f"mkdir -p {release_path}")
        run(f"tar -xzf /tmp/{archive_name} -C {release_path}")

        run(f"rm /tmp/{archive_name}")

        run(f"mv {release_path}/web_static/* {release_path}")
        run(f"rm -rf {release_path}/web_static")

        run("rm -rf /data/web_static/current")
        run(f"ln -s {release_path} /data/web_static/current")

        print("New version deployed locally and on servers!")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def deploy():
    """Creates and distributes an archive to web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
