import settings
import re

class CoffeeScriptMiddleWare:

    def process_request(self, request):
        media_path = re.compile("^%s" % settings.MEDIA_URL)


        if media_path.match(request.path) and request.path[-2:] == "js":
            print "Requesting js file : %s" % request.path


        return None
