#!/usr/bin/python3
"""This module is a fabfile"""
from fabric.api import put, run, cd, env, lcd, local, runs_once
import os
import tarfile
from datetime import datetime

env.hosts = ['100.26.121.248', '18.234.107.186']


@runs_once
def do_pack():
    """Archive the contents of web-static into a .tgz file."""
    directory = "versions"
    if not os.path.exists(directory):
        os.mkdir(directory)
    now = datetime.now()
    output = "web_static_" + now.strftime("%Y%m%d%H%M%S") + ".tgz"
    path = os.path.join(directory, output)
    relative_path = os.path.join("../", path)
    with lcd("web_static"):
        local(f"tar -czf {relative_path} .")
    if os.path.exists(path):
        return path


def do_deploy(archive_path):
    """distributes an archive to my web servers"""
    if not os.path.exists(archive_path):
        return False
    run('mkdir -p /tmp/')
    put(archive_path, '/tmp/')  # upload this archive
    archive_filename = archive_path.split("/")[1]
    remote_path_archive = os.path.join("/tmp", archive_filename)
    uncompress_file_dir = archive_filename.split(".")[0]
    uncompress_file_path = os.path.join("/data/web_static/releases/",
                                        uncompress_file_dir)
    run("mkdir -p " + uncompress_file_path)  # enforce directory
    with cd(uncompress_file_path):
        run("tar xzvf " + remote_path_archive)

    # delete archive file from web server
    run("rm " + remote_path_archive)

    # delete the symbolic link /data/web_static/current
    run("rm /data/web_static/current")

    # create symbolic link to uncompress_file_path
    run("ln -s " + uncompress_file_path + " /data/web_static/current")

    return True


def deploy():
    """this definition calls do_deploy and do_pack"""

    path = do_pack()

    if not path:
        return False

    deploy = do_deploy(path)
    return deploy
