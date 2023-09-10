from fabric.api import local
from datetime import datetime

def do_pack():
    """
    Create a compressed archive of the web_static folder
    """

    # Create the current date and time string for the archive name
    now = datetime.now()
    archive_name = "web_static_{}{}{}{}{}{}.tgz".format(
        now.year, now.month, now.day, now.hour, now.minute, now.second)

    # Create the versions directory if it doesn't exist
    local("mkdir -p versions")

    # Compress the web_static folder into the archive
    result = local("tar -cvzf versions/{} web_static".format(archive_name))

    # Check if the compression was successful
    if result.failed:
        return None
    return "versions/{}".format(archive_name)
