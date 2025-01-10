"""
WSGI config for facecheck project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facecheck.settings')

application = get_wsgi_application()

# for versel deployment
app = application #this connected to settings.py file host [vercel.app]

