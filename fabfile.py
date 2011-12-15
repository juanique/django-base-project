from fabric.api import run, cd, sudo
from fabric.operations import local as lrun
from fabric.context_managers import lcd
from fabric_helpers import lsudo
import project.settings as settings


def info():
    if settings.DEBUG:
        print "Server is in development mode."
    else:
        print "Server is in production mode."

def test():
    with cd("project"):
        run("python manage.py test")

def init_submodules():
    lrun("git submodule init")
    lrun("git submodule update")

def install():
    init_submodules()

    try:
        import tastypie
    except ImportError, e:
        with lcd('lib/django-tastypie'):
            lsudo("python setup.py install")

    try:
        import jsonrpc
    except ImportError, e:
        if e.message == "No module named jsonrpc":
            with cd('lib/django-json-rpc'):
                lsudo("python setup.py install")
