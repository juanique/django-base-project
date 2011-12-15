from resources import UserResource
from django.http import HttpResponse
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
            print "=============================="
            print response_data
            print "=============================="

            response = HttpResponse(content=json.dumps(response_data), status=400)
            return response

        response = HttpResponse(status=201)
        return response

    def get(self, request):
        response = HttpResponse(content=json.dumps(self.resource._meta.examples['GET']), 
                status=200)
        return response

    def put(self, request):
        raise Exception("Not implemented")

    def delete(self, request):
        raise Exception("Not implemented")

    @staticmethod
    def get_view(self, resource):
        dummy_resource = DummyResource(resource)

        def view(request):
            if request.method == "POST":
                return dummy_resource.post(request)
            elif request.method == "GET":
                return dummy_resource.get(request)
            elif request.method == "PUT":
                return dummy_resource.put(request)
            elif request.method == "DELETE":
                return dummy_resource.delete(request)
