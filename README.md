# groupchat_apis
GroupChat Application APIs:

This django application contains following endpoints with their implementation:
1) [POST]<base_url>/api/login/ : (access: anyone) allows an existing user to login and generates a token for authorization
2) [POST]<base_url>/api/logout/ : (access: existing user) allows an existing user to logout when token is passed in header as "Authorization: Token <token>"
3) [GET]<base_url>/api/users/ : (access: existing user) list all the users
4) [GET]<base_url>/api/users/<id> : (access: existing user) list a particular user
5) [POST]<base_url>/api/users/ : (access: only admins) create new user
6) [PUT]<base_url>/api/users/<id> : (access: only admins) edit existing user
7) [DELETE]<base_url>/api/users/<id> : (access: only admins) delete existing user
8) [GET]<base_url>/api/groups/ : (access: existing user) allows existing user to list groups which he is part of.
9) [GET]<base_url>/api/groups/<id> : (access : existing user part of given group) allows existing user to list group which he is part of.
10) [GET]<base_url>/api/groups/?search=<name> : (access : existing user part of given group) allows existing user to list group which he is part of.
11) [POST]<base_url>/api/groups/ : (access: existing user) allows existing user to create a group
12) [PUT]<base_url>/api/groups/<id> : (access : existing user part of given group) update group
13) [DELETE]<base_url>/api/groups/<id>: (access : existing user part of given group) delete group
14) [GET]<base_url>/api/groups/<id>/messages/ : (access : existing user part of given group) list messages
15) [GET]<base_url>/api/groups/<id>/messages/<id> : (access : existing user part of given group) list messages
16) [POST]<base_url>/api/groups/<id>/messages/ : (access : existing user part of given group) send message
17) [DELETE]<base_url>/api/groups/<id>/messages/<id> : (access : existing user part of given group) send message
18) [POST]<base_url>/api/groups/<id>/add_member/?user_id=<id> : (access : existing user part of given group) add user to the group
19) [POST]<base_url>/api/like_message/<id> : (access : existing user part of given group message) like message

**Note: for post api payloads, please look into tests.py.


Steps to configure the application[using git bash, if you are using any other terminal, your commands may differ a bit]:
1. install python
2. create virtual environment
	command: python -m venv venv
4. activate the virtual environment
	command: source venv/Scripts/activate
5. install all the modules listed in requirements file
	command: pip install <module>
6. pull the source code from git.
7. run the django commands for migrations
	command: python manage.py makemigrations
		 python manage.py migrate
8. run the django command to start the server:
	command: python manage.py runserver
9. start another terminal, login to virtual environment, and run tests while server is running on another terminal
	command: python manage.py test
(You can also test apis via postman after starting the server)
