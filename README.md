victim-empowerment
==================

Road to Justice's Victim Empowerment project.

The demo can be found at http://ec2-54-194-198-122.eu-west-1.compute.amazonaws.com/


NOTES:
------
To access this server via SSH:

    ssh -v -i ~/.ssh/aws_code4sa.pem ubuntu@ec2-54-194-198-122.eu-west-1.compute.amazonaws.com

Logs can be found at:

* Flask:

        /var/www/odac-victim-empowerment/debug.log

* Nginx:

        /var/log/nginx/error.log
        /var/log/nginx/access.log

* uWSGI:

        /var/log/uwsgi/emperor.log
        /var/log/uwsgi/uwsgi.log