from firebase_functions import https_fn
from firebase_admin import initialize_app
import os
import sys

# Add project directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Initialize Firebase Admin
initialize_app()

# Import Django WSGI application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bgh_erp.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

@https_fn.on_request()
def api(req: https_fn.Request) -> https_fn.Response:
    return application(req.environ, req.start_response)
