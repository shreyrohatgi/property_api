from django.shortcuts import render
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework import status
from django.http import Http404
from rest_framework.response import Response
from rest_framework import viewsets, filters
from selenium import webdriver
# Create your views here.
class UserList(APIView):
    permission_classes = []
    def get(self, request, format = None):
        users = User.objects.all().order_by('-pk')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format = None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format = None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)      
        return Response(serializer.data)

    def put(self, request, pk, format = None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format = None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class LinkingAccounts(APIView):
    def post(self, request, format = None):
        email = request.data['email']
        password = request.data['password']
        try:
            ## OLX
            driver = webdriver.Chrome(executable_path='/home/shrey/property_upload/chromedriver')
            driver.get('https://www.olx.in/')

            # Login
            login_btn = driver.find_elements_by_xpath("//button[@type='button' and @data-aut-id='btnLogin']")[0]
            login_btn.click()

            while 1:
                try:
                    email_login_btn = driver.find_elements_by_xpath("//button[@type='button' and @data-aut-id='emailLogin']")[0]
                    email_login_btn.click()
                    break
                except IndexError:
                    continue

            email_input = driver.find_elements_by_xpath("//input[@name='email']")[0]
            email_input.send_keys(email)

            next_btn = driver.find_elements_by_xpath("//button[@type='submit']")[1]
            next_btn.click()

            while 1:
                try:
                    password_input = driver.find_elements_by_xpath("//input[@name='password']")[0]
                    password_input.click()
                    break
                except IndexError:
                    continue

            password_input.send_keys(password)

            log_in_btn = driver.find_elements_by_xpath("//button[@type='submit']")[1]
            log_in_btn.click()
            return Response({'status': 'success'})

        except:
            raise status.HTTP_400_BAD_REQUEST    