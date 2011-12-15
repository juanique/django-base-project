from fabric.api import run
import project.settings as settings

def info():
    if settings.DEBUG:
        print "Server is in development mode."
    else:
        print "Server is in production mode."

def init_submodules():
    run("git submodule init")
    run("git submodule update")

def install():
    try:
        import tastypie
    except ImportError:
        pass

