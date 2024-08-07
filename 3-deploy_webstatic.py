#!/usr/bin/python3

from fabric.api import env, local, put, run
from datetime import datetime
import os

# Define the web servers
env.hosts = ['54.157.138.77', '100.26.155.31']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder."""
    try:
        if not os.path.exists("versions"):
            os.makedirs("versions")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = f"versions/web_static_{timestamp}.tgz"
        local(f"tar -cvzf {archive_path} web_static")
        return archive_path
    except Exception as e:
        print(f"Error: {e}")
        return None


def do_deploy(archive_path):
    """Distributes an archive to the web servers."""
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        archive_name = os.path.basename(archive_path)
        archive_folder = archive_name.split(".")[0]
        release_path = f"/data/web_static/releases/{archive_folder}/"

        put(archive_path, "/tmp/")

        # Uncompress the archive to the folder
        run(f"mkdir -p {release_path}")
        run(f"tar -xzf /tmp/{archive_name} -C {release_path}")

        # Delete the archive from the web server
        run(f"rm /tmp/{archive_name}")

        # Move contents out of the extracted folder
        run(f"mv {release_path}web_static/* {release_path}")
        run(f"rm -rf {release_path}web_static")

        # Delete the symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run(f"ln -s {release_path} /data/web_static/current")

        print("New version deployed!")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def deploy():
    """Creates and distributes an archive to the web servers."""
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
