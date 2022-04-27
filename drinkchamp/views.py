# from django.shortcuts import render
from django.http import JsonResponse
# from requests import Response

# decorator to extend function's functionality
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import DrinkSerializer
from .models import Drink

# Create your views here.
# The API ENDPOINTS will be created here.


# This function takes a GET Request
#To add more functionality to this function to access multiple requests I use a decorator
@api_view(['GET', 'POST'])
def drink_list(request, format=None):

    if request.method == 'GET':
        # fetch all the drinks from the database
        drinks = Drink.objects.all()
        # This will serialize the drinks with the case of many=True as the drinks are alot
        serializer = DrinkSerializer(drinks, many=True)
        # return json using the JsonResponse
        # Instead of returning a list of json objects, I want to return an Object
        return Response(serializer.data)

    # if the request method is POST
    if request.method =='POST':
        # Take a data they sent deserialize it and create a drink object from it.
        # I'm getting data from the request instead of passing values like in the GET request
        serializer = DrinkSerializer(data=request.data)
        # Check to see if the data sent is valid
        if serializer.is_valid():
            # save the data
            serializer.save()
            # return a response with a status to show a drink has been created
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# PUT means to Update
@api_view(['GET', 'PUT', 'DELETE'])
def drink_detail(request, id, format=None):

    # Apply this condition to see if an object exists or not
    try:
        # we get an individual drink by its id
        drink = Drink.objects.get(id=id)
        # if the drink does not exist then I get a 404 error 
    except Drink.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        # This will serialize the drink object
        serializer = DrinkSerializer(drink)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # the object is desearilized and is retrieved from the request data
        serializer = DrinkSerializer(drink, data=request.data)
        # if the data object sent is valid then
        if serializer.is_valid():
            # save the data
            serializer.save()
            # return the data
            return Response(serializer.data)
        else:
            # if the data object is not valid then throw an error
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        drink.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
