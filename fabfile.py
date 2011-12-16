import sys
import project.settings as settings
from fabric_helpers import sudo, cd, run

def local():
    print "Running in local mode."

def remote():
    print "Running in remote mode."

def info():
    if settings.DEBUG:
        print "Server is in development mode."
    else:
        print "Server is in production mode."

def test():
    with cd("project"):
        run("python manage.py test")

def init_submodules():
    run("git submodule init")
    run("git submodule update")

def install_tastypie():
    try:
        import tastypie
        print "tastypie is installed - version %s." % str(tastypie.__version__)
    except ImportError, e:
        with cd('lib/django-tastypie'):
            sudo("python setup.py install")

def install_jsonrpc():
    try:
        import jsonrpc
        print "jsonrpc is installed."
    except ImportError, e:
        if e.message == "No module named jsonrpc":
            with cd('lib/django-json-rpc'):
                sudo("python setup.py install")

def install_django():
    try:
        import django
        print "django is installed - version %s." % str(django.VERSION)

    except ImportError, e:
        if e.message == "No module named django":
            with cd('lib/Django-1.3.1'):
                sudo("python setup.py install")

def install():
    init_submodules()
    install_django()
    install_jsonrpc()
    install_tastypie()
    test()
