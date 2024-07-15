#!/usr/bin/python3

from fabric.api import env, put, run
import os

# Define the web servers
env.hosts = ['54.157.138.77', '100.26.155.31']

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
