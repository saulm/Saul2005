Instructions to install/run on development mode: (Tested on python 3.4)

pip install -r requirements.txt
python manage.py syncdb
python manage.py runserver


Known Issues:
*Pending require email pipeline test
*Pending views tests
*Hardcoded development url on utils.py:17
*Tests can be improved by overriding the USER_TYPE setting and writting independent tests for each type
