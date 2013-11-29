victim-empowerment
==================

Road to Justice's Victim Empowerment project.

The demo can be found at http://ec2-54-194-94-222.eu-west-1.compute.amazonaws.com/


NOTES:
------
To access this server via SSH:

    ssh -v -i ~/.ssh/aws_code4sa.pem ubuntu@ec2-54-194-94-222.eu-west-1.compute.amazonaws.com

Error logs can be found at:

    tail -n 100 /var/log/apache2/error.log
    tail -n 100 /var/www/victim-empowerment/debug.log