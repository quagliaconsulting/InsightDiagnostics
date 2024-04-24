import os

def debug_log(thing):
    if os.getenv('DEBUG_LOGGING'):
        print(thing)