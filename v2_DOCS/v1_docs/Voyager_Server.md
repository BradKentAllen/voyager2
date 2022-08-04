# Voyager - Server

Voyager server is a flask server and can be used for a variety of networking and communications functions.  Before starting this, you must have completed the RPi_voyager setup.

## Set up fixed IP Address on your network Router

xxxxx



## Install and Set up Server Software

Install nginx ('engine - X') Load Balancer/Web Server and uwsgi Web Server Gateway.

```
sudo apt-get install nginx

sudo pip3 install flask uwsgi	# these must be installed together
```



### Set up file structure for Flask server

```
# create directory
mkdir flask_app

# put RPi_flask_app.py into flask_app folder

# give permission for server to access directory:
sudo chown www-data /home/pi/flask_app


```



XXXX - Add example/instructions here:   Move RPi_flask_app.py to main directory

### Test Server

Test nginx by going to your RPi's IP address in your Internet browser.  You should see:

![nginx_welcome](../static/markdown_images/nginx_welcome.png)

Test uwsgi:

```
# You must be in your /home/pi directory
# test uwsgi
uwsgi --socket 0.0.0.0:8000 --protocol=http -w RPi_flask_app:app
```

You should get a response that the uwsgi 

Now test in your browser by entering your IP address with :8000 at the end:

192.168.1.15:8000

You should get the index page from the RPi_flask_app.py



### Create uwsgi initialization file

```
# open nano editor and create file (in your /home/pi directory):
sudo nano uwsgi.ini

# copy the code below into the editor
```

uwsgi.ini:

```
[uwsgi]

chdir = /home/pi/flask_app
module = RPi_flask_app:app

master = true
processes = 1
threads = 2

uid = www-data
gid = www-data

socket = /tmp/flask_app.sock
chmod-socket = 664
vacuum = true

die-on-term = true
touch-reload = /home/pi/RPi_flask_app.py
```



Test uwsgi.ini

```
# in /home/pi:
uwsgi --ini uwsgi.ini
```

Open a second ssh window to your RPi and check the following:

```
ls /tmp
```

You should see a **flask_app.sock** file in that directory while uwsgi.ini is running



### Configure nginx to run uwsgi

Create proxy file

```
# delete the default site setting in nginx
sudo rm /etc/nginx/sites-aenabled/default

# create flasktest_proxy file (this will be a regular file)
sudo nano /etc/nginx/sites-enabled/flask_app_proxy

# paste in code below:
```

Flask_app_proxy:

```
server {
listen 80;
server_name localhost;

location / { try_files $uri @app; }
location @app {
include uwsgi_params;
uwsgi_pass unix:/tmp/flask_app.sock;
}
}
```

### test the nginx server by restarting

```
# restart nginx server
sudo systemctl restart nginx

# NOTE:  You will get a "502 Bad Gateway" because uwsgi is not running and nginx can't pass the browser request.
```

### Set up uwsgi to run when pi boots

```
cd /etc/systemd/system

# create uwsgi.service
sudo nano uwsgi.service

```



### Test uwsgi auto start

```
sudo systemctl daemon-reload		# restart daemon so it picks up service
sudo systemctl start uwsgi.service	# start the service
sudo systemctl status uwsgi.service	# check status of service, should be active

#### If you get a permission error in the status report, verify flask_app directory has owner www-data:
sudo chown www-data /home/pi/flask_app
sudo systemctl stop uwsgi.serve 	# you have to start the service you started
sudo systemctl start uwsgi.service	# now restart it
```



In your browser, go to the IP address without the socket. (e.g. 192.168.1.14).  You should see the flask index page.

### Set up to start on boot

```
sudo systemctl enable uwsgi.service # enables service to run on every reboot
```

### Test your RPi_voyger server is working:

```
sudo reboot

# once it reboots, use your browser to go to the IP address and verify is working
```





# Maintenance and Troubleshooting

### systemctl

https://www.raspberrypi.org/documentation/linux/usage/systemd.md

systemd documents:  https://docs.fedoraproject.org/en-US/quick-docs/understanding-and-administering-systemd/index.html

```
sudo systemctl stop Start.service
sudo systemctl start Start.service
sudo systemctl status Start.service

sudo systemctl enable Start.service		# makes it happen at boot
sudo systemctl disable Start.servic

# other services
sudo systemctl status Start.service
sudo systemctl status uwsgi.service
sudo systemctl status pigpiod
```





