from django.urls import path
from .views import RegisterView, UserView, Logout
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', Logout.as_view()),
]
