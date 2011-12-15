from django.http import HttpResponse
from django.contrib.auth import authenticate
from jsonrpc import jsonrpc_method
from jsonrpc.exceptions import Error
from api.resources import Api

api = Api()

class ClientError(Error):
    status = 400

class WrongPassword(ClientError):
    message = "Incorrect username/password combination."

class InactiveUser(ClientError):
    message = "User is not active."


@jsonrpc_method('authenticate(String, String) -> Object', validate=True)
def authenticate_user(request, username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            return api.dehydrate(request=request,resource_name='user',obj=user)
        else:
            raise InactiveUser()
    else:
        raise WrongPassword()
