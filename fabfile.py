import sys
from fabric_helpers import sudo, cd, run
from fabric.api import settings

def local():
    print "Running in local mode."

def remote():
    print "Running in remote mode."

def info():
    import project.settings as django_settings
    if django_settings.DEBUG:
        print "Server is in development mode."
    else:
        print "Server is in production mode."

def test():
    with cd("project"):
        run("python manage.py test")

def init_submodules():
    run("git submodule init")
    run("git submodule update")

def install_nodejs():
    NODE_VERSION = "v0.6.5"

    with settings(warn_only=True):
        result = run("node --version")
        
    if result.failed:
        with cd("lib/node"):
            run("git checkout %s" % NODE_VERSION)
            sudo("apt-get install libssl-dev openssl")
            run("./configure")
            run("make")
            sudo("make install")
    else:
        print "Node.js already installed"

    install_npm()

def install_npm():
    with settings(warn_only=True):
        result = run("npm --version")

    if result.failed:
        sudo("apt-get install curl")
        run("curl http://npmjs.org/install.sh | sh")
    else:
        print "npm already installed"

def install_coffee():
    with settings(warn_only=True):
        result = run("coffee --version")

    if result.failed:
        sudo("npm install -g coffee-script")
    else:
        print "Coffeescript already installed"


def install_tastypie():
    try:
        import tastypie
        print "tastypie is installed - version %s." % str(tastypie.__version__)
    except ImportError, e:
        sudo("pip install mimeparse")
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
    install_nodejs()
    #test()

def run_development():
    with cd("project"):
        run("python manage.py runserver 0.0.0.0:8000")
