# Add these to your existing users/urls.py
# Make sure you import the new views first.

from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # --- existing ---
    path('register/',           views.register_view,        name='register'),
    path('login/',              views.login_view,            name='login'),
    path('logout/',             views.logout_view,           name='logout'),
    path('profile/',            views.profile_view,          name='profile'),

    # --- messaging (new) ---
    path('messages/',                           views.inbox_view,            name='inbox'),
    path('messages/new/',                       views.new_conversation_view, name='new_conversation'),
    path('messages/<str:username>/',            views.conversation_view,     name='conversation'),
]