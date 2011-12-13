import settings

def info():
    if settings.DEBUG:
        print "Server is in development mode."
    else:
        print "Server is in production mode."
