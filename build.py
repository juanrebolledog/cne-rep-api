import subprocess
import sys
import os

from pynt import task

_curpath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(_curpath)


@task()
def server():
    """ Run the development server, don't use this in production! """
    subprocess.call(['./server.py'])
