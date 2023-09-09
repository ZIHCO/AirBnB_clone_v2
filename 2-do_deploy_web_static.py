#!/usr/bin/python3
"""This module is a fabfile"""
from fabric.api import put, run, cd, env
import os

env.hosts = ['100.26.121.248', '18.234.107.186']


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
