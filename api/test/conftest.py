
from app import create_app, celery
from celery.signals import worker_ready
import pytest
import threading
import time


WORKER_READY = list()

@pytest.fixture
def app():
    app = create_app()
    return app


class Worker(threading.Thread):
    """Run the Celery worker in a background thread."""

    def run(self):
        """Run the thread."""
        celery_args = ['-C', '-q', '-c', '1', '-P', 'solo', '--without-gossip']
        with create_app().app_context():
            celery.worker_main(celery_args)


@worker_ready.connect
def on_worker_ready(**_):
    """Called when the Celery worker thread is ready to do work.
    This is to avoid race conditions since everything is in one python process.
    """
    WORKER_READY.append(True)


@pytest.fixture(autouse=True, scope='session')
def celery_worker():
    """Start the Celery worker in a background thread."""
    thread = Worker()
    thread.daemon = True
    thread.start()
    for i in range(10):  # Wait for worker to finish initializing to avoid a race condition I've been experiencing.
        if WORKER_READY:
            break
        time.sleep(1)