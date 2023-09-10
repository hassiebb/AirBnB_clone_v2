#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""

from fabric.api import env, put, run, local
from os.path import exists, isdir
from datetime import datetime

env.hosts = ['54.172.86.31', '54.236.44.220']
env.user = 'ubuntu'

def do_pack():
    """Generates a tgz archive"""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if not isdir("versions"):
            local("mkdir versions")
        file_name = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except Exception as e:
        return None

def do_deploy(archive_path):
    """Deploys an archive to your web servers"""
    if not exists(archive_path):
        return False
    try:
        archive_name = archive_path.split('/')[-1]
        archive_name_no_ext = archive_name.split('.')[0]
        release_path = "/data/web_static/releases/{}".format(archive_name_no_ext)

        # Upload the archive to /tmp/ directory on the server
        put(archive_path, "/tmp/")

        # Create the release directory
        run("mkdir -p {}".format(release_path))

        # Uncompress the archive
        run("tar -xzf /tmp/{} -C {}".format(archive_name, release_path))

        # Delete the archive from the server
        run("rm /tmp/{}".format(archive_name))

        # Move the contents of the release directory to the web_static directory
        run("mv {}/web_static/* {}".format(release_path, release_path))

        # Remove the empty web_static directory
        run("rm -rf {}/web_static".format(release_path))

        # Delete the existing symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link to the deployed version
        run("ln -s {} /data/web_static/current".format(release_path))

        return True
    except Exception as e:
        return False

if __name__ == "__main__":
    archive_path = do_pack()
    if archive_path:
        result = do_deploy(archive_path)
        print("New version deployed!" if result else "Deployment failed.")
