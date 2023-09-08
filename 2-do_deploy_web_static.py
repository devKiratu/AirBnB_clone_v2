#!/usr/bin/python3
"""
This script distributes an archive to your web servers, using the function
do_deploy
"""

import os
from fabric.api import *


env.hosts = ['100.26.49.192', '107.22.143.52']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """deploys an archive to remote servers and prepares it for use"""
    # check if archive_path exists
    if not os.path.exists(archive_path):
        return False
    try:
        # Upload the archive to the /tmp/ directory of the web server
        upload = put(archive_path, '/tmp/')
        if upload.failed:
            return False
        # Uncompress .tgz to  /data/web_static/releases/<file_name>
        files_path = "web_static_{}".format(archive_path[-18:-4])
        c = "sudo mkdir -p /data/web_static/releases/{}".format(files_path)
        if run(c).failed:
            return False
        c = "sudo tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}"\
            .format(files_path, files_path)
        if run(c).failed:
            return False
        # Delete the archive from the web server
        if run("sudo rm -f /tmp/{}.tgz".format(files_path)).failed:
            return False

        # Delete the symbolic link /data/web_static/current from web server
        if run("sudo rm -rf /data/web_static/current").failed:
            return False

        # Create new symbolic link /data/web_static/current to uploaded files
        c = "sudo ln -s -f /data/web_static/releases/{}\
 /data/web_static/current".format(files_path)
        if run(c).failed:
            return False

        # move unzipped files to base files_path
        c = "sudo mv /data/web_static/releases/{}/web_static/*\
 /data/web_static/releases/{}".format(files_path, files_path)
        if run(c).failed:
            return False

        # delete empty folder
        c = "sudo rm -rf /data/web_static/releases/{}/web_static"\
            .format(files_path)
        if run(c).failed:
            return False
        return True
    except Exception:
        return False
