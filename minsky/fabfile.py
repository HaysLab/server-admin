from __future__ import with_statement
from fabric.api import task, run, sudo, env, settings
from fabric.contrib.console import confirm
import getpass
import csv
import os.path as osp
import yaml

def read_credentials():
    """
    Function to read in credentials from the user.
    """
    # check if the credentials exist in a yaml file
    if osp.exists('credentials.yaml'):
        # load up the credentials
        with open('credentials.yaml') as c:
            creds = yaml.load(c)

        env.user = creds['username']
        env.password = creds['password']

    else:
        # credentials not saved, so we get them from the user
        env.user = raw_input("GT username: ")
        env.password = getpass.getpass("GT Password for Minsky: ")
        # save the credentials for future use
        with open('credentials.yaml', 'w') as c:
            yaml.dump({'username': env.user, 'password': env.password}, c)
    
    env.sudo_password = env.password
    env.hosts = ["minsky{0}.cc.gatech.edu".format(x) for x in range(1, 8)]

read_credentials()

def list_dir():
    """
    List the directories in the user's home folder.
    This function is intended to be used as a lightweight test for your infrastructure.
    """
    sudo("ls -al")

def add_docker_users(csv_file=None):
    """
    Add users in the CSV file to the docker group on the server(s).
    """
    if not csv_file:
        print("Need CSV file with column 'User ID' for GT usernames")
        return

    with open(csv_file, 'rb') as f:
        roster = csv.DictReader(f, delimiter=',')
        for x in roster:
            add_docker_user(x['User ID'])
    
def add_docker_user(username="$USER"):
    """
    Add `username` to the Docker group on Minsky.
    Once this is done, `username` can access docker without sudo privileges.
    """
    sudo("usermod -aG docker {0}".format(username))

def run_command(command):
    """
    Run arbitrary commands on the remote machine
    E.g. `fab run_command:command="apt-get install emacs"`
    """
    with settings(warn_only=True):
        sudo(command)
