Installation Guide:
```
1. Clone repository
2. python3 venv -m venv
3. pip install -r requirements.txt
4. cd ABSCS
5. python3 manage.py makemigrations
6. python3 manage.py migrate
```

> [!IMPORTANT]
> When pulling from updated repository, ensure to remigrate the database by running the last two commands.

Execution Guide:
```
1. Open the ABSCS directory with manage.py
2. 'python3 manage.py runserver 0.0.0.0:8000' in terminal to start server
```
