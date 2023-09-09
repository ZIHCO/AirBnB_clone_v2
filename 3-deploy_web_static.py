#!/usr/bin/python3
"""this module is fabfile"""
from fabric.api import env
do_deploy = __import__("2-do_deploy_web_static").do_deploy
do_pack = __import__("1-pack_web_static").do_pack
env.hosts = __import__("2-do_deploy_web_static").env.hosts


def deploy():
    """this definition calls do_deploy and do_pack"""

    path = do_pack()

    if not path:
        return False

    deploy = do_deploy(path)
    return deploy
