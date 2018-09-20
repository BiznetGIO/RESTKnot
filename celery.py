import os
from srv import celery, create_app

app = create_app()
app.app_context().push()