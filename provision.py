import app_logging
import logging
import gdrive

def provision(dummy, payload=None):
    print(f"provision {dummy}")
    if not payload:
        payload = 0