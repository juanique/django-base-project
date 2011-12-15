from fabric.operations import local

def lsudo(cmd):
    return local("sudo %s" % cmd)
