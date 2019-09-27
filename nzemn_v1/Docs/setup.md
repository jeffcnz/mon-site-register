
## Set Up Virtual Development Environment


```
$ mkdir nzemn_v1
$ cd nzemn_v1
```
Setup v environments  
```
$ python3 -m venv venv
```
Activate Venv
```
$ source venv/bin/activate
```
Command prompt should change to
```
(venv) $
```
Install pip  
```
(venv) $ pip install Django
```

## Create a Django Project

Create project  
```
$ django-admin startproject nzemn1
```
Navigate to project directory
```
cd nzemn1
```

Create an application within the project

```
$ python manage.py startapp sites  
```
The build was based on the Django tutorials and initially built using SQLite for a basic prototype.

## PostGIS set up  
Install postgresql and postGIS on machine
Create a new user and make that user the owner, open psql as postgres user
```
$ sudo -u postgres psql
```
 and then enter the commands.
```
CREATE USER user PASSWORD 'password';
ALTER DATABASE dbname WITH OWNER user;
```

check where the configuration files are stored
```
SELECT name, setting FROM pg_settings where category='File Locations';
```
Install python-dev and libpq-dev  
Install psycopg2 in virtual environment

NOTE when installing the extensions (PostGIS) make sure that you are connected as the database owner (not postgres) and that you have superuser permissions.  



## Migrate from SQLite to Postgresql

Create a backup of the existing database
```
python manage.py dumpdata > db.json  
```
Change the settings file (follow tutorial instructions), you may need to check the configuration file to confirm the port that is being used.

```
python manage.py migrate
```
Check that the app is running using runserver, then to load data in
```
python manage.py shell
```
Enter the following in the shell
```
from django.contrib.contenttypes.models import ContentType
ContentType.objects.all().delete()
```
Control D to exit from the shell and then
```
python manage.py loaddata db.json
```
Running the server should now show data.

## Postgresql database control.
Start the postgres server, this should be automatic on startup, to check use  
```
sudo systemctl status postgresql
```
starting the service
```
sudo systemctl start postgresql  
```
stopping the service
```
sudo systemctl stop postgresql
```
