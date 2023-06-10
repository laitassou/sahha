"""Sahha URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from sahha_service import settings
from rest_framework import routers

from sahha_service.apps.users.views import (
    SignupView,
    LoginView,
    LogoutView,
    UserView,
    UsersListView,
)

from sahha_service.apps.annonces.views import (
    AnnoncesListView,
    AnnonceDetailApiView,
    CategoryListView,
    AgencesListView,
    SlotListView,
    SlotView,
    InterventionView,
)

router = routers.DefaultRouter()

# router.register('client', ClientViewSet, basename='client')


# Main API URLS
urlpatterns = [
    # Registartion
    path("user/signup/", SignupView.as_view(), name="auth-signup"),
    # Login
    path("user/login/", LoginView.as_view(), name="auth-login"),
    path("user/logout/", LogoutView.as_view(), name="auth-logout"),
    # User
    path("user/", UserView.as_view(), name="user-details"),
    # Annonces
    path("annonces/", AnnoncesListView.as_view(), name="user-details"),
    path("annonces/<int:user_id>/", AnnoncesListView.as_view(), name="user-details"),
    # Single annonce
    path("annonce/<int:ads_id>/", AnnonceDetailApiView.as_view()),
    # Category
    path("categories/", CategoryListView.as_view()),
    # Agences
    path("agences/", AgencesListView.as_view()),

    #Slots
    path("slots/<int:ads_id>/", SlotListView.as_view()),
    #update slot
    path("slot/<int:slot_id>/annonce/<int:ads_id>/worker/<int:worker_id>/", SlotView.as_view()),

    #feedback
    path("feedback/<int:slot_id>/<int:worker_id>", InterventionView.as_view()),

    # Manager
    path("users/<slug:type>/",    UsersListView.as_view()),

    # Router
    path("", include(router.urls)),
]
