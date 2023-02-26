## what you need to setup the project

1. need to have docker installed
2. vscode

### steps
1. in vscode install the dev containers 
2. open folder in container (this might take a few minutes)
3. cd backend
4. create a virtualenvironment
5. pip install -r requirements.txt
6. create .env file inside of backend/
7. run `python manage.py migrate`
3. in the integrated terminal `python manange.py runserver`