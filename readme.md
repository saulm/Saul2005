Instructions to install/run on development mode: (Tested on python 3.4)

pip install -r requirements.txt
python manage.py syncdb
python manage.py runserver

In order to use the facebook login, add to /etc/hosts:

127.0.0.1       local.stigy.com

And test in the URL: http://local.stigy.com:8000/


Known Issues:
*Pending require email pipeline test
*Pending views tests
*Hardcoded development url on utils.py:17
*Tests can be improved by overriding the USER_TYPE setting and writting independent tests for each type
