from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views
from django.contrib import admin

urlpatterns = [
	path('', admin.site.urls ),
]