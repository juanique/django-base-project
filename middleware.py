import settings
import re
import os
import subprocess
from django.http import HttpResponse

class CoffeeException(Exception):
    pass

class CoffeeScriptMiddleWare:

    @staticmethod
    def compile_cs(filename):
        process = subprocess.Popen(['coffee','-p', filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        if err:
            raise CoffeeException(err)
        return out

    def render_response(self, request,response):
        #if not request.is_ajax():
        #    response = response.replace("\n","<br>\n")
        return response

    def process_request(self, request):
        media_path = re.compile("^/%s" % settings.MEDIA_URL)

        request_js_file = os.path.join(
                settings.MEDIA_ROOT, 
                request.path[len(settings.MEDIA_URL)+1:])
        request_cs_file = request_js_file[:-2] + "coffee"

        js_file_exists = os.path.isfile(request_js_file)
        cs_file_exists = os.path.isfile(request_cs_file)
        request_is_js = media_path.match(request.path) and request.path[-2:] == "js"

        if request_is_js and not js_file_exists and cs_file_exists:
                try:
                    response = self.compile_cs(request_cs_file)
                except CoffeeException, e:
                    response = e.message
                return HttpResponse(self.render_response(request, response))
                


        return None
