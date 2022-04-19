from tokenize import group
from urllib import response

from django.contrib.auth.models import User
from django.shortcuts import render
from knox.auth import AuthToken, TokenAuthentication
from rest_framework import status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from users import serializers
from users.models import Group, Message

from .serializers import GroupSerializer, MessageSerializer, UserSerializer

# generic login api
@api_view(['POST'])
def login(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    _, token = AuthToken.objects.create(user)
    return Response({
        'user_data': UserSerializer(user).data,
        'token': token
    })
        

# implementation for list/create/update/delete user apis
@api_view(['GET','POST','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def users_api(request, key=None):
    if request.method == 'POST':
        if(request.user.is_superuser):
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                _, token = AuthToken.objects.create(user)
                return Response({
                    "user_info": UserSerializer(user).data,
                    "token": token
                })
        return Response({"error":"you are not authorised to perform this operation"},status=status.HTTP_401_UNAUTHORIZED)
    if request.method == 'GET':
        if key is not None:
            try:
                user = User.objects.get(id=key)
            except User.DoesNotExist:
                return Response({'error':'user does not exist.'},status = status.HTTP_404_NOT_FOUND)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    if request.method == 'PUT':
        if(request.user.is_superuser):
            if key is not None:
                try:
                    user = User.objects.get(id=key)
                except User.DoesNotExist:
                    return Response({'error':'user does not exist.'},status = status.HTTP_404_NOT_FOUND)
                serializer = UserSerializer(user, data=request.data)
                if(serializer.is_valid()):
                    serializer.save()
                    return Response(serializer.data)
            else:
                return Response({'error':'please provide a user id. eg. /api/users/1/'},status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error':'you are not authorised to perform this operation'},status=status.HTTP_401_UNAUTHORIZED)
    if request.method == 'DELETE':
        if(request.user.is_superuser):
            if key is not None:
                try:
                    user = User.objects.get(id=key)
                except User.DoesNotExist:
                    return Response({'error':'user does not exist.'},status = status.HTTP_404_NOT_FOUND)
                user.delete()
                return Response({'response':'user deleted successfully!'})
            else:
                return Response({'error':'please provide a user id. eg. /api/users/1/'},status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error':'you are not authorised to perform this operation'},status=status.HTTP_401_UNAUTHORIZED)
        

#implementation for list/create/update/delete group apis
@api_view(['GET','POST','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def groups_api(request, key=None):
    if request.method == 'POST':
        data = request.data.copy()
        user_id=request.user.id
        list(data['users']).append(user_id)
        serializer = GroupSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            group = serializer.save()
            return Response(GroupSerializer(group).data)
    
    if request.method =='GET':
        if key is not None:
            try:
                group = Group.objects.get(id=key)
            except Group.DoesNotExist:
                return Response({'error':'user does not exist.'},status = status.HTTP_404_NOT_FOUND)
            serializer = GroupSerializer(group)
            user_id=request.user.id
            if user_id not in serializer.data['users']:
                return Response({"error":"you are not allowed to perform this task in this group because you are not part of this group"},status=status.HTTP_401_UNAUTHORIZED)
            return Response(serializer.data)
        
        if(request.query_params):
            name = request.query_params['search']
            group = Group.objects.get(name=name)
            serializer = GroupSerializer(group)
            user_id=request.user.id
            if user_id not in serializer.data['users']:
                return Response({"error":"you are not allowed to perform this task in this group because you are not part of this group"},status=status.HTTP_401_UNAUTHORIZED)

        user_id=request.user.id
        list_user = []
        list_user.append(user_id)
        serializer=GroupSerializer(Group.objects.filter(users__in=list_user), many=True)
        return Response(serializer.data)

    if request.method =='PUT':
        if key is not None:
            try:
                group = Group.objects.get(id=key)
            except Group.DoesNotExist:
                return Response({'error':'user does not exist.'},status = status.HTTP_404_NOT_FOUND)
            serializer = GroupSerializer(group)
            user_id = request.user.id
            if user_id not in serializer.data['users']:
                return Response({"error":"you are not allowed to perform this task in this group because you are not part of this group"},status=status.HTTP_401_UNAUTHORIZED)

            serializer = GroupSerializer(group, data=request.data)
            if(serializer.is_valid()):
                    serializer.save()
                    return Response(serializer.data)
            else:
                return Response({'error':'please provide a group id. eg. /api/groups/1/'},status = status.HTTP_400_BAD_REQUEST)

    if request.method =='DELETE':
        if key is not None:
            try:
                group = Group.objects.get(id=key)
            except Group.DoesNotExist:
                return Response({'error':'group does not exist.'},status = status.HTTP_404_NOT_FOUND)
            serializer = GroupSerializer(group)
            user_id = request.user.id
            if user_id not in serializer.data['users']:
                return Response({"error":"you are not allowed to perform this task in this group because you are not part of this group"},status=status.HTTP_401_UNAUTHORIZED)

            group.delete()
            return Response({'response':'group deleted successfully!'})
        else:
            return Response({'error':'please provide a group id. eg. /api/groups/1/'},status = status.HTTP_400_BAD_REQUEST)


# implementation for list/create/delete message apis
@api_view(['GET','POST','DELETE'])
@permission_classes([IsAuthenticated])
def messages_api(request,key=None,id=None):
    group = Group.objects.get(id=key)
    serializer = GroupSerializer(group)
    user_id = request.user.id
    if(user_id not in serializer.data['users']):
        return Response({"error":"you are not allowed to perform this task in this group because you are not part of this group"},status=status.HTTP_401_UNAUTHORIZED)
    
    if request.method == 'GET':
        serializer = MessageSerializer(Message.objects.filter(group=key),many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        data = request.data.copy()
        data['group'] = key
        serializer = MessageSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            message = serializer.save()
            return Response(MessageSerializer(message).data)

    if request.method == 'DELETE':
        if id is not None:
            try:
                message = Message.objects.get(id=key)
            except Message.DoesNotExist:
                return Response({'error':'message does not exist.'},status = status.HTTP_404_NOT_FOUND)
            message.delete()
            return Response({'response':'message deleted successfully!'})
        else:
            return Response({'error':'please provide a message id. eg. /api/groups/1/messages/1/'},status = status.HTTP_400_BAD_REQUEST)

# implementation for adding member to the group api
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_member(request, key=None):
    group = Group.objects.get(id=key)
    serializer = GroupSerializer(group)
    user_id = request.user.id
    if(user_id not in serializer.data['users']):
        return Response({"error":"you are not allowed to perform this task in this group because you are not part of this group"},status=status.HTTP_401_UNAUTHORIZED)
    
    data = serializer.data
    user_id = request.query_params['user_id']
    data['users'] = list(data['users'])
    data['users'].append(int(user_id))
    serializer = GroupSerializer(group, data=data)
    if serializer.is_valid(raise_exception=True):
        group = serializer.save()
        return Response(serializer.data)

#implementation for liking message
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_message(request, key=None):
    message_id = key
    message = Message.objects.get(id = message_id)
    serializer = MessageSerializer(message)
    data=serializer.data.copy()
    group_id = data['group']
    group = Group.objects.get(id=group_id)
    serializer = GroupSerializer(group)
    user_id = request.user.id
    if(user_id not in serializer.data['users']):
        return Response({"error":"you are not allowed to perform this task in this group because you are not part of this group"},status=status.HTTP_401_UNAUTHORIZED)
    
    data['liked'].append(user_id)
    serializer = MessageSerializer(message,data=data)
    if serializer.is_valid(raise_exception=True):
            message = serializer.save()
            return Response(serializer.data)
    return Response({"error":"please verify the endpoint"},status = status.HTTP_400_BAD_REQUEST)
