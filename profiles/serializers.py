from rest_framework import serializers
from profiles.models import Profile, ProfileStatus
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.parsers import FileUploadParser
from djoser.conf import settings
from djoser.compat import get_user_email, get_user_email_field_name
from djoser.serializers import UserSerializer
from django.contrib.auth import authenticate

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField(read_only=True)    

    class Meta:
        model = Profile       
        fields = ("__all__")
        
class ProfileStatusSerializer(serializers.ModelSerializer):

    # user_profile = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ProfileStatus       
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False, allow_null=True, partial=True)
    parser_class = (FileUploadParser,)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'profile','password', 'id']
        extra_kwargs = {"password":{'write_only': True}}

    def update(self, instance, validated_data):

        if 'profile' in validated_data:
            nested_serializer = self.fields['profile']
            nested_instance = instance.profile
            nested_data = validated_data.pop('profile')
            nested_serializer.update(nested_instance, nested_data)
            validated_data.pop('password')

        return super(UserSerializer, self).update(instance, validated_data) 

    def create(self, validated_data):
        return User.objects.create_user(
           validated_data['username'],validated_data['email'],validated_data['password'])





    

        

    
        