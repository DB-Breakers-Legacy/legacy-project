"""
WSGI config for breadbreaker project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys

project_dir = r"C:\Users\user\Documents\projects\breakersdjango"
if project_dir not in sys.path:
    sys.path.append(project_dir)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'breadbreaker.settings')

application = get_wsgi_application()
