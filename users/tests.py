import imp
import json
from urllib import response

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse
from knox.auth import AuthToken, TokenAuthentication
from rest_framework import status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.test import APITestCase

from .models import Group, Message
from .serializers import GroupSerializer, MessageSerializer, UserSerializer


class TestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        User.objects.create_superuser('admin', 'admin@gmail.com', 'admin')
        data = {"username":"admin","password":"admin"}
        response = self.client.post("/api/login/",data)
        self.admin_token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.admin_token)

        data = {"username":"alice","password":"alice","email":"alice@gmail.com","first_name":"alice","last_name":"hunter","is_superuser":"false"}
        response = self.client.post('/api/users/',data)
        self.normal_token = response.data['token']

    def test_create_user_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.admin_token)
        data = {"username":"bob","password":"bob","email":"bob@gmail.com","first_name":"bob","last_name":"hunter","is_superuser":"false"}
        response = self.client.post('/api/users/',data)
        self.assertEqual(response.status_code, 200)

    def test_create_user_by_normal_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.normal_token)
        data = {"username":"john","password":"john","email":"john@gmail.com","first_name":"john","last_name":"hunter","is_superuser":"false"}
        response = self.client.post('/api/users/',data)
        self.assertEqual(response.status_code, 401)

    def test_edit_user_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.admin_token)
        data={"username":"alice","password":"alice","email":"alice@gmail.com","first_name":"alice","last_name":"hunter","is_superuser":"false"}
        id = User.objects.filter(username='alice').values('id')[0]['id']
        response = self.client.put('/api/users/'+str(id)+'/',data)
        self.assertEqual(response.status_code, 200)

    def test_edit_user_by_normal_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.normal_token)
        data={"username":"alice","password":"alice","email":"alice@gmail.com","first_name":"alice","last_name":"hunter","is_superuser":"false"}
        id = User.objects.filter(username='alice').values('id')[0]['id']
        response = self.client.put('/api/users/'+str(id)+'/',data)
        self.assertEqual(response.status_code, 401)

    def test_list_users(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.normal_token)
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.admin_token)
        id = User.objects.filter(username='alice').values('id')[0]['id']
        response = self.client.delete('/api/users/'+str(id)+'/')
        self.assertEqual(response.status_code, 200)

    def test_list_group(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.normal_token)
        response = self.client.get('/api/groups/')
        self.assertEqual(response.status_code, 200)

    def test_search_group(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.normal_token)
        id1 = int(User.objects.filter(username='admin').values('id')[0]['id'])
        id2 = int(User.objects.filter(username='alice').values('id')[0]['id'])
        data = {"name":"groupA","users":[id1,id2]}
        response = self.client.post('/api/groups/?search=groupA',data)
        self.assertEqual(response.status_code, 200)

    def test_create_group(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.normal_token)
        id1 = int(User.objects.filter(username='admin').values('id')[0]['id'])
        id2 = int(User.objects.filter(username='alice').values('id')[0]['id'])
        data = {"name":"groupA","users":[id1,id2]}
        response = self.client.post('/api/groups/',data)
        self.assertEqual(response.status_code, 200)


    def test_edit_group_by_group_member(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.normal_token)
        id1 = int(User.objects.filter(username='admin').values('id')[0]['id'])
        id2 = int(User.objects.filter(username='alice').values('id')[0]['id'])
        data = {"name":"groupA","users":[id1,id2]}
        response = self.client.post('/api/groups/',data)
        id = Group.objects.filter(name='groupA').values('id')[0]['id']
        response = self.client.put('/api/groups/'+str(id)+'/',data)
        self.assertEqual(response.status_code, 200)

    def test_edit_group_by_not_group_member(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.admin_token)
        data = {"username":"bob","password":"bob","email":"bob@gmail.com","first_name":"bob","last_name":"hunter","is_superuser":"false"}
        response = self.client.post('/api/users/',data)

        data = {"username":"john","password":"john","email":"john@gmail.com","first_name":"john","last_name":"hunter","is_superuser":"false"}
        response = self.client.post('/api/users/',data)

        id1 = int(User.objects.filter(username='admin').values('id')[0]['id'])
        id2 = int(User.objects.filter(username='bob').values('id')[0]['id'])

        data = {"name":"groupA","users":[id1,id2]}
        response = self.client.post('/api/groups/',data)

        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.normal_token)
        id = Group.objects.filter(name='groupA').values('id')[0]['id']
        response = self.client.put('/api/groups/'+str(id)+'/',data)
        self.assertEqual(response.status_code, 401)

    def test_add_member_by_group_member(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.admin_token)
        data = {"username":"bob","password":"bob","email":"bob@gmail.com","first_name":"bob","last_name":"hunter","is_superuser":"false"}
        response = self.client.post('/api/users/',data)

        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.normal_token)
        id1 = int(User.objects.filter(username='admin').values('id')[0]['id'])
        id2 = int(User.objects.filter(username='alice').values('id')[0]['id'])
        id3 = int(User.objects.filter(username='bob').values('id')[0]['id'])

        data = {"name":"groupA","users":[id1,id2]}
        response = self.client.post('/api/groups/',data)
        id = Group.objects.filter(name='groupA').values('id')[0]['id']

        response = self.client.post('/api/groups/'+str(id)+'/add_member/?user_id='+str(id3),data)
        self.assertEqual(response.status_code, 200)

    def test_add_member_by_not_group_member(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.admin_token)
        data = {"username":"bob","password":"bob","email":"bob@gmail.com","first_name":"bob","last_name":"hunter","is_superuser":"false"}
        response = self.client.post('/api/users/',data)

        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.normal_token)
        id1 = int(User.objects.filter(username='admin').values('id')[0]['id'])
        id2 = int(User.objects.filter(username='alice').values('id')[0]['id'])
        id3 = int(User.objects.filter(username='bob').values('id')[0]['id'])

        data = {"name":"groupA","users":[id1,id3]}
        response = self.client.post('/api/groups/',data)
        id = Group.objects.filter(name='groupA').values('id')[0]['id']

        response = self.client.post('/api/groups/'+str(id)+'/add_member/?user_id='+str(id2),data)
        self.assertEqual(response.status_code, 401)

    def test_send_message_in_group_by_group_member(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.normal_token)
        id1 = int(User.objects.filter(username='admin').values('id')[0]['id'])
        id2 = int(User.objects.filter(username='alice').values('id')[0]['id'])

        data = {"name":"groupA","users":[id1,id2]}
        response = self.client.post('/api/groups/',data)
        id = Group.objects.filter(name='groupA').values('id')[0]['id']

        data = {"title":"test message","text":"test message text","group":id}
        response = self.client.post('/api/groups/'+str(id)+'/messages/',data)
        self.assertEqual(response.status_code, 200)

    def test_send_message_in_group_by_not_group_member(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.admin_token)
        data = {"username":"bob","password":"bob","email":"bob@gmail.com","first_name":"bob","last_name":"hunter","is_superuser":"false"}
        response = self.client.post('/api/users/',data)

        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.normal_token)
        id1 = int(User.objects.filter(username='admin').values('id')[0]['id'])
        id2 = int(User.objects.filter(username='alice').values('id')[0]['id'])
        id3 = int(User.objects.filter(username='bob').values('id')[0]['id'])

        data = {"name":"groupA","users":[id1,id3]}
        response = self.client.post('/api/groups/',data)
        id = Group.objects.filter(name='groupA').values('id')[0]['id']

        data = {"title":"test message","text":"test message text","group":id}
        response = self.client.post('/api/groups/'+str(id)+'/messages/',data)
        self.assertEqual(response.status_code, 401)

    def test_like_message_in_group_by_group_member(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.normal_token)
        id1 = int(User.objects.filter(username='admin').values('id')[0]['id'])
        id2 = int(User.objects.filter(username='alice').values('id')[0]['id'])

        data = {"name":"groupA","users":[id1,id2]}
        response = self.client.post('/api/groups/',data)
        id = Group.objects.filter(name='groupA').values('id')[0]['id']

        data = {"title":"test message","text":"test message text","group":id}
        response = self.client.post('/api/groups/'+str(id)+'/messages/',data)

        id = Message.objects.filter(title='test message').values('id')[0]['id']
        response = self.client.post('/api/like_message/'+str(id)+'/')
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.normal_token)
        response = self.client.post('/api/logout/')
        self.assertEqual(response.status_code, 204)






