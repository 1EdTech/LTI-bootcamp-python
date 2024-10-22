import datetime
from tempfile import mkdtemp

class Config:
    DEBUG = True
    ENV = "development"
    CACHE_TYPE = "simple"
    CACHE_DEFAULT_TIMEOUT = 600
    SECRET_KEY = "replace-me"
    SESSION_TYPE = "filesystem"
    SESSION_FILE_DIR = mkdtemp()
    SESSION_COOKIE_NAME = "lti1p3session-id"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True  # Set True for production HTTPS
    SESSION_COOKIE_SAMESITE = "None"  # Set 'None' for production HTTPS
    SESSION_COOKIE_PARTITIONED = True
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(minutes=60)
    DEBUG_TB_INTERCEPT_REDIRECTS = False
