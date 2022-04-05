import requests
from django.shortcuts import render
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import (api_view, authentication_classes, permission_classes,)
from rest_framework import permissions
from rest_framework.views import APIView
from .models import Profile
from .serializers import ProfileSerializer

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_profiles(request):
    profile_id = request.GET.get('profile_id', '')
    profiles = Profile.objects.all()

    if profile_id:
        profiles = Profile.filter(profiles__in=[int(profile_id)])

    serializer = ProfileSerializer(profiles, many=True)
    return Response(serializer.data)

# class UserActivationView(APIView):
#     def get (self, request, uid, token):
#         protocol = 'https://' if request.is_secure() else 'http://'
#         web_url = protocol + request.get_host()
#         post_url = web_url + "api/v1/users/activation/"
#         post_data = {'uid': uid, 'token': token}
#         result = requests.post(post_url, data = post_data)
#         content = result.text
#         return Response(content)
