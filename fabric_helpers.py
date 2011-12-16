from fabric.operations import local


import sys

if "local" in sys.argv:
    from fabric.operations import local as run
    from fabric.context_managers import lcd as cd

    def sudo(cmd):
        return local("sudo %s" % cmd)
else:
    from fabric.api import run, cd, sudo

