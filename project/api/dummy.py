from django.http import HttpResponse
from django.contrib.csrf.middleware import csrf_exempt
import json

class Dummy:
    pass

class DummyResource:
    def __init__(self, resource):
        self.resource = resource

    def post(self, request):
        json_data = json.loads(request.raw_post_data)
        bundle = Dummy()
        bundle.data = json_data

        response_data = self.resource._meta.validation.is_valid(bundle, request)

        if response_data:
            response = HttpResponse(content=json.dumps(response_data), status=400,
                    content_type="application/json")
            return response

        response = HttpResponse(status=201)
        response['Location'] = request.path+"1/"
        return response

    def get(self, request, res_id=None):
        resource = self.resource._meta.examples['GET']
        resource['resource_uri'] = "/api/resources/"+self.resource._meta.resource_name+"/1/"

        if not res_id:
            json_data = {
                    "meta" : {
                        "limit" : 20,
                        "next" : None,
                        "offset": 0,
                        "previous": None,
                        "total_count": 1
                    },
                    "objects" : [resource]
                }
        else:
            json_data = resource

        response = HttpResponse(content=json.dumps(json_data), 
                status=200, content_type="application/json")

        return response

    def put(self, request):
        response = HttpResponse(status=200)
        return response

    def delete(self, request):
        return HttpResponse(status=200)

    @staticmethod
    def get_view(resource):
        dummy_resource = DummyResource(resource)

        @csrf_exempt
        def view(request, res_id=None):
            if request.method == "POST":
                return dummy_resource.post(request)
            elif request.method == "GET":
                return dummy_resource.get(request,res_id)
            elif request.method == "PUT":
                return dummy_resource.put(request,res_id)
            elif request.method == "DELETE":
                return dummy_resource.delete(request,res_id)

        return view
