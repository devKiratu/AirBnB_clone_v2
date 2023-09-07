#!/usr/bin/python3
"""
This Fabric script that generates a .tgz archive from the contents of the
web_static folder of the AirBnB Clone repo, using the function do_pack.
"""

from fabric.api import local
from time import strftime


def do_pack():
    """generate a .tgz archive from the web_static folder"""
    try:
        slug = strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(slug)
        local("mkdir -p versions")
        local("tar -czvf {} web_static".format(archive_path))
        return archive_path
    except Exception:
        return None
