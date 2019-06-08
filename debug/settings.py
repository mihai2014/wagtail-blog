MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    # ...
]

ANONYMOUS_SESSION_PROCESS_FUNCTION = 'apps.common.middleware.process_anonymous_session'
