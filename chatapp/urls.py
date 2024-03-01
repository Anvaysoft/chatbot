from django.contrib import admin
from django.urls import include, path

from .views import *

urlpatterns = [
    path("startcon", StartConvUserView.as_view(), name="startcon"),
    path("conversation", StartChat.as_view(), name="conversation"),
    path("user", UserDataSave.as_view(), name="user"),
    path("resetlimit", UserDatareset.as_view(), name="resetlimit"),
]
