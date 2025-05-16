from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.generic import TemplateView

from . import views
from .views import SignUpView, LoginView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('my-boards/', TemplateView.as_view(template_name='MiroBoards/boards.html'), name='my_boards'),
]
