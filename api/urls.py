from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views
from django.contrib import admin

urlpatterns = [
	path('api/user/', views.UserList.as_view(), name='user-list'),
	path('api/user/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
]