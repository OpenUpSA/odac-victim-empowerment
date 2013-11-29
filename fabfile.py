from __future__ import with_statement
from fabric.api import *


def staging():
    """
    Env parameters for the staging environment.
    """

    env.hosts = ['ec2-54-194-94-222.eu-west-1.compute.amazonaws.com']
    env.envname = 'staging'
    env.user = 'ubuntu'
    env.group = 'ubuntu'
    env.key_filename = '~/.ssh/aws_code4sa.pem'
    env['config_dir'] = 'config_staging'
    print("STAGING ENVIRONMENT\n")


def setup():
    """
    Install dependencies and create an application directory.
    """

    # update locale
    sudo('locale-gen en_ZA.UTF-8')

    # install pip
    sudo('apt-get install python-pip')

    # TODO: setup virtualenv

    # create application directory if it doesn't exist yet
    code_dir = '/var/www/victim-empowerment'
    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            # create project folder
            sudo('mkdir -p /var/www/victim-empowerment')
            sudo('mkdir -p /var/www/victim-empowerment/msg_handler')
            sudo('mkdir /var/www/victim-empowerment/instance')

    # clear pip's cache
    with settings(warn_only=True):
        sudo('rm -r /tmp/pip-build-root')

    # install the necessary Python packages
    put('requirements/base.txt', '/tmp/base.txt')
    put('requirements/production.txt', '/tmp/production.txt')
    sudo('pip install -r /tmp/production.txt')

    # install apache2 and mod-wsgi
    sudo('apt-get install apache2')
    sudo('apt-get install libapache2-mod-wsgi')

    # ensure that apache user www-data has access to the application folder
    sudo('chmod -R 770 /var/www/victim-empowerment')
    sudo('chown -R ' + env.user + ':www-data /var/www/victim-empowerment')


def configure():
    """
    Upload config files, and restart apache.
    """

    # upload files to /tmp
    put(env.config_dir + '/apache.conf', '/tmp/apache.conf')
    put(env.config_dir + '/config.py', '/tmp/config.py')
    put(env.config_dir + '/wsgi.py', '/tmp/wsgi.py')

    # move files to their intended directories
    sudo('mv -f /tmp/apache.conf /etc/apache2/sites-available/apache.conf')
    sudo('mv -f /tmp/config.py /var/www/victim-empowerment/instance/config.py')
    sudo('mv -f /tmp/wsgi.py /var/www/victim-empowerment/wsgi.py')

    # de-activate default site
    with settings(warn_only=True):
        sudo('a2dissite 000-default')

    ## enable apache's caching plugin
    #sudo('a2enmod expires')
    #
    ## enable apache's gzip plugin
    #sudo('a2enmod deflate')

    # activate site
    sudo('a2ensite apache.conf')

    # restart apache
    sudo('/etc/init.d/apache2 reload')



def deploy():
    """
    Upload our package to the server, unzip it, and restart apache.
    """

    # create a tarball of our package
    local('tar -czf msg_handler.tar.gz msg_handler/', capture=False)

    # upload the source tarball to the temporary folder on the server
    put('msg_handler.tar.gz', '/tmp/msg_handler.tar.gz')

    # turn off apache
    with settings(warn_only=True):
        sudo('/etc/init.d/apache2 stop')

    # enter application directory
    with cd('/var/www/victim-empowerment'):
        # and unzip new files
        sudo('tar xzf /tmp/msg_handler.tar.gz')

    # now that all is set up, delete the tarball again
    sudo('rm /tmp/msg_handler.tar.gz')
    local('rm msg_handler.tar.gz')

    # clean out old logfiles
    with settings(warn_only=True):
        sudo('rm /var/www/victim-empowerment/msg_handler/debug.log*')

    # ensure that apache user has access to all files
    sudo('chmod -R 770 /var/www/victim-empowerment/msg_handler')
    sudo('chown -R ' + env.user + ':www-data /var/www/victim-empowerment/msg_handler')

    # and finally reload the application
    sudo('/etc/init.d/apache2 start')