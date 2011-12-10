from django.contrib.auth.models import User
from tastypie.resources import ModelResource
from tastypie.serializers import Serializer
from tastypie.authorization import Authorization
from tastypie.validation import Validation
from tastypie import fields
from tastypie.api import Api as TastypieApi
import json

class FieldsValidation(Validation):
    def __init__(self, required = [], validated = [] ):
        self.required_fields = required
        self.validated_fields = validated
        Validation.__init__(self)


    def is_valid(self, bundle, request):
        if not bundle.data:
            return {'__all__' : 'Missing data.'}

        required_errors = self.validate_required(bundle, request)
        validation_errors = self.validate_fields(bundle, request)

        errors = {}
        errors.update(required_errors)
        errors.update(validation_errors)

        return errors

    def validate_fields(self, bundle, request=None):
        errors = {}
        for field in self.validated_fields:
            validation_func = getattr(self, '%s_is_valid' % field)
            if field in bundle.data:
                valid, reason = validation_func(bundle.data[field])
                if not valid:
                    errors[field] = reason
        return errors

    def validate_required(self, bundle, request=None):
        errors = {}
        for required_field in self.required_fields:
            if required_field not in bundle.data:
                errors[required_field] = ['%s field is required.' % required_field]
        return errors

class UserValidation(FieldsValidation):

    def __init__(self):
        super(UserValidation, self).__init__( required=['password','username','email','first_name','last_name'],
                                              validated=['password','username'] )

    @staticmethod
    def password_is_valid(password):
        if len(password) < 6:
            return False, 'Password is too short.'
        return True, ""

    @staticmethod
    def username_is_valid(username):
        try:
            user = User.objects.get(username=username)
            if user is not None:
                return False, "The username is already taken."

        except User.DoesNotExist:
            return True, ""


class UserResource(ModelResource):
    username = fields.CharField(attribute='username', unique=True)

    class Meta:
        queryset = User.objects.all()
        allowed_methods = ['get','post','put']
        authorization = Authorization()
        validation = UserValidation()
        fields = ['username','first_name','last_name','last_login','password']
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
        return bundle

    def dehydrate_password(self, bundle):
        return 'PRIVATE'

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
