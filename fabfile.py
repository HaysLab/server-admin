from __future__ import with_statement
from fabric.api import task, run, sudo, env
from fabric.contrib.console import confirm
import getpass

env.password = getpass.getpass("Password: ")
env.sudo_password = env.password
env.hosts = ["minsky{0}.cc.gatech.edu".format(x) for x in range(1, 8)]
env.user = "vagrawal38"


def list_dir():
    sudo("ls -al")
    #run("ls -al")


def add_docker_user(username="$USER"):
    sudo("usermod -aG docker {0}".format(username))

def run_command(command):
    """
    Run arbitrary commands on the remote machine
    E.g. `fab run_command:command="apt-get install emacs"`
    """
    sudo(command)
