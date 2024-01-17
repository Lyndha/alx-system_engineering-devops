#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""A fabric script to automate firewall rules for a new server.
"""

from fabric.api import env, run, local, put, sudo
from sys import argv
import subprocess
from termcolor import colored
from os.path import exists
from datetime import datetime
from fabric.api import hide


env.user = 'ubuntu'
env.hosts = []
env.key_filename = '~/.ssh/school'

def do_sqluser():
    """Create a new user for MySQL.
    """

    sudo('mysql -u root -pYourRootPassword -e "CREATE USER IF NOT EXISTS \'holberton_user\'@\'localhost\' IDENTIFIED BY \'projectcorrection280hbtn\';"')
    sudo('mysql -u root -pYourRootPassword -e "GRANT REPLICATION CLIENT ON *.* TO \'holberton_user\'@\'localhost\';"')
    sudo('mysql -u root -pYourRootPassword -e "FLUSH PRIVILEGES;"')
    print(colored(sudo('mysql -uholberton_user -pprojectcorrection280hbtn -e "SHOW GRANTS FOR \'holberton_user\'@\'localhost\'"'), 'green'))

# master database
def master_sql():
    """Create the master database.
    """
    sudo('mysql -u root -pYourRootPassword -e "CREATE DATABASE IF NOT EXISTS tyrell_corp;"')
    sudo('mysql -u root -pYourRootPassword -e "GRANT SELECT ON tyrell_corp.* TO \'holberton_user\'@\'localhost\';"')
    sudo('mysql -u root -pYourRootPassword -e "FLUSH PRIVILEGES;"')
    sudo('mysql -u root -pYourRootPassword -e "CREATE TABLE IF NOT EXISTS tyrell_corp.nexus6 (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL);"')
    sudo('mysql -u root -pYourRootPassword -e "INSERT INTO tyrell_corp.nexus6 (name) VALUES (\'Leon\');"')
    # replica_user()
    sudo('mysql -u root -pYourRootPassword -e "CREATE USER IF NOT EXISTS \'replica_user\'@\'%\' IDENTIFIED BY \'YourPassword\';"')
    sudo('mysql -u root -pYourRootPassword -e "GRANT REPLICATION SLAVE ON . TO \'replica_user\'@\'%\';"')
    sudo('mysql -u root -pYourRootPassword -e "GRANT SELECT ON mysql.user TO \'holberton_user\'@\'localhost\';"')
    sudo('mysql -u root -pYourRootPassword -e "FLUSH PRIVILEGES;"')
    print(colored(sudo('mysql -u root -pYourRootPassword -e "SHOW GRANTS FOR \'replica_user\'@\'%\'"'), 'green'))
    # master_setup()
    sudo('ufw allow from 54.236.46.170 to any port 3306')
    sudo('sed -i "s/^bind-address/# bind-address/" /etc/mysql/mysql.conf.d/mysqld.cnf')
    sudo('echo "server-id       = 1\nlog_bin         = /var/log/mysql/mysql-bin.log\nbinlog_do_db    = tyrell_corp\n" | tee -a /etc/mysql/mysql.conf.d/mysqld.cnf')
    sudo('service mysql restart')
    print(colored(sudo('mysql -u root -pYourRootPassword -e "SHOW MASTER STATUS;"'), 'blue'))
    print(colored(sudo('mysql -u root -pYourRootPassword -e "SELECT * FROM tyrell_corp.nexus6;"'), 'blue'))
    # sudo('mysql -u root -pYourRootPassword -e "DROP DATABASE IF EXISTS tyrell_corp;"')


