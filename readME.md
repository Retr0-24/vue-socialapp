# Frontend

Create VueJS Project
npm create vue@latest

Go into folder
cd /foldername

Install VueJS
npm install

Install Tailwind
npm install tailwindcss @tailwindcss/vite

Install Dependencies
npm install vue-router
npm install pinia
npm install axios

Compile and hot-reload for Production
npm run dev

Compile and minify for Production
npm run build

# Backend

Create local environment
python3 -m venv env

Activate local enironment
source env/bin/activate

Install Django
pip3 install django

Install Dependencies
pip3 install djangorestframework
pip3 install djangorestframework-simplejwt
pip3 install pillow
pip3 install django-cors-headers

Create Django Project
django-admin startproject backend

Add in the settings.py the installed Apps
'rest_framework',
'rest_framework-simplejwt',
'corsheaders',

Application definition SimpleJWT
SIMPLE_JWT = {
'ACCES_TOKEN_LIFETIME': timedelta(days=30),
'REFRESH_TOKEN_LIFETIME': timedelta(days=180),
'ROTATE_REFRESH_TOKEN': False,
}

REST_FRAMEWORK = {
'DEFAULT_AUTHENTICATION_CLASSES': (
'rest_framework_simplejwt.authentication.JWTAuthentication',
),
'DEFAULT_PERMISSION_CLASSES': (  
'rest_framework.permissions.IsAuthenticated',
),
}
CORS_ALLOWED_ORIGINS = [
"http:127.0.0.1:5173",
]
CSRF_TRUSTED_ORIGINS = [
"http:127.0.0.1:5173",
]

Set Cors Headers in Middleware
'cors_headers.middleware.CorsMiddleware', (BETWEEN DJANGO SESSION.MIDDLEWARE AND DJANGO COMMON.MIDDLEWARE)

Start Django Project
python manage.py startapp account

Configure models.py
Create User Manager
Create User Model

Configure settings.py
Tell django default user model with AUTH_USER_MODEL
Add 'account', to INSTALLED APPS

Make migrations
python3 manage.py makemigrations

Run Migrations
python3 manage.py migrate

Run Server
python3 manage.py runserver
