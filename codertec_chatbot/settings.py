from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ⚙️ Segurança
SECRET_KEY = 'django-insecure-t=d1a4uq4a2%-otpkj#sdozjd3&fvqa6=fq31qioypjtsq4&ut'

# 💡 DEBUG = True no local (para ver CSS e erros); False no Railway
DEBUG = True  # 🔄 altere para False ao subir para produção

ALLOWED_HOSTS = [
    'codertec-backend.onrender.com',
    'www.codertec.com.br',
    'web-production-6e4b.up.railway.app',
    '.up.railway.app',
    '127.0.0.1',
    'localhost'
]

CSRF_TRUSTED_ORIGINS = [
    "https://codertec-backend.onrender.com",
    "https://web-production-6e4b.up.railway.app",
    "https://www.codertec.com.br"
]

# ---------------------------------------------------------------------
# 🧠 APPS
# ---------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'chatbot',
]

# ---------------------------------------------------------------------
# ⚙️ Middleware
# ---------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # 🔹 Deve vir antes de CommonMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ---------------------------------------------------------------------
# 🌍 CORS (para integração com o site da HostGator)
# ---------------------------------------------------------------------
CORS_ALLOWED_ORIGINS = [
    "https://www.codertec.com.br",
]
CORS_ALLOW_ALL_ORIGINS = True  # 🔹 opcional — útil para teste

# ---------------------------------------------------------------------
# 🔗 URLs / WSGI
# ---------------------------------------------------------------------
ROOT_URLCONF = 'codertec_chatbot.urls'
WSGI_APPLICATION = 'codertec_chatbot.wsgi.application'

# ---------------------------------------------------------------------
# 💾 Banco de dados
# ---------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ---------------------------------------------------------------------
# 🧱 Templates
# ---------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ---------------------------------------------------------------------
# 🌎 Localização
# ---------------------------------------------------------------------
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------
# 🧾 Arquivos estáticos (Admin e API)
# ---------------------------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ❌ Você não precisa dessa linha porque seus CSS/JS estão na HostGator
# STATICFILES_DIRS = [BASE_DIR / 'static']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
