from .settings import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'), # type: ignore
    }
}

ALLOWED_HOSTS = ['localhost', '127.0.0.1','127.0.0.1:8000']