#!/usr/bin/python3
"""This module is a fabric script"""
from fabric.api import task, lcd, local
import tarfile
import os
from datetime import datetime


@task
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
