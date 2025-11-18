# Developing

## Frontend

Create VueJS Project
<br>npm create vue@latest

Go into folder
<br>cd /foldername

Install VueJS
<br>npm install

Install Tailwind
<br>npm install tailwindcss @tailwindcss/vite

Install Dependencies
<br>npm install vue-router
<br>npm install pinia
<br>npm install axios

Compile and hot-reload for Production
<br>npm run dev

Compile and minify for Production
<br>npm run build

## Backend

Create local environment
<br>python3 -m venv env

Activate local enironment
<br>source env/bin/activate

Install Django
<br>pip3 install django

Install Dependencies
<br>pip3 install djangorestframework
<br>pip3 install djangorestframework-simplejwt
<br>pip3 install pillow
<br>pip3 install django-cors-headers

Or Pip install all Dependencies from requirements.txt
<br>pip3 install -r requirements.txt

Create Django Project
<br>django-admin startproject backend

Add in the settings.py the installed Apps
<br>'rest_framework',
<br>'rest_framework-simplejwt',
<br>'corsheaders',

Application definition SimpleJWT
<br>SIMPLE_JWT = {
<br>'ACCES_TOKEN_LIFETIME': timedelta(days=30),
<br>'REFRESH_TOKEN_LIFETIME': timedelta(days=180),
<br>'ROTATE_REFRESH_TOKEN': False,
<br>}

<br>REST_FRAMEWORK = {
<br>'DEFAULT_AUTHENTICATION_CLASSES': (
<br>'rest_framework_simplejwt.authentication.JWTAuthentication',
<br>),
<br>'DEFAULT_PERMISSION_CLASSES': (  
<br>'rest_framework.permissions.IsAuthenticated',
<br>),
<br>}
<br>CORS_ALLOWED_ORIGINS = [
<br>"http:127.0.0.1:5173",
<br>]
<br>CSRF_TRUSTED_ORIGINS = [
<br>"http:127.0.0.1:5173",
<br>]

Set Cors Headers in Middleware
<br>'cors_headers.middleware.CorsMiddleware', (BETWEEN DJANGO SESSION.MIDDLEWARE AND DJANGO COMMON.MIDDLEWARE)

Start Django Project
<br>python manage.py startapp account

Configure models.py
<br>Create User Manager
<br>Create User Model

Configure settings.py
<br>Tell django default user model with AUTH_USER_MODEL
<br>Add 'account', to INSTALLED APPS

Make migrations
<br>python3 manage.py makemigrations

Run Migrations
<br>python3 manage.py migrate

Run Server
<br>python3 manage.py runserver

# Production

## Backend

Create .env file and insert VITE_API_URL
<br>VITE_API_URL=http://api.sma.com

Load settingsprod.py instead of settings.py

# Notes

## Packages NPM

<br>tailwindcss @4.1.14
<br>axios @1.12.2
<br>pinia @3.0.3

## Packages PIP

<br>asgiref @3.10.0
<br>Django @5.2.7
<br>django-cors-headers @4.9.0
<br>djangorestframework @3.16.1
<br>djangorestframework_simplejwt @5.5.1
<br>pillow @12.0.0
<br>PyJWT @2.10.1
<br>sqlparse @0.5.3

## User

Main Dev User:
<br>Id: deeda893-1cf5-4065-b012-a08d552f061b
<br>Username: Retr0
<br>Email: crankywright1@justzeus.com
<br>Password: testingpassword

Test User 1:
<br>Id: 71d84f01-537b-430d-9711-b71df5028321
<br>Username: testname
<br>Email: test@gmail.com
<br>Password: testpassword

Test User 2:
<br>Id: 0d5ffc60-b432-4d02-9680-12a8098cec10
<br>Username: LoL
<br>Email: lol@gmail.com
<br>Password: testpassword

First Real User:
<br>Username: John Smith
<br>Email: john.smith@gmail.com
<br>Password: testingpassword

Dev Notes Temp:

Create Architecture.md
Comment Code
