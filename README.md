# Apollo
Notification Manger

Dependencies: Django, requests, psycopg2, Python 3.5.1

Once Downloaded and dependencies installed:

1. Change Database Settings in SunLoan.settings.py to point to your PostGres Database
2. If you are reloading run manage.py flush to kill previous data
3. Run manage.py makemigration
4. Run manage.py migrate
5. Run manage.py createsuper so that you can access the site
6. Go to Manage Data (http://127.0.0.1:8000/data) so that you can load the default data sets for Stores, Statuses, etc.
