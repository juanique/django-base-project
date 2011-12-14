from django.contrib.auth.models import User
from tastypie.resources import ModelResource
from tastypie.serializers import Serializer
from tastypie.authorization import Authorization
from tastypie import fields
from tastypie.api import Api as TastypieApi
from api.helpers import FieldsValidation
import json


class UserValidation(FieldsValidation):

    def __init__(self):
        super(UserValidation, self).__init__( required=['username','first_name','last_name'],
                                              validated=['username'],
                                              required_post = ['email', 'password'],
                                              validated_post = ['password'],
                                            )

    @staticmethod
    def password_is_valid(password, bundle):
        if len(password) < 6:
            return False, 'Password is too short.'
        return True, ""

    @staticmethod
    def username_is_valid(username, bundle):
        try:
            user = User.objects.get(username=username)
            print bundle.data

            if user is not None and str(user.id) != str(bundle.data.get('id',0)):
                return False, "The username is already taken."

        except User.DoesNotExist:
            return True, ""
        return True, ""


class UserResource(ModelResource):
    username = fields.CharField(attribute='username', unique=True)

    class Meta:
        queryset = User.objects.all()
        allowed_methods = ['get','post','put']
        authorization = Authorization()
        validation = UserValidation()
        fields = ['id','username','first_name','last_name','last_login']
        #excludes =['email','password','is_active','is_staff','is_superuser']

    def obj_create(self, bundle, request=None, **kwargs):
        bundle = self.full_hydrate(bundle)
        create_data = { 'username' : bundle.data['username'], 
                        'email' : bundle.data['email'], 
                        'password' : bundle.data['password'] }
        user = User.objects.create_user(**create_data)
        user.first_name = bundle.data['first_name']
        user.last_name = bundle.data['last_name']
        user.is_staff = False
        user.is_active = True
        user.is_superuser = False
        user.save()
        bundle.obj = user

        return bundle

    def dehydrate_password(self, bundle):
        return 'PRIVATE'

    def wrap_view(self, view):
        return super(UserResource, self).wrap_view(view)


class Api:
    def __init__(self):
        self.tastypieApi = TastypieApi(api_name='resources')
        self.resources = {
            'user' : UserResource(),
        }

        self.registerResources()

    def registerResources(self):
        for resource_name, resource in self.resources.items():
            self.tastypieApi.register(resource)

    @property
    def urls(self):
        return self.tastypieApi.urls

    def dehydrate(self,request, resource_name, obj):
        resource = self.resources[resource_name]
        bundle = resource.build_bundle(obj=obj, request=request)
        bundle = resource.full_dehydrate(bundle)
        return bundle.data
