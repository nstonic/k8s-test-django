from django.shortcuts import redirect
from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('', lambda request: redirect('/admin/')),
    path('home/', lambda request: redirect('/admin/')),
    path('users/', lambda request: redirect('/admin/')),
    path('admin/', admin.site.urls),
]
