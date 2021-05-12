import multiprocessing
import os


def max_workers():
    return multiprocessing.cpu_count() * 2 + 1


host = os.environ.get("APP_HOST", "0.0.0.0")
port = os.environ.get("APP_PORT", "8000")

bind = f"{host}:{port}"
workers = max_workers()
