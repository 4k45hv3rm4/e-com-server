from . import apis
from django.urls import path

urlpatterns = [
    path('register', apis.RegisterView.as_view(),)
]