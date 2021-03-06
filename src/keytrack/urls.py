"""keytrack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView

from .views import DashboardView
from .views import PeopleView
from .views import ProjectsView
from .views import AnyProfileView
from .views import OwnProfileView
from .views import ProcessRegisterView
from .views import RegisterView
from .views import RegisterRequestsView
from .views import SecureLogoutView

urlpatterns = [
    path('admin/regreqs/<int:pk>/', ProcessRegisterView.as_view(),
    	name='dashboard.admin.regreq'),

    path('admin/regreqs/', RegisterRequestsView.as_view(),
    	name='dashboard.admin.regreqs'),

    path('admin/people/<int:pk>/', AnyProfileView.as_view(),
    	name='dashboard.admin.anyprofile'),

    path('admin/people/', PeopleView.as_view(),
    	name='dashboard.admin.people'),

    path('admin/projects/', ProjectsView.as_view(),
    	name='dashboard.admin.projects'),

    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name="login.html")),
    path('logout/', SecureLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('', DashboardView.as_view(), name='dashboard'),
    path('profile/', OwnProfileView.as_view(), name='profile'),
]
