from django.urls import path
from knox import views as knox_views

from . import views

# different API endpoints
urlpatterns = [
    # endpoints for user login and logout
    path('login/', views.login, name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),

    # endpoints for list/create/update/delete users
    path('users/', views.users_api, name='create_list_users'),
    path('users/<int:key>/', views.users_api, name='update_delete_users'),

    # endpoints for search/list/create/update/delete groups
    path('groups/', views.groups_api, name='create_list_groups'),
    path('groups/<int:key>/', views.groups_api, name='update_delete_groups'),

    # endpoints for list/create/update/delete messages
    path('groups/<int:key>/messages/',views.messages_api, name='send_list_messages'),
    path('groups/<int:key>/messages/<int:id>/',views.messages_api, name='delete_messages'),

    # endpoints for adding memeber to the group and liking message
    path('groups/<int:key>/add_member/',views.add_member, name='add_member'), # accepts user id from query parameters ?user_id=<id>
    path('like_message/<int:key>/',views.like_message, name = 'like_message'),
]
