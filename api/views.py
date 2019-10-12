from django.shortcuts import render
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework import status
from django.http import Http404
from rest_framework.response import Response
from rest_framework import viewsets, filters
from django.shortcuts import get_object_or_404
from selenium import webdriver
import selenium.common.exceptions as selenium_exceptions
from django.core.files.storage import default_storage
from property.settings import BASE_DIR
import time

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
            driver.close()
            linkedObjs = LinkedAccounts.objects.filter(auth_user=request.user, site='olx')
            if len(linkedObjs):
                linkedObj = linkedObjs[0]
                linkedObj.email = email
                linkedObj.password = password
                linkedObj.save()
            else:
                LinkedAccounts.objects.create(
                    auth_user=request.user,
                    site='olx',
                    email=email,
                    password=password,
                )
            return Response({'status': 'success'})

        except:
            return Response({'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)

class AddProperty(APIView):
    def post(self, request, format = None):
        user = request.user
        linkedAccountObj = get_object_or_404(LinkedAccounts, auth_user=user, site='olx')
        email = linkedAccountObj.email
        password = linkedAccountObj.password

        data = request.data
        property_for = data['property_for']
        property_type = data['property_type']
        property_sub_type = data['property_sub_type']
        bedrooms_num = int(data['bedrooms'])
        bathroom_num = int(data['bathrooms'])
        furnishing = data['furnishing']
        super_buildup_area = data['super_buildup_area']
        carpet_area = data['carpet_area']
        title = data['title']
        description = data['description']
        price = data['price']
        state = data['state']
        city = data['city']
        locality = data['neighbourhood']

        photo_content = data['photo']
        photo = default_storage.save('media/' + photo_content.name, photo_content)
        photo = default_storage.url(photo)

        try:
            ## Details
            prop_options = ['Sale', 'Rent', 'PG']

            # For sale or rent
            sale = {'Residential': ['Residential House', 'Multistorey Apartment', 'Builder Floor Apartment',
                                    'Villa', 'Penthouse', 'Studio Apartment', 'Farm House'],
                    'Commercial': ['Commercial Office', 'Commercial Shop', 'Commercial Showroom', 'Warehouse/Godown',
                                'Industrial Building', 'Industrial Shed'],
                    'Land': ['Commercial Land', 'Residential Plot', 'Industrial Land', 'Agricultural Land'],
                    }

            # For pg
            pg = ['Guest Houses', 'PG', 'Roommate']

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

            # Sell
            while 1:
                try:
                    sell_btn = driver.find_elements_by_xpath("//a[@data-aut-id='btnSell']")[0]
                    sell_btn.click()
                    break
                except selenium_exceptions.ElementClickInterceptedException:
                    continue

            # Fill Property Details
            while 1:
                try:
                    property_btn = driver.find_elements_by_xpath("//li[@data-aut-id='item']")[0]
                    property_btn.click()
                    break
                except IndexError:
                    continue

            # Sub category index to be clicked
            index = -1
            if property_sub_type in sale['Land']:
                index = 2
            elif property_for == 'Sale':
                if property_sub_type in sale['Residential']:
                    index = 0
                elif property_sub_type in sale['Commercial']:
                    index = 4
            elif property_for == 'Rent':
                if property_sub_type in sale['Residential']:
                    index = 1
                elif property_sub_type in sale['Commercial']:
                    index = 3
            elif property_for == 'PG':
                index = 5

            time.sleep(1)
            property_category = driver.find_elements_by_xpath("//li[@class='_27cbh']")[index + 10]
            property_category.click()

            time.sleep(2)
            if index == 0 or index == 1:
                apartments = ('Multistorey Apartment', 'Studio Apartment')
                builder_floors = ('Builder Floor Apartment', )
                farm_houses = ('Farm House', )
                houses_villas = ('Residential House', 'Villa', 'Penthouse', )
                sub_in = -1
                if property_sub_type in apartments:
                    sub_in = 0
                elif property_sub_type in builder_floors:
                    sub_in = 1
                elif property_sub_type in farm_houses:
                    sub_in = 2
                else:
                    if property_type == 'Sale':
                        sub_in = 3
                    else:
                        sub_in = 2
                type_btn = driver.find_elements_by_xpath("//button[@data-aut-id='optype" + str(sub_in) + "']")[0]
                type_btn.click()

                if bedrooms_num <= 5:
                    bedroom_btn = driver.find_elements_by_xpath("//button[@data-aut-id='oprooms" + str(bedrooms_num - 1) + "']")[0]
                    bedroom_btn.click()
                else:
                    bedroom_btn = driver.find_elements_by_xpath("//button[@data-aut-id='oprooms" + str(5) + "']")[0]
                    bedroom_btn.click()
                
                if bathroom_num <= 5:
                    bathroom_btn = driver.find_elements_by_xpath("//button[@data-aut-id='opbathrooms" + str(bedrooms_num - 1) + "']")[0]
                    bathroom_btn.click()
                else:
                    bathroom_btn = driver.find_elements_by_xpath("//button[@data-aut-id='opbathrooms" + str(5) + "']")[0]
                    bathroom_btn.click()
                
                if furnishing == 'Furnished':
                    furnish_btn = driver.find_elements_by_xpath("//button[@data-aut-id='opfurnished0']")[0]
                    furnish_btn.click()
                elif furnishing == 'Semi-Furnished':
                    furnish_btn = driver.find_elements_by_xpath("//button[@data-aut-id='opfurnished1']")[0]
                    furnish_btn.click()
                else:
                    furnish_btn = driver.find_elements_by_xpath("//button[@data-aut-id='opfurnished2']")[0]
                    furnish_btn.click()

                dealer_btn = driver.find_elements_by_xpath("//button[@data-aut-id='oplisted_by1']")[0]
                dealer_btn.click()

                super_buildup_input = driver.find_elements_by_xpath("//input[@id='ft']")[0]
                super_buildup_input.send_keys(super_buildup_area)

                carpet_area_input = driver.find_elements_by_xpath("//input[@id='carpetarea']")[0]
                carpet_area_input.send_keys(carpet_area)

                title_input = driver.find_elements_by_xpath("//input[@id='title']")[0]
                title_input.send_keys(title)

                description_input = driver.find_elements_by_xpath("//textarea[@id='description']")[0]
                description_input.send_keys(description)

                price_input = driver.find_elements_by_xpath("//input[@id='price']")[0]
                price_input.send_keys(price)

                photo_input = driver.find_elements_by_xpath("//input[@type='file']")[0]
                photo_input.send_keys(BASE_DIR + '/' + photo)

                state_input = driver.find_element_by_xpath("//select[@name='State']/option[text()='" + state + "']")
                state_input.click()

                while 1:
                    try:
                        city_input = driver.find_element_by_xpath("//select[@name='City']/option[text()='" + city + "']")
                        city_input.click()
                        break
                    except selenium_exceptions.NoSuchElementException:
                        continue

                while 1:
                    try:
                        neighbourhood_input = driver.find_element_by_xpath("//select[@name='Locality']/option[text()='" + locality + "']")
                        neighbourhood_input.click()
                        break
                    except selenium_exceptions.NoSuchElementException:
                        continue
                
                time.sleep(3)
                post_btn = driver.find_elements_by_xpath("//button[@data-aut-id='btnPost']")[0]
                post_btn.click()

            time.sleep(5)
            driver.close()
            return Response({'status': 'success'})
        except:
            return Response({'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
