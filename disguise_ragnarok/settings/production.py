from .settings import *
import dj_database_url

DEBUG = False

DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
}

ALLOWED_HOSTS = ['ragnarok-disguise.herokuapp.com']